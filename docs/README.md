# 📚 Documentación FastAPI Restaurant Backend

<div align="center">

![Documentation](https://img.shields.io/badge/Documentation-Complete-brightgreen?style=for-the-badge&logo=gitbook)
![FastAPI](https://img.shields.io/badge/FastAPI-Framework-009688?style=for-the-badge&logo=fastapi)
![MySQL](https://img.shields.io/badge/MySQL-Database-blue?style=for-the-badge&logo=mysql)

</div>

Bienvenido a la **documentación completa** del sistema de gestión para restaurantes. Esta documentación está organizada por temas para facilitar la navegación.

## 📖 Índice de Documentación

### 🏗️ Arquitectura y Diseño
- **[Esquema de Base de Datos](esquema_restaurante.md)** - Documentación técnica completa del modelo de datos
- **[Modelo Visual](Modelo_Datos.svg)** - Diagrama de relaciones entre entidades
- **[Archivo DrawIO](Modelo_Datos.drawio)** - Diagrama editable del modelo

### 🛡️ Administración del Sistema
- **[Guía del Panel de Administración](admin-guide.md)** - Manual completo del panel admin con todos los endpoints

### 📋 Documentación Técnica
- **[Guía Detallada](guia-detallada.md)** - Documentación técnica completa del desarrollo

## 🚀 Enlaces Rápidos

### Para Desarrolladores
- [README Principal](../README.md) - Información de instalación y configuración
- [Guía del Panel Admin](admin-guide.md) - Para gestión de datos
- [Esquema de BD](esquema_restaurante.md) - Para desarrollo de características

### Para Administradores del Sistema
- [Panel de Administración](admin-guide.md) - Gestión completa del sistema
- [Scripts de Ejemplo](../scripts-examples/) - Herramientas y datos de prueba

## 📁 Estructura de la Documentación

```
docs/
├── README.md                   # Este índice
├── admin-guide.md             # Guía del panel de administración
├── esquema_restaurante.md     # Esquema de base de datos
├── guia-detallada.md         # Guía técnica detallada
├── Modelo_Datos.svg          # Diagrama visual del modelo
└── Modelo_Datos.drawio       # Diagrama editable
```

## 🔧 Herramientas y Recursos

### Scripts de Gestión de Base de Datos
Ubicados en `../scripts-examples/`:
- `setup_complete_database.py` - Configuración completa de la base de datos
- `clear_database.py` - Limpieza y reseteo de la base de datos
- `load_sample_data.py` - Carga de datos de ejemplo

### Scripts de Utilidad de Base de Datos
Ubicados en `../src/scripts/`:
- `create_db.py` - Creación de base de datos
- `seed.py` - Datos iniciales y semilla

### Datos de Ejemplo
- `example_categorias.csv` - Categorías de ejemplo
- `example_alergenos.csv` - Alérgenos de ejemplo
- `example_bodegas.csv` - Bodegas de ejemplo

## 🎯 Características del Sistema

### Core del Backend
- **FastAPI**: Framework moderno y rápido para APIs
- **MySQL**: Base de datos relacional robusta
- **JWT Authentication**: Sistema de autenticación seguro
- **Soft Delete**: Eliminación lógica con posibilidad de restauración
- **CRUD Completo**: Operaciones completas para todas las entidades

### Panel de Administración
- **Gestión de Platos**: Crear, editar, eliminar y restaurar platos
- **Gestión de Vinos**: Control completo de inventario de vinos
- **Gestión de Categorías**: Organización de platos y vinos
- **Gestión de Alérgenos**: Control de restricciones alimentarias
- **Carga Masiva CSV**: Importación de datos desde archivos CSV

### Seguridad y Auditoría
- **Campos de auditoría**: Seguimiento de creación, modificación y eliminación
- **Autenticación JWT**: Tokens seguros para acceso administrativo
- **CORS configurado**: Soporte para aplicaciones frontend
- **Logs detallados**: Registro de operaciones del sistema

## 📞 Contacto y Soporte

Si tienes preguntas sobre la documentación o necesitas ayuda adicional:

1. **Issues de GitHub**: Abre un issue en el repositorio
2. **Documentación técnica**: Consulta los archivos de documentación específicos
3. **Ejemplos prácticos**: Revisa los scripts de ejemplo para casos de uso

---

**Nota**: Esta documentación se actualiza regularmente. Asegúrate de consultar la versión más reciente en el repositorio oficial.
