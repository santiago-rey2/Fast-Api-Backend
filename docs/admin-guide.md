# 👨‍💼 Guía de Administración - Gestión de Cartas de Restaurante

<div align="center">

![Admin Panel](https://img.shields.io/badge/Admin-Panel-blue?style=for-the-badge&logo=settings)
![CRUD](https://img.shields.io/badge/Full-CRUD-green?style=for-the-badge&logo=database)
![JWT](https://img.shields.io/badge/JWT-Secured-orange?style=for-the-badge&logo=jsonwebtokens)

</div>

## 🚀 Funcionalidades del Panel de Administración

### 📋 Gestión de Platos
- **CRUD completo** para platos
- **Filtrado por categoría** y búsqueda por nombre
- **Paginación** con límite y offset
- **Gestión de alérgenos** por plato
- **Soft delete** con opción de restaurar

### 🍷 Gestión de Vinos
- **CRUD completo** para vinos
- **Filtrado por categoría y bodega**
- **Relaciones** con bodegas, enólogos, denominaciones de origen
- **Gestión de uvas** por vino
- **Control de inventario** y precios

### ⚙️ Configuración del Sistema
- **Gestión de Categorías** (platos y vinos)
- **Gestión de Alérgenos**
- **Gestión de Bodegas**
- **Gestión de Denominaciones de Origen**
- **Gestión de Enólogos**
- **Gestión de Uvas**
- **Carga masiva desde CSV**

## 📡 Endpoints de la API

### Gestión de Platos (`/api/v1/platos/`)

```http
GET    /api/v1/platos/              # Listar platos con filtros y paginación
POST   /api/v1/platos/              # Crear nuevo plato
GET    /api/v1/platos/{id}          # Obtener plato específico
PUT    /api/v1/platos/{id}          # Actualizar plato
DELETE /api/v1/platos/{id}          # Eliminar plato (soft delete)
POST   /api/v1/platos/{id}/restore  # Restaurar plato eliminado
```

### Gestión de Vinos (`/api/v1/vinos/`)

```http
GET    /api/v1/vinos/               # Listar vinos con filtros y paginación
POST   /api/v1/vinos/               # Crear nuevo vino
GET    /api/v1/vinos/{id}           # Obtener vino específico
PUT    /api/v1/vinos/{id}           # Actualizar vino
DELETE /api/v1/vinos/{id}           # Eliminar vino (soft delete)
POST   /api/v1/vinos/{id}/restore   # Restaurar vino eliminado
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

### 📋 Formato del CSV

Todos los archivos CSV deben tener el formato:

```csv
nombre
Nombre del Item 1
Nombre del Item 2
Nombre del Item 3
```

### 🗂️ Tipos de entidad soportados

- `categorias` - Categorías de platos
- `alergenos` - Alérgenos
- `categorias_vinos` - Categorías de vinos
- `bodegas` - Bodegas
- `denominaciones_origen` - Denominaciones de origen
- `enologos` - Enólogos
- `uvas` - Tipos de uva

### 💻 Ejemplo de uso con curl

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/admin/upload-csv?entity_type=categorias" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@example_categorias.csv"
```

### 📊 Respuesta del endpoint

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

### 6. Eliminar un plato (soft delete)
```bash
curl -X DELETE "http://127.0.0.1:8000/api/v1/admin/platos/123" \
     -H "Authorization: Bearer tu_jwt_token"
```

### 7. Restaurar un plato eliminado
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/admin/platos/123/restore" \
     -H "Authorization: Bearer tu_jwt_token"
```

## 🔐 Autenticación

### Obtener Token JWT
```bash
curl -X POST "http://127.0.0.1:8000/auth/token" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=admin&password=admin123"
```

### Usar Token en Peticiones
```bash
curl -X GET "http://127.0.0.1:8000/admin/platos" \
     -H "Authorization: Bearer tu_jwt_token_aqui"
```

## 🗂️ Archivos CSV de Ejemplo

El proyecto incluye archivos CSV de ejemplo para carga masiva:
- `example_categorias.csv` - Categorías de platos
- `example_alergenos.csv` - Alérgenos comunes
- `example_bodegas.csv` - Bodegas españolas famosas

## 🚀 Inicio Rápido

1. **Activar entorno virtual:**
```bash
# Windows
.\venv\Scripts\Activate.ps1

# Linux/Mac
source venv/bin/activate
```

2. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

3. **Configurar base de datos:**
```bash
# Crear base de datos
python -c "from src.scripts.create_db import create_database; create_database()"

# Aplicar migraciones
python -c "from src.database import init_db; init_db()"

# Cargar datos iniciales
python -c "from src.scripts.seed import create_initial_data; create_initial_data()"
```

4. **Iniciar servidor:**
```bash
uvicorn src.main:app --reload --host 127.0.0.1 --port 8000
```

5. **Acceder a la documentación:**
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## 🔧 Gestión de Base de Datos

### Scripts Disponibles

#### Setup Completo (scripts-examples/)
```bash
python scripts-examples/setup_complete_database.py
```
Ejecuta la configuración completa: crea DB, tablas y carga datos de ejemplo.

#### Limpiar Base de Datos
```bash
python scripts-examples/clear_database.py
```
Elimina todos los datos y resetea la base de datos.

#### Cargar Datos de Ejemplo
```bash
python scripts-examples/load_sample_data.py
```
Carga un conjunto completo de datos de prueba.

## 📊 Características de los Datos

### Platos
- Categorización por tipos (entrantes, principales, postres, etc.)
- Información nutricional y descripción
- Gestión de alérgenos múltiples
- Precios y disponibilidad
- Campos de auditoría (creado, modificado, activo, eliminado)

### Vinos
- Denominaciones de origen
- Información de bodegas y enólogos
- Tipos de uva y características
- Añadas y maridajes
- Control de inventario y precios

### Auditoría Completa
Todas las entidades incluyen:
- `created_at`: Fecha de creación
- `updated_at`: Fecha de última modificación
- `is_active`: Estado activo/inactivo
- `deleted_at`: Fecha de eliminación (soft delete)

## 🛠️ Troubleshooting

### Problemas Comunes

1. **Error de autenticación**
   - Verificar que el token JWT no haya expirado
   - Comprobar formato del header Authorization
   - Usar credenciales válidas (admin/admin123)

2. **Error al cargar CSV**
   - Verificar formato del CSV (header "nombre")
   - Comprobar codificación del archivo (UTF-8)
   - Validar tipo de entidad en la URL

3. **Error de conexión a base de datos**
   - Verificar que MySQL esté ejecutándose
   - Comprobar credenciales en archivo .env
   - Asegurar que la base de datos existe

### Logs de Sistema
Los logs incluyen:
- Operaciones CRUD detalladas
- Errores de autenticación
- Resultados de carga masiva
- Excepciones del sistema

## 📈 Monitoreo y Métricas

### Endpoints de Estadísticas
- Total de platos por categoría
- Inventario de vinos por bodega
- Alérgenos más comunes
- Elementos recientemente añadidos

### Logs de Auditoría
- Seguimiento de todas las operaciones CRUD
- Historial de modificaciones
- Estadísticas de uso de la API
- Análisis de patrones de acceso

## 🎉 Sistema Completamente Funcional

El panel de administración incluye:
- ✅ **CRUD completo** para todas las entidades
- ✅ **Autenticación JWT** robusta
- ✅ **Carga masiva** desde CSV
- ✅ **Soft delete** con restauración
- ✅ **Filtros avanzados** y paginación
- ✅ **Documentación automática** con Swagger
- ✅ **Base de datos** con campos de auditoría
- ✅ **Manejo de errores** completo
