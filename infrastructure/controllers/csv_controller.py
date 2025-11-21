"""CSV controller - Handles CSV processing endpoints"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from application.use_cases.process_csv_use_case import ProcessCSVUseCase
from infrastructure.models.response_models import CSVResponse
from infrastructure.dependencies import get_process_csv_use_case
from domain.exceptions.domain_exceptions import CSVProcessingError, InvalidFileError

router = APIRouter(prefix="/upload", tags=["CSV"])


@router.post("/csv", response_model=CSVResponse)
async def upload_csv(
    file: UploadFile = File(...),
    process_csv_use_case: ProcessCSVUseCase = Depends(get_process_csv_use_case)
):
    """
    Endpoint para subir un CSV y leer su contenido.
    Retorna los datos del CSV en formato JSON.
    
    Args:
        file: Archivo CSV a procesar
        process_csv_use_case: Caso de uso para procesar CSV inyectado como dependencia
        
    Returns:
        CSVResponse con los datos del CSV
    """
    # Validate file type
    if not file.filename or not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="El archivo debe ser un CSV")
    
    try:
        # Read file content
        contents = await file.read()
        
        # Execute use case
        csv_document = await process_csv_use_case.execute(
            file_content=contents,
            filename=file.filename
        )
        
        # Build response
        response = CSVResponse(
            filename=csv_document.filename,
            total_rows=csv_document.total_rows,
            columns=csv_document.columns,
            data=csv_document.data
        )
        
        return response
        
    except InvalidFileError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except CSVProcessingError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar el CSV: {str(e)}")

