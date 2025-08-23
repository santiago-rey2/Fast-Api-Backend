# API de Gestión de Restaurante - Sistema Completo

## 🚀 Funcionalidades Implementadas

### 📋 Gestión de Platos
- **CRUD completo** para platos
- **Filtrado por categoría** y búsqueda por nombre
- **Paginación** con límite y offset
- **Gestión de alérgenos** por plato

### 🍷 Gestión de Vinos
- **CRUD completo** para vinos
- **Filtrado por categoría y bodega**
- **Relaciones** con bodegas, enólogos, denominaciones de origen
- **Gestión de uvas** por vino

### ⚙️ Panel de Administración
- **Gestión de Categorías** (platos y vinos)
- **Gestión de Alérgenos**
- **Gestión de Bodegas**
- **Gestión de Denominaciones de Origen**
- **Gestión de Enólogos**
- **Gestión de Uvas**
- **Carga masiva desde CSV**

### 🌐 Web Scraping Inteligente
- **Extracción automática** de datos de restaurantes
- **Creación dinámica** de categorías y alérgenos
- **Mapeo automático** de iconos de alérgenos
- **Procesamiento** de más de 60 platos reales

## 📡 Endpoints de la API

### Gestión de Platos (`/api/v1/platos/`)
```http
GET    /api/v1/platos/              # Listar platos con filtros y paginación
POST   /api/v1/platos/              # Crear nuevo plato
GET    /api/v1/platos/{id}          # Obtener plato específico
PUT    /api/v1/platos/{id}          # Actualizar plato
DELETE /api/v1/platos/{id}          # Eliminar plato
```

### Gestión de Vinos (`/api/v1/vinos/`)
```http
GET    /api/v1/vinos/               # Listar vinos con filtros y paginación
POST   /api/v1/vinos/               # Crear nuevo vino
GET    /api/v1/vinos/{id}           # Obtener vino específico
PUT    /api/v1/vinos/{id}           # Actualizar vino
DELETE /api/v1/vinos/{id}           # Eliminar vino
```

### Panel de Administración (`/api/v1/admin/`)

#### Categorías de Platos
```http
GET    /api/v1/admin/categorias/              # Listar categorías
POST   /api/v1/admin/categorias/              # Crear categoría
PUT    /api/v1/admin/categorias/{id}          # Actualizar categoría
DELETE /api/v1/admin/categorias/{id}          # Eliminar categoría
```

#### Alérgenos
```http
GET    /api/v1/admin/alergenos/               # Listar alérgenos
POST   /api/v1/admin/alergenos/               # Crear alérgeno
PUT    /api/v1/admin/alergenos/{id}           # Actualizar alérgeno
DELETE /api/v1/admin/alergenos/{id}           # Eliminar alérgeno
```

#### Categorías de Vinos
```http
GET    /api/v1/admin/categorias-vinos/        # Listar categorías de vinos
POST   /api/v1/admin/categorias-vinos/        # Crear categoría de vino
PUT    /api/v1/admin/categorias-vinos/{id}    # Actualizar categoría de vino
DELETE /api/v1/admin/categorias-vinos/{id}    # Eliminar categoría de vino
```

#### Bodegas
```http
GET    /api/v1/admin/bodegas/                 # Listar bodegas
POST   /api/v1/admin/bodegas/                 # Crear bodega
PUT    /api/v1/admin/bodegas/{id}             # Actualizar bodega
DELETE /api/v1/admin/bodegas/{id}             # Eliminar bodega
```

#### Denominaciones de Origen
```http
GET    /api/v1/admin/denominaciones-origen/      # Listar denominaciones
POST   /api/v1/admin/denominaciones-origen/      # Crear denominación
PUT    /api/v1/admin/denominaciones-origen/{id}  # Actualizar denominación
DELETE /api/v1/admin/denominaciones-origen/{id}  # Eliminar denominación
```

#### Enólogos
```http
GET    /api/v1/admin/enologos/                # Listar enólogos
POST   /api/v1/admin/enologos/                # Crear enólogo
PUT    /api/v1/admin/enologos/{id}            # Actualizar enólogo
DELETE /api/v1/admin/enologos/{id}            # Eliminar enólogo
```

