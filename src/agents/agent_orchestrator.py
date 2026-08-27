import logging
from typing import Dict, Any, List, Optional
from .image_generation_agent import ImageGenerationAgent
from .image_analysis_agent import ImageAnalysisAgent

logger = logging.getLogger(__name__)

class AgentOrchestrator:
    """Orchestrator for managing multiple automation agents"""
    
    def __init__(self):
        self.agents: Dict[str, Any] = {}
        self.logger = logging.getLogger("AgentOrchestrator")
        self._initialize_default_agents()
    
    def _initialize_default_agents(self):
        """Initialize default agents"""
        self.register_agent('image_generation', ImageGenerationAgent())
        self.register_agent('image_analysis', ImageAnalysisAgent())
        self.logger.info("Default agents initialized")
    
    def register_agent(self, name: str, agent: Any) -> bool:
        """Register a new agent
        
        Args:
            name: Agent name/identifier
            agent: Agent instance
            
        Returns:
            True if registered successfully
        """
        try:
            self.agents[name] = agent
            self.logger.info(f"Agent '{name}' registered")
            return True
        except Exception as e:
            self.logger.error(f"Failed to register agent '{name}': {str(e)}")
            return False
    
    def unregister_agent(self, name: str) -> bool:
        """Unregister an agent
        
        Args:
            name: Agent name/identifier
            
        Returns:
            True if unregistered successfully
        """
        if name in self.agents:
            del self.agents[name]
            self.logger.info(f"Agent '{name}' unregistered")
            return True
        return False
    
    def get_agent(self, name: str) -> Optional[Any]:
        """Get agent by name
        
        Args:
            name: Agent name/identifier
            
        Returns:
            Agent instance or None
        """
        return self.agents.get(name)
    
    def list_agents(self) -> List[str]:
        """List all registered agents
        
        Returns:
            List of agent names
        """
        return list(self.agents.keys())
    
    def execute_agent(self, agent_name: str, **kwargs) -> Dict[str, Any]:
        """Execute a specific agent
        
        Args:
            agent_name: Name of agent to execute
            **kwargs: Agent-specific parameters
            
        Returns:
            Execution result
        """
        agent = self.get_agent(agent_name)
        if not agent:
            return {
                'success': False,
                'error': f"Agent '{agent_name}' not found"
            }
        
        try:
            self.logger.info(f"Executing agent: {agent_name}")
            result = agent.execute(**kwargs)
            return result
        except Exception as e:
            self.logger.error(f"Agent execution failed: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def execute_workflow(self, workflow_name: str, **kwargs) -> Dict[str, Any]:
        """Execute a predefined workflow combining multiple agents
        
        Args:
            workflow_name: Name of workflow to execute
            **kwargs: Workflow parameters
            
        Returns:
            Workflow execution result
        """
        workflows = {
            'product_enhancement': self._workflow_product_enhancement,
            'image_optimization': self._workflow_image_optimization,
            'metadata_generation': self._workflow_metadata_generation
        }
        
        if workflow_name not in workflows:
            return {
                'success': False,
                'error': f"Workflow '{workflow_name}' not found"
            }
        
        return workflows[workflow_name](**kwargs)
    
    def _workflow_product_enhancement(self, **kwargs) -> Dict[str, Any]:
        """Workflow: Analyze image -> Generate enhanced version"""
        try:
            image_path = kwargs.get('image_path')
            
            # Step 1: Analyze original image
            analysis_result = self.execute_agent('image_analysis', image_path=image_path)
            if not analysis_result['success']:
                return analysis_result
            
            # Step 2: Generate enhanced image
            prompt = f"Professional product photography: {analysis_result.get('analysis', '')[:200]}"
            gen_result = self.execute_agent('image_generation', prompt=prompt)
            
            return {
                'success': True,
                'workflow': 'product_enhancement',
                'analysis': analysis_result,
                'generated_image': gen_result
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _workflow_image_optimization(self, **kwargs) -> Dict[str, Any]:
        """Workflow: Optimize image for ecommerce platforms"""
        try:
            image_url = kwargs.get('image_url')
            platform = kwargs.get('platform', 'meesho')
            
            # Analyze image
            analysis = self.execute_agent('image_analysis', image_url=image_url)
            
            return {
                'success': True,
                'workflow': 'image_optimization',
                'platform': platform,
                'analysis': analysis
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _workflow_metadata_generation(self, **kwargs) -> Dict[str, Any]:
        """Workflow: Generate complete metadata for product listing"""
        try:
            image_path = kwargs.get('image_path')
            
            analysis = self.execute_agent('image_analysis', image_path=image_path)
            
            return {
                'success': True,
                'workflow': 'metadata_generation',
                'metadata': analysis
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}