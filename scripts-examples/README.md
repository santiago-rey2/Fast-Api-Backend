# 📋 Scripts de Ejemplo

Esta carpeta contiene scripts útiles para la gestión de la base de datos y carga de datos de ejemplo.

## 🗃️ Scripts Disponibles

### 1. `reset_database.py` - Reset Completo de Base de Datos

**Propósito:** Elimina completamente la base de datos y la recrea con datos por defecto.

```bash
python scripts-examples/reset_database.py
```

**Qué hace:**
- 🔥 Elimina todas las tablas existentes
- 🏗️ Recrea la estructura de la base de datos
- 🌱 Carga datos por defecto (categorías, alérgenos, etc.)
- 👤 Crea usuario administrador por defecto

**Datos por defecto incluidos:**
- 10 categorías de platos
- 14 alérgenos (legislación española)
- 10 categorías de vinos
- 5 denominaciones de origen básicas
- 10 tipos de uva comunes
- Usuario administrador: `admin` / `admin123`

---

### 2. `load_sample_data.py` - Cargar Datos de Ejemplo

**Propósito:** Carga datos de ejemplo realistas para desarrollo y testing.

```bash
python scripts-examples/load_sample_data.py
```

**Prerrequisitos:** La base de datos debe estar inicializada con datos por defecto.

**Qué carga:**
- 🏭 8 bodegas españolas famosas
- 👨‍🔬 6 enólogos reconocidos
- 🍽️ 11 platos típicos españoles con alérgenos
- 🍷 6 vinos representativos con sus características

**Ejemplos de datos:**
- **Platos:** Croquetas de jamón, Paella valenciana, Cochinillo asado, Crema catalana...
- **Vinos:** Marqués de Riscal Reserva, Vega Sicilia Único, Martín Códax Albariño...
- **Bodegas:** Marqués de Riscal, Vega Sicilia, Torres, González Byass...

---

### 3. `setup_complete_database.py` - Setup Completo Automático

**Propósito:** Ejecuta el setup completo en un solo comando.

```bash
python scripts-examples/setup_complete_database.py
```

**Qué hace:**
1. ✅ Ejecuta `reset_database.py`
2. ✅ Ejecuta `load_sample_data.py`
3. ✅ Verifica que todo esté correcto

**Ideal para:** Configuración inicial del proyecto o reset completo para development.

---

### 4. `run_extraction.py` - Web Scraping de Restaurantes

**Propósito:** Extrae datos reales de cartas de restaurantes usando web scraping.

```bash
python scripts-examples/run_extraction.py
```

**Características:**
- 🕷️ Web scraping inteligente
- 🏷️ Creación dinámica de categorías
- 💰 Extracción automática de precios
- 📊 Datos realistas de restaurantes

---

## 🔄 Flujos de Trabajo Comunes

### Configuración Inicial del Proyecto
```bash
# Setup completo automático
python scripts-examples/setup_complete_database.py

# Iniciar servidor
python -m uvicorn src.main:app --reload
```

### Reset Solo con Datos Por Defecto
```bash
# Solo datos básicos
python scripts-examples/reset_database.py

# Iniciar servidor
python -m uvicorn src.main:app --reload
```

### Agregar Datos de Ejemplo a Base Existente
```bash
# Solo si ya tienes datos por defecto
python scripts-examples/load_sample_data.py
```

### Cargar Datos Reales de Restaurantes
```bash
# Después de tener la base configurada
python scripts-examples/run_extraction.py
```

## ⚠️ Consideraciones Importantes

### Seguridad
- 🔐 Estos scripts están diseñados para **desarrollo**
- 🚫 **NO** usar en producción sin revisar configuraciones
- 📝 Cambiar credenciales por defecto en producción

### Base de Datos
- 💾 Los scripts requieren conexión a MySQL
- ⚙️ Verificar configuración en `src/core/config.py`
- 🔄 Hacer backup antes de ejecutar reset en datos importantes

### Dependencias
- 📦 Asegurar que `requirements.txt` esté instalado
- 🐍 Python 3.11+ requerido
- 🗄️ MySQL Server corriendo

## 🆘 Solución de Problemas

### Error de Conexión a Base de Datos
```bash
# Verificar que MySQL esté corriendo
# Verificar configuración en src/core/config.py
# Verificar credenciales de base de datos
```

### Error de Módulos no Encontrados
```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar desde el directorio raíz del proyecto
cd Fast-Api-Backend
python scripts-examples/reset_database.py
```

### Error de Permisos
```bash
# En Windows, ejecutar como administrador si es necesario
# Verificar permisos de escritura en la base de datos
```

## 📖 Recursos Adicionales

- **Documentación de la API:** `http://localhost:8000/docs`
- **Panel de administración:** Usar credenciales `admin` / `admin123`
- **Endpoints públicos:** `GET /api/v1/platos/` y `GET /api/v1/vinos/`
