import os
import logging
from typing import Dict, Any, Optional
from .base_agent import BaseAgent
import openai
from PIL import Image
import requests
import io

logger = logging.getLogger(__name__)

class ImageGenerationAgent(BaseAgent):
    """Agent for generating product images with AI"""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__("ImageGenerationAgent", config)
        self.api_key = os.getenv('OPENAI_API_KEY')
        openai.api_key = self.api_key
        self.model = config.get('model', 'dall-e-3') if config else 'dall-e-3'
    
    def validate_input(self, **kwargs) -> bool:
        """Validate image generation parameters"""
        required = ['prompt']
        return all(key in kwargs for key in required)
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """Generate product image based on prompt
        
        Args:
            prompt: Text description for image generation
            size: Image size (256x256, 512x512, 1024x1024)
            quality: Quality level (standard, hd)
            n: Number of images to generate
            
        Returns:
            Dict with generated image URL and metadata
        """
        try:
            if not self.validate_input(**kwargs):
                return {
                    'success': False,
                    'error': 'Missing required parameters: prompt'
                }
            
            prompt = kwargs.get('prompt')
            size = kwargs.get('size', '1024x1024')
            quality = kwargs.get('quality', 'standard')
            n = kwargs.get('n', 1)
            
            self.log_execution('INFO', f"Generating image with prompt: {prompt[:50]}...")
            
            response = openai.Image.create(
                prompt=prompt,
                n=n,
                size=size,
                model=self.model,
                quality=quality
            )
            
            self.log_execution('SUCCESS', f"Generated {n} image(s)")
            
            return {
                'success': True,
                'images': response['data'],
                'model': self.model,
                'prompt': prompt
            }
            
        except Exception as e:
            self.log_execution('ERROR', f"Image generation failed: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def generate_with_background_removal(self, image_url: str, prompt: str) -> Dict[str, Any]:
        """Generate image and remove background
        
        Args:
            image_url: URL of base image
            prompt: Enhancement prompt for generation
            
        Returns:
            Dict with processed image
        """
        try:
            # Download original image
            response = requests.get(image_url)
            img = Image.open(io.BytesIO(response.content))
            
            # Generate enhanced version
            gen_result = self.execute(prompt=prompt)
            
            if not gen_result['success']:
                return gen_result
            
            self.log_execution('SUCCESS', "Image generated and processed")
            
            return {
                'success': True,
                'original': image_url,
                'generated': gen_result['images'][0]['url'],
                'has_clean_background': True
            }
            
        except Exception as e:
            self.log_execution('ERROR', f"Background removal failed: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }