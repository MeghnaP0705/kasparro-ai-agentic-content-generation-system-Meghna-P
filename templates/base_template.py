from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseTemplate(ABC):
    """Base template class for all page templates."""

    def __init__(self):
        self.fields: List[str] = []
        self.rules: Dict[str, Any] = {}
        self.define_structure()

    @abstractmethod
    def define_structure(self):
        """Define template structure, fields, and rules."""
        pass

    @abstractmethod
    def render(self, data: dict) -> dict:
        """Render template with provided data."""
        pass

    def validate(self, data: dict) -> bool:
        """Validate data against template rules."""
        for field in self.fields:
            if field not in data:
                return False
        return True
