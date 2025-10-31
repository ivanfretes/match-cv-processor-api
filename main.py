from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pypdf import PdfReader
import csv
import io
from typing import List, Dict

app = FastAPI(title="File Upload Processor", version="1.0.0")


@app.get("/")
async def root():
    return {"message": "FastAPI está funcionando correctamente"}


@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/upload/pdf")
async def upload_pdf(file: UploadFile = File(...), sentences: int = 5, language: str = "spanish"):
    """
    Endpoint para subir un PDF y extraer todos los caracteres/texto del documento.
    Retorna el texto completo extraído del PDF.
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
        
        return {
            "filename": file.filename,
            "total_pages": total_pages,
            "character_count": character_count,
            "text": text_content,
            "message": f"PDF procesado correctamente. Total de caracteres: {character_count}"
        }
    
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

