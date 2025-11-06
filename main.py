from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
from pypdf import PdfReader
import csv
import io
from typing import List, Dict
from openai import APIError

from config import config
from services.openai_service import OpenAIService

app = FastAPI(title="File Upload Processor", version="1.0.0")


def get_openai_service() -> OpenAIService:
    """
    Dependency injection para el servicio de OpenAI.
    
    Returns:
        Instancia configurada de OpenAIService
    """
    api_key = config.get_required("OPENAI_API_KEY")
    model = config.get("OPENAI_MODEL", "gpt-3.5-turbo")
    return OpenAIService(api_key=api_key, model=model)


@app.get("/")
async def root():
    return {"message": "FastAPI está funcionando correctamente"}


@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/upload/pdf")
async def upload_pdf(
    file: UploadFile = File(...),
    language: str = "spanish",
    generate_summary: bool = True,
    openai_service: OpenAIService = Depends(get_openai_service)
):
    """
    Endpoint para subir un PDF y extraer el texto del documento.
    Opcionalmente genera un resumen del CV utilizando OpenAI.
    
    Args:
        file: Archivo PDF a procesar
        language: Idioma para el resumen (spanish/english)
        generate_summary: Si True, genera un resumen usando OpenAI
        openai_service: Servicio de OpenAI inyectado como dependencia
        
    Returns:
        Diccionario con información del PDF y opcionalmente el resumen generado
    """
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="El archivo debe ser un PDF")
    
    try:
        # Leer el contenido del archivo
        contents = await file.read()
        
        # Crear un objeto PdfReader desde bytes
        pdf_file = io.BytesIO(contents)
        reader = PdfReader(pdf_file)
        
        # Extraer texto de todas las páginas
        text_content = ""
        total_pages = len(reader.pages)
        
        for page_num, page in enumerate(reader.pages, 1):
            page_text = page.extract_text() or ""
            text_content += ("\n" + page_text)
        
        # Contar caracteres
        character_count = len(text_content)
        
        # Preparar respuesta base
        response = {
            "filename": file.filename,
            "total_pages": total_pages,
            "character_count": character_count,
            "text": text_content,
            "message": f"PDF procesado correctamente. Total de caracteres: {character_count}"
        }
        
        # Generar resumen si está habilitado
        if generate_summary and text_content.strip():
            try:
                summary = openai_service.generate_cv_summary(
                    cv_text=text_content,
                    language=language
                )
                response["summary"] = summary
                response["summary_generated"] = True
            except APIError as e:
                # Si falla la generación del resumen, no falla toda la operación
                response["summary"] = None
                response["summary_generated"] = False
                response["summary_error"] = str(e)
            except ValueError as e:
                response["summary"] = None
                response["summary_generated"] = False
                response["summary_error"] = str(e)
        else:
            response["summary_generated"] = False
        
        return response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar el PDF: {str(e)}")


@app.post("/upload/csv")
async def upload_csv(file: UploadFile = File(...)):
    """
    Endpoint para subir un CSV y leer su contenido.
    Retorna los datos del CSV en formato JSON.
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="El archivo debe ser un CSV")
    
    try:
        # Leer el contenido del archivo
        contents = await file.read()
        
        # Decodificar el contenido
        content_str = contents.decode('utf-8')
        
        # Leer el CSV
        csv_reader = csv.DictReader(io.StringIO(content_str))
        rows = list(csv_reader)
        
        # Obtener los nombres de las columnas
        if rows:
            columns = list(rows[0].keys())
        else:
            columns = []
        
        return {
            "filename": file.filename,
            "total_rows": len(rows),
            "columns": columns,
            "data": rows
        }
    
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="Error de codificación. El archivo debe estar en UTF-8")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar el CSV: {str(e)}")

