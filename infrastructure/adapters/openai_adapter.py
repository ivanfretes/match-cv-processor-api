"""OpenAI adapter - Implements LLMServicePort using OpenAI"""
from openai import OpenAI
from domain.ports.llm_service_port import LLMServicePort


class OpenAIAdapter(LLMServicePort):
    """Adapter for OpenAI API that implements LLMServicePort"""
    
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        """
        Initialize the OpenAI adapter
        
        Args:
            api_key: OpenAI API key
            model: Model to use (default: gpt-3.5-turbo)
        """
        self.client = OpenAI(api_key=api_key)
        self.model = model
    
    async def generate_cv_summary(
        self,
        cv_text: str,
        language: str = "spanish"
    ) -> str:
        """
        Generate a CV summary using OpenAI
        
        Args:
            cv_text: Full text of the CV extracted from PDF
            language: Language for the summary (spanish/english)
            
        Returns:
            Generated CV summary text
            
        Raises:
            Exception: If summary generation fails
        """
        if not cv_text or not cv_text.strip():
            raise ValueError("El texto del CV no puede estar vacío")
        
        # Build prompt based on language
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
                max_tokens=500,
                temperature=0.3  # Low temperature for more consistent responses
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            # Detect if it's an OpenAI-related exception
            error_module = str(type(e).__module__).lower()
            error_type = type(e).__name__
            
            is_openai_error = (
                "openai" in error_module or 
                "APIError" in error_type or 
                "APIConnectionError" in error_type or
                "RateLimitError" in error_type or
                "APITimeoutError" in error_type
            )
            
            error_message = str(e) if e else "Error desconocido"
            
            if is_openai_error:
                raise Exception(f"Error al generar resumen con OpenAI: {error_message}") from e
            else:
                raise Exception(f"Error inesperado al generar resumen: {error_message}") from e

