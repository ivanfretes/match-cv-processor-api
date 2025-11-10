# Match CV Processor API

API para procesar archivos PDF (CVs) y generar resúmenes utilizando OpenAI.

## Requisitos Previos

- Python 3.11 o superior
- Docker y Docker Compose (opcional, para ejecutar con Docker)
- API Key de OpenAI

## Configuración

### Opción 1: Archivo de Propiedades (Recomendado para desarrollo local)

1. Crea el archivo `application.properties` a partir del ejemplo:
   ```bash
   cp application.properties.example application.properties
   ```

2. Edita `application.properties` y agrega tu API key:
   ```properties
   OPENAI_API_KEY=sk-tu-api-key-aqui
   OPENAI_MODEL=gpt-3.5-turbo
   ```

### Opción 2: Variables de Entorno (Recomendado para producción)

Puedes configurar las variables de entorno directamente:
```bash
export OPENAI_API_KEY=sk-tu-api-key-aqui
export OPENAI_MODEL=gpt-3.5-turbo
```

Las variables de entorno tienen prioridad sobre el archivo de propiedades.

## Ejecución

### Opción 1: Ejecución Local (Terminal)

1. Crea un entorno virtual (recomendado):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. Configura las variables de entorno o crea el archivo `application.properties` (ver sección de Configuración).

4. Ejecuta la aplicación:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

   El flag `--reload` permite que la aplicación se recargue automáticamente cuando cambies el código (útil para desarrollo).

5. La API estará disponible en: `http://localhost:8000`

6. Documentación interactiva disponible en:
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

### Opción 2: Ejecución con Docker Compose

1. Crea el archivo `application.properties` o configura las variables de entorno:
   ```bash
   export OPENAI_API_KEY=sk-tu-api-key-aqui
   export OPENAI_MODEL=gpt-3.5-turbo
   ```

2. Ejecuta con Docker Compose:
   ```bash
   docker-compose up --build
   ```

   O en modo detach (en segundo plano):
   ```bash
   docker-compose up -d --build
   ```

3. La API estará disponible en: `http://localhost:8000`

4. Para ver los logs:
   ```bash
   docker-compose logs -f
   ```

5. Para detener el contenedor:
   ```bash
   docker-compose down
   ```

## Pruebas con Postman

### 1. Endpoint: Health Check

**GET** `http://localhost:8000/health`

- **Headers**: Ninguno requerido
- **Body**: No requiere body
- **Respuesta esperada**:
  ```json
  {
    "status": "healthy"
  }
  ```

### 2. Endpoint: Root

**GET** `http://localhost:8000/`

- **Headers**: Ninguno requerido
- **Body**: No requiere body
- **Respuesta esperada**:
  ```json
  {
    "message": "FastAPI está funcionando correctamente"
  }
  ```

### 3. Endpoint: Upload PDF (Con Resumen)

**POST** `http://localhost:8000/upload/pdf`

**Configuración en Postman:**

1. **Method**: POST
2. **URL**: `http://localhost:8000/upload/pdf`
3. **Headers**: 
   - No se requieren headers especiales, Postman los configurará automáticamente
4. **Body**: 
   - Selecciona `form-data`
   - Agrega una clave `file` de tipo `File`
   - Selecciona un archivo PDF desde tu computadora
   - (Opcional) Agrega parámetros:
     - `language`: `spanish` o `english` (por defecto: `spanish`)
     - `generate_summary`: `true` o `false` (por defecto: `true`)

**Ejemplo con parámetros:**
- `file`: [Selecciona tu archivo PDF]
- `language`: `spanish`
- `generate_summary`: `true`

**Respuesta esperada**:
```json
{
  "filename": "cv.pdf",
  "total_pages": 2,
  "character_count": 1234,
  "text": "Texto extraído del PDF...",
  "message": "PDF procesado correctamente. Total de caracteres: 1234",
  "summary": "Resumen profesional del CV generado por OpenAI...",
  "summary_generated": true
}
```

