"""
Servicio para interactuar con APIs de modelos de lenguaje (LLM)
Actualmente soporta Claude de Anthropic
"""

import os
from anthropic import Anthropic


class LLMService:
    """Servicio para consumir APIs de modelos de lenguaje"""
    
    def __init__(self):
        """Inicializa el servicio con las credenciales del entorno"""
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY no está configurada. "
                "Por favor, configura tu API key en el archivo .env"
            )
        
        self.client = Anthropic(api_key=api_key)
        self.model = os.getenv("CLAUDE_MODEL", "claude-3-5-sonnet-20240620")
    
    def generate_completion(self, prompt: str, max_tokens: int = 2000) -> str:
        """
        Genera una completación usando Claude
        
        Args:
            prompt: El prompt completo a enviar al modelo
            max_tokens: Número máximo de tokens en la respuesta
            
        Returns:
            El texto generado por el modelo
            
        Raises:
            Exception: Si hay un error al comunicarse con la API
        """
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            # Extraer el texto de la respuesta
            if message.content and len(message.content) > 0:
                return message.content[0].text
            else:
                raise Exception("La respuesta del modelo está vacía")
                
        except Exception as e:
            raise Exception(f"Error al comunicarse con la API de Claude: {str(e)}")

