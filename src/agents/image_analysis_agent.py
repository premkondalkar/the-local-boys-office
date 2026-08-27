import os
import logging
from typing import Dict, Any, List
from .base_agent import BaseAgent
import openai
import base64
from pathlib import Path

logger = logging.getLogger(__name__)

class ImageAnalysisAgent(BaseAgent):
    """Agent for analyzing product images and extracting metadata"""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__("ImageAnalysisAgent", config)
        self.api_key = os.getenv('OPENAI_API_KEY')
        openai.api_key = self.api_key
        self.model = config.get('model', 'gpt-4-vision') if config else 'gpt-4-vision'
    
    def validate_input(self, **kwargs) -> bool:
        """Validate image analysis parameters"""
        required = ['image_path'] or ['image_url']
        return any(key in kwargs for key in required)
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """Analyze product image and extract metadata
        
        Args:
            image_path: Local path to image file
            image_url: URL of image
            max_keywords: Maximum keywords to extract
            
        Returns:
            Dict with keywords, description, and importance score
        """
        try:
            if not self.validate_input(**kwargs):
                return {
                    'success': False,
                    'error': 'Missing required parameters: image_path or image_url'
                }
            
            image_source = kwargs.get('image_path') or kwargs.get('image_url')
            max_keywords = kwargs.get('max_keywords', 10)
            
            self.log_execution('INFO', f"Analyzing image: {image_source}")
            
            # Prepare image for API
            if 'image_path' in kwargs:
                image_data = self._encode_image(kwargs['image_path'])
                image_param = {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}
                }
            else:
                image_param = {
                    "type": "image_url",
                    "image_url": {"url": kwargs['image_url']}
                }
            
            # Analyze with vision model
            analysis_prompt = f"""Analyze this product image and provide:
            1. Top {max_keywords} SEO keywords relevant to the product
            2. A concise product description (2-3 sentences)
            3. Importance/Relevance score (1-10)
            4. Product category
            5. Key product features
            
            Format response as JSON with keys: keywords, description, importance_score, category, features"""
            
            # Using gpt-4-turbo with vision capability
            response = openai.ChatCompletion.create(
                model="gpt-4-turbo",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            image_param,
                            {"type": "text", "text": analysis_prompt}
                        ]
                    }
                ],
                max_tokens=1000
            )
            
            result_text = response['choices'][0]['message']['content']
            
            self.log_execution('SUCCESS', "Image analysis completed")
            
            return {
                'success': True,
                'analysis': result_text,
                'model': self.model,
                'image_source': image_source
            }
            
        except Exception as e:
            self.log_execution('ERROR', f"Image analysis failed: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _encode_image(self, image_path: str) -> str:
        """Encode image to base64
        
        Args:
            image_path: Path to image file
            
        Returns:
            Base64 encoded image string
        """
        with open(image_path, 'rb') as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    def extract_keywords(self, image_path: str, num_keywords: int = 10) -> Dict[str, Any]:
        """Extract SEO keywords from image
        
        Args:
            image_path: Path to image file
            num_keywords: Number of keywords to extract
            
        Returns:
            Dict with extracted keywords and their importance scores
        """
        analysis = self.execute(image_path=image_path, max_keywords=num_keywords)
        
        if not analysis['success']:
            return analysis
        
        return {
            'success': True,
            'image_path': image_path,
            'analysis': analysis['analysis']
        }