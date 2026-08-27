import os
from dotenv import load_dotenv
import yaml

load_dotenv()

class Config:
    """Base configuration"""
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key')
    
    # OpenAI
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # Meesho
    MEESHO_API_KEY = os.getenv('MEESHO_API_KEY')
    MEESHO_SELLER_ID = os.getenv('MEESHO_SELLER_ID')
    
    # Redis/Celery
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')
    
    # File Upload
    UPLOAD_FOLDER = 'uploads'
    PROCESSED_FOLDER = 'processed_images'
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 52428800))
    
    # Image Processing
    IMAGE_QUALITY = int(os.getenv('IMAGE_QUALITY', 95))
    IMAGE_BACKGROUND_COLOR = os.getenv('IMAGE_BACKGROUND_COLOR', 'white')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True

def get_config():
    """Get appropriate config based on environment"""
    env = os.getenv('FLASK_ENV', 'development')
    if env == 'production':
        return ProductionConfig()
    elif env == 'testing':
        return TestingConfig()
    return DevelopmentConfig()

config = get_config()