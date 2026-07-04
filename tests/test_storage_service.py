"""Unit tests for the document storage module."""

from hashlib import sha256
from pathlib import Path
from uuid import UUID

import pytest
from pydantic import PostgresDsn

from app.core.config import Settings
from app.infrastructure.storage.exceptions import (
    EmptyFileError,
    FileTooLargeError,
    HiddenExtensionError,
    InvalidMimeTypeError,
    UnsupportedFileTypeError,
)
from app.infrastructure.storage.models import DocumentType
from app.infrastructure.storage.provider import FileSystemStorageProvider
from app.infrastructure.storage.storage_service import DocumentStorageService
from app.infrastructure.storage.validator import FileValidator

PDF_MIME = "application/pdf"
DOCX_MIME = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"


def make_settings(tmp_path: Path, *, max_upload_size_bytes: int = 1024) -> Settings:
    """Create isolated settings for storage tests."""
    return Settings(
        database_url=PostgresDsn("postgresql+psycopg://arip:arip@localhost:5432/arip"),
        storage_root=tmp_path,
        uploads_root=tmp_path / "uploads",
        generated_root=tmp_path / "generated",
        resume_upload_dir=tmp_path / "uploads" / "resumes",
        job_upload_dir=tmp_path / "uploads" / "jobs",
        report_output_dir=tmp_path / "generated" / "reports",
        generated_resume_dir=tmp_path / "generated" / "resumes",
        max_upload_size_bytes=max_upload_size_bytes,
        allowed_upload_extensions=("pdf", "docx"),
        allowed_upload_mime_types=(PDF_MIME, DOCX_MIME),
    )


def make_service(
    tmp_path: Path,
    *,
    max_upload_size_bytes: int = 1024,
) -> DocumentStorageService:
    """Create a storage service backed by temporary filesystem storage."""
    settings = make_settings(tmp_path, max_upload_size_bytes=max_upload_size_bytes)
    validator = FileValidator(
        allowed_extensions=settings.allowed_upload_extensions,
        allowed_mime_types=settings.allowed_upload_mime_types,
        max_size_bytes=settings.max_upload_size_bytes,
    )
    provider = FileSystemStorageProvider(settings=settings)
    return DocumentStorageService(provider=provider, validator=validator)


def test_valid_pdf_upload(tmp_path: Path) -> None:
    """Store a valid PDF file."""
    service = make_service(tmp_path)
    content = b"%PDF-1.7 valid pdf bytes"

    metadata = service.store_resume(
        original_filename="resume.pdf",
        mime_type=PDF_MIME,
        content=content,
    )

    assert metadata.original_filename == "resume.pdf"
    assert metadata.extension == "pdf"
    assert metadata.mime_type == PDF_MIME
    assert metadata.size == len(content)
    assert Path(metadata.storage_path).is_file()


def test_valid_docx_upload(tmp_path: Path) -> None:
    """Store a valid DOCX file."""
    service = make_service(tmp_path)
    content = b"docx bytes"

    metadata = service.store_job_description(
        original_filename="job.docx",
        mime_type=DOCX_MIME,
        content=content,
    )

    assert metadata.document_type == DocumentType.JOB_DESCRIPTION
    assert metadata.extension == "docx"
    assert Path(metadata.storage_path).is_file()


def test_empty_file_is_rejected(tmp_path: Path) -> None:
    """Reject zero-byte files."""
    service = make_service(tmp_path)

    with pytest.raises(EmptyFileError):
        service.store_resume(
            original_filename="resume.pdf",
            mime_type=PDF_MIME,
            content=b"",
        )


def test_wrong_extension_is_rejected(tmp_path: Path) -> None:
    """Reject unsupported file extensions."""
    service = make_service(tmp_path)

    with pytest.raises(UnsupportedFileTypeError):
        service.store_resume(
            original_filename="resume.txt",
            mime_type=PDF_MIME,
            content=b"not a pdf",
        )


def test_invalid_mime_is_rejected(tmp_path: Path) -> None:
    """Reject unsupported MIME types."""
    service = make_service(tmp_path)

    with pytest.raises(InvalidMimeTypeError):
        service.store_resume(
            original_filename="resume.pdf",
            mime_type="text/plain",
            content=b"%PDF-1.7",
        )


def test_oversized_file_is_rejected(tmp_path: Path) -> None:
    """Reject files larger than the configured size limit."""
    service = make_service(tmp_path, max_upload_size_bytes=4)

    with pytest.raises(FileTooLargeError):
        service.store_resume(
            original_filename="resume.pdf",
            mime_type=PDF_MIME,
            content=b"12345",
        )


def test_checksum_generation(tmp_path: Path) -> None:
    """Generate a SHA-256 checksum for stored content."""
    service = make_service(tmp_path)
    content = b"%PDF checksum"

    metadata = service.store_resume(
        original_filename="resume.pdf",
        mime_type=PDF_MIME,
        content=content,
    )

    assert metadata.sha256 == sha256(content).hexdigest()


def test_uuid_filename(tmp_path: Path) -> None:
    """Store files with UUID filenames."""
    service = make_service(tmp_path)

    metadata = service.store_resume(
        original_filename="resume.pdf",
        mime_type=PDF_MIME,
        content=b"%PDF uuid",
    )

    stored_id = metadata.stored_filename.removesuffix(".pdf")
    assert UUID(stored_id) == metadata.id
    assert metadata.stored_filename != metadata.original_filename


def test_duplicate_uploads_use_distinct_filenames(tmp_path: Path) -> None:
    """Store duplicate uploads as distinct UUID-backed files."""
    service = make_service(tmp_path)
    content = b"%PDF duplicate"

    first = service.store_resume(
        original_filename="resume.pdf",
        mime_type=PDF_MIME,
        content=content,
    )
    second = service.store_resume(
        original_filename="resume.pdf",
        mime_type=PDF_MIME,
        content=content,
    )

    assert first.stored_filename != second.stored_filename
    assert first.sha256 == second.sha256
    assert Path(first.storage_path).is_file()
    assert Path(second.storage_path).is_file()


def test_hidden_extension_is_rejected(tmp_path: Path) -> None:
    """Reject filenames with hidden extensions."""
    service = make_service(tmp_path)

    with pytest.raises(HiddenExtensionError):
        service.store_resume(
            original_filename="resume.exe.pdf",
            mime_type=PDF_MIME,
            content=b"%PDF hidden",
        )
