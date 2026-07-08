"""Unit and integration tests for FastAPI application endpoints."""

from pathlib import Path
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.core.config import get_settings
from app.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def override_directories(tmp_path: Path) -> None:
    """Redirect upload directories to a safe temporary test directory."""
    settings = get_settings()
    # Cache and override
    old_resume_dir = settings.resume_upload_dir
    old_job_dir = settings.job_upload_dir

    settings.resume_upload_dir = tmp_path / "resumes"
    settings.job_upload_dir = tmp_path / "jobs"
    settings.resume_upload_dir.mkdir(parents=True, exist_ok=True)
    settings.job_upload_dir.mkdir(parents=True, exist_ok=True)

    yield

    # Restore settings
    settings.resume_upload_dir = old_resume_dir
    settings.job_upload_dir = old_job_dir


# ── Tests ─────────────────────────────────────────────────────────────────────


def test_api_endpoint_health() -> None:
    """Verify health endpoint creation and success status."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_api_uploads() -> None:
    """Test POST /api/resume/upload and POST /api/job/upload."""
    # 1. Upload Resume
    res_file = {
        "file": ("resume.pdf", b"%PDF-1.4 dummy resume content", "application/pdf")
    }
    response = client.post("/api/resume/upload", files=res_file)
    assert response.status_code == 201
    assert "file_id" in response.json()
    resume_id = response.json()["file_id"]

    # Verify stored file exists
    settings = get_settings()
    stored_files = list(settings.resume_upload_dir.glob(f"{resume_id}.*"))
    assert len(stored_files) == 1
    assert stored_files[0].read_bytes() == b"%PDF-1.4 dummy resume content"

    # 2. Upload Job Description
    job_file = {"file": ("job.pdf", b"%PDF-1.4 dummy job content", "application/pdf")}
    response = client.post("/api/job/upload", files=job_file)
    assert response.status_code == 201
    assert "file_id" in response.json()
    job_id = response.json()["file_id"]

    stored_jobs = list(settings.job_upload_dir.glob(f"{job_id}.*"))
    assert len(stored_jobs) == 1
    assert stored_jobs[0].read_bytes() == b"%PDF-1.4 dummy job content"


def test_api_analyze_and_retrieve_success() -> None:
    """Verify successful end-to-end trigger, query, and report retrieval."""
    settings = get_settings()

    # Pre-populate test uploads
    res_id = str(uuid4())
    job_id = str(uuid4())

    resume_file = settings.resume_upload_dir / f"{res_id}.pdf"
    resume_file.write_bytes(b"%PDF-1.4 dummy resume content")

    job_file = settings.job_upload_dir / f"{job_id}.pdf"
    job_file.write_bytes(b"%PDF-1.4 dummy job description content")

    # 1. Trigger analysis
    payload = {"resume_id": res_id, "job_id": job_id}
    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert "analysis_id" in data
    assert "status" in data
    analysis_id = data["analysis_id"]

    # 2. Retrieve analysis results via GET /api/analysis/{id}
    resp_get = client.get(f"/api/analysis/{analysis_id}")
    assert resp_get.status_code == 200
    assert resp_get.json()["analysis_id"] == analysis_id
    assert resp_get.json()["result"]["summary"]["candidate_name"] == "N/A"

    # 3. Retrieve report via GET /api/report/{id}
    resp_report = client.get(f"/api/report/{analysis_id}")
    assert resp_report.status_code == 200
    assert resp_report.json()["analysis_id"] == analysis_id
    assert resp_report.json()["result"]["scores"]["overall"] == 0.0


def test_api_analyze_validation_and_not_found_errors() -> None:
    """Test validation errors for bad payloads and not found files/runs."""
    # 1. Missing fields payload
    bad_payload = {"resume_id": "only-resume"}
    response = client.post("/api/analyze", json=bad_payload)
    assert response.status_code == 422  # FastAPI validation error

    # 2. Non-existent file IDs
    missing_id_payload = {"resume_id": str(uuid4()), "job_id": str(uuid4())}
    response_missing = client.post("/api/analyze", json=missing_id_payload)
    assert response_missing.status_code == 404
    assert "not found" in response_missing.json()["detail"].lower()

    # 3. Non-existent analysis run ID
    bad_run_id = str(uuid4())
    resp_run = client.get(f"/api/analysis/{bad_run_id}")
    assert resp_run.status_code == 404
    assert "not found" in resp_run.json()["detail"].lower()

    # 4. Non-existent report run ID
    resp_rep = client.get(f"/api/report/{bad_run_id}")
    assert resp_rep.status_code == 404
    assert "not found" in resp_rep.json()["detail"].lower()
