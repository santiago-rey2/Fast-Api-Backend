# 🗄️ Scripts de Base de Datos - Gestión de Restaurante

<div align="center">

![Database](https://img.shields.io/badge/Database-Management-blue?style=for-the-badge&logo=database)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange?style=for-the-badge&logo=mysql)
![Scripts](https://img.shields.io/badge/Python-Scripts-green?style=for-the-badge&logo=python)

</div>

Esta carpeta contiene **scripts de utilidad** para la gestión de la base de datos del sistema de restaurante FastAPI.

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
# Luego usar la API para cargar datos manualmente
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

## 🚀 Instalación y Configuración

### Requisitos previos
- Python 3.8+
- MySQL 8.0+
- Base de datos configurada según el archivo `.env`

### Pasos recomendados

1. **Configurar variables de entorno**
   ```bash
   cp .env.example .env
   # Editar .env con los datos de tu base de datos
   ```

2. **Ejecutar setup completo**
   ```bash
   python scripts-examples/setup_complete_database.py
   ```

3. **Verificar instalación**
   ```bash
   uvicorn src.main:app --reload
   # Acceder a http://localhost:8000/docs
   ```

## 🔧 Resolución de Problemas

### ❌ Error de conexión a MySQL

```
Error: Can't connect to MySQL server
```

**💡 Solución:**

- ✅ Verificar que MySQL esté ejecutándose
- ✅ Comprobar credenciales en el archivo `.env`
- ✅ Asegurar que la base de datos existe

### 🚫 Error de permisos

```
Error: Access denied for user
```

**💡 Solución:**

- ✅ Verificar usuario y contraseña en `.env`
- ✅ Asegurar que el usuario tenga permisos de DDL (CREATE, DROP)

### 📋 Error de estructura

```
Error: Table doesn't exist
```

**💡 Solución:**

- ✅ Ejecutar `setup_complete_database.py` para crear la estructura
- ✅ Verificar que todas las migraciones se aplicaron correctamente

## 📞 Soporte

Si encuentras problemas con estos scripts:

1. 📊 Verificar logs del sistema
2. ⚙️ Revisar configuración de base de datos
3. 📚 Consultar documentación en `docs/`
4. 🐛 Abrir un issue en el repositorio

---

<div align="center">

**⚠️ Nota Importante**

Estos scripts están diseñados para **desarrollo y testing**. En producción, usar herramientas de migración más robustas como **Alembic**.

![Development](https://img.shields.io/badge/Environment-Development-yellow)
![Testing](https://img.shields.io/badge/Purpose-Testing-orange)

</div>
