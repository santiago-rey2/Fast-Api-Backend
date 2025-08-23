-- Script de inicialización para FastAPI Restaurant Backend
-- Este script se ejecuta automáticamente cuando se crea el contenedor

-- Configurar el modo SQL para permitir ID 0
SET SESSION sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

-- Usar la base de datos restaurante_db
USE restaurante_db;

-- Configurar charset
ALTER DATABASE restaurante_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Crear usuario adicional para la aplicación (si no existe)
CREATE USER IF NOT EXISTS 'app_user'@'%' IDENTIFIED BY 'app_password_secure';
GRANT ALL PRIVILEGES ON restaurante_db.* TO 'app_user'@'%';

-- Crear índices adicionales para optimización (se aplicarán cuando existan las tablas)
-- Estas consultas fallarán inicialmente pero se aplicarán después cuando FastAPI cree las tablas

-- Configurar variables de sesión por defecto
SET GLOBAL sql_mode = 'NO_AUTO_VALUE_ON_ZERO,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';

-- Mensaje de confirmación
SELECT 'Base de datos inicializada correctamente para FastAPI Restaurant Backend' AS status;
