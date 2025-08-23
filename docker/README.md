# 🐳 Docker Configuration for FastAPI Restaurant Backend

Esta carpeta contiene toda la configuración necesaria para ejecutar el sistema de restaurante usando Docker.

## 📋 Archivos Incluidos

### 🐳 Docker Compose
- `../docker-compose.yml` - Solo base de datos MySQL + Adminer
- `../docker-compose.full.yml` - Sistema completo (MySQL + FastAPI + Adminer)

### ⚙️ Configuración MySQL
- `mysql/conf/mysql.cnf` - Configuración personalizada de MySQL
- `mysql/init/01-init.sql` - Script de inicialización de la base de datos

### 🔧 Scripts de Utilidad
- `start-docker.sh` - Script de inicio para Linux/Mac
- `start-docker.bat` - Script de inicio para Windows
- `.env.docker` - Variables de entorno para Docker

## 🚀 Inicio Rápido

### 📋 Requisitos Previos
- Docker Desktop instalado
- Docker Compose disponible

### 🏃‍♂️ Ejecutar Solo Base de Datos

```bash
# Desde la raíz del proyecto
docker-compose up -d

# O usando el script
cd docker
./start-docker.sh  # Linux/Mac
start-docker.bat   # Windows
```

### 🚀 Ejecutar Sistema Completo

```bash
# Desde la raíz del proyecto
docker-compose -f docker-compose.full.yml up -d

# O usando el script y seleccionando opción 2
cd docker
./start-docker.sh  # Linux/Mac
start-docker.bat   # Windows
```

## 📡 Servicios Disponibles

Después de ejecutar Docker Compose:

| Servicio | URL | Descripción |
|----------|-----|-------------|
| 🗄️ MySQL | `localhost:3306` | Base de datos MySQL |
| 🌐 Adminer | `http://localhost:8080` | Gestión web de BD |
| 🚀 FastAPI | `http://localhost:8000` | API del restaurante |
| 📚 Swagger Docs | `http://localhost:8000/docs` | Documentación interactiva |

## 🔐 Credenciales por Defecto

### MySQL (Root)
- **Usuario**: `root`
- **Contraseña**: `restaurante_root_2024!`

### MySQL (Usuario App)
- **Usuario**: `restaurante_user`
- **Contraseña**: `restaurante_secure_pass_2024`
- **Base de datos**: `restaurante_db`

### Adminer
- **Sistema**: `MySQL`
- **Servidor**: `mysql-db`
- **Usuario**: `restaurante_user` o `root`
- **Contraseña**: Ver arriba
- **Base de datos**: `restaurante_db`

## ⚙️ Configuración Personalizada

### 🔧 Variables de Entorno

Edita `docker/.env.docker` para personalizar:

```env
DB_ROOT_PASSWORD=tu_password_root
DB_NAME=tu_base_datos
DB_USER=tu_usuario
DB_PASSWORD=tu_password
DB_PORT=3306
```

### 🗄️ Configuración MySQL

Edita `mysql/conf/mysql.cnf` para modificar:
- Configuración de caracteres
- Parámetros de rendimiento
- Configuración de logs
- Zona horaria

## 🔧 Comandos Útiles

### 📊 Gestión de Servicios
```bash
# Ver estado de contenedores
docker-compose ps

# Ver logs en tiempo real
docker-compose logs -f

# Ver logs de un servicio específico
docker-compose logs -f mysql-db

# Reiniciar servicios
docker-compose restart

# Detener servicios
docker-compose down

# Detener y eliminar volúmenes (⚠️ ELIMINA DATOS)
docker-compose down -v
```

### 🗄️ Gestión de Base de Datos
```bash
# Conectar a MySQL desde terminal
docker exec -it restaurante-mysql mysql -u root -p

# Backup de base de datos
docker exec restaurante-mysql mysqldump -u root -p restaurante_db > backup.sql

# Restaurar backup
docker exec -i restaurante-mysql mysql -u root -p restaurante_db < backup.sql

# Ver logs de MySQL
docker exec restaurante-mysql tail -f /var/log/mysql/error.log
```

### 🐛 Debugging
```bash
# Entrar al contenedor MySQL
docker exec -it restaurante-mysql bash

# Entrar al contenedor FastAPI
docker exec -it restaurante-api bash

# Ver información del contenedor
docker inspect restaurante-mysql

# Ver uso de recursos
docker stats
```

## 📁 Estructura de Volúmenes

```
docker/
├── mysql/
│   ├── conf/
│   │   └── mysql.cnf              # Configuración MySQL
│   └── init/
│       └── 01-init.sql            # Script de inicialización
├── .env.docker                    # Variables de entorno
├── start-docker.sh               # Script Linux/Mac
├── start-docker.bat              # Script Windows
└── README.md                     # Esta documentación

Volúmenes Docker:
├── mysql_data                    # Datos persistentes de MySQL
└── restaurante-network           # Red Docker interna
```

## 🚨 Consideraciones de Producción

### 🔒 Seguridad
- [ ] Cambiar todas las contraseñas por defecto
- [ ] Usar secretos de Docker para credenciales
- [ ] Configurar firewall para puertos expuestos
- [ ] Habilitar SSL/TLS para conexiones

### 📊 Rendimiento
- [ ] Ajustar parámetros de MySQL según carga esperada
- [ ] Configurar límites de recursos para contenedores
- [ ] Implementar backup automático
- [ ] Configurar monitoreo y alertas

### 🔄 Backup
```bash
# Script de backup automático
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
docker exec restaurante-mysql mysqldump -u root -p$DB_ROOT_PASSWORD restaurante_db > backup_$DATE.sql
```

## 🆘 Troubleshooting

### ❌ Problemas Comunes

1. **Puerto 3306 ocupado**:
   ```bash
   # Cambiar puerto en docker-compose.yml
   ports:
     - "3307:3306"  # Usar puerto 3307
   ```

2. **Contenedor no inicia**:
   ```bash
   # Ver logs detallados
   docker-compose logs mysql-db
   ```

3. **No se conecta a la BD**:
   ```bash
   # Verificar que esté healthy
   docker-compose ps
   # Esperar a que aparezca "(healthy)"
   ```

4. **Datos perdidos**:
   ```bash
   # Verificar volúmenes
   docker volume ls
   # Restaurar desde backup
   ```

### 📞 Soporte

Para problemas específicos:
1. Revisar logs: `docker-compose logs -f`
2. Verificar configuración: `docker-compose config`
3. Reiniciar servicios: `docker-compose restart`
4. Buscar en issues del repositorio GitHub
