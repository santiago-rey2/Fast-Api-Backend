# 🍽️ Gestión de Cartas de Restaurante - FastAPI Backend

<div align="center">

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![MySQL](https://img.shields.io/badge/mysql-4479A1.svg?style=for-the-badge&logo=mysql&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens)

</div>

## 📖 Descripción

Este proyecto es un **sistema completo de gestión de cartas de restaurante** desarrollado con FastAPI. Incluye funcionalidades de autenticación JWT, gestión de platos y vinos, y un panel de administración con operaciones CRUD completas.

## 📑 Tabla de Contenidos

- [✨ Características principales](#-características-principales)
- [🗂️ Estructura del proyecto](#️-estructura-del-proyecto)
- [📦 Instalación](#-instalación)
- [🎮 Uso](#-uso)
- [🛣️ API Endpoints](#️-api-endpoints)
- [🗄️ Scripts de Base de Datos](#️-scripts-de-base-de-datos)
- [📊 Estructura de Datos](#-estructura-de-datos)
- [⚙️ Configuración Avanzada](#️-configuración-avanzada)
- [🧪 Desarrollo](#-desarrollo)
- [🛠️ Troubleshooting](#️-troubleshooting)
- [🤝 Contribuir](#-contribuir)
- [📄 Licencia](#-licencia)

## ✨ Características principales

### 🔧 Core del Sistema

- **🚀 API REST con FastAPI**: Backend robusto con documentación automática
- **🔐 Autenticación JWT**: Sistema de tokens seguros para usuarios y administradores
- **🗄️ Base de datos MySQL**: Estructura relacional optimizada con campos de auditoría
- **🗑️ Soft Delete**: Eliminación lógica de registros manteniendo integridad referencial
- **🌐 CORS configurado**: Soporte para aplicaciones frontend

### 👨‍💼 Panel de Administración

- **🍽️ Gestión completa de platos**: CRUD con validaciones
- **🍷 Gestión de vinos**: Categorización y control de inventario
- **📊 Dashboard administrativo**: Interface para operaciones de mantenimiento
- **📝 Logs de auditoría**: Seguimiento de todas las operaciones

## 🗂️ Estructura del proyecto

```text
src/
├── 📱 main.py                 # Aplicación principal FastAPI
├── 🔧 core/
│   ├── config.py              # Configuración y variables de entorno
│   ├── security.py            # Funciones de autenticación JWT
│   └── exceptions.py          # Excepciones personalizadas
├── 🏗️ entities/              # Modelos de base de datos
│   ├── platos.py             # Entidades de platos y categorías
│   ├── vinos.py              # Entidades de vinos y bodegas
│   └── base.py               # Clase base con auditoría
├── 🛣️ routes/               # Endpoints de la API
│   ├── platos.py            # Rutas CRUD para platos
│   ├── vinos.py             # Rutas CRUD para vinos
│   ├── admin.py             # Panel de administración
│   └── auth.py              # Autenticación y autorización
├── ⚙️ services/            # Lógica de negocio
│   ├── platos_service.py
│   ├── vinos_service.py
│   └── auth_service.py
└── 📝 scripts/             # Scripts de utilidad
    ├── create_db.py         # Creación de base de datos
    └── seed.py              # Datos iniciales

📁 scripts-examples/        # Scripts adicionales de gestión
├── setup_complete_database.py    # Configuración completa de DB
├── clear_database.py            # Limpieza de base de datos
└── load_sample_data.py          # Carga de datos de ejemplo
```

## 📦 Instalación

### 📋 Requisitos previos

- ![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python) Python 3.8+
- ![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange?logo=mysql) MySQL 8.0+
- ![pip](https://img.shields.io/badge/pip-package_manager-green) pip (Python package manager)

### 🚀 Pasos de instalación

1. **📥 Clonar el repositorio**

```bash
git clone https://github.com/santiago-rey2/Fast-Api-Backend.git
cd Fast-Api-Backend
```

2. **🐍 Crear entorno virtual**

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **📦 Instalar dependencias**

```bash
pip install -r requirements.txt
```

4. **⚙️ Configurar variables de entorno**

Crear archivo `.env` en la raíz del proyecto:

```env
# Base de datos
DB_HOST=localhost
DB_PORT=3306
DB_USER=tu_usuario
DB_PASSWORD=tu_password
DB_NAME=restaurante_db

# JWT
SECRET_KEY=tu_clave_secreta_muy_segura
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Entorno
ENV=dev
APP_NAME=Restaurante API
DEBUG=True
```

5. **🗄️ Crear y configurar la base de datos**

```bash
# Crear la base de datos
python -c "from src.scripts.create_db import create_database; create_database()"

# Aplicar migraciones (crear tablas)
python -c "from src.database import init_db; init_db()"

# Cargar datos iniciales
python -c "from src.scripts.seed import create_initial_data; create_initial_data()"
```

## 🎮 Uso

### 🚀 Ejecutar el servidor de desarrollo

```bash
uvicorn src.main:app --reload --port 8000
```

La API estará disponible en: <http://localhost:8000>

### 📚 Documentación automática

- **📖 Swagger UI**: <http://localhost:8000/docs>
- **📋 ReDoc**: <http://localhost:8000/redoc>

### 🔐 Autenticación

#### 🎟️ Obtener token de acceso

```bash
curl -X POST "http://localhost:8000/auth/token" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=admin&password=admin123"
```

#### 🔑 Usar token en peticiones

```bash
curl -X GET "http://localhost:8000/admin/platos" \
     -H "Authorization: Bearer tu_jwt_token_aqui"
```

## 🛣️ API Endpoints

### 🌍 Públicos

- `GET /platos/` - Listar platos activos
- `GET /platos/{id}` - Obtener plato específico
- `GET /vinos/` - Listar vinos activos
- `GET /vinos/{id}` - Obtener vino específico

### 🔒 Autenticación

- `POST /auth/token` - Obtener token JWT

### 👨‍💼 Admin (requieren autenticación)

- `GET /admin/platos/` - Listar todos los platos (incluidos eliminados)
- `POST /admin/platos/` - Crear nuevo plato
- `PUT /admin/platos/{id}` - Actualizar plato
- `DELETE /admin/platos/{id}` - Eliminar plato (soft delete)
- `POST /admin/platos/{id}/restore` - Restaurar plato eliminado
- Endpoints similares para vinos en `/admin/vinos/`

## 🗄️ Scripts de Base de Datos

### 📂 Scripts principales (src/scripts/)

- **🏗️ create_db.py**: Crea la base de datos si no existe
- **🌱 seed.py**: Carga datos iniciales (categorías, alérgenos, datos base)

### 📁 Scripts de ejemplo (scripts-examples/)

#### 🚀 Setup Completo

```bash
python scripts-examples/setup_complete_database.py
```

Ejecuta la configuración completa: crea DB, tablas y carga datos de ejemplo.

#### 🗑️ Limpiar Base de Datos

```bash
python scripts-examples/clear_database.py
```

Elimina todos los datos y resetea la base de datos.

#### 📦 Cargar Datos de Ejemplo

```bash
python scripts-examples/load_sample_data.py
```

Carga un conjunto completo de datos de prueba.

## 📊 Estructura de Datos

### 🍽️ Platos

- Categorización por tipos
- Información nutricional
- Gestión de alérgenos
- Precios y disponibilidad
- Control de versiones

### 🍷 Vinos

- Denominaciones de origen
- Información de bodegas
- Tipos de uva
- Añadas y características
- Maridajes recomendados

### 📝 Auditoría

Todas las entidades incluyen:

- `created_at`: Fecha de creación
- `updated_at`: Fecha de última modificación
- `is_active`: Estado activo/inactivo
- `deleted_at`: Fecha de eliminación (soft delete)

## ⚙️ Configuración Avanzada

### 🔧 Variables de Entorno Adicionales

```env
# Configuración de base de datos para producción
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20
DB_POOL_TIMEOUT=30
DB_ECHO=False

# Logs
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
```

## 🧪 Desarrollo

### 🔍 Ejecutar tests

```bash
pytest tests/ -v
```

### 🔄 Generar migraciones

```bash
alembic revision --autogenerate -m "Descripción del cambio"
alembic upgrade head
```

### ✨ Linting y formato

```bash
black src/
flake8 src/
```

## 🛠️ Troubleshooting

### ⚠️ Problemas comunes

1. **🔌 Error de conexión a la base de datos**
   - Verificar que MySQL esté ejecutándose
   - Comprobar credenciales en `.env`
   - Asegurar que la base de datos existe

2. **🔐 Error de autenticación JWT**
   - Verificar que `SECRET_KEY` esté configurado
   - Comprobar que el token no haya expirado
   - Validar formato del header Authorization

### 📋 Logs de aplicación

Los logs se guardan en `logs/app.log` e incluyen:

- Operaciones de base de datos
- Errores de autenticación
- Excepciones del sistema

## 🤝 Contribuir

1. 🍴 Fork el proyecto
2. 🌿 Crear una rama para la nueva característica
3. 💾 Hacer commit de los cambios
4. 📤 Push a la rama
5. 🔄 Crear un Pull Request

## 📄 Licencia

Este proyecto está bajo la **Licencia MIT**. Ver el archivo `LICENSE` para más detalles.

---

<div align="center">

**🍽️ ¡Disfruta gestionando tu restaurante con FastAPI! 🍷**

![Made with ❤️](https://img.shields.io/badge/Made%20with-❤️-red)
![FastAPI](https://img.shields.io/badge/Powered%20by-FastAPI-009688)

</div>
