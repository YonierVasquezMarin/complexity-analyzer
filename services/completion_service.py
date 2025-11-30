"""
Servicio para completar pseudocódigo usando IA
Detecta comentarios con "completar" o "Completar" y genera código faltante
"""

import os
import re
from typing import Tuple
from services.llm_service import LLMService


class CompletionService:
    """Servicio para completar pseudocódigo con IA"""
    
    def __init__(self):
        """Inicializa el servicio de completado"""
        self.llm_service = LLMService()
        self.prompt_template_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "prompts",
            "complete_pseudocode.txt"
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
    
    def _load_grammar(self) -> str:
        """Carga la gramática desde el archivo grammar.lark"""
        grammar_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "syntax",
            "grammar.lark"
        )
        try:
            with open(grammar_path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(
                f"No se encontró el archivo de gramática en: {grammar_path}"
            )
    
    def _has_completion_comments(self, code: str) -> bool:
        """
        Verifica si el código tiene comentarios que inician con "completar" o "Completar"
        
        Args:
            code: El código a verificar
            
        Returns:
            True si hay comentarios de completado, False en caso contrario
        """
        # Buscar comentarios que inician con ► seguido de espacios opcionales y "completar" (case-insensitive)
        # El patrón busca: ► seguido de espacios opcionales, luego "completar" en cualquier caso
        pattern = r'►\s*[Cc]ompletar'
        return bool(re.search(pattern, code, re.IGNORECASE))
    
    def _build_prompt(self, code: str, grammar: str, template: str) -> str:
        """
        Construye el prompt final combinando el template con el código y la gramática
        
        Args:
            code: El pseudocódigo a completar
            grammar: La gramática del pseudocódigo
            template: El template del prompt
            
        Returns:
            El prompt completo listo para enviar al LLM
        """
        return template.format(grammar=grammar, code=code)
    
    def _clean_markdown_blocks(self, code: str) -> str:
        """
        Limpia bloques de código markdown que el LLM pueda haber generado.
        Remueve triple comillas invertidas (```) al inicio y final del código.
        
        Args:
            code: El código a limpiar
            
        Returns:
            El código sin bloques de markdown
        """
        # Remover bloques de código markdown (``` al inicio y final)
        # Patrón: ``` opcionalmente seguido de un identificador de lenguaje, luego el código, luego ```
        code = code.strip()
        
        # Remover triple comillas invertidas al inicio
        if code.startswith('```'):
            # Encontrar el primer salto de línea después de ```
            lines = code.split('\n')
            if len(lines) > 0 and lines[0].startswith('```'):
                # Remover la primera línea (``` o ```language)
                lines = lines[1:]
                code = '\n'.join(lines)
        
        # Remover triple comillas invertidas al final
        if code.endswith('```'):
            # Encontrar el último salto de línea antes de ```
            lines = code.split('\n')
            if len(lines) > 0 and lines[-1].strip() == '```':
                # Remover la última línea (```)
                lines = lines[:-1]
                code = '\n'.join(lines)
        
        # También remover si está al inicio/final sin saltos de línea
        code = code.strip()
        if code.startswith('```'):
            code = code.lstrip('`')
        if code.endswith('```'):
            code = code.rstrip('`')
        
        return code.strip()
    
    def complete_code(self, code: str) -> Tuple[str, bool]:
        """
        Completa el pseudocódigo si tiene comentarios de completado
        
        Args:
            code: El pseudocódigo a completar
            
        Returns:
            Tupla con (código_completado, extendido_por_llm)
            - código_completado: El código original o completado
            - extendido_por_llm: True si se usó IA para completar, False en caso contrario
        """
        # Verificar si hay comentarios de completado
        if not self._has_completion_comments(code):
            return code, False
        
        try:
            # Cargar template y gramática
            template = self._load_prompt_template()
            grammar = self._load_grammar()
            
            # Construir el prompt
            prompt = self._build_prompt(code, grammar, template)
            
            # Generar completación con LLM
            completed_code = self.llm_service.generate_completion(prompt)
            
            # Limpiar bloques de markdown que el LLM pueda haber generado
            completed_code = self._clean_markdown_blocks(completed_code)
            
            # Limpiar el código generado
            # Eliminar espacios en blanco al inicio, pero preservar saltos de línea al final si el original los tenía
            completed_code = completed_code.lstrip()
            
            # Preservar el salto de línea final si el código original terminaba con uno
            original_ends_with_newline = code.endswith('\n')
            if original_ends_with_newline and not completed_code.endswith('\n'):
                completed_code += '\n'
            elif not original_ends_with_newline and completed_code.endswith('\n'):
                # Si el original no terminaba con salto de línea, eliminar el del generado
                completed_code = completed_code.rstrip('\n')
            
            return completed_code, True
            
        except Exception as e:
            # Si hay un error, retornar el código original
            # En producción, podrías querer loguear el error
            raise Exception(f"Error al completar el código: {str(e)}")

