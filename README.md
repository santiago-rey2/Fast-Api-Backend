# Fast API Backend

API de gestión para una carta de restaurante común, formada por dos entidades básicas: **Platos** y **Vinos**.

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

## 📝 Notas

Los campos de denominación, bodega, uva y enólogo son campos que admiten valores nulos.

