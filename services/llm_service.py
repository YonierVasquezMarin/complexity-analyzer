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
    
    def generate_json_completion(self, prompt: str, max_tokens: int = 4000) -> dict:
        """
        Genera una completación en formato JSON usando Claude
        
        Args:
            prompt: El prompt completo a enviar al modelo
            max_tokens: Número máximo de tokens en la respuesta
            
        Returns:
            El JSON generado por el modelo como diccionario
            
        Raises:
            Exception: Si hay un error al comunicarse con la API o al parsear JSON
        """
        import json
        import re
        
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
                response_text = message.content[0].text.strip()
                
                # Intentar extraer JSON del texto (puede venir envuelto en markdown)
                # Primero intentar encontrar bloques de código JSON
                json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', response_text, re.DOTALL)
                if json_match:
                    json_str = json_match.group(1)
                else:
                    # Si no hay bloques de código, buscar directamente el JSON
                    # Buscar desde el primer { hasta el último } balanceado
                    brace_count = 0
                    start_idx = response_text.find('{')
                    if start_idx != -1:
                        for i in range(start_idx, len(response_text)):
                            if response_text[i] == '{':
                                brace_count += 1
                            elif response_text[i] == '}':
                                brace_count -= 1
                                if brace_count == 0:
                                    json_str = response_text[start_idx:i+1]
                                    break
                        else:
                            # Si no se encontró el cierre balanceado, usar todo el texto
                            json_str = response_text
                    else:
                        json_str = response_text
                
                # Limpiar el JSON (remover espacios al inicio/final)
                json_str = json_str.strip()
                
                # Parsear el JSON
                return json.loads(json_str)
            else:
                raise Exception("La respuesta del modelo está vacía")
                
        except json.JSONDecodeError as e:
            raise Exception(f"Error al parsear JSON de la respuesta: {str(e)}")
        except Exception as e:
            raise Exception(f"Error al comunicarse con la API de Claude: {str(e)}")

