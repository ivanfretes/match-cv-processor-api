"""
Servicio para interactuar con la API de OpenAI.
Implementa la generación de resúmenes de CVs utilizando LLM.
"""
from typing import Optional
from openai import OpenAI

# No necesitamos importar las excepciones específicas
# Las capturaremos de forma genérica y verificaremos si son de OpenAI


class OpenAIServiceError(Exception):
    """Excepción personalizada para errores del servicio de OpenAI."""
    pass


class OpenAIService:
    """Servicio para interactuar con OpenAI API."""
    
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        """
        Inicializa el servicio de OpenAI.
        
        Args:
            api_key: Clave API de OpenAI
            model: Modelo a utilizar (por defecto gpt-3.5-turbo)
        """
        self.client = OpenAI(api_key=api_key)
        self.model = model
    
    def generate_cv_summary(
        self,
        cv_text: str,
        language: str = "spanish",
        max_tokens: int = 500
    ) -> str:
        """
        Genera un resumen del CV utilizando OpenAI.
        
        Args:
            cv_text: Texto completo del CV extraído del PDF
            language: Idioma para el resumen (por defecto español)
            max_tokens: Número máximo de tokens para la respuesta
            
        Returns:
            Resumen del CV generado por el LLM
            
        Raises:
            OpenAIServiceError: Si hay un error al comunicarse con la API de OpenAI
            ValueError: Si el texto del CV está vacío
        """
        if not cv_text or not cv_text.strip():
            raise ValueError("El texto del CV no puede estar vacío")
        
        # Construir el prompt según el idioma
        if language.lower() == "spanish" or language.lower() == "es":
            system_prompt = (
                "Eres un experto en recursos humanos y análisis de CVs. "
                "Tu tarea es generar un resumen profesional y conciso de un CV."
            )
            user_prompt = (
                f"Por favor, genera un resumen profesional del siguiente CV. "
                f"Incluye información clave como: experiencia profesional, habilidades técnicas, "
                f"educación y logros destacados. El resumen debe ser claro y estructurado.\n\n"
                f"CV:\n{cv_text}"
            )
        else:
            system_prompt = (
                "You are an expert in human resources and CV analysis. "
                "Your task is to generate a professional and concise summary of a CV."
            )
            user_prompt = (
                f"Please generate a professional summary of the following CV. "
                f"Include key information such as: professional experience, technical skills, "
                f"education and outstanding achievements. The summary should be clear and structured.\n\n"
                f"CV:\n{cv_text}"
            )
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.3  # Baja temperatura para respuestas más consistentes
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            # Capturar cualquier excepción que pueda ocurrir
            # Verificar si es una excepción relacionada con OpenAI
            error_module = str(type(e).__module__).lower()
            error_type = type(e).__name__
            
            # Detectar si es una excepción de OpenAI basándonos en el módulo o tipo
            is_openai_error = (
                "openai" in error_module or 
                "APIError" in error_type or 
                "APIConnectionError" in error_type or
                "RateLimitError" in error_type or
                "APITimeoutError" in error_type
            )
            
            # Extraer el mensaje de error
            error_message = str(e) if e else "Error desconocido"
            
            if is_openai_error:
                # Es un error de la API de OpenAI
                raise OpenAIServiceError(f"Error al generar resumen con OpenAI: {error_message}") from e
            else:
                # Es un error inesperado (conexión, timeout, etc.)
                raise OpenAIServiceError(f"Error inesperado al generar resumen: {error_message}") from e

