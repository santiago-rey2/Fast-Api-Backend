# Scripts de Base de Datos

# Scripts - Examples

Esta carpeta contiene scripts de ejemplo para demostrar las capacidades del sistema.

## 📁 Archivos Disponibles

### 🕷️ `restaurant_scraper.py`
**Sistema completo de web scraping para cartas de restaurantes**

Extrae automáticamente información de menús desde URLs de restaurantes y los carga en el sistema.

**Características:**
- Detección inteligente de precios (€, EUR, euros)
- Clasificación automática por categorías
- Mapeo de alérgenos comunes
- Soporte para plataformas especializadas (WordPress, Wix, Squarespace)
- Carga directa a base de datos
- Exportación a JSON

**Ejemplo de uso:**
```python
from restaurant_scraper import RestaurantScraper

scraper = RestaurantScraper()
data = scraper.scrape_restaurant("https://restaurante-ejemplo.com/carta")

if data['total_items'] > 0:
    scraper.load_to_database(data)
    print(f"✅ {data['total_items']} elementos cargados")
```

### 🧪 `test_scraper.py`
**Herramienta de testing para el scraper**

Proporciona una interfaz para probar el scraper de manera interactiva o automática.

**Funcionalidades:**
- Prueba interactiva con URL personalizada
- Tests automáticos con URLs de ejemplo
- Vista previa de datos antes de cargar en BD
- Exportación automática a JSON

**Uso:**
```bash
cd scripts-examples
python test_scraper.py
```

### 🎯 `specialized_extractors.py`
**Extractores especializados para diferentes plataformas web**

Contiene métodos específicos para extraer datos de plataformas populares como WordPress, Wix, Squarespace, etc.

**Extractores disponibles:**
- WordPress (clases específicas de menús)
- Wix (estructura de componentes)
- Squarespace (layout de productos)
- Tablas HTML genéricas
- JSON-LD estructurado

## 🚀 Instrucciones de Uso

### 1. Instalación de Dependencias
```bash
pip install beautifulsoup4 requests lxml
```

### 2. Configuración de Base de Datos
Asegúrate de que la base de datos esté configurada:
```bash
cd scripts
python setup_complete_database.py
```

### 3. Prueba del Scraper
```bash
cd scripts-examples
python test_scraper.py
```

### 4. Uso Programático
```python
# Importar el scraper
from restaurant_scraper import RestaurantScraper

# Crear instancia
scraper = RestaurantScraper()

# Scrappear restaurante
data = scraper.scrape_restaurant("https://ejemplo.com/menu")

# Cargar en base de datos
success = scraper.load_to_database(data)

# O guardar como JSON
filepath = scraper.save_to_json(data)
```

## 📊 Formato de Datos Extraídos

El scraper devuelve datos en el siguiente formato:

```json
{
    "restaurante_info": {
        "url": "https://ejemplo.com",
        "titulo": "Restaurante Ejemplo"
    },
    "total_items": 25,
    "items": [
        {
            "nombre": "Paella Valenciana",
            "descripcion": "Arroz tradicional con mariscos",
            "precio": 18.50,
            "categoria": "Principales",
            "alergenos": ["gluten", "mariscos"]
        }
    ],
    "categorias": {
        "Entrantes": [...],
        "Principales": [...],
        "Postres": [...]
    },
    "extraction_date": "2024-01-15T10:30:00"
}
```

## 🎯 Casos de Uso

### Cargar Menú Completo
```python
scraper = RestaurantScraper()
data = scraper.scrape_restaurant("https://restaurante.com/carta")
scraper.load_to_database(data)
```

### Solo Obtener Datos (sin cargar)
```python
scraper = RestaurantScraper()
data = scraper.scrape_restaurant("https://restaurante.com/carta")
scraper.save_to_json(data, "menu_backup.json")
```

### Procesar Múltiples Restaurantes
```python
urls = [
    "https://restaurante1.com/menu",
    "https://restaurante2.com/carta",
    "https://restaurante3.com/platos"
]

scraper = RestaurantScraper()
for url in urls:
    try:
        data = scraper.scrape_restaurant(url)
        scraper.load_to_database(data)
        print(f"✅ {url} procesado")
    except Exception as e:
        print(f"❌ Error en {url}: {e}")
```

## 🔧 Personalización

### Añadir Nuevos Patrones de Precios
Edita `restaurant_scraper.py` y añade patrones al método `extract_price()`:

```python
price_patterns = [
    r'(\d+[.,]\d{2})\s*€',
    r'(\d+[.,]\d{2})\s*EUR',
    r'(\d+[.,]\d{2})\s*euros',
    # Añadir nuevo patrón aquí
    r'Precio:\s*(\d+[.,]\d{2})'
]
```

### Añadir Nuevas Categorías
Modifica el diccionario `categoria_keywords` en `detect_categoria()`:

```python
categoria_keywords = {
    'Entrantes': ['entrada', 'aperitivo', 'tapa'],
    'Principales': ['principal', 'segundo', 'plato fuerte'],
    'Postres': ['postre', 'dulce', 'helado'],
    # Nueva categoría
    'Bebidas': ['bebida', 'refresco', 'agua', 'vino']
}
```

## 📝 Notas Importantes

- **Respeto por robots.txt**: El scraper respeta las políticas de scraping
- **Rate Limiting**: Incluye delays entre solicitudes para no sobrecargar servidores
- **Error Handling**: Manejo robusto de errores con fallbacks
- **Logging**: Registro detallado de operaciones para debugging

## 🐛 Troubleshooting

### Error de Conexión
```
Error: Timeout o conexión rechazada
```
**Solución**: Verificar conectividad y que la URL sea accesible

### No se Encuentran Elementos
```
Warning: 0 elementos encontrados
```
**Solución**: La página puede usar JavaScript dinámico o tener una estructura no estándar

### Error de Base de Datos
```
Error: No se pudo cargar en BD
```
**Solución**: Verificar configuración de BD en `src/core/database.py`

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
