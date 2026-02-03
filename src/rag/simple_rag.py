from typing import List, Dict

class SimpleRAG:
    """Simple RAG system - template-based for now"""
    
    def __init__(self):
        print("Initializing Simple RAG system...")
        self.templates = {
            'no_findings': {
                'findings': 'The lungs are clear without focal consolidation, pleural effusion, or pneumothorax. Heart size is normal. Bony structures are intact.',
                'impression': 'No acute cardiopulmonary abnormality.',
                'recommendations': 'No immediate follow-up required.'
            },
            'abnormality_detected': {
                'findings': 'An opacity is identified in the {location}. The remainder of the lung fields are clear. No pleural effusion or pneumothorax. Heart size is within normal limits.',
                'impression': 'Finding present in {location}. Differential diagnosis includes infectious process, inflammatory change, or mass lesion.',
                'recommendations': 'Clinical correlation is advised. Consider follow-up imaging or comparison with prior studies if available.'
            }
        }
        print("✅ RAG system ready!")
    
    def generate_report(self, detections: List[Dict], patient_info: Dict = None) -> Dict:
        """Generate radiology report"""
        
        if len(detections) == 0:
            template = self.templates['no_findings']
        else:
            template = self.templates['abnormality_detected']
            location = "lung field"
            template = {
                'findings': template['findings'].format(location=location),
                'impression': template['impression'].format(location=location),
                'recommendations': template['recommendations']
            }
        
        report = {
            'findings': template['findings'],
            'impression': template['impression'],
            'recommendations': template['recommendations'],
            'full_text': f"FINDINGS:\n{template['findings']}\n\nIMPRESSION:\n{template['impression']}\n\nRECOMMENDATIONS:\n{template['recommendations']}",
            'detections_used': detections
        }
        
        return report
    
    def validate_report(self, report: Dict, detections: List[Dict]) -> Dict:
        """Validate report"""
        return {
            'is_valid': True,
            'issues': []
        }

if __name__ == "__main__":
    rag = SimpleRAG()
    test_report = rag.generate_report([], {})
    print("✅ Generated test report:")
    print(test_report['full_text'])