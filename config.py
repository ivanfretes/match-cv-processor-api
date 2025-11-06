"""
Configuración de la aplicación.
Maneja la lectura de propiedades desde archivos de configuración.
"""
import os
from pathlib import Path
from typing import Optional


class Config:
    """Clase para manejar la configuración de la aplicación."""
    
    def __init__(self, properties_file: str = "application.properties"):
        """
        Inicializa la configuración.
        
        Args:
            properties_file: Ruta al archivo de propiedades
        """
        self.properties_file = Path(properties_file)
        self._properties: dict[str, str] = {}
        self._load_properties()
    
    def _load_properties(self) -> None:
        """Carga las propiedades desde el archivo."""
        if self.properties_file.exists():
            with open(self.properties_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        self._properties[key.strip()] = value.strip()
    
    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """
        Obtiene un valor de configuración.
        
        Args:
            key: Clave de configuración
            default: Valor por defecto si no se encuentra
            
        Returns:
            Valor de configuración o None
        """
        # Primero intenta obtener desde variables de entorno (mayor prioridad)
        env_value = os.getenv(key)
        if env_value:
            return env_value
        
        # Luego desde el archivo de propiedades
        return self._properties.get(key, default)
    
    def get_required(self, key: str) -> str:
        """
        Obtiene un valor de configuración requerido.
        
        Args:
            key: Clave de configuración
            
        Returns:
            Valor de configuración
            
        Raises:
            ValueError: Si la clave no existe
        """
        value = self.get(key)
        if value is None:
            raise ValueError(f"Configuración requerida '{key}' no encontrada")
        return value


# Instancia global de configuración
config = Config()

