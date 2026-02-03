# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] - 2026-02-03

### Added
- Initial MVP release
- DICOM file handler with metadata extraction
- YOLOv8-based anomaly detection
- Template-based report generation
- FastAPI REST API backend
- Streamlit web interface
- Complete end-to-end pipeline
- Basic documentation

### Features
- Upload DICOM or image files
- Automatic detection of abnormalities
- Professional radiology report generation
- Visual detection overlay
- Downloadable reports

### Known Limitations
- Uses pretrained YOLOv8 (not specialized for radiology)
- Template-based reports (not LLM-powered)
- No user authentication
- No database persistence
- Limited to chest X-rays

## [Unreleased]

### Planned
- Custom model training on RSNA dataset
- LLM-powered report generation
- Vector database for RAG
- User authentication
- Production deployment