#### Uvas
```http
GET    /api/v1/admin/uvas/                    # Listar uvas
POST   /api/v1/admin/uvas/                    # Crear uva
PUT    /api/v1/admin/uvas/{id}                # Actualizar uva
DELETE /api/v1/admin/uvas/{id}                # Eliminar uva
```

#### Carga Masiva CSV
```http
POST   /api/v1/admin/upload-csv               # Cargar datos desde CSV
```

## 📤 Carga Masiva con CSV

### Formato del CSV
Todos los archivos CSV deben tener el formato:
```csv
nombre
Nombre del Item 1
Nombre del Item 2
Nombre del Item 3
```

### Tipos de entidad soportados:
- `categorias` - Categorías de platos
- `alergenos` - Alérgenos
- `categorias_vinos` - Categorías de vinos
- `bodegas` - Bodegas
- `denominaciones_origen` - Denominaciones de origen
- `enologos` - Enólogos
- `uvas` - Tipos de uva

### Ejemplo de uso con curl:
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/admin/upload-csv?entity_type=categorias" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@example_categorias.csv"
```

### Respuesta del endpoint:
```json
{
  "entity_type": "categorias",
  "total_rows": 10,
  "created_count": 8,
  "error_count": 2,
  "errors": [
    "Fila 3: 'Entrantes' ya existe",
    "Fila 7: 'Postres' ya existe"
  ]
}
```

## 🤖 Web Scraping Automático

### Funcionalidades
- **Extracción inteligente** de menús de restaurantes
- **Creación automática** de categorías dinámicas
- **Mapeo de alérgenos** por iconos
- **Procesamiento** de precios y descripciones
- **Integración** directa con la base de datos

### Ejecutar el scraping:
```bash
python src/scripts/extract_restaurant_data.py
```

### Características del script:
- ✅ **Crea categorías automáticamente** si no existen
- ✅ **Mapea alérgenos** por iconos de la web
- ✅ **Evita duplicados** verificando nombres existentes
- ✅ **Manejo de errores** robusto
- ✅ **Logging detallado** del proceso

## 🎯 Ejemplos de Uso

### 1. Obtener platos de una categoría específica
```bash
curl "http://127.0.0.1:8000/api/v1/platos/?categoria_id=1&limit=5"
```

### 2. Buscar platos por nombre
```bash
curl "http://127.0.0.1:8000/api/v1/platos/?search=croquetas&limit=10"
```

### 3. Crear nueva categoría
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/admin/categorias/" \
     -H "Content-Type: application/json" \
     -d '{"nombre": "Tapas Especiales"}'
```

### 4. Crear nuevo alérgeno
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/admin/alergenos/" \
     -H "Content-Type: application/json" \
     -d '{"nombre": "Sin Gluten"}'
```

### 5. Cargar bodegas desde CSV
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/admin/upload-csv?entity_type=bodegas" \
     -F "file=@example_bodegas.csv"
```

## 🗂️ Archivos CSV de Ejemplo

El proyecto incluye archivos CSV de ejemplo:
- `example_categorias.csv` - Categorías de platos
- `example_alergenos.csv` - Alérgenos comunes
- `example_bodegas.csv` - Bodegas españolas famosas

## 🚀 Inicio Rápido

1. **Activar entorno virtual:**
```bash
.\venv\Scripts\Activate.ps1
```

2. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

3. **Iniciar servidor:**
```bash
python -m uvicorn src.main:app --reload --host 127.0.0.1 --port 8000
```

4. **Acceder a la documentación:**
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## 📊 Estado del Proyecto

✅ **Completado:**
- API completa de platos y vinos
- Panel de administración total
- Carga masiva CSV
- Web scraping inteligente
- Base de datos poblada con 56+ platos reales
- Documentación completa

🔄 **En desarrollo:**
- Mejoras en el mapeo de alérgenos
- Extensión a otros restaurantes
- Sistema de autenticación

## 🎉 ¡Sistema Completamente Funcional!

El sistema ahora incluye:
- ✅ **496+ líneas** de código de administración
- ✅ **Todos los CRUD** implementados
- ✅ **Carga masiva** desde CSV
- ✅ **Web scraping** con categorías dinámicas
- ✅ **Base de datos** poblada con datos reales
- ✅ **Documentación** completa
