"""CV controller - Handles CV processing endpoints"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from application.use_cases.process_cv_use_case import ProcessCVUseCase
from infrastructure.models.response_models import CVResponse
from infrastructure.dependencies import get_process_cv_use_case
from domain.exceptions.domain_exceptions import CVProcessingError, InvalidFileError

router = APIRouter(prefix="/upload", tags=["CV"])


@router.post("/pdf", response_model=CVResponse)
async def upload_pdf(
    file: UploadFile = File(...),
    language: str = "spanish",
    generate_summary: bool = True,
    process_cv_use_case: ProcessCVUseCase = Depends(get_process_cv_use_case)
):
    """
    Endpoint para subir un PDF y extraer el texto del documento.
    Opcionalmente genera un resumen del CV utilizando OpenAI.
    
    Args:
        file: Archivo PDF a procesar
        language: Idioma para el resumen (spanish/english)
        generate_summary: Si True, genera un resumen usando OpenAI
        process_cv_use_case: Caso de uso para procesar CVs inyectado como dependencia
        
    Returns:
        CVResponse con información del PDF y opcionalmente el resumen generado
    """
    # Validate file type
    if not file.filename or not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="El archivo debe ser un PDF")
    
    try:
        # Read file content
        contents = await file.read()
        
        # Execute use case
        cv = await process_cv_use_case.execute(
            file_content=contents,
            filename=file.filename,
            language=language,
            generate_summary=generate_summary
        )
        
        # Build response
        response = CVResponse(
            filename=cv.filename,
            total_pages=cv.total_pages,
            character_count=cv.character_count,
            text=cv.text,
            message=f"PDF procesado correctamente. Total de caracteres: {cv.character_count}",
            summary=cv.summary,
            summary_generated=cv.summary_generated,
            summary_error=cv.summary_error
        )
        
        return response
        
    except InvalidFileError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except CVProcessingError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar el PDF: {str(e)}")