**Nota**: Si `generate_summary` es `false` o hay un error al generar el resumen, la respuesta incluirá `summary_generated: false` y posiblemente `summary_error`.

### 4. Endpoint: Upload PDF (Sin Resumen)

**POST** `http://localhost:8000/upload/pdf`

**Configuración en Postman:**

1. **Method**: POST
2. **URL**: `http://localhost:8000/upload/pdf?generate_summary=false`
   O en el body:
   - `file`: [Archivo PDF]
   - `generate_summary`: `false`

**Respuesta esperada**:
```json
{
  "filename": "cv.pdf",
  "total_pages": 2,
  "character_count": 1234,
  "text": "Texto extraído del PDF...",
  "message": "PDF procesado correctamente. Total de caracteres: 1234",
  "summary_generated": false
}
```

### 5. Endpoint: Upload CSV

**POST** `http://localhost:8000/upload/csv`

**Configuración en Postman:**

1. **Method**: POST
2. **URL**: `http://localhost:8000/upload/csv`
3. **Body**: 
   - Selecciona `form-data`
   - Agrega una clave `file` de tipo `File`
   - Selecciona un archivo CSV

**Respuesta esperada**:
```json
{
  "filename": "data.csv",
  "total_rows": 10,
  "columns": ["col1", "col2", "col3"],
  "data": [
    {"col1": "value1", "col2": "value2", "col3": "value3"},
    ...
  ]
}
```

## Ejemplos de Uso con cURL

### Health Check
```bash
curl http://localhost:8000/health
```

### Upload PDF con Resumen
```bash
curl -X POST "http://localhost:8000/upload/pdf?language=spanish&generate_summary=true" \
  -F "file=@/ruta/a/tu/cv.pdf"
```

### Upload PDF sin Resumen
```bash
curl -X POST "http://localhost:8000/upload/pdf?generate_summary=false" \
  -F "file=@/ruta/a/tu/cv.pdf"
```

### Upload CSV
```bash
curl -X POST "http://localhost:8000/upload/csv" \
  -F "file=@/ruta/a/tu/archivo.csv"
```

## Solución de Problemas

### Error: "Configuración requerida 'OPENAI_API_KEY' no encontrada"

**Solución**: Asegúrate de tener configurada la API key:
- Crea el archivo `application.properties` con tu API key, o
- Configura la variable de entorno `OPENAI_API_KEY`

### Error: "Error al generar resumen con OpenAI"

**Posibles causas**:
- API key inválida o expirada
- Problemas de conexión a Internet
- Límite de uso de la API de OpenAI alcanzado
- El texto del CV está vacío

**Solución**: 
- Verifica que tu API key sea válida
- Revisa tu conexión a Internet
- Verifica tu cuenta de OpenAI y los límites de uso

### El servidor no inicia

**Solución**:
- Verifica que el puerto 8000 no esté en uso: `lsof -i :8000` (Linux/Mac) o `netstat -ano | findstr :8000` (Windows)
- Cambia el puerto en el comando: `uvicorn main:app --host 0.0.0.0 --port 8001`

## Estructura del Proyecto

```
.
├── main.py                      # Aplicación principal FastAPI
├── config.py                    # Manejo de configuración
├── services/
│   ├── __init__.py
│   └── openai_service.py        # Servicio de OpenAI
├── requirements.txt             # Dependencias Python
├── application.properties.example # Plantilla de configuración
├── application.properties       # Archivo de configuración (no versionado)
├── Dockerfile                   # Imagen Docker
├── docker-compose.yml           # Configuración Docker Compose
└── README.md                    # Este archivo
```

## Documentación de la API

Cuando la aplicación está ejecutándose, puedes acceder a la documentación interactiva en:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

Estas interfaces te permiten probar los endpoints directamente desde el navegador.

