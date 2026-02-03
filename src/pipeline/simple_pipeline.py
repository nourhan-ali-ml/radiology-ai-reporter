from src.dicom.dicom_handler import DICOMHandler
from src.detection.simple_detector import SimpleDetector
from src.rag.simple_rag import SimpleRAG
from datetime import datetime
import json
import os

class SimplePipeline:
    """Simple end-to-end pipeline for testing"""
    
    def __init__(self):
        print("🚀 Initializing pipeline...")
        self.dicom_handler = DICOMHandler()
        self.detector = SimpleDetector()
        self.rag = SimpleRAG()
        print("✅ Pipeline ready!")
    
    def process_dicom(self, dicom_path: str, output_dir: str = 'outputs') -> dict:
        """Process a DICOM file"""
        start_time = datetime.now()
        
        print(f"\n{'='*60}")
        print(f"Processing: {os.path.basename(dicom_path)}")
        print(f"{'='*60}\n")
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Step 1: Read DICOM
        print("Step 1/5: Reading DICOM file...")
        try:
            dicom_data = self.dicom_handler.read_dicom(dicom_path)
            validation = self.dicom_handler.validate_dicom(dicom_path)
            
            if not validation['is_valid']:
                return {
                    'success': False,
                    'error': 'Invalid DICOM file',
                    'validation': validation
                }
            
            print("✅ DICOM read successfully")
        except Exception as e:
            return {
                'success': False,
                'error': f'Failed to read DICOM: {str(e)}'
            }
        
        # Step 2: Save image
        print("Step 2/5: Extracting image...")
        temp_image_path = f"{output_dir}/temp_image.png"
        self.dicom_handler.save_as_png(dicom_data['image'], temp_image_path)
        print(f"✅ Image saved to {temp_image_path}")
        
        # Step 3: Detect abnormalities
        print("Step 3/5: Running anomaly detection...")
        detections = self.detector.detect(temp_image_path)
        print(f"✅ Found {len(detections)} finding(s)")
        
        # Visualize
        detection_viz_path = f"{output_dir}/detections_visualized.png"
        self.detector.visualize_detections(
            temp_image_path,
            detections,
            detection_viz_path
        )
        
        # Step 4: Extract patient info
        print("Step 4/5: Extracting patient information...")
        patient_info = {
            'age': dicom_data['metadata']['patient_age'],
            'sex': dicom_data['metadata']['patient_sex'],
            'patient_id': dicom_data['metadata']['patient_id']
        }
        print("✅ Patient info extracted")
        
        # Step 5: Generate report
        print("Step 5/5: Generating radiology report...")
        report = self.rag.generate_report(detections, patient_info)
        validation_result = self.rag.validate_report(report, detections)
        print("✅ Report generated")
        
        # Calculate time
        processing_time = (datetime.now() - start_time).total_seconds()
        
        # Compile result
        result = {
            'success': True,
            'processing_time_seconds': processing_time,
            'dicom_metadata': dicom_data['metadata'],
            'patient_info': patient_info,
            'detections': detections,
            'report': report,
            'validation': validation_result,
            'output_files': {
                'detection_visualization': detection_viz_path,
                'report_json': f"{output_dir}/report.json",
                'report_text': f"{output_dir}/report.txt"
            }
        }
        
        # Save outputs
        self.save_results(result, output_dir)
        
        print(f"\n{'='*60}")
        print(f"✅ Processing completed in {processing_time:.2f} seconds")
        print(f"{'='*60}\n")
        
        return result
    
    def save_results(self, result: dict, output_dir: str):
        """Save all results"""
        # Save JSON
        with open(f"{output_dir}/complete_result.json", 'w') as f:
            json.dump(result, f, indent=2, default=str)
        
        # Save text report
        with open(f"{output_dir}/report.txt", 'w') as f:
            f.write("RADIOLOGY REPORT\n")
            f.write("="*60 + "\n\n")
            f.write(f"Patient ID: {result['patient_info']['patient_id']}\n")
            f.write(f"Age: {result['patient_info']['age']}, Sex: {result['patient_info']['sex']}\n")
            f.write("\n" + "="*60 + "\n\n")
            f.write(result['report']['full_text'])
        
        print(f"✅ Results saved to {output_dir}/")

if __name__ == "__main__":
    pipeline = SimplePipeline()
    print("\n🎉 Pipeline is ready to use!")
    print("\nTo process a DICOM file:")
    print("  result = pipeline.process_dicom('path/to/file.dcm')")