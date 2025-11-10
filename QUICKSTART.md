# Guía Rápida de Inicio

## Inicio Rápido (3 pasos)

### 1. Configurar API Key

**Opción A: Archivo de propiedades (Recomendado)**
```bash
cp application.properties.example application.properties
# Edita application.properties y agrega tu OPENAI_API_KEY
```

**Opción B: Variable de entorno**
```bash
export OPENAI_API_KEY=sk-tu-api-key-aqui
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Ejecutar la aplicación
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## Probar con Postman (Paso a Paso)

### Paso 1: Verificar que la API está funcionando

1. Abre Postman
2. Crea una nueva solicitud GET
3. URL: `http://localhost:8000/health`
4. Click en "Send"
5. Deberías ver: `{"status": "healthy"}`

### Paso 2: Probar upload de PDF con resumen

1. Crea una nueva solicitud POST
2. URL: `http://localhost:8000/upload/pdf`
3. Ve a la pestaña "Body"
4. Selecciona "form-data"
5. Agrega:
   - Key: `file` (tipo: File) → Selecciona un PDF
   - Key: `language` (tipo: Text) → Valor: `spanish`
   - Key: `generate_summary` (tipo: Text) → Valor: `true`
6. Click en "Send"
7. Deberías ver la respuesta con el texto extraído y el resumen generado

### Paso 3: Probar sin generar resumen

1. Misma configuración que el Paso 2
2. Cambia `generate_summary` a `false`
3. Click en "Send"
4. Deberías ver solo el texto extraído sin resumen

## Probar desde la Terminal (cURL)

```bash
# Health check
curl http://localhost:8000/health

# Upload PDF con resumen
curl -X POST "http://localhost:8000/upload/pdf?language=spanish&generate_summary=true" \
  -F "file=@/ruta/a/tu/cv.pdf"

# Upload PDF sin resumen
curl -X POST "http://localhost:8000/upload/pdf?generate_summary=false" \
  -F "file=@/ruta/a/tu/cv.pdf"
```

## Documentación Interactiva

Una vez que la aplicación esté corriendo, visita:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

Puedes probar los endpoints directamente desde el navegador.

## Solución Rápida de Problemas

**Error: "OPENAI_API_KEY no encontrada"**
→ Crea `application.properties` o configura la variable de entorno

**Error: Puerto 8000 en uso**
→ Cambia el puerto: `uvicorn main:app --host 0.0.0.0 --port 8001`

**Error: No se puede conectar**
→ Verifica que la aplicación esté corriendo y escuchando en el puerto correcto

