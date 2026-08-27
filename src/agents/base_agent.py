from abc import ABC, abstractmethod
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    """Base class for all automation agents"""
    
    def __init__(self, name: str, config: Dict[str, Any] = None):
        self.name = name
        self.config = config or {}
        self.logger = logging.getLogger(f"Agent.{name}")
    
    @abstractmethod
    def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute agent task
        
        Args:
            **kwargs: Task-specific parameters
            
        Returns:
            Dict with execution results
        """
        pass
    
    @abstractmethod
    def validate_input(self, **kwargs) -> bool:
        """Validate input parameters
        
        Args:
            **kwargs: Parameters to validate
            
        Returns:
            True if valid, False otherwise
        """
        pass
    
    def log_execution(self, status: str, message: str):
        """Log agent execution
        
        Args:
            status: Execution status (INFO, WARNING, ERROR, SUCCESS)
            message: Log message
        """
        if status == 'ERROR':
            self.logger.error(f"[{self.name}] {message}")
        elif status == 'WARNING':
            self.logger.warning(f"[{self.name}] {message}")
        elif status == 'SUCCESS':
            self.logger.info(f"[{self.name}] SUCCESS: {message}")
        else:
            self.logger.info(f"[{self.name}] {message}")