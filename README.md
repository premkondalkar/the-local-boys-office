# 🏢 The Local Boys Office - Automation Agents

A powerful office automation system with AI-powered agents for Meesho and ecommerce shop product management, image generation, and metadata optimization.

## 🎯 Features

### Agent 1: Image Generation Agent
- Generate professional product images using DALL-E 3
- Convert uploaded images to clean white background
- Create attractive product photos for ecommerce
- Support for different image sizes and quality levels
- Batch image generation

### Agent 2: Image Analysis Agent  
- Analyze product images with AI vision models
- Extract SEO keywords automatically
- Generate product descriptions
- Identify product categories and features
- Importance/Relevance scoring

### Agent 3: Agent Orchestrator
- Manage multiple automation agents
- Execute predefined workflows
- Combine agents for complex tasks
- Easy scaling for new agents and workflows

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- OpenAI API Key (for image generation and analysis)
- Meesho API Key (for integration)
- Redis (optional, for task queuing)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/premkondalkar/the-local-boys-office.git
   cd the-local-boys-office
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

5. **Run the application**
   ```bash
   python main.py
   ```

The server will start at `http://localhost:5000`

## 📡 API Endpoints

### List Available Agents
```bash
GET /api/v1/agents
```

### Generate Product Image
```bash
POST /api/v1/agents/image-generation

Body:
{
  "prompt": "professional product photo of modern smartphone",
  "size": "1024x1024",
  "quality": "hd"
}
```

### Analyze Product Image
```bash
POST /api/v1/agents/image-analysis

# With file upload:
Form-data:
- file: <image-file>
- max_keywords: 10

# Or with URL:
Body:
{
  "image_url": "https://...",
  "max_keywords": 10
}
```

### Run Product Enhancement Workflow
```bash
POST /api/v1/workflows/product-enhancement

Form-data:
- file: <product-image>
```

### Generate Product Metadata
```bash
POST /api/v1/workflows/metadata-generation

Form-data:
- file: <product-image>
```

### Health Check
```bash
GET /api/v1/health
```

## 📁 Project Structure

```
the-local-boys-office/
├── src/
│   ├── agents/
│   │   ├── base_agent.py           # Base agent class
│   │   ├── image_generation_agent.py
│   │   ├── image_analysis_agent.py
│   │   └── agent_orchestrator.py   # Agent manager
│   ├── api/
│   │   └── routes.py               # API endpoints
│   ├── config.py                   # Configuration
│   └── app.py                      # Flask app factory
├── uploads/                         # User uploaded files
├── processed_images/                # Generated/processed images
├── logs/                            # Application logs
├── main.py                          # Entry point
├── requirements.txt                 # Dependencies
├── config.yaml                      # Agent configuration
└── .env.example                     # Environment template
```

## 🔧 Configuration

Edit `config.yaml` to customize:
- Agent models and API keys
- Image processing parameters
- Platform integrations (Meesho, Flipkart, Amazon)
- Storage and queue settings

## 🤖 Creating Custom Agents

```python
from src.agents.base_agent import BaseAgent

class MyCustomAgent(BaseAgent):
    def __init__(self, config=None):
        super().__init__("MyCustomAgent", config)
    
    def validate_input(self, **kwargs) -> bool:
        return 'data' in kwargs
    
    def execute(self, **kwargs):
        # Your agent logic here
        return {'success': True, 'result': 'Done'}

# Register with orchestrator
from src.agents import AgentOrchestrator
orchestrator = AgentOrchestrator()
orchestrator.register_agent('my_agent', MyCustomAgent())
```

## 🔄 Workflows

### Product Enhancement
1. Analyze uploaded product image
2. Extract product details
3. Generate enhanced professional image
4. Return analysis + generated image

### Image Optimization
1. Analyze image for platform requirements
2. Extract platform-specific metadata
3. Recommend optimizations

### Metadata Generation
1. Analyze product image
2. Extract keywords, description, category
3. Generate SEO-friendly metadata
4. Return structured metadata

## 📊 Example Usage

### Python Client
```python
from src.agents import AgentOrchestrator

orchestrator = AgentOrchestrator()

# Generate image
result = orchestrator.execute_agent(
    'image_generation',
    prompt='professional product photo of wireless earbuds'
)

# Analyze image
analysis = orchestrator.execute_agent(
    'image_analysis',
    image_path='./product.jpg',
    max_keywords=10
)

# Run workflow
workflow_result = orchestrator.execute_workflow(
    'product_enhancement',
    image_path='./product.jpg'
)
```

### cURL Examples
```bash
# List agents
curl http://localhost:5000/api/v1/agents

# Generate image
curl -X POST http://localhost:5000/api/v1/agents/image-generation \
  -H "Content-Type: application/json" \
  -d '{"prompt": "professional product photo"}'

# Analyze image
curl -X POST http://localhost:5000/api/v1/agents/image-analysis \
  -F "file=@product.jpg"
```

## 🛠️ Troubleshooting

### OpenAI API Errors
- Check `OPENAI_API_KEY` in `.env`
- Verify API key has required permissions
- Check API rate limits

### File Upload Issues
- Ensure `uploads/` directory exists and is writable
- Check `MAX_CONTENT_LENGTH` setting
- Verify file format is supported (PNG, JPG, GIF, WebP)

### Agent Registration Errors
- Check agent initialization parameters
- Verify agent inherits from `BaseAgent`
- Check logs for detailed error messages

## 📝 Logging

Logs are stored in `logs/app.log` and console output.
Configure logging level in `config.yaml`

## 🔐 Security

- Store API keys in `.env` file (not in code)
- Use environment-specific configurations
- Validate all file uploads
- Implement rate limiting (recommended)
- Use HTTPS in production

## 🚢 Deployment

### Docker
```bash
docker build -t local-boys-office .
docker run -p 5000:5000 --env-file .env local-boys-office
```

### Gunicorn (Production)
```bash
gunicorn -w 4 -b 0.0.0.0:5000 main:app
```

## 📄 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check existing issues first
- Provide detailed error messages and logs

## 🎉 Acknowledgments

Built by The Local Boys for automated office and ecommerce management.

---

**Happy Automating! 🚀**