# Análisis de Arquitectura y Recomendaciones

## 📋 Resumen del Proyecto

**Match CV Processor API** es una aplicación FastAPI que procesa archivos PDF (CVs) y genera resúmenes utilizando OpenAI. La aplicación permite:
- Subir y procesar archivos PDF
- Extraer texto de PDFs
- Generar resúmenes profesionales usando LLM (OpenAI)
- Procesar archivos CSV

---

## 🏗️ Estructura Actual del Proyecto

### 1. **Controllers (Endpoints)**
**Ubicación:** `main.py`

Los controllers están definidos directamente en `main.py` como funciones de FastAPI:

```python
@app.post("/upload/pdf")
async def upload_pdf(...)

@app.post("/upload/csv")
async def upload_csv(...)

@app.get("/health")
async def health()

@app.get("/")
async def root()
```

**Problema:** Los controllers están mezclados con la lógica de negocio y el código de infraestructura (lectura de PDFs, procesamiento de archivos).

---

### 2. **Lógica de Negocio**
**Ubicación:** Mezclada entre `main.py` y `services/openai_service.py`

**En `main.py`:**
- Lógica de extracción de texto de PDFs (líneas 60-79)
- Lógica de procesamiento de CSV (líneas 132-153)
- Construcción de respuestas HTTP
- Manejo de errores HTTP

**En `services/openai_service.py`:**
- Lógica de generación de prompts
- Construcción de mensajes para OpenAI
- Manejo de errores de OpenAI

**Problema:** La lógica de negocio no está separada de la infraestructura. No hay una capa de dominio clara.

---

### 3. **Comunicación con LLM**
**Ubicación:** `services/openai_service.py`

La comunicación con OpenAI está encapsulada en la clase `OpenAIService`:

```python
class OpenAIService:
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo")
    def generate_cv_summary(self, cv_text: str, language: str, max_tokens: int) -> str
```

**Aspectos positivos:**
- ✅ Encapsulación del cliente de OpenAI
- ✅ Manejo de errores personalizado (`OpenAIServiceError`)
- ✅ Validación de entrada (texto vacío)

**Problemas:**
- ❌ La clase está acoplada directamente a la librería `openai`
- ❌ No hay abstracción/interfaz para facilitar testing o cambio de proveedor
- ❌ Los prompts están hardcodeados en el servicio

---

### 4. **Utilidades**
**Ubicación:** `utils/text_cleaner.py`

Funciones para limpiar y normalizar texto extraído de PDFs:
- `clean_pdf_text()`: Limpieza agresiva del texto
- `clean_text_preserve_structure()`: Limpieza conservadora

---

### 5. **Configuración**
**Ubicación:** `config.py`

Clase `Config` que maneja:
- Lectura de archivos `.properties`
- Variables de entorno (con prioridad)
- Valores requeridos vs opcionales

---

## 🔍 Problemas Identificados

### 1. **Arquitectura No Hexagonal**

**Problema:** El proyecto no sigue arquitectura hexagonal (ports & adapters). Todo está acoplado directamente.

**Evidencia:**
- Los controllers (`main.py`) conocen directamente `PdfReader`, `csv.DictReader`
- No hay separación entre dominio, aplicación e infraestructura
- No hay interfaces/abstracciones para servicios externos

**Impacto:**
- Difícil de testear (mocks complejos)
- Difícil cambiar proveedores (ej: cambiar de OpenAI a otro LLM)
- Difícil cambiar frameworks (ej: cambiar de FastAPI a otro)

---

### 2. **Violación de Principios SOLID**

#### **Single Responsibility Principle (SRP)**
- `upload_pdf()` hace demasiadas cosas:
  - Valida el archivo
  - Lee el PDF
  - Extrae texto
  - Limpia texto
  - Genera resumen (opcional)
  - Construye respuesta HTTP

#### **Dependency Inversion Principle (DIP)**
- Los controllers dependen de implementaciones concretas (`PdfReader`, `OpenAIService`)
- No hay abstracciones/interfaces

#### **Open/Closed Principle (OCP)**
- Para agregar otro tipo de archivo (ej: DOCX), hay que modificar `main.py`
- Para cambiar el proveedor de LLM, hay que modificar código existente

---

### 3. **Falta de Capas de Dominio**

**Problema:** No hay entidades de dominio, value objects, o casos de uso claros.

**Lo que falta:**
- Entidades: `CV`, `PDFDocument`, `Summary`
- Value Objects: `Language`, `FileType`
- Casos de Uso: `ProcessCVUseCase`, `GenerateSummaryUseCase`
- Repositorios: Interfaces para persistencia (si se necesita en el futuro)

---

### 4. **Manejo de Errores Inconsistente**

**Problemas:**
- Mezcla de `HTTPException` (FastAPI) con excepciones de dominio
- Errores de OpenAI se convierten en strings en la respuesta HTTP
- No hay un sistema centralizado de manejo de errores

---

### 5. **Falta de Validación de Entrada**

**Problemas:**
- Validación de tipo de archivo solo por extensión (línea 56, 128)
- No hay validación de tamaño de archivo
- No hay validación de parámetros con Pydantic models

---

### 6. **Testing**

**Problema:** No hay tests visibles en el proyecto.

**Lo que falta:**
- Tests unitarios
- Tests de integración
- Mocks para servicios externos

---

### 7. **Código Duplicado**

**Problema:** Lógica similar en diferentes lugares:
- Manejo de errores genérico en múltiples endpoints
- Construcción de respuestas HTTP similar

---

## ✅ Recomendaciones de Mejora

### 1. **Implementar Arquitectura Hexagonal**

**Estructura propuesta:**
```
match-cv-processor-api/
├── domain/                    # Capa de dominio (núcleo)
│   ├── entities/
│   │   ├── cv.py             # Entidad CV
│   │   └── document.py       # Entidad Document
│   ├── value_objects/
│   │   ├── language.py
│   │   └── file_type.py
│   ├── ports/                # Interfaces (puertos)
│   │   ├── llm_service.py    # Interfaz para LLM
│   │   ├── pdf_extractor.py # Interfaz para extraer PDFs
│   │   └── text_cleaner.py  # Interfaz para limpiar texto
│   └── exceptions/
│       └── domain_exceptions.py
│
├── application/              # Capa de aplicación (casos de uso)
│   ├── use_cases/
│   │   ├── process_cv_use_case.py
│   │   └── generate_summary_use_case.py
│   └── dto/
│       ├── cv_dto.py
│       └── summary_dto.py
│
├── infrastructure/           # Capa de infraestructura (adaptadores)
│   ├── adapters/
│   │   ├── openai_adapter.py      # Implementa llm_service port
│   │   ├── pypdf_extractor.py     # Implementa pdf_extractor port
│   │   └── text_cleaner_impl.py   # Implementa text_cleaner port
│   ├── config/
│   │   └── config.py
│   └── persistence/          # Si se necesita en el futuro
│
├── presentation/             # Capa de presentación
│   ├── api/
│   │   ├── controllers/
│   │   │   ├── cv_controller.py
│   │   │   └── health_controller.py
│   │   ├── models/
│   │   │   ├── request_models.py
│   │   │   └── response_models.py
│   │   └── dependencies.py
│   └── exceptions/
│       └── exception_handlers.py
│
├── main.py                   # Configuración de FastAPI
└── tests/
    ├── unit/
    ├── integration/
    └── e2e/
```

---

### 2. **Separar Responsabilidades**

#### **Controllers (Solo HTTP)**
```python
# presentation/api/controllers/cv_controller.py
@router.post("/upload/pdf")
async def upload_pdf(
    file: UploadFile,
    language: str = "spanish",
    generate_summary: bool = True,
    use_case: ProcessCVUseCase = Depends(get_process_cv_use_case)
):
    """Solo valida entrada HTTP y llama al caso de uso"""
    request = ProcessCVRequest(
        file=file,
        language=language,
        generate_summary=generate_summary
    )
    result = await use_case.execute(request)
    return ProcessCVResponse.from_domain(result)
```

#### **Casos de Uso (Lógica de Negocio)**
```python
# application/use_cases/process_cv_use_case.py
class ProcessCVUseCase:
    def __init__(
        self,
        pdf_extractor: PDFExtractorPort,
        text_cleaner: TextCleanerPort,
        summary_generator: LLMServicePort
    ):
        self.pdf_extractor = pdf_extractor
        self.text_cleaner = text_cleaner
        self.summary_generator = summary_generator
    
    async def execute(self, request: ProcessCVRequest) -> CVProcessResult:
        # Orquestar la lógica de negocio
        document = await self.pdf_extractor.extract(file)
        cleaned_text = self.text_cleaner.clean(document.text)
        # ...
```

#### **Adaptadores (Infraestructura)**
```python
# infrastructure/adapters/openai_adapter.py
class OpenAIAdapter(LLMServicePort):
    """Implementa la interfaz LLMServicePort usando OpenAI"""
    def __init__(self, client: OpenAI, model: str):
        self.client = client
        self.model = model
    
    async def generate_summary(self, text: str, language: Language) -> Summary:
        # Implementación específica de OpenAI
```

---

### 3. **Crear Interfaces (Ports)**

```python
# domain/ports/llm_service.py
from abc import ABC, abstractmethod
from domain.entities.summary import Summary
from domain.value_objects.language import Language

class LLMServicePort(ABC):
    """Puerto (interfaz) para servicios de LLM"""
    
    @abstractmethod
    async def generate_cv_summary(
        self,
        cv_text: str,
        language: Language
    ) -> Summary:
        """Genera un resumen del CV"""
        pass
```

**Beneficios:**
- Fácil cambiar de OpenAI a otro proveedor
- Fácil hacer mocks para testing
- Cumple Dependency Inversion Principle

---

### 4. **Usar Pydantic para Validación**

```python
# presentation/api/models/request_models.py
from pydantic import BaseModel, Field, validator
from enum import Enum

class Language(str, Enum):
    SPANISH = "spanish"
    ENGLISH = "english"

class ProcessCVRequest(BaseModel):
    language: Language = Field(default=Language.SPANISH)
    generate_summary: bool = Field(default=True)
    max_file_size: int = Field(default=10 * 1024 * 1024)  # 10MB
    
    @validator('language')
    def validate_language(cls, v):
        return v.lower()
```

---

### 5. **Manejo Centralizado de Errores**

```python
# presentation/api/exceptions/exception_handlers.py
from fastapi import Request
from fastapi.responses import JSONResponse
from domain.exceptions.domain_exceptions import (
    CVProcessingError,
    InvalidFileError,
    LLMServiceError
)

@app.exception_handler(CVProcessingError)
async def cv_processing_error_handler(request: Request, exc: CVProcessingError):
    return JSONResponse(
        status_code=400,
        content={"error": exc.message, "code": exc.code}
    )

@app.exception_handler(LLMServiceError)
async def llm_service_error_handler(request: Request, exc: LLMServiceError):
    return JSONResponse(
        status_code=503,
        content={"error": "LLM service unavailable", "details": exc.message}
    )
```

---

### 6. **Crear Entidades de Dominio**

```python
# domain/entities/cv.py
from dataclasses import dataclass
from domain.value_objects.language import Language
from domain.entities.summary import Summary

@dataclass
class CV:
    """Entidad de dominio: CV"""
    filename: str
    text: str
    total_pages: int
    character_count: int
    summary: Summary | None = None
    language: Language = Language.SPANISH
    
    def has_summary(self) -> bool:
        return self.summary is not None
    
    def is_valid(self) -> bool:
        return len(self.text.strip()) > 0
```

---

### 7. **Inyección de Dependencias Mejorada**

```python
# presentation/api/dependencies.py
from infrastructure.adapters.openai_adapter import OpenAIAdapter
from infrastructure.adapters.pypdf_extractor import PyPDFExtractor
from application.use_cases.process_cv_use_case import ProcessCVUseCase

def get_llm_service() -> LLMServicePort:
    api_key = config.get_required("OPENAI_API_KEY")
    model = config.get("OPENAI_MODEL", "gpt-3.5-turbo")
    client = OpenAI(api_key=api_key)
    return OpenAIAdapter(client, model)

def get_pdf_extractor() -> PDFExtractorPort:
    return PyPDFExtractor()

def get_process_cv_use_case(
    pdf_extractor: PDFExtractorPort = Depends(get_pdf_extractor),
    text_cleaner: TextCleanerPort = Depends(get_text_cleaner),
    llm_service: LLMServicePort = Depends(get_llm_service)
) -> ProcessCVUseCase:
    return ProcessCVUseCase(
        pdf_extractor=pdf_extractor,
        text_cleaner=text_cleaner,
        summary_generator=llm_service
    )
```

