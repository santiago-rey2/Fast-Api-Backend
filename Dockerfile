
# Imagen base oficial de Python
FROM python:3.13

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /code

# Copiamos el archivo de dependencias
COPY requirements.txt /code/requirements.txt

# Instalamos dependencias
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copiamos todo el contenido del backend (incluyendo src/, docs/, etc.)
COPY . /code


CMD ["fastapi", "run", "src/main.py", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]