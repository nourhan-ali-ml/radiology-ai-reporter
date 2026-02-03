import pydicom
from pydicom.dataset import Dataset, FileDataset
from datetime import datetime
import numpy as np
from PIL import Image
import json
from typing import Dict, Optional

class DICOMHandler:
    """Handle DICOM files - read, parse, convert"""
    
    def __init__(self):
        self.supported_modalities = ['CR', 'DX', 'CT', 'MR']
    
    def read_dicom(self, dicom_path: str) -> Dict:
        """Read DICOM file and extract metadata + image"""
        try:
            dcm = pydicom.dcmread(dicom_path)
            
            dicom_data = {
                'metadata': self.extract_metadata(dcm),
                'image': self.extract_image(dcm),
                'raw_dicom': dcm
            }
            
            return dicom_data
            
        except Exception as e:
            raise Exception(f"Error reading DICOM: {str(e)}")
    
    def extract_metadata(self, dcm: FileDataset) -> Dict:
        """Extract relevant DICOM metadata"""
        metadata = {
            'patient_id': str(dcm.get('PatientID', 'Unknown')),
            'patient_name': str(dcm.get('PatientName', 'Unknown')),
            'patient_age': self.calculate_age(dcm),
            'patient_sex': str(dcm.get('PatientSex', 'Unknown')),
            'study_date': str(dcm.get('StudyDate', '')),
            'modality': str(dcm.get('Modality', '')),
            'rows': int(dcm.get('Rows', 0)),
            'columns': int(dcm.get('Columns', 0))
        }
        
        return metadata
    
    def calculate_age(self, dcm: FileDataset) -> Optional[int]:
        """Calculate patient age"""
        try:
            if 'PatientAge' in dcm:
                age_str = str(dcm.PatientAge)
                return int(age_str.replace('Y', ''))
            return None
        except:
            return None
    
    def extract_image(self, dcm: FileDataset) -> np.ndarray:
        """Extract and normalize image from DICOM"""
        img = dcm.pixel_array
        img = self.normalize_image(img)
        
        if hasattr(dcm, 'PhotometricInterpretation'):
            if dcm.PhotometricInterpretation == "MONOCHROME1":
                img = np.max(img) - img
        
        return img
    
    def normalize_image(self, image):
        """Normalize image to 0-255 range"""
        img_min = np.min(image)
        img_max = np.max(image)
        
        if img_max > img_min:
            image = ((image - img_min) / (img_max - img_min) * 255).astype(np.uint8)
        
        return image
    
    def save_as_png(self, image: np.ndarray, output_path: str):
        """Save DICOM image as PNG"""
        img_pil = Image.fromarray(image)
        if img_pil.mode != 'RGB':
            img_pil = img_pil.convert('RGB')
        img_pil.save(output_path)
    
    def validate_dicom(self, dicom_path: str) -> Dict:
        """Validate DICOM file"""
        validation = {
            'is_valid': True,
            'errors': [],
            'warnings': []
        }
        
        try:
            dcm = pydicom.dcmread(dicom_path)
            
            required_tags = ['PatientID', 'Modality']
            
            for tag in required_tags:
                if tag not in dcm:
                    validation['errors'].append(f"Missing required tag: {tag}")
                    validation['is_valid'] = False
            
            if 'PixelData' not in dcm:
                validation['errors'].append("No pixel data found")
                validation['is_valid'] = False
            
        except Exception as e:
            validation['is_valid'] = False
            validation['errors'].append(f"Failed to read DICOM: {str(e)}")
        
        return validation

if __name__ == "__main__":
    handler = DICOMHandler()
    print("✅ DICOM Handler created successfully!")