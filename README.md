# 🍽️ FastAPI Restaurant Backend

**Sistema completo de gestión para restaurantes** construido con FastAPI, que incluye gestión de menús, vinos, panel de administración y sistema de web scraping para extracción de datos de cartas de restaurantes.

## 🌟 Características Principales

- ✅ **API REST completa** con CRUD para platos y vinos
- 🛡️ **Panel de administración** con 25+ endpoints para gestión completa
- 🕷️ **Web scraping inteligente** con creación dinámica de categorías
- 📊 **Sistema robusto de precios** con extracción automática de datos
- 🏷️ **Gestión completa de alérgenos** según legislación española (14 alérgenos)
- 🍷 **Gestión avanzada de vinos** con bodegas, denominaciones de origen y enólogos
- 📋 **Paginación y filtrado** en todos los endpoints
- 🔄 **Carga automática de datos** por defecto al iniciar

## 🗄️ Modelo de Datos

### 🍽️ Platos
- **Nombre** *(obligatorio)*
- **Precio** *(≥ 0.00€)*
- **Descripción** *(opcional/null)*
- **Categoría** *(con valores por defecto)*
- **Alérgenos** *(relación many-to-many)*

### 🍷 Vinos
- **Nombre** *(obligatorio)*
- **Precio** *(≥ 0.00€)*
- **Categoría** *(10 categorías por defecto)*
- **Bodega** *(opcional, con región)*
- **Denominación de origen** *(opcional, con región)*
- **Enólogo** *(opcional, con años de experiencia)*
- **Tipos de uva** *(relación many-to-many)*

### 📚 Datos por Defecto Incluidos

#### 🏷️ Categorías de Platos
- Sin categoría
- Entrantes
- Platos principales
- Postres
- Ensaladas
- Tapas
- Arroces
- Carnes
- Pescados
- Mariscos

#### 🚨 Alérgenos (Legislación Española)
Los 14 alérgenos obligatorios:
1. Cereales que contienen gluten
2. Crustáceos
3. Huevos
4. Pescado
5. Cacahuetes
6. Soja
7. Leche
8. Frutos de cáscara
9. Apio
10. Mostaza
11. Granos de sésamo
12. Dióxido de azufre y sulfitos
13. Altramuces
14. Moluscos

#### 🍷 Categorías de Vinos
- Tinto joven/crianza/reserva/gran reserva
- Blanco joven/fermentado en barrica
- Rosado
- Espumoso
- Dulce
- Generoso

## 🚀 Instalación y Configuración

### 📋 Requisitos Previos
- Python 3.11 o superior
- MySQL 8.0 o superior
- pip (gestor de paquetes)

### 🔧 Configuración del Entorno

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/santiago-rey2/Fast-Api-Backend.git
   cd Fast-Api-Backend
   ```

2. **Crear y activar entorno virtual**:
   ```bash
   python -m venv venv
   
   # Windows
   .\venv\Scripts\Activate.ps1
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar base de datos**:
   - Crea un archivo `.env` basado en `.env.example`
   - Configura tu conexión MySQL
   ```env
   DB_HOST=localhost
   DB_PORT=3306
   DB_USER=tu_usuario
   DB_PASSWORD=tu_password
   DB_NAME=restaurante_db
   ```

### 🏃‍♂️ Ejecutar la Aplicación

#### 💻 Modo Desarrollo Local

1. **Iniciar servidor de desarrollo**:
   ```bash
   uvicorn src.main:app --reload
   ```

2. **Acceso a la aplicación**:
   - API: http://localhost:8000
   - Documentación Swagger: http://localhost:8000/docs
   - Documentación ReDoc: http://localhost:8000/redoc

#### 🐳 Modo Docker (Recomendado para Producción)

1. **Solo base de datos**:
   ```bash
   docker-compose up -d
   ```

2. **Sistema completo** (Base de datos + API):
   ```bash
   docker-compose -f docker-compose.full.yml up -d
   ```

3. **Scripts automatizados**:
   ```bash
   # Windows
   cd docker
   start-docker.bat
   
   # Linux/Mac
   cd docker
   ./start-docker.sh
   ```

4. **Servicios disponibles**:
   - 🗄️ MySQL: `localhost:3306`
   - 🌐 Adminer: `http://localhost:8080`
   - 🚀 FastAPI: `http://localhost:8000` (solo en modo completo)

**Ver [Documentación Docker](docker/README.md) para más detalles.**

### 🗃️ Gestión de Base de Datos

**Reset completo de base de datos**:
```bash
python src/scripts/force_reset_db.py
```
*Elimina todas las tablas. Al reiniciar el servidor se recrean automáticamente con datos por defecto.*

## 📡 Endpoints de la API

### 🍽️ Gestión de Platos
- `GET /platos/` - Listar platos (con paginación y filtros)
- `POST /platos/` - Crear plato
- `GET /platos/{id}` - Obtener plato específico
- `PUT /platos/{id}` - Actualizar plato completo
- `PATCH /platos/{id}` - Actualizar plato parcialmente
- `DELETE /platos/{id}` - Eliminar plato

### 🍷 Gestión de Vinos
- `GET /vinos/` - Listar vinos (con paginación y filtros)
- `POST /vinos/` - Crear vino
- `GET /vinos/{id}` - Obtener vino específico
- `PUT /vinos/{id}` - Actualizar vino completo
- `PATCH /vinos/{id}` - Actualizar vino parcialmente
- `DELETE /vinos/{id}` - Eliminar vino

### ⚙️ Panel de Administración (`/admin`)
- **Categorías**: CRUD completo para categorías de platos y vinos
- **Alérgenos**: CRUD completo para gestión de alérgenos
- **Bodegas**: CRUD con gestión de región
- **Denominaciones**: CRUD con gestión de región
- **Enólogos**: CRUD con años de experiencia
- **Uvas**: CRUD con tipos de uva (tinta/blanca)

## 🕷️ Sistema de Web Scraping

### Características del Scraper
- 🎯 **Extracción inteligente** de menús de restaurantes
- 🏗️ **Creación dinámica** de categorías basada en la estructura web
- 💰 **Detección automática de precios** en múltiples formatos (€, números)
- 🏷️ **Mapeo automático de alérgenos** mediante diccionario inteligente
- 📊 **Más de 50 platos reales** con precios de 4.50€ a 85.00€

### Uso del Scraper
```bash
python src/scripts/extract_restaurant_data.py
```

## 📁 Estructura del Proyecto

```
Fast-Api-Backend/
├── src/                          # Código fuente principal
│   ├── auth/                     # Sistema de autenticación
│   ├── core/                     # Configuración central
│   ├── database/                 # Conexión y configuración DB
│   ├── entities/                 # Modelos de datos (SQLAlchemy)
│   ├── repositories/             # Capa de acceso a datos
│   ├── routes/                   # Endpoints de la API
│   │   ├── platos.py            # Rutas de platos
│   │   ├── vinos.py             # Rutas de vinos
│   │   └── admin.py             # Panel de administración
│   ├── schemas/                  # Validación de datos (Pydantic)
│   ├── scripts/                  # Scripts de utilidad
│   │   ├── extract_restaurant_data.py  # Web scraper
│   │   └── force_reset_db.py           # Reset de BD
│   ├── services/                 # Lógica de negocio
│   └── main.py                   # Punto de entrada
├── docs/                         # Documentación
│   ├── admin-guide.md           # Guía del panel admin
│   ├── esquema_restaurante.md   # Esquema de BD
│   └── *.pdf                    # Documentación técnica
├── scripts-examples/             # Scripts de ejemplo
│   ├── test_*.py                # Scripts de prueba
│   └── example_*.csv            # Datos de ejemplo
├── .env.example                  # Configuración de ejemplo
├── requirements.txt              # Dependencias Python
└── README.md                     # Esta documentación
```

## 🛠️ Tecnologías Utilizadas

- **FastAPI** - Framework web moderno para APIs
- **SQLAlchemy** - ORM para Python
- **Pydantic v2** - Validación y serialización de datos
- **MySQL** - Sistema de gestión de base de datos
- **BeautifulSoup4** - Web scraping
- **Requests** - Cliente HTTP
- **Uvicorn** - Servidor ASGI

## 🧪 Testing y Desarrollo

### Scripts de Prueba Incluidos
- `test_api.py` - Pruebas de endpoints
- `test_imports.py` - Verificación de imports
- `test_prices.py` - Validación de precios

### Datos de Ejemplo
- Archivos CSV con datos de ejemplo para carga masiva
- Más de 50 platos reales con pricing realista
- Datos completos de bodegas, denominaciones y enólogos

## 📖 Documentación Adicional

- 📋 **[Guía de Administración](docs/admin-guide.md)** - Manual completo del panel de administración
- 🗄️ **[Esquema de Base de Datos](docs/esquema_restaurante.md)** - Documentación técnica del modelo
- 📊 **[Modelo de Datos](docs/Modelo_Datos.svg)** - Diagrama visual de relaciones

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
