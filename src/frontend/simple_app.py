import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import streamlit as st
import requests
from PIL import Image
import io
import time

# Config
st.set_page_config(
    page_title="Radiology AI Reporter",
    page_icon="🏥",
    layout="wide"
)

API_URL = "http://localhost:8000"

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🏥 Radiology AI Reporter</h1>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar
with st.sidebar:
    st.markdown("### About")
    st.info("""
    **Quick Start Version v0.1**
    
    🔍 Anomaly Detection  
    📝 Report Generation  
    🏥 DICOM Support
    
    This is an MVP version demonstrating the core workflow.
    """)
    
    st.markdown("---")
    st.markdown("### System Status")
    
    try:
        response = requests.get(f"{API_URL}/health", timeout=2)
        if response.status_code == 200:
            st.success("✅ API Connected")
        else:
            st.error("❌ API Error")
    except:
        st.error("❌ API Offline")
        st.warning("Please start the API:\n```python src/api/simple_api.py```")

# Main content
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 📤 Upload Image")
    uploaded_file = st.file_uploader(
        "Choose a DICOM or X-ray image",
        type=['dcm', 'png', 'jpg', 'jpeg'],
        help="Upload a chest X-ray image or DICOM file"
    )
    
    if uploaded_file:
        if uploaded_file.type.startswith('image'):
            st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
        else:
            st.success(f"✅ DICOM file: {uploaded_file.name}")

with col2:
    st.markdown("### ⚙️ Process")
    
    if uploaded_file:
        if st.button("🚀 Analyze Image", type="primary", use_container_width=True):
            with st.spinner("Processing..."):
                try:
                    files = {'file': (uploaded_file.name, uploaded_file.getvalue())}
                    response = requests.post(f"{API_URL}/upload", files=files)
                    
                    if response.status_code == 200:
                        data = response.json()
                        job_id = data['job_id']
                        
                        if data['status'] == 'completed':
                            st.success("✅ Processing completed!")
                            
                            result_response = requests.get(f"{API_URL}/result/{job_id}")
                            result = result_response.json()
                            
                            st.session_state.result = result
                            st.session_state.job_id = job_id
                            st.rerun()
                        else:
                            st.error(f"Processing failed: {data.get('message')}")
                    else:
                        st.error(f"Upload failed: {response.text}")
                
                except Exception as e:
                    st.error(f"Error: {str(e)}")

st.markdown("---")

# Results section
if 'result' in st.session_state and st.session_state.result:
    result = st.session_state.result
    job_id = st.session_state.job_id
    
    st.markdown("## 📊 Analysis Results")
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Findings Detected", len(result['detections']))
    with col2:
        if result['detections']:
            urgencies = [d['urgency'] for d in result['detections']]
            high_count = urgencies.count('high')
            st.metric("High Urgency", high_count)
        else:
            st.metric("Status", "Clear")
    with col3:
        if result.get('processing_time_seconds'):
            st.metric("Processing Time", f"{result['processing_time_seconds']:.1f}s")
    
    # Visualization and Findings
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔍 Detection Visualization")
        try:
            viz_response = requests.get(f"{API_URL}/visualization/{job_id}")
            if viz_response.status_code == 200:
                image = Image.open(io.BytesIO(viz_response.content))
                st.image(image, use_container_width=True)
        except:
            st.warning("Visualization not available")
    
    with col2:
        st.markdown("### 📋 Detected Findings")
        
        if len(result['detections']) == 0:
            st.success("✅ No significant abnormalities detected")
        else:
            for i, det in enumerate(result['detections'], 1):
                urgency_emoji = {
                    'high': '🔴',
                    'moderate': '🟠',
                    'low': '🟢'
                }[det['urgency']]
                
                with st.expander(f"{urgency_emoji} Finding {i}: {det['finding'].title()}"):
                    st.write(f"**Confidence:** {det['confidence']:.2%}")
                    st.write(f"**Urgency:** {det['urgency'].title()}")
    
    # Report
    st.markdown("---")
    st.markdown("### 📄 Generated Report")
    
    report = result['report']
    
    st.markdown("#### FINDINGS")
    st.info(report['findings'])
    
    st.markdown("#### IMPRESSION")
    st.info(report['impression'])
    
    if report.get('recommendations'):
        st.markdown("#### RECOMMENDATIONS")
        st.info(report['recommendations'])
    
    # Download button
    st.markdown("---")
    report_text = report['full_text']
    st.download_button(
        label="📥 Download Report",
        data=report_text,
        file_name=f"report_{job_id}.txt",
        mime="text/plain"
    )

else:
    st.info("👆 Upload an image to get started!")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p><strong>Radiology AI Reporter</strong> - Quick Start Version v0.1</p>
    <p>For research and educational purposes only</p>
</div>
""", unsafe_allow_html=True)