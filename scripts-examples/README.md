# Scripts de Base de Datos

Esta carpeta contiene los scripts esenciales para gestionar la base de datos del proyecto.

## 📋 Scripts Disponibles

### 1. 🗑️ `clear_database.py`
**Propósito**: Elimina todas las tablas de la base de datos dejándola completamente vacía.

**Uso**:
```bash
python scripts-examples/clear_database.py
```

**Características**:
- ✅ Elimina TODAS las tablas de la base de datos
- ✅ Maneja foreign key constraints de MySQL
- ✅ Verifica que la base de datos quede completamente vacía
- ⚠️ NO carga ningún dato - solo eliminación

---

### 2. 📦 `load_sample_data.py`
**Propósito**: Carga datos de ejemplo en la base de datos (platos y vinos realistas).

**Uso**:
```bash
python scripts-examples/load_sample_data.py
```

**Prerrequisitos**:
- La base de datos debe tener la estructura básica (categorías, alérgenos, etc.)
- Se recomienda ejecutar primero `setup_complete_database.py`

**Datos que carga**:
- 🍽️ Platos de ejemplo con descripciones realistas
- 🍷 Vinos de ejemplo con bodegas y enólogos
- 🏭 Bodegas españolas
- 👨‍🍳 Enólogos reconocidos

---

### 3. 🚀 `setup_complete_database.py`
**Propósito**: Script completo que hace todo - elimina, crea estructura y carga datos.

**Uso**:
```bash
python scripts-examples/setup_complete_database.py
```

**Lo que hace**:
1. 🔥 Elimina todas las tablas existentes
2. 🏗️ Recrea la estructura de la base de datos
3. 🌱 Carga datos por defecto (categorías, alérgenos, etc.)
4. 👤 Crea usuario administrador (admin/admin123)
5. 📦 Carga datos de ejemplo (platos y vinos)

**¡Recomendado para setup inicial!**

---

## 🔄 Flujos de Trabajo Comunes

### Setup inicial completo
```bash
python scripts-examples/setup_complete_database.py
```

### Limpiar y empezar de cero (sin datos de ejemplo)
```bash
python scripts-examples/clear_database.py
# Luego usar la API o cargar datos manualmente
```

### Solo cargar datos de ejemplo
```bash
python scripts-examples/load_sample_data.py
```

---

## 📁 Archivos CSV de Ejemplo

- `example_alergenos.csv` - Lista de alérgenos según legislación española
- `example_bodegas.csv` - Bodegas españolas de referencia  
- `example_categorias.csv` - Categorías de platos y vinos

## 🔐 Usuario Administrador

Los scripts que crean estructura también crean un usuario administrador:
- **Username**: admin
- **Password**: admin123
- **Role**: admin

Este usuario puede acceder a todos los endpoints protegidos de la API.
