# 🏥 Radiology AI Reporter

**AI-Powered Chest X-Ray Analysis and Report Generation System**

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![YOLOv8](https://img.shields.io/badge/YOLOv8-Latest-yellow.svg)](https://github.com/ultralytics/ultralytics)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-MVP-yellow.svg)]()

> **Quick Start Version v0.1** - An MVP demonstrating AI-powered radiology workflow

---

## 🎯 Overview

An end-to-end AI system that:
- ✅ Analyzes chest X-ray images using YOLOv8
- ✅ Detects abnormalities and findings
- ✅ Generates professional radiology reports
- ✅ Provides complete clinical workflow integration
- ✅ Supports DICOM files

**Built for:** Healthcare IT companies, radiologists, AI researchers

---

## ✨ Features

- 🔍 **Anomaly Detection** - YOLOv8-based detection
- 📝 **Report Generation** - Automated professional reports
- 🏥 **DICOM Support** - Full DICOM file handling
- 🚀 **REST API** - FastAPI backend with Swagger docs
- 💻 **Web Interface** - Streamlit dashboard
- 📊 **Visualization** - Detection overlays on images

---

## 🚀 Quick Start

### Prerequisites
\\\ash
Python 3.10+
pip
virtualenv
\\\

### Installation

\\\powershell
# 1. Clone repository
git clone https://github.com/yourusername/radiology-ai-reporter.git
cd radiology-ai-reporter

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set Python path
$env:PYTHONPATH = "D:\projects\radiology-ai-reporter"  # Windows
# export PYTHONPATH=/path/to/radiology-ai-reporter  # Mac/Linux

# 5. Start API (Terminal 1)
python src\api\simple_api.py

# 6. Start Frontend (Terminal 2)
streamlit run src\frontend\simple_app.py
\\\

### Access
- **Frontend:** http://localhost:8501
- **API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

---

## 📖 Usage

### Web Interface
1. Open http://localhost:8501
2. Upload a chest X-ray image or DICOM file
3. Click "Analyze Image"
4. View results and download report

### API
\\\python
import requests

# Upload image
files = {'file': open('xray.jpg', 'rb')}
response = requests.post('http://localhost:8000/upload', files=files)
job_id = response.json()['job_id']

# Get result
result = requests.get(f'http://localhost:8000/result/{job_id}')
print(result.json())
\\\

---

## 🏗️ Architecture

\\\
Input (DICOM/Image)
    ↓
DICOM Handler
    ↓
Anomaly Detection (YOLOv8)
    ↓
Report Generation (Template-based)
    ↓
Output (Report + Visualization)
\\\

---

## 📁 Project Structure

\\\
radiology-ai-reporter/
├── src/
│   ├── api/              # FastAPI backend
│   ├── detection/        # Anomaly detection
│   ├── rag/             # Report generation
│   ├── dicom/           # DICOM handling
│   ├── pipeline/        # End-to-end pipeline
│   └── frontend/        # Streamlit UI
├── data/                # Data storage
├── models/              # Model weights
├── outputs/             # Results
├── requirements.txt     # Dependencies
└── README.md
\\\

---

## 🛣️ Roadmap

### ✅ Phase 1: MVP (Current)
- [x] Basic pipeline
- [x] YOLOv8 detection
- [x] Template reports
- [x] FastAPI backend
- [x] Streamlit frontend

### 🔄 Phase 2: Enhanced Detection
- [ ] Train on chest X-ray dataset (RSNA)
- [ ] Fine-tune YOLOv8 for radiology
- [ ] Multi-class detection (pneumonia, fractures, etc.)
- [ ] Improved accuracy metrics

### 📋 Phase 3: Advanced RAG
- [ ] Vector database (ChromaDB)
- [ ] LLM integration (LLaMA 3.1)
- [ ] Context-aware reports
- [ ] MIMIC-CXR dataset integration

### 🚢 Phase 4: Production Ready
- [ ] Docker containerization
- [ ] Authentication & authorization
- [ ] Database persistence (PostgreSQL)
- [ ] CI/CD pipeline
- [ ] Kubernetes deployment

---

## 📊 Performance

**Current Version (v0.1):**
- Processing Time: ~5-10 seconds per image
- Detection: YOLOv8 pretrained model
- Report: Template-based generation

**Planned Improvements:**
- Custom-trained detection model
- AI-powered report generation with LLM
- Sub-5 second processing time

---

## 🧪 Testing

\\\powershell
# Test individual components
python src\dicom\dicom_handler.py
python src\detection\simple_detector.py
python src\rag\simple_rag.py
python src\pipeline\simple_pipeline.py
\\\

---

## 🤝 Contributing

Contributions are welcome! This is an MVP with lots of room for improvement.

**Areas for contribution:**
- Model training and fine-tuning
- Additional datasets
- UI/UX improvements
- Documentation
- Testing

---

## ⚠️ Disclaimer

**For Research and Educational Use Only**

This is a proof-of-concept system. All AI-generated reports must be reviewed by qualified radiologists before any clinical use. This tool is designed to assist, not replace, professional medical judgment.

---

## 📄 License

MIT License - see LICENSE file for details

---

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your Profile](https://linkedin.com/in/yourprofile)
- Email: your.email@example.com

---

## 🙏 Acknowledgments

- [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Streamlit](https://streamlit.io/)
- RSNA for medical imaging datasets

---

## 📸 Screenshots

### Frontend Interface
![Frontend](docs/screenshots/frontend.png)

### Detection Results
![Detection](docs/screenshots/detection.png)

### Generated Report
![Report](docs/screenshots/report.png)

---

**⭐ Star this repo if you find it useful!**

**Built with ❤️ for the healthcare AI community**
