"""
Servicio para analizar pseudocódigo usando LLM
Genera un análisis completo de complejidad computacional
"""

import os
import time
import json
from typing import Dict, Any
from services.llm_service import LLMService


class LLMAnalysisService:
    """Servicio para analizar pseudocódigo con LLM"""
    
    def __init__(self):
        """Inicializa el servicio de análisis por LLM"""
        self.llm_service = LLMService()
        self.prompt_template_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "prompts",
            "analyze_by_llm.txt"
        )
    
    def _load_prompt_template(self) -> str:
        """Carga el template del prompt desde el archivo"""
        try:
            with open(self.prompt_template_path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(
                f"No se encontró el archivo de prompt en: {self.prompt_template_path}"
            )
    
    def _build_prompt(self, pseudocode: str, template: str) -> str:
        """
        Construye el prompt final combinando el template con el pseudocódigo
        
        Args:
            pseudocode: El pseudocódigo a analizar
            template: El template del prompt
            
        Returns:
            El prompt completo listo para enviar al LLM
        """
        return template.format(pseudocode=pseudocode)
    
    def _extract_metadata_from_response(self, response_dict: Dict[str, Any], 
                                       processing_time_ms: float) -> Dict[str, Any]:
        """
        Extrae o actualiza los metadatos del LLM en la respuesta
        
        Args:
            response_dict: El diccionario de respuesta del LLM
            processing_time_ms: Tiempo de procesamiento en milisegundos
            
        Returns:
            Diccionario con los metadatos actualizados
        """
        # Obtener el modelo usado del servicio
        model_used = self.llm_service.model
        
        # Si ya hay metadatos en la respuesta, actualizarlos
        if "llm_metadata" in response_dict:
            metadata = response_dict["llm_metadata"]
            # Asegurar que tokens sea un diccionario con las claves correctas
            if isinstance(metadata.get("tokens"), dict):
                tokens = metadata["tokens"]
            else:
                tokens = {"input": 0, "output": 0, "total": 0}
            
            metadata = {
                "model_used": metadata.get("model_used", model_used),
                "tokens": {
                    "input": tokens.get("input", 0),
                    "output": tokens.get("output", 0),
                    "total": tokens.get("total", 0)
                },
                "estimated_cost_usd": metadata.get("estimated_cost_usd"),
                "processing_time_ms": processing_time_ms
            }
        else:
            # Crear metadatos si no existen
            metadata = {
                "model_used": model_used,
                "tokens": {
                    "input": 0,
                    "output": 0,
                    "total": 0
                },
                "estimated_cost_usd": None,
                "processing_time_ms": processing_time_ms
            }
        
        return metadata
    
    def analyze_pseudocode(self, pseudocode: str) -> Dict[str, Any]:
        """
        Analiza el pseudocódigo usando LLM y genera un análisis completo
        
        Args:
            pseudocode: El pseudocódigo a analizar
            
        Returns:
            Diccionario con el análisis completo de complejidad
            
        Raises:
            Exception: Si hay un error al analizar el pseudocódigo
        """
        try:
            # Medir tiempo de inicio
            start_time = time.time()
            
            # Cargar template
            template = self._load_prompt_template()
            
            # Construir el prompt
            prompt = self._build_prompt(pseudocode, template)
            
            # Generar análisis con LLM (usando JSON estructurado)
            # Usar max_tokens más alto para respuestas completas
            analysis_dict = self.llm_service.generate_json_completion(
                prompt, 
                max_tokens=8000
            )
            
            # Calcular tiempo de procesamiento
            processing_time_ms = (time.time() - start_time) * 1000
            
            # Asegurar que el pseudocódigo esté en la respuesta
            if "pseudocode" not in analysis_dict:
                analysis_dict["pseudocode"] = pseudocode
            
            # Actualizar metadatos
            analysis_dict["llm_metadata"] = self._extract_metadata_from_response(
                analysis_dict, 
                processing_time_ms
            )
            
            # Asegurar que los campos opcionales estén presentes o sean None
            if "execution_diagram" not in analysis_dict:
                analysis_dict["execution_diagram"] = None
            if "cost_analysis" not in analysis_dict:
                analysis_dict["cost_analysis"] = None
            
            return analysis_dict
            
        except Exception as e:
            raise Exception(f"Error al analizar el pseudocódigo con LLM: {str(e)}")

