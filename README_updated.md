# 🍽️ FastAPI Restaurant Backend

**Sistema completo de gestión para restaurantes** construido con FastAPI, que incluye gestión de menús, vinos, sistema de autenticación JWT y campos de auditoría completos.

## 🌟 Características Principales

- ✅ **API REST completa** con CRUD para platos y vinos
- 🔐 **Sistema de autenticación JWT** con roles de administrador
- 🛡️ **Endpoints protegidos** - solo administradores pueden modificar datos
- 📅 **Campos de auditoría** - seguimiento automático de cambios (created_at, updated_at, is_active, deleted_at)
- 🗑️ **Eliminación lógica (soft delete)** - preserva datos históricos
- 🏷️ **Gestión completa de alérgenos** según legislación española (14 alérgenos obligatorios)
- 🍷 **Gestión avanzada de vinos** con bodegas, denominaciones de origen y enólogos
- 📋 **Paginación y filtrado** en todos los endpoints
- 🔄 **Scripts automatizados** para gestión de base de datos

## 🔐 Sistema de Autenticación y Seguridad

### 🌍 Endpoints Públicos (sin autenticación)
**Solo operaciones de lectura:**
- `GET /api/v1/platos/` - Listar platos
- `GET /api/v1/platos/{id}` - Ver plato específico
- `GET /api/v1/vinos/` - Listar vinos
- `GET /api/v1/vinos/{id}` - Ver vino específico

### 🔒 Endpoints Protegidos (requieren autenticación de administrador)
**Todas las operaciones de modificación:**
- `POST /api/v1/platos/` - Crear plato
- `PUT /api/v1/platos/{id}` - Actualizar plato
- `DELETE /api/v1/platos/{id}` - Eliminar plato (soft delete)
- `POST /api/v1/vinos/` - Crear vino
- `PUT /api/v1/vinos/{id}` - Actualizar vino
- `DELETE /api/v1/vinos/{id}` - Eliminar vino (soft delete)
- `ALL /api/v1/admin/*` - Panel de administración completo

### 🔑 Usuario Administrador por Defecto

Al ejecutar el setup de la base de datos, se crea automáticamente:

- **Username:** `admin`
- **Password:** `admin123`
- **Email:** `admin@restaurant.com`
- **Role:** Administrador (is_admin=True)

### 🚀 Proceso de Autenticación

1. **Login:** `POST /api/v1/auth/login`
   ```json
   {
     "username": "admin",
     "password": "admin123"
   }
   ```

2. **Respuesta con token JWT:**
   ```json
   {
     "access_token": "eyJhbGciOiJIUzI1NiIs...",
     "token_type": "bearer"
   }
   ```

3. **Usar token en requests protegidos:**
   ```
   Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
   ```

## 📅 Sistema de Auditoría

Todas las entidades incluyen campos de auditoría automáticos:

### 🔍 Campos de Auditoría
- **`created_at`** - Fecha/hora de creación (automático)
- **`updated_at`** - Fecha/hora de última modificación (automático)
- **`is_active`** - Estado activo/inactivo (default: True)
- **`deleted_at`** - Fecha/hora de eliminación lógica (null por defecto)

### 🗑️ Eliminación Lógica (Soft Delete)
- Los registros NO se eliminan físicamente
- Se marca `deleted_at` con la fecha de eliminación
- Los registros "eliminados" se excluyen automáticamente de consultas
- Posibilidad de restaurar registros eliminados

## 🗄️ Modelo de Datos

### 🍽️ Platos
```json
{
  "id": 1,
  "nombre": "Paella Valenciana",
  "precio": 18.50,
  "descripcion": "Arroz con pollo, conejo y verduras",
  "categoria_id": 7,
  "alergenos": [1, 12],
  "created_at": "2025-08-23T10:00:00Z",
  "updated_at": "2025-08-23T10:00:00Z",
  "is_active": true,
  "deleted_at": null
}
```

### 🍷 Vinos
```json
{
  "id": 1,
  "nombre": "Marqués de Riscal Reserva",
  "precio": 25.90,
  "categoria_id": 2,
  "bodega_id": 1,
  "denominacion_origen_id": 1,
  "enologo_id": 1,
  "uvas": [1, 3],
  "created_at": "2025-08-23T10:00:00Z",
  "updated_at": "2025-08-23T10:00:00Z",
  "is_active": true,
  "deleted_at": null
}
```

### 📚 Datos por Defecto Incluidos

#### 🏷️ Categorías de Platos (10 categorías)
1. Sin categoría
2. Entrantes
3. Platos principales
4. Postres
5. Ensaladas
6. Tapas
7. Arroces
8. Carnes
9. Pescados
10. Mariscos

#### 🚨 Alérgenos (Legislación Española - 14 alérgenos + Sin alérgenos)
1. Sin alérgenos
2. Cereales que contienen gluten
3. Crustáceos
4. Huevos
5. Pescado
6. Cacahuetes
7. Soja
8. Leche
9. Frutos de cáscara
10. Apio
11. Mostaza
12. Granos de sésamo
13. Dióxido de azufre y sulfitos
14. Altramuces
15. Moluscos

#### 🍷 Categorías de Vinos (11 categorías)
1. Sin categoría
2. Tinto crianza
3. Tinto reserva
4. Tinto gran reserva
5. Tinto joven
6. Blanco joven
7. Blanco fermentado en barrica
8. Rosado
9. Espumoso
10. Dulce
11. Generoso

#### 🗺️ Denominaciones de Origen (6 básicas)
1. Sin denominación
2. Rioja
3. Ribera del Duero
4. Rías Baixas
5. Jerez
6. Cava
7. Penedès

#### 🍇 Tipos de Uva (11 variedades)
1. Sin especificar
2. Tempranillo (tinta)
3. Garnacha (tinta)
4. Monastrell (tinta)
5. Albariño (blanca)
6. Verdejo (blanca)
7. Godello (blanca)
8. Mencía (tinta)
9. Bobal (tinta)
10. Macabeo (blanca)
11. Palomino (blanca)

## 🚀 Instalación y Configuración

### 📋 Requisitos Previos
- Python 3.11 o superior
- MySQL 8.0 o superior
- pip (gestor de paquetes de Python)

### 🔧 Configuración del Entorno

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/santiago-rey2/Fast-Api-Backend.git
   cd Fast-Api-Backend
   ```

2. **Crear y activar entorno virtual:**
   ```bash
   python -m venv venv
   
   # Windows
   .\venv\Scripts\Activate.ps1
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar base de datos:**
   
   Crear archivo `.env` en la raíz del proyecto:
   ```env
   # Configuración de Base de Datos
   DB_HOST=localhost
   DB_PORT=3306
   DB_USER=tu_usuario
   DB_PASSWORD=tu_password
   DB_NAME=restaurante_db
   
   # Configuración JWT
   SECRET_KEY=tu_clave_secreta_muy_segura
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

5. **Crear base de datos en MySQL:**
   ```sql
   CREATE DATABASE restaurante_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

### 🏃‍♂️ Inicialización del Proyecto

#### ⚡ Setup Completo Automático (Recomendado)

```bash
python scripts-examples/setup_complete_database.py
```

**Este script realiza:**
1. 🗑️ Elimina todas las tablas existentes
2. 🏗️ Crea la estructura de la base de datos con campos de auditoría
3. 📦 Carga datos por defecto (categorías, alérgenos, etc.)
4. 👤 Crea usuario administrador (admin/admin123)
5. 🎭 Carga datos de ejemplo (platos y vinos realistas)

#### 🔧 Scripts Individuales

**Solo limpiar base de datos:**
```bash
python scripts-examples/clear_database.py
```

**Solo cargar datos de ejemplo:**
```bash
python scripts-examples/load_sample_data.py
```

### 🚀 Ejecutar la Aplicación

```bash
python -m uvicorn src.main:app --reload
```

**Acceso a la aplicación:**
- 🌐 **API:** http://localhost:8000
- 📖 **Documentación Swagger:** http://localhost:8000/docs
- 📋 **Documentación ReDoc:** http://localhost:8000/redoc

## 📡 Endpoints de la API

### 🔓 Autenticación
- `POST /api/v1/auth/login` - Iniciar sesión y obtener token JWT

### 🍽️ Gestión de Platos
- `GET /api/v1/platos/` - 🌍 Listar platos (público)
- `GET /api/v1/platos/{id}` - 🌍 Obtener plato específico (público)
- `POST /api/v1/platos/` - 🔒 Crear plato (admin)
- `PUT /api/v1/platos/{id}` - 🔒 Actualizar plato (admin)
- `DELETE /api/v1/platos/{id}` - 🔒 Eliminar plato - soft delete (admin)

### 🍷 Gestión de Vinos
- `GET /api/v1/vinos/` - 🌍 Listar vinos (público)
- `GET /api/v1/vinos/{id}` - 🌍 Obtener vino específico (público)
- `POST /api/v1/vinos/` - 🔒 Crear vino (admin)
- `PUT /api/v1/vinos/{id}` - 🔒 Actualizar vino (admin)
- `DELETE /api/v1/vinos/{id}` - 🔒 Eliminar vino - soft delete (admin)

### ⚙️ Panel de Administración (`/api/v1/admin/`) - 🔒 Solo administradores

#### Categorías
- `GET /api/v1/admin/categoria-platos/` - Listar categorías de platos
- `POST /api/v1/admin/categoria-platos/` - Crear categoría de plato
- `PUT /api/v1/admin/categoria-platos/{id}` - Actualizar categoría de plato
- `DELETE /api/v1/admin/categoria-platos/{id}` - Eliminar categoría de plato
- `GET /api/v1/admin/categoria-vinos/` - Listar categorías de vinos
- `POST /api/v1/admin/categoria-vinos/` - Crear categoría de vino
- `PUT /api/v1/admin/categoria-vinos/{id}` - Actualizar categoría de vino
- `DELETE /api/v1/admin/categoria-vinos/{id}` - Eliminar categoría de vino

#### Alérgenos
- `GET /api/v1/admin/alergenos/` - Listar alérgenos
- `POST /api/v1/admin/alergenos/` - Crear alérgeno
- `PUT /api/v1/admin/alergenos/{id}` - Actualizar alérgeno
- `DELETE /api/v1/admin/alergenos/{id}` - Eliminar alérgeno

#### Gestión de Vinos
- `GET /api/v1/admin/bodegas/` - Listar bodegas
- `POST /api/v1/admin/bodegas/` - Crear bodega
- `PUT /api/v1/admin/bodegas/{id}` - Actualizar bodega
- `DELETE /api/v1/admin/bodegas/{id}` - Eliminar bodega
- `GET /api/v1/admin/denominaciones-origen/` - Listar denominaciones
- `POST /api/v1/admin/denominaciones-origen/` - Crear denominación
- `PUT /api/v1/admin/denominaciones-origen/{id}` - Actualizar denominación
- `DELETE /api/v1/admin/denominaciones-origen/{id}` - Eliminar denominación
- `GET /api/v1/admin/enologos/` - Listar enólogos
- `POST /api/v1/admin/enologos/` - Crear enólogo
- `PUT /api/v1/admin/enologos/{id}` - Actualizar enólogo
- `DELETE /api/v1/admin/enologos/{id}` - Eliminar enólogo
- `GET /api/v1/admin/uvas/` - Listar tipos de uva
- `POST /api/v1/admin/uvas/` - Crear tipo de uva
- `PUT /api/v1/admin/uvas/{id}` - Actualizar tipo de uva
- `DELETE /api/v1/admin/uvas/{id}` - Eliminar tipo de uva

## 🗃️ Gestión de Base de Datos

### 📋 Scripts Disponibles

En la carpeta `scripts-examples/` encontrarás:

#### 1. 🚀 `setup_complete_database.py` - Setup Completo
```bash
python scripts-examples/setup_complete_database.py
```
**Realiza todo el proceso de inicialización automáticamente**

#### 2. 🗑️ `clear_database.py` - Limpiar Base de Datos
```bash
python scripts-examples/clear_database.py
```
**Solo elimina todas las tablas, dejando la BD vacía**

#### 3. 📦 `load_sample_data.py` - Cargar Datos de Ejemplo
```bash
python scripts-examples/load_sample_data.py
```
**Carga platos y vinos de ejemplo (requiere estructura básica)**

### 🔄 Flujos de Trabajo Comunes

**Setup inicial completo (recomendado):**
```bash
python scripts-examples/setup_complete_database.py
```

**Limpiar y empezar de cero:**
```bash
python scripts-examples/clear_database.py
# Luego usar la API para cargar datos manualmente
```

**Solo agregar datos de ejemplo:**
```bash
python scripts-examples/load_sample_data.py
```

## 📁 Estructura del Proyecto

```
Fast-Api-Backend/
├── src/                          # Código fuente principal
│   ├── auth/                     # Sistema de autenticación JWT
│   │   ├── dependencies.py      # Dependencias de autenticación
│   │   ├── routes.py            # Endpoints de login
│   │   └── service.py           # Lógica de autenticación
│   ├── core/                     # Configuración central
│   │   └── config.py            # Variables de entorno
│   ├── database/                 # Conexión y configuración DB
│   │   └── __init__.py          # Setup de SQLAlchemy
│   ├── entities/                 # Modelos de datos (SQLAlchemy)
│   │   ├── mixins.py            # AuditMixin con campos de auditoría
│   │   ├── plato.py             # Modelo de Plato
│   │   ├── vino.py              # Modelo de Vino
│   │   ├── user.py              # Modelo de Usuario
│   │   └── *.py                 # Otros modelos
│   ├── repositories/             # Capa de acceso a datos
│   ├── routes/                   # Endpoints de la API
│   │   ├── auth.py              # Rutas de autenticación
│   │   ├── platos.py            # Rutas de platos (públicas GET, protegidas POST/PUT/DELETE)
│   │   ├── vinos.py             # Rutas de vinos (públicas GET, protegidas POST/PUT/DELETE)
│   │   └── admin.py             # Panel de administración (todo protegido)
│   ├── schemas/                  # Validación de datos (Pydantic)
│   ├── services/                 # Lógica de negocio
│   └── main.py                   # Punto de entrada
├── scripts-examples/             # Scripts de gestión de BD
│   ├── setup_complete_database.py  # Setup completo automático
│   ├── clear_database.py           # Limpiar base de datos
│   ├── load_sample_data.py         # Cargar datos de ejemplo
│   ├── example_*.csv               # Datos de referencia CSV
│   └── README.md                   # Documentación de scripts
├── .env.example                     # Configuración de ejemplo
├── requirements.txt                 # Dependencias Python
└── README.md                        # Esta documentación
```

## 🛠️ Tecnologías Utilizadas

### Backend Core
- **FastAPI** - Framework web moderno y rápido para APIs
- **SQLAlchemy** - ORM potente para Python
- **Pydantic v2** - Validación y serialización de datos
- **MySQL** - Sistema de gestión de base de datos relacional

### Autenticación y Seguridad
- **python-jose** - Implementación JWT para Python
- **passlib** - Hashing seguro de contraseñas
- **bcrypt** - Algoritmo de hashing robusto

### Servidor y Desarrollo
- **Uvicorn** - Servidor ASGI de alto rendimiento
- **python-multipart** - Manejo de formularios multipart

## 🧪 Testing y Desarrollo

### 🔧 Modo Desarrollo

El servidor incluye recarga automática en modo desarrollo:
```bash
python -m uvicorn src.main:app --reload
```

### 📊 Verificación del Sistema

Después del setup, verifica que todo funcione:

1. **API funcionando:** http://localhost:8000
2. **Documentación:** http://localhost:8000/docs
3. **Login con usuario admin:** `admin` / `admin123`
4. **Endpoints públicos funcionando sin autenticación**
5. **Endpoints protegidos requiriendo token JWT**

### 🎯 Datos de Ejemplo Incluidos

Al ejecutar el setup completo, obtienes:
- **📊 Estructura completa** con campos de auditoría
- **👤 Usuario administrador** listo para usar
- **🏷️ Categorías y alérgenos** según legislación española
- **🍽️ Platos de ejemplo** con precios realistas
- **🍷 Vinos de ejemplo** con bodegas y características

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 👨‍💻 Autor

**Santiago Rey** - [@santiago-rey2](https://github.com/santiago-rey2)

---

⭐ **¡Dale una estrella al proyecto si te ha sido útil!**
