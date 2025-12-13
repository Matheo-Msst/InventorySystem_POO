from abc import ABC, abstractmethod
from typing import Dict, Any

class Factory(ABC):
    """Classe abstraite pour le pattern Factory"""
    
    @abstractmethod
    def create(self) -> Any:
        pass

class Registry:
    """Registry pour stocker toutes les factories et leurs métadonnées"""
    
    def __init__(self):
        self._registry: Dict[str, Dict[str, Any]] = {}

    def register(self, key: str, factory: Factory, metadata: dict = None):
        self._registry[key] = {
            'factory': factory,
            'metadata': metadata or {}
        }

    def create(self, key: str) -> Any:
        return self._registry[key]['factory'].create()

    def get(self, key: str) -> dict:
        return self._registry[key]

    def all(self) -> Dict[str, dict]:
        return self._registry

    def filter(self, **criteria) -> Dict[str, dict]:
        """Filtre les items par métadonnées"""
        result = {}
        for key, data in self._registry.items():
            if all(data['metadata'].get(k) == v for k, v in criteria.items()):
                result[key] = data
        return result

    def keys(self):
        return self._registry.keys()
