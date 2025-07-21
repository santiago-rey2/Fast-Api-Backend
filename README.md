# Fast API Backend

API de gestión para - Vinos Dulces

## 🚀 Instalación y Despliegue

### 📋 Requisitos Previosarta```

## 📝 Notas

Los campos de denominación, bodega, uva y enólogo son campos que admiten valores nulos.estaurante común, formada por dos entidades básicas: **Platos** y **Vinos**.

## 📋 Entidades

### 🍽️ Platos

Para los platos almacenaremos:

- **Nombre**
- **Precio**
- **Descripción**
- **Alérgenos**
- **Categoría**

#### Categorías de Platos

Las categorías dependerán de cada implementación específica de las mismas, partiendo de base de:

- Entrantes
- Platos principales
- Postres

### 🍷 Vinos

En cuanto a los vinos almacenaremos:

- **Nombre**
- **Precio**
- **Bodega** *(admite nulos)*
- **Denominación de origen** *(admite nulos)*
- **Tipos de uva** *(admite nulos)*
- **Enólogo** *(admite nulos)*
- **Categorías**

#### Categorías de Vinos

Las categorías de vinos serán adaptables para cada implementación, pero por defecto implementaremos las siguientes:

- Vinos Blancos
- Vinos Tintos
- Vinos Dulces

## � Instalación y Despliegue

### 📋 Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### 🔧 Instalación del Entorno

1. **Clonar el repositorio**:

   ```bash
   git clone https://github.com/santiago-rey2/Fast-Api-Backend.git
   cd Fast-Api-Backend
   ```

2. **Crear un entorno virtual** (recomendado):

   ```bash
   python -m venv venv
   ```

3. **Activar el entorno virtual**:

   - En Windows:

     ```bash
     venv\Scripts\activate
     ```

   - En macOS/Linux:

     ```bash
     source venv/bin/activate
     ```

4. **Instalar las dependencias**:

   ```bash
   pip install -r requirements.txt
   ```

### 🏃‍♂️ Ejecutar el Servidor

1. **Modo desarrollo**:

   ```bash
   cd src
   fastapi dev main.py
   ```

2. **Modo producción**:

   ```bash
   cd src
   fastapi run main.py
   ```

### 🌐 Acceso a la API

Una vez ejecutado el servidor, podrás acceder a:

- **API**: [http://localhost:8000](http://localhost:8000)
- **Documentación interactiva (Swagger)**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Documentación alternativa (ReDoc)**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### 📦 Estructura del Proyecto

```text
Fast-Api-Backend/
├── src/
│   ├── main.py          # Punto de entrada de la aplicación
│   └── __pycache__/     # Cache de Python
├── requirements.txt     # Dependencias del proyecto
└── README.md           # Documentación del proyecto
```

## �📝 Notas

Los campos de denominación, bodega, uva y enólogo son campos que admiten valores nulos.