---

### 8. **Agregar Tests**

```python
# tests/unit/application/use_cases/test_process_cv_use_case.py
import pytest
from unittest.mock import Mock, AsyncMock
from application.use_cases.process_cv_use_case import ProcessCVUseCase

@pytest.mark.asyncio
async def test_process_cv_with_summary():
    # Arrange
    mock_pdf_extractor = Mock()
    mock_pdf_extractor.extract = AsyncMock(return_value=MockDocument(...))
    
    mock_llm = Mock()
    mock_llm.generate_cv_summary = AsyncMock(return_value=MockSummary(...))
    
    use_case = ProcessCVUseCase(
        pdf_extractor=mock_pdf_extractor,
        text_cleaner=Mock(),
        summary_generator=mock_llm
    )
    
    # Act
    result = await use_case.execute(request)
    
    # Assert
    assert result.has_summary()
    mock_llm.generate_cv_summary.assert_called_once()
```

---

### 9. **Mejorar Validación de Archivos**

```python
# domain/services/file_validator.py
class FileValidator:
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS = {'.pdf', '.csv'}
    
    @staticmethod
    def validate_file(file: UploadFile) -> None:
        if not file.filename:
            raise InvalidFileError("Filename is required")
        
        extension = Path(file.filename).suffix.lower()
        if extension not in FileValidator.ALLOWED_EXTENSIONS:
            raise InvalidFileError(f"Extension {extension} not allowed")
        
        # Validar tamaño (requiere leer el archivo)
        # ...
```

---

### 10. **Separar Prompts del Servicio**

```python
# domain/services/prompt_builder.py
class PromptBuilder:
    """Construye prompts para diferentes idiomas y casos de uso"""
    
    @staticmethod
    def build_cv_summary_prompt(language: Language) -> tuple[str, str]:
        if language == Language.SPANISH:
            return (
                "Eres un experto en recursos humanos...",
                "Por favor, genera un resumen profesional..."
            )
        else:
            return (
                "You are an expert in human resources...",
                "Please generate a professional summary..."
            )
```

---

## 📊 Comparación: Antes vs Después

| Aspecto | Antes | Después (Propuesto) |
|---------|-------|---------------------|
| **Separación de capas** | ❌ Todo mezclado | ✅ Domain/Application/Infrastructure/Presentation |
| **Testabilidad** | ❌ Difícil (acoplamiento) | ✅ Fácil (interfaces) |
| **Cambio de proveedor LLM** | ❌ Modificar código | ✅ Cambiar adaptador |
| **Validación** | ❌ Solo en controllers | ✅ En múltiples capas |
| **Manejo de errores** | ❌ Inconsistente | ✅ Centralizado |
| **Principios SOLID** | ❌ Violados | ✅ Respetados |
| **Arquitectura** | ❌ Monolítica | ✅ Hexagonal |

---

## 🎯 Prioridades de Implementación

### **Fase 1: Fundamentos (Alta Prioridad)**
1. ✅ Crear estructura de carpetas (domain/application/infrastructure/presentation)
2. ✅ Crear interfaces (ports) para servicios externos
3. ✅ Separar controllers de lógica de negocio
4. ✅ Crear casos de uso básicos

### **Fase 2: Mejoras (Media Prioridad)**
5. ✅ Implementar entidades de dominio
6. ✅ Mejorar validación con Pydantic
7. ✅ Centralizar manejo de errores
8. ✅ Agregar tests unitarios

### **Fase 3: Optimizaciones (Baja Prioridad)**
9. ✅ Separar prompts en servicio dedicado
10. ✅ Agregar logging estructurado
11. ✅ Agregar métricas/monitoreo
12. ✅ Documentación de API mejorada

---

## 📝 Conclusión

El proyecto actual funciona, pero tiene problemas de arquitectura que dificultan:
- **Mantenibilidad**: Código acoplado es difícil de modificar
- **Testabilidad**: Sin interfaces, los tests son complejos
- **Escalabilidad**: Agregar nuevas features requiere modificar código existente
- **Flexibilidad**: Cambiar proveedores o frameworks es costoso

La implementación de arquitectura hexagonal y principios de clean code mejorará significativamente la calidad del código y facilitará el crecimiento del proyecto.

