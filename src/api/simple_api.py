import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import shutil
from datetime import datetime
import uuid
import json

from src.pipeline.simple_pipeline import SimplePipeline

# Initialize FastAPI
app = FastAPI(
    title="Radiology AI Reporter API",
    description="Quick Start Version - AI-powered radiology report generation",
    version="0.1.0-alpha"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize pipeline
print("🚀 Initializing pipeline...")
pipeline = SimplePipeline()
print("✅ Pipeline ready!")

# Simple in-memory job storage
jobs = {}

@app.get("/")
async def root():
    """API welcome message"""
    return {
        "service": "Radiology AI Reporter",
        "version": "0.1.0-alpha",
        "status": "running",
        "description": "Quick Start Version - MVP",
        "endpoints": {
            "health": "/health",
            "upload": "/upload (POST)",
            "status": "/status/{job_id}",
            "result": "/result/{job_id}",
            "report": "/report/{job_id}"
        }
    }

@app.get("/health")
async def health():
    """Health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "components": {
            "pipeline": "ready",
            "detector": "ready",
            "rag": "ready"
        }
    }

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload file for processing"""
    if not file.filename.lower().endswith(('.dcm', '.png', '.jpg', '.jpeg')):
        raise HTTPException(
            status_code=400, 
            detail="File must be DICOM (.dcm) or image (.png, .jpg)"
        )
    
    job_id = str(uuid.uuid4())[:8]
    
    upload_dir = f"uploads/{job_id}"
    output_dir = f"outputs/{job_id}"
    os.makedirs(upload_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    
    file_path = f"{upload_dir}/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    jobs[job_id] = {
        'job_id': job_id,
        'filename': file.filename,
        'status': 'uploaded',
        'created_at': datetime.now().isoformat(),
        'file_path': file_path,
        'output_dir': output_dir
    }
    
    try:
        jobs[job_id]['status'] = 'processing'
        
        if file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            result = process_image(file_path, output_dir)
        else:
            result = pipeline.process_dicom(file_path, output_dir)
        
        jobs[job_id]['status'] = 'completed'
        jobs[job_id]['result'] = result
        jobs[job_id]['completed_at'] = datetime.now().isoformat()
        
    except Exception as e:
        jobs[job_id]['status'] = 'failed'
        jobs[job_id]['error'] = str(e)
    
    return {
        "job_id": job_id,
        "status": jobs[job_id]['status'],
        "message": "Processing started" if jobs[job_id]['status'] != 'failed' else f"Error: {jobs[job_id].get('error')}"
    }

def process_image(image_path: str, output_dir: str):
    """Process regular image file"""
    from src.detection.simple_detector import SimpleDetector
    from src.rag.simple_rag import SimpleRAG
    
    detector = SimpleDetector()
    rag = SimpleRAG()
    
    detections = detector.detect(image_path)
    
    detector.visualize_detections(
        image_path,
        detections,
        f"{output_dir}/detections_visualized.png"
    )
    
    report = rag.generate_report(detections, {})
    
    with open(f"{output_dir}/report.txt", 'w') as f:
        f.write(report['full_text'])
    
    return {
        'success': True,
        'detections': detections,
        'report': report,
        'processing_time_seconds': 0,
        'output_files': {
            'visualization': f"{output_dir}/detections_visualized.png",
            'report': f"{output_dir}/report.txt"
        }
    }

@app.get("/status/{job_id}")
async def get_status(job_id: str):
    """Get job status"""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = jobs[job_id]
    return {
        "job_id": job_id,
        "status": job['status'],
        "created_at": job['created_at'],
        "completed_at": job.get('completed_at'),
        "error": job.get('error')
    }

@app.get("/result/{job_id}")
async def get_result(job_id: str):
    """Get complete result"""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = jobs[job_id]
    
    if job['status'] != 'completed':
        raise HTTPException(
            status_code=400,
            detail=f"Job not completed. Status: {job['status']}"
        )
    
    return job['result']

@app.get("/report/{job_id}")
async def get_report_text(job_id: str):
    """Download report as text file"""
    if job_id not in jobs or jobs[job_id]['status'] != 'completed':
        raise HTTPException(status_code=404, detail="Report not available")
    
    report_path = f"outputs/{job_id}/report.txt"
    
    if not os.path.exists(report_path):
        raise HTTPException(status_code=404, detail="Report file not found")
    
    return FileResponse(
        report_path,
        media_type='text/plain',
        filename=f'report_{job_id}.txt'
    )

@app.get("/visualization/{job_id}")
async def get_visualization(job_id: str):
    """Get detection visualization"""
    if job_id not in jobs or jobs[job_id]['status'] != 'completed':
        raise HTTPException(status_code=404, detail="Visualization not available")
    
    viz_path = f"outputs/{job_id}/detections_visualized.png"
    
    if not os.path.exists(viz_path):
        raise HTTPException(status_code=404, detail="Visualization not found")
    
    return FileResponse(viz_path, media_type='image/png')

@app.get("/jobs")
async def list_jobs():
    """List all jobs"""
    return {
        "total": len(jobs),
        "jobs": list(jobs.values())
    }

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🚀 Starting Radiology AI Reporter API")
    print("="*60)
    print("\n📍 API will be available at: http://localhost:8000")
    print("📚 API Documentation at: http://localhost:8000/docs")
    print("\n" + "="*60 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)