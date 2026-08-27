from flask import Blueprint, request, jsonify
from src.agents import AgentOrchestrator
import logging
import os
from werkzeug.utils import secure_filename

logger = logging.getLogger(__name__)

# Initialize orchestrator
orchestrator = AgentOrchestrator()

# Create blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@api_bp.route('/agents', methods=['GET'])
def list_agents():
    """List all registered agents"""
    try:
        agents = orchestrator.list_agents()
        return jsonify({
            'success': True,
            'agents': agents,
            'count': len(agents)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@api_bp.route('/agents/image-generation', methods=['POST'])
def generate_image():
    """Generate product image using AI
    
    Request JSON:
    {
        "prompt": "professional product photo of...",
        "size": "1024x1024",
        "quality": "standard"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'prompt' not in data:
            return jsonify({'success': False, 'error': 'Missing prompt'}), 400
        
        result = orchestrator.execute_agent('image_generation', **data)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Image generation error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@api_bp.route('/agents/image-analysis', methods=['POST'])
def analyze_image():
    """Analyze product image and extract metadata
    
    Request Form:
    - file: Image file upload OR
    
    Request JSON:
    {
        "image_url": "https://...",
        "max_keywords": 10
    }
    """
    try:
        # Handle file upload
        if 'file' in request.files:
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                upload_folder = os.getenv('UPLOAD_FOLDER', 'uploads')
                os.makedirs(upload_folder, exist_ok=True)
                filepath = os.path.join(upload_folder, filename)
                file.save(filepath)
                
                result = orchestrator.execute_agent('image_analysis', image_path=filepath)
                return jsonify(result)
        
        # Handle URL
        data = request.get_json()
        if data and 'image_url' in data:
            result = orchestrator.execute_agent('image_analysis', **data)
            return jsonify(result)
        
        return jsonify({'success': False, 'error': 'Missing file or image_url'}), 400
    except Exception as e:
        logger.error(f"Image analysis error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@api_bp.route('/workflows/product-enhancement', methods=['POST'])
def workflow_product_enhancement():
    """Run product enhancement workflow
    
    Request Form:
    - file: Product image to enhance
    """
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'Missing file'}), 400
        
        file = request.files['file']
        if not file or not allowed_file(file.filename):
            return jsonify({'success': False, 'error': 'Invalid file type'}), 400
        
        filename = secure_filename(file.filename)
        upload_folder = os.getenv('UPLOAD_FOLDER', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)
        
        result = orchestrator.execute_workflow('product_enhancement', image_path=filepath)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Workflow error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@api_bp.route('/workflows/metadata-generation', methods=['POST'])
def workflow_metadata():
    """Run metadata generation workflow
    
    Request Form:
    - file: Product image
    """
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'Missing file'}), 400
        
        file = request.files['file']
        if not file or not allowed_file(file.filename):
            return jsonify({'success': False, 'error': 'Invalid file type'}), 400
        
        filename = secure_filename(file.filename)
        upload_folder = os.getenv('UPLOAD_FOLDER', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)
        
        result = orchestrator.execute_workflow('metadata_generation', image_path=filepath)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Workflow error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'agents_count': len(orchestrator.list_agents())
    })