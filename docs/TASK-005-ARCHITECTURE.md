# TASK-005 (Phase A) — Structured Document Analyzer Architecture

> **Status**: Architecture Only — No Implementation  
> **Input**: `DocumentContent` (output of TASK-004 pipeline)  
> **Output**: `StructuredDocument` (document-type-agnostic)

---

## 1. Architecture Overview

The Structured Document Analyzer is a pure domain-analysis module.

It sits between the Document Intelligence Pipeline (TASK-004) and all downstream
type-specific parsers (Resume Parser, JD Parser, etc.).

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     CLEAN ARCHITECTURE LAYERS                           │
├─────────────────────────────────────────────────────────────────────────┤
│  PRESENTATION        (FastAPI routes)                                   │
│       ↓                                                                 │
│  APPLICATION         (future: AnalyzerApplicationService)               │
│       ↓                                                                 │
│  INFRASTRUCTURE      app/infrastructure/analyzer/                       │
│       ├── HeadingDetector                                               │
│       ├── SectionDetector                                               │
│       ├── SectionClassifier                                             │
│       └── StructuredDocumentBuilder                                     │
│       ↓                                                                 │
│  DOMAIN              app/domain/entities/                               │
│       ├── DocumentContent  ← INPUT                                      │
│       ├── DocumentSection                                               │
│       ├── SectionType  (enum)                                           │
│       └── StructuredDocument  ← OUTPUT                                  │
└─────────────────────────────────────────────────────────────────────────┘
```

**Key invariant**: The analyzer receives only `DocumentContent`.
It has zero knowledge of whether the document is a resume, JD, or certificate.

---

## 2. Architecture Diagram

```
                          DocumentContent
                               │
                               ▼
              ┌────────────────────────────────┐
              │  StructuredDocumentAnalyzer    │  ← public entry point
              │  (infrastructure orchestrator) │
              └───────────────┬────────────────┘
                              │
              ┌───────────────┼───────────────┐
              │               │               │
              ▼               ▼               ▼
     ┌──────────────┐ ┌──────────────┐ ┌──────────────────────┐
     │ HeadingDetec-│ │SectionDetect-│ │  SectionClassifier   │
     │ tor          │ │or            │ │                      │
     │              │ │              │ │  (rule-based only,   │
     │ Detects which│ │Groups TextBl-│ │   no AI)             │
     │ TextBlocks   │ │ocks into     │ │                      │
     │ are headings │ │candidate     │ │  Assigns SectionType │
     └──────┬───────┘ │sections using│ │  enum value to each  │
            │         │heading bound-│ │  candidate section   │
            │         │aries         │ └──────────┬───────────┘
            │         └──────┬───────┘            │
            │                │                    │
            └────────────────▼────────────────────┘
                             │
                             ▼
              ┌──────────────────────────────────┐
              │    StructuredDocumentBuilder     │
              │                                  │
              │  Assembles DocumentSection list  │
              │  and produces StructuredDocument │
              └────────────────┬─────────────────┘
                               │
                               ▼
                      StructuredDocument
```

---

## 3. Sequence Diagram

```
Caller                  StructuredDocumentAnalyzer
  │                              │
  │  analyze(document_content)   │
  │─────────────────────────────►│
  │                              │
  │                              │──── heading_detector.detect(pages)
  │                              │         │
  │                              │◄────────┘  list[HeadingCandidate]
  │                              │
  │                              │──── section_detector.detect(
  │                              │         pages, heading_candidates)
  │                              │         │
  │                              │◄────────┘  list[RawSection]
  │                              │
  │                              │──── section_classifier.classify(
  │                              │         raw_sections)
  │                              │         │
  │                              │◄────────┘  list[ClassifiedSection]
  │                              │
  │                              │──── builder.build(
  │                              │         document_content,
  │                              │         classified_sections)
  │                              │         │
  │                              │◄────────┘  StructuredDocument
  │                              │
  │◄─────────────────────────────│  StructuredDocument
  │
```

---

## 4. Class Diagram

```
┌────────────────────────────────────────────────────────────────────────┐
│                        DOMAIN ENTITIES                                  │
├────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────────────────┐                                   │
│  │  «frozen dataclass»             │                                   │
│  │  StructuredDocument             │                                   │
│  ├─────────────────────────────────┤                                   │
│  │  document_content: DocumentCont │                                   │
│  │  sections: list[DocumentSection]│                                   │
│  │  section_count: int             │                                   │
│  │  has_clear_structure: bool      │                                   │
│  └─────────────────────────────────┘                                   │
│              1 ──────────────────── *                                   │
│  ┌─────────────────────────────────┐                                   │
│  │  «frozen dataclass»             │                                   │
│  │  DocumentSection                │                                   │
│  ├─────────────────────────────────┤                                   │
│  │  section_index: int             │                                   │
│  │  section_type: SectionType      │                                   │
│  │  title: str | None              │                                   │
│  │  content: str                   │                                   │
│  │  text_blocks: list[TextBlock]   │                                   │
│  │  start_page: int                │                                   │
│  │  end_page: int                  │                                   │
│  │  confidence: float              │                                   │
│  └─────────────────────────────────┘                                   │
│                                                                         │
│  ┌─────────────────────────────────┐                                   │
│  │  «StrEnum»                      │                                   │
│  │  SectionType                    │                                   │
│  ├─────────────────────────────────┤                                   │
│  │  HEADER          SKILLS         │                                   │
│  │  SUMMARY         PROJECTS       │                                   │
│  │  EXPERIENCE      EDUCATION      │                                   │
│  │  CERTIFICATIONS  LANGUAGES      │                                   │
│  │  PUBLICATIONS    AWARDS         │                                   │
│  │  REFERENCES      BODY           │                                   │
│  │  UNKNOWN                        │                                   │
│  └─────────────────────────────────┘                                   │
└────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────┐
│                     INFRASTRUCTURE (INTERNAL)                           │
├────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌──────────────────────────────────┐                                  │
│  │  «frozen dataclass» (internal)   │                                  │
│  │  HeadingCandidate                │                                  │
│  ├──────────────────────────────────┤                                  │
│  │  text_block: TextBlock           │                                  │
│  │  confidence: float               │                                  │
│  │  signals: list[str]              │                                  │
│  └──────────────────────────────────┘                                  │
│                                                                         │
│  ┌──────────────────────────────────┐                                  │
│  │  «frozen dataclass» (internal)   │                                  │
│  │  RawSection                      │                                  │
│  ├──────────────────────────────────┤                                  │
│  │  section_index: int              │                                  │
│  │  heading: HeadingCandidate|None  │                                  │
│  │  text_blocks: list[TextBlock]    │                                  │
│  │  content: str                    │                                  │
│  │  start_page: int                 │                                  │
│  │  end_page: int                   │                                  │
│  └──────────────────────────────────┘                                  │
│                                                                         │
│  ┌──────────────────────────────────┐                                  │
│  │  «frozen dataclass» (internal)   │                                  │
│  │  ClassifiedSection               │                                  │
│  ├──────────────────────────────────┤                                  │
│  │  raw_section: RawSection         │                                  │
│  │  section_type: SectionType       │                                  │
│  │  confidence: float               │                                  │
│  └──────────────────────────────────┘                                  │
│                                                                         │
└────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────┐
│                      INFRASTRUCTURE COMPONENTS                          │
├────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  «Protocol»  HeadingDetectorProtocol                                   │
│    detect(*, pages: list[Page]) → list[HeadingCandidate]               │
│  ▲ implements: HeadingDetector                                          │
│    _score_block(block) → float                                          │
│    _is_short_line / _is_all_caps / _ends_without_period                 │
│                                                                         │
│  «Protocol»  SectionDetectorProtocol                                   │
│    detect(*, pages, headings) → list[RawSection]                        │
│  ▲ implements: SectionDetector                                          │
│    _group_blocks_into_sections(…)                                       │
│                                                                         │
│  «Protocol»  SectionClassifierProtocol                                 │
│    classify(*, sections: list[RawSection]) → list[ClassifiedSection]   │
│  ▲ implements: SectionClassifier                                        │
│    _keyword_map: dict[str, SectionType]  (class constant)              │
│    _match_keywords(title) → tuple[SectionType, float]                  │
│                                                                         │
│  «Protocol»  StructuredDocumentBuilderProtocol                         │
│    build(*, document_content, classified_sections)→StructuredDocument  │
│  ▲ implements: StructuredDocumentBuilder                                │
│    _has_clear_structure(sections) → bool                               │
│                                                                         │
│  StructuredDocumentAnalyzer  (orchestrator — public entry point)        │
│    __init__(heading_detector, section_detector,                         │
│             section_classifier, builder)                                │
│    analyze(*, document_content) → StructuredDocument                   │
│                                                                         │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Folder Structure

```text
backend/app/
├── domain/
│   └── entities/
│       ├── document_content.py       ← existing (TASK-004)
│       ├── document_section.py       ← NEW: DocumentSection + SectionType
│       └── structured_document.py   ← NEW: StructuredDocument
│
└── infrastructure/
    └── analyzer/                     ← NEW module (TASK-005)
        ├── __init__.py               ← exports StructuredDocumentAnalyzer
        ├── exceptions.py             ← AnalyzerError hierarchy
        ├── interfaces.py             ← Protocols for all 4 components
        ├── models.py                 ← HeadingCandidate, RawSection, ClassifiedSection
        ├── heading_detector.py       ← Stage 1
        ├── section_detector.py       ← Stage 2
        ├── section_classifier.py     ← Stage 3
        ├── structured_document_builder.py  ← Stage 4
        └── document_analyzer.py     ← StructuredDocumentAnalyzer orchestrator

tests/
└── test_structured_document_analyzer.py   ← NEW (Phase B — implementation)
```

---

## 6. Interface Definitions

### 6.1 Domain Entities (new)

```
SectionType  (StrEnum)
─────────────────────
HEADER          — Name / contact block at the document top
SUMMARY         — Summary, profile, objective, about
EXPERIENCE      — Work history, employment, career
EDUCATION       — Education, academic background, qualifications
SKILLS          — Skills, competencies, technologies, tools
CERTIFICATIONS  — Certifications, licenses, credentials
PROJECTS        — Projects, portfolio items
AWARDS          — Awards, honors, achievements, recognition
LANGUAGES       — Languages, spoken languages
PUBLICATIONS    — Publications, papers, research
REFERENCES      — References, referees
BODY            — Unheaded content that is not the header block
UNKNOWN         — Could not be classified with confidence ≥ threshold


DocumentSection  (frozen dataclass)
────────────────────────────────────
section_index : int              — 0-based position in document
section_type  : SectionType      — classifier result
title         : str | None       — heading text if found, else None
content       : str              — full section text (concatenated blocks)
text_blocks   : list[TextBlock]  — ordered source blocks
start_page    : int              — 1-based first page
end_page      : int              — 1-based last page
confidence    : float            — classifier confidence [0.0 – 1.0]


StructuredDocument  (frozen dataclass)
───────────────────────────────────────
document_content    : DocumentContent     — source (pass-through)
sections            : list[DocumentSection] — ordered, non-overlapping
section_count       : int                 — len(sections)
has_clear_structure : bool                — true if ≥ 2 sections with
                                            confidence ≥ 0.7
```

### 6.2 Infrastructure Internal Models

```
HeadingCandidate  (frozen dataclass — internal, never escapes analyzer/)
───────────────────────────────────────────────────────────────────────
text_block : TextBlock
confidence : float           — scoring result [0.0 – 1.0]
signals    : list[str]       — e.g. ["all_caps", "short_line", "no_period"]


RawSection  (frozen dataclass — internal)
─────────────────────────────────────────
section_index : int
heading       : HeadingCandidate | None
text_blocks   : list[TextBlock]
content       : str
start_page    : int
end_page      : int


ClassifiedSection  (frozen dataclass — internal)
─────────────────────────────────────────────────
raw_section  : RawSection
section_type : SectionType
confidence   : float
```

### 6.3 Component Protocols

```
HeadingDetectorProtocol
  detect(*, pages: list[Page]) → list[HeadingCandidate]
  Contract: preserves reading order, confidence ∈ [0.0, 1.0], no mutation

SectionDetectorProtocol
  detect(*, pages: list[Page], headings: list[HeadingCandidate]) → list[RawSection]
  Contract: every TextBlock appears in exactly one RawSection, order preserved

SectionClassifierProtocol
  classify(*, sections: list[RawSection]) → list[ClassifiedSection]
  Contract: 1-to-1 output, rule-based only, UNKNOWN if no match

StructuredDocumentBuilderProtocol
  build(*, document_content: DocumentContent,
            classified_sections: list[ClassifiedSection]) → StructuredDocument
  Contract: always returns, never raises
```

### 6.4 Exception Hierarchy

```
AnalyzerError               (base)
├── HeadingDetectionError
├── SectionDetectionError
├── SectionClassificationError
└── AnalyzerBuildError
```

---

## 7. Data Flow

```
DocumentContent.pages  →  HeadingDetector  →  list[HeadingCandidate]
                                                        │
DocumentContent.pages  ──────────────────────►  SectionDetector
                                                        │
                                               list[RawSection]
                                                        │
                                            SectionClassifier
                                                        │
                                        list[ClassifiedSection]
                                                        │
DocumentContent  ────────────────────► StructuredDocumentBuilder
                                                        │
                                           StructuredDocument
```

**Heading detection signals** (heuristic, no AI):

| Signal | Rule |
|---|---|
| `short_line` | `len(text.split()) ≤ 6` |
| `all_caps` | `text.upper() == text` and `len(text) > 1` |
| `title_case` | `text.istitle()` |
| `no_period` | `not text.strip().endswith(".")` |
| `bbox_tall` | `bbox height > avg_block_height × 1.2` (PDF only) |
| `isolated` | no adjacent blocks within 10pt vertical gap (PDF only) |

**Classification keyword map** (exact substring match, case-insensitive):

| Keywords | SectionType |
|---|---|
| `summary`, `profile`, `about`, `objective`, `overview` | `SUMMARY` |
| `experience`, `work`, `employment`, `career`, `history` | `EXPERIENCE` |
| `education`, `academic`, `qualification`, `degree` | `EDUCATION` |
| `skill`, `competenc`, `technolog`, `tool`, `expertise` | `SKILLS` |
| `certif`, `licens`, `credential` | `CERTIFICATIONS` |
| `project`, `portfolio` | `PROJECTS` |
| `award`, `honor`, `achievement`, `recognition` | `AWARDS` |
| `language`, `spoken` | `LANGUAGES` |
| `publication`, `paper`, `research` | `PUBLICATIONS` |
| `reference`, `referee` | `REFERENCES` |
| `heading=None` (first block) | `HEADER` |
| no match | `UNKNOWN` |

---

## 8. Design Decisions

| Decision | Rationale |
|---|---|
| Protocols for all 4 components | Independent testability; swappable in future (e.g. ML heading detector) |
| `SectionType.UNKNOWN` not an exception | Downstream parsers must handle partially-structured docs |
| `SectionType.HEADER` for pre-heading block | Resume/CV always starts with name/contact before any section title |
| `SectionType.BODY` for unheaded non-header blocks | Covers prose documents (cover letters) with no section headings |
| Keyword map as a class-level constant | Deterministic, auditable, no hidden state |
| `confidence` on all domain and internal models | Full XAI traceability from detection to final output |
| `signals: list[str]` on `HeadingCandidate` | Human-readable audit trail — required for M.Sc. research quality |
| Internal models never leave `infrastructure/analyzer/` | Domain layer stays pure — only `DocumentSection` and `StructuredDocument` cross the boundary |

---

## 9. Future Extensibility

| Future Capability | Extension Point |
|---|---|
| Font-size / bold-aware heading detection | New class implementing `HeadingDetectorProtocol` |
| ML/LLM section classification | New class implementing `SectionClassifierProtocol` |
| Multi-language keyword maps | Constructor injection in `SectionClassifier` |
| Sub-section hierarchy | Add `sub_sections: list[DocumentSection]` to `DocumentSection` |
| Table/image-aware sections | Pass `Page.tables` / `Page.images` into `SectionDetector` |
