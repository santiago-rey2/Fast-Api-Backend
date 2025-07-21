
# 📦 Esquema de Base de Datos – Carta de Restaurante (FastAPI Backend)

Este modelo representa una base de datos relacional pensada para una API de gestión de una carta de restaurante común con FastAPI. Se incluyen dos entidades principales: **Platos** y **Vinos**.

---

## 🗂️ Esquema General (Resumen ERD)

```
[Plato] --- (N:1) ---> [CategoriaPlato]
   |
   |--< (N:M) >-- [PlatoAlergeno] -- (N:1) --> [Alergeno]

[Vino] --- (N:1) ---> [CategoriaVino]
   |
   |-- (N:1) --> [Bodega] (nullable)
   |-- (N:1) --> [DenominacionOrigen] (nullable)
   |-- (N:1) --> [Enologo] (nullable)
   |--< (N:M) >-- [VinoUva] -- (N:1) --> [Uva]
```

---

## 🍽️ Entidad: `plato`

| Campo        | Tipo        | Restricciones           |
|--------------|-------------|--------------------------|
| id           | INTEGER     | PK, AutoIncrement        |
| nombre       | TEXT        | NOT NULL                 |
| precio       | DECIMAL     | NOT NULL                 |
| descripcion  | TEXT        |                          |
| categoria_id | INTEGER     | FK → categoria_plato.id  |

### 📁 Tabla: `categoria_plato`

| Campo   | Tipo    | Restricciones |
|---------|---------|---------------|
| id      | INTEGER | PK            |
| nombre  | TEXT    | Único, NOT NULL (ej: 'Entrantes') |

### ⚠️ Tabla: `alergeno`

| Campo   | Tipo    | Restricciones |
|---------|---------|---------------|
| id      | INTEGER | PK            |
| nombre  | TEXT    | Único, NOT NULL (ej: 'Gluten') |

### 🔗 Tabla intermedia: `plato_alergeno`

| Campo       | Tipo    | Restricciones                      |
|-------------|---------|-----------------------------------|
| plato_id    | INTEGER | FK → plato.id, PK (compuesto)      |
| alergeno_id | INTEGER | FK → alergeno.id, PK (compuesto)   |

---

## 🍷 Entidad: `vino`

| Campo                  | Tipo    | Restricciones                         |
|------------------------|---------|--------------------------------------|
| id                     | INTEGER | PK                                   |
| nombre                 | TEXT    | NOT NULL                             |
| precio                 | DECIMAL | NOT NULL                             |
| categoria_id           | INTEGER | FK → categoria_vino.id               |
| bodega_id              | INTEGER | FK → bodega.id, nullable             |
| denominacion_origen_id | INTEGER | FK → denominacion_origen.id, nullable|
| enologo_id             | INTEGER | FK → enologo.id, nullable            |

### 🏷️ Tabla: `categoria_vino`

| Campo   | Tipo    | Restricciones |
|---------|---------|---------------|
| id      | INTEGER | PK            |
| nombre  | TEXT    | Único, NOT NULL (ej: 'Vino Tinto') |

### 🏭 Tabla: `bodega`

| Campo   | Tipo    | Restricciones |
|---------|---------|---------------|
| id      | INTEGER | PK            |
| nombre  | TEXT    | Único, nullable |

### 🌍 Tabla: `denominacion_origen`

| Campo   | Tipo    | Restricciones |
|---------|---------|---------------|
| id      | INTEGER | PK            |
| nombre  | TEXT    | Único, nullable |

### 👨‍🔬 Tabla: `enologo`

| Campo   | Tipo    | Restricciones |
|---------|---------|---------------|
| id      | INTEGER | PK            |
| nombre  | TEXT    | Único, nullable |

### 🍇 Tabla: `uva`

| Campo   | Tipo    | Restricciones |
|---------|---------|---------------|
| id      | INTEGER | PK            |
| nombre  | TEXT    | Único, NOT NULL |

### 🔗 Tabla intermedia: `vino_uva`

| Campo    | Tipo    | Restricciones                    |
|----------|---------|----------------------------------|
| vino_id  | INTEGER | FK → vino.id, PK (compuesto)     |
| uva_id   | INTEGER | FK → uva.id, PK (compuesto)      |

---

## ✅ Ventajas del Modelo

- **Flexible:** Ampliable a más categorías, tipos de uva, menús por temporada, etc.
- **Escalable:** Preparado para integración futura con reservas, menús, maridajes, etc.
- **Compatible con FastAPI:** Fácil mapeo con modelos de `SQLAlchemy` y `Pydantic`.

---
