"""
Script para recopilar datos de la carta de Asador A Ferreira y guardarlos en la BD
"""
import sys
import os
import re
from decimal import Decimal
from typing import List, Dict, Optional
import requests
from bs4 import BeautifulSoup

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.database import SessionLocal
from src.entities.plato import Plato
from src.entities.categoria_plato import CategoriaPlato
from src.entities.alergeno import Alergeno
from sqlalchemy import select

# Mapeo de alérgenos por iconos de la web
ALERGENOS_MAP = {
    'gluten.svg': 'Gluten',
    'milk.svg': 'Lácteos', 
    'egg.svg': 'Huevos',
    'nuts.svg': 'Frutos secos',
    'fish.svg': 'Pescado',
    'shellfish.svg': 'Mariscos',
    'crustaceans.svg': 'Mariscos',
    'sulfites.svg': 'Sulfitos',
    'soy.svg': 'Soja',
    'celery.svg': 'Apio',
    'mustard.svg': 'Mostaza',
    'sesame.svg': 'Sésamo',
    'peanut.svg': 'Cacahuetes',
    'lupins.svg': 'Altramuces'
}

class RestaurantDataExtractor:
    def __init__(self):
        self.session = SessionLocal()
        self.categoria_cache = {}
        self.alergeno_cache = {}
        self._load_caches()
    
    def _load_caches(self):
        """Carga las categorías y alérgenos existentes en cache"""
        # Cargar categorías
        categorias = self.session.execute(select(CategoriaPlato)).scalars().all()
        for cat in categorias:
            self.categoria_cache[cat.nombre] = cat.id
        
        # Cargar alérgenos
        alergenos = self.session.execute(select(Alergeno)).scalars().all()
        for alerg in alergenos:
            self.alergeno_cache[alerg.nombre] = alerg.id
    
    def extract_price(self, price_text: str) -> Optional[Decimal]:
        """Extrae el precio de un texto"""
        if not price_text or 'S/Mercado' in price_text:
            return None
        
        # Buscar patrón de precio con símbolo €
        price_pattern = r'(\d+(?:[.,]\d{1,2})?)\s*€'
        match = re.search(price_pattern, price_text)
        
        if match:
            price_str = match.group(1).replace(',', '.')
            return Decimal(price_str)
        
        # Si no tiene €, intentar extraer número directo
        # Para datos hardcodeados que son solo números
        try:
            # Limpiar y convertir directamente
            clean_price = price_text.strip().replace(',', '.')
            # Verificar que es un número válido
            if re.match(r'^\d+(?:\.\d{1,2})?$', clean_price):
                return Decimal(clean_price)
        except (ValueError, Exception):
            pass
        
        return None
    
    def extract_allergens_from_icons(self, allergen_icons: List[str]) -> List[int]:
        """Extrae IDs de alérgenos basándose en los iconos"""
        allergen_ids = []
        
        for icon in allergen_icons:
            for icon_name, allergen_name in ALERGENOS_MAP.items():
                if icon_name in icon:
                    if allergen_name in self.alergeno_cache:
                        allergen_id = self.alergeno_cache[allergen_name]
                        if allergen_id not in allergen_ids:
                            allergen_ids.append(allergen_id)
        
        return allergen_ids if allergen_ids else [0]  # Sin alérgenos por defecto
    
    def get_categoria_id(self, categoria_name: str) -> int:
        """Obtiene el ID de categoría, creándola si no existe"""
        if not categoria_name:
            return 0  # Sin categoría
            
        # Normalizar nombre de categoría
        categoria_clean = categoria_name.strip().title()
        
        # Buscar en cache primero
        if categoria_clean in self.categoria_cache:
            return self.categoria_cache[categoria_clean]
            
        # Buscar en base de datos
        categoria = self.session.execute(
            select(CategoriaPlato).where(CategoriaPlato.nombre == categoria_clean)
        ).scalar_one_or_none()
        
        if categoria:
            self.categoria_cache[categoria_clean] = categoria.id
            return categoria.id
        else:
            # Crear nueva categoría
            nueva_categoria = CategoriaPlato(nombre=categoria_clean)
            self.session.add(nueva_categoria)
            self.session.commit()
            self.session.refresh(nueva_categoria)
            
            self.categoria_cache[categoria_clean] = nueva_categoria.id
            print(f"✅ Nueva categoría creada: {categoria_clean} (ID: {nueva_categoria.id})")
            return nueva_categoria.id
    
    def parse_restaurant_data(self) -> List[Dict]:
        """Parse manual de los datos extraídos de la web"""
        platos_data = [
            # SUGERENCIAS DEL DÍA - ENTRANTES
            {
                'nombre': 'Brioche de Carrillera',
                'precio': '14.00',
                'categoria': 'ENTRANTES',
                'descripcion': 'Brioche relleno de carrillera',
                'alergenos': ['gluten.svg', 'sulfites.svg', 'egg.svg']
            },
            
            # SUGERENCIAS DEL DÍA - PLATOS PRINCIPALES  
            {
                'nombre': 'Chuletón de Minhota',
                'precio': '69.00',  # Por kg
                'categoria': 'PLATOS PRINCIPALES',
                'descripcion': 'Chuletón de carne Minhota (precio por kg)',
                'alergenos': []
            },
            {
                'nombre': 'Chuletón de Old Special Beef',
                'precio': '85.00',  # Por kg
                'categoria': 'PLATOS PRINCIPALES', 
                'descripcion': 'Chuletón de Old Special Beef (precio por kg)',
                'alergenos': []
            },
            
            # SUGERENCIAS DEL DÍA - POSTRES
            {
                'nombre': 'Tarta Cremosa de Nocilla',
                'precio': '7.00',
                'categoria': 'POSTRES',
                'descripcion': 'Tarta cremosa con sabor a Nocilla',
                'alergenos': ['nuts.svg', 'milk.svg', 'soy.svg', 'gluten.svg']
            },
            {
                'nombre': 'Mouse de Limón',
                'precio': '6.50',
                'categoria': 'POSTRES',
                'descripcion': 'Mousse de limón casero',
                'alergenos': ['milk.svg', 'gluten.svg']
            },
            
            # ENTRANTES
            {
                'nombre': 'Chipirones a la plancha',
                'precio': '10.50',
                'categoria': 'ENTRANTES',
                'descripcion': 'Chipirones frescos a la plancha',
                'alergenos': ['shellfish.svg']
            },
            {
                'nombre': 'Chipirones encebollados',
                'precio': '10.80',
                'categoria': 'ENTRANTES',
                'descripcion': 'Chipirones con cebolla',
                'alergenos': ['shellfish.svg', 'sulfites.svg']
            },
            {
                'nombre': 'Pulpo A Feira',
                'precio': '18.00',
                'categoria': 'ENTRANTES',
                'descripcion': 'Pulpo gallego a feira',
                'alergenos': ['shellfish.svg']
            },
            {
                'nombre': 'Pulpo a la Brasa',
                'precio': '18.80',
                'categoria': 'ENTRANTES',
                'descripcion': 'Pulpo cocinado a la brasa',
                'alergenos': ['shellfish.svg']
            },
            {
                'nombre': 'Pimiento de Padrón',
                'precio': '5.50',
                'categoria': 'ENTRANTES',
                'descripcion': 'Pimientos de Padrón en temporada',
                'alergenos': []
            },
            {
                'nombre': 'Empanada Atún/Bacalao/Carne',
                'precio': '6.00',
                'categoria': 'ENTRANTES',
                'descripcion': 'Empanada con relleno de atún, bacalao o carne',
                'alergenos': ['gluten.svg', 'fish.svg', 'egg.svg', 'sulfites.svg']
            },
            {
                'nombre': 'Empanada Zamburiñas/Xoubas', 
                'precio': '9.80',
                'categoria': 'ENTRANTES',
                'descripcion': 'Empanada de zamburiñas o xoubas',
                'alergenos': ['gluten.svg', 'soy.svg', 'celery.svg', 'shellfish.svg', 'mustard.svg', 'milk.svg', 'sesame.svg']
            },
            {
                'nombre': 'Tabla Mixta A Ferreira',
                'precio': '18.00',
                'categoria': 'ENTRANTES',
                'descripcion': 'Tabla mixta de la casa',
                'alergenos': ['milk.svg', 'nuts.svg', 'egg.svg']
            },
            {
                'nombre': 'Cecina de Origen con Queso Trufado',
                'precio': '18.00',
                'categoria': 'ENTRANTES',
                'descripcion': 'Cecina con queso trufado',
                'alergenos': ['milk.svg']
            },
            {
                'nombre': 'Croquetas de Carne',
                'precio': '7.50',
                'categoria': 'ENTRANTES',
                'descripcion': 'Croquetas caseras de carne (12 unidades)',
                'alergenos': ['gluten.svg', 'milk.svg', 'egg.svg']
            },
            {
                'nombre': 'Croquetas de Marisco o Choco',
                'precio': '8.50',
                'categoria': 'ENTRANTES',
                'descripcion': 'Croquetas de marisco o choco (12 unidades)',
                'alergenos': ['gluten.svg', 'milk.svg', 'egg.svg', 'crustaceans.svg', 'fish.svg', 'shellfish.svg']
            },
            {
                'nombre': 'Croquetas Variadas',
                'precio': '14.00',
                'categoria': 'ENTRANTES',
                'descripcion': '6 Cr. Carne / 6 Cr. Choco / 6 Cr. Marisco',
                'alergenos': ['gluten.svg', 'milk.svg', 'egg.svg', 'crustaceans.svg', 'fish.svg', 'shellfish.svg']
            },
            {
                'nombre': 'Pan Bao de Cerdo o Marisco con Queso',
                'precio': '7.20',
                'categoria': 'ENTRANTES',
                'descripcion': 'Pan bao relleno (2 unidades)',
                'alergenos': ['gluten.svg', 'milk.svg', 'egg.svg', 'crustaceans.svg', 'fish.svg', 'shellfish.svg']
            },
            {
                'nombre': 'Pan Bao Negro de Calamar',
                'precio': '8.50',
                'categoria': 'ENTRANTES',
                'descripcion': 'Pan bao negro de calamar (2 unidades)',
                'alergenos': ['gluten.svg', 'milk.svg', 'egg.svg', 'crustaceans.svg', 'fish.svg', 'shellfish.svg', 'nuts.svg', 'celery.svg', 'mustard.svg', 'sesame.svg']
            },
            
            # ENSALADAS
            {
                'nombre': 'Ensalada Grande',
                'precio': '6.50',
                'categoria': 'ENSALADAS',
                'descripcion': 'Tomate / Lechuga / Cebolla',
                'alergenos': []
            },
            {
                'nombre': 'Ensalada Pequeña',
                'precio': '5.50',
                'categoria': 'ENSALADAS', 
                'descripcion': 'Tomate / Lechuga / Cebolla',
                'alergenos': []
            },
            {
                'nombre': 'Ensalada Mixta Grande',
                'precio': '9.00',
                'categoria': 'ENSALADAS',
                'descripcion': 'Tomate / Lechuga / Cebolla / Espárragos / Remolacha / Zanahoria / Huevo / Atún',
                'alergenos': ['egg.svg', 'fish.svg']
            },
            {
                'nombre': 'Ensalada Mixta Pequeña',
                'precio': '7.00',
                'categoria': 'ENSALADAS',
                'descripcion': 'Tomate / Lechuga / Cebolla / Espárragos / Remolacha / Zanahoria / Huevo / Atún',
                'alergenos': ['egg.svg', 'fish.svg']
            },
            {
                'nombre': 'Ensalada A Ferreira',
                'precio': '8.50',
                'categoria': 'ENSALADAS',
                'descripcion': 'Variado ensalada / Nuez / Soja / Naranja / Langostino / Tomate Cherry',
                'alergenos': ['nuts.svg', 'soy.svg', 'crustaceans.svg']
            },
            {
                'nombre': 'Ensalada templada de Vieira y Langostino',
                'precio': '10.00',
                'categoria': 'ENSALADAS',
                'descripcion': 'Variado ensalada / Vieira / Langostino / Salsa De miel y Vinagre',
                'alergenos': ['gluten.svg', 'nuts.svg', 'shellfish.svg', 'crustaceans.svg']
            },
            {
                'nombre': 'Ensalada de tomate y queso burrata',
                'precio': '9.30',
                'categoria': 'ENSALADAS',
                'descripcion': 'Tomate / Anchoa / Queso de Burrata / Albahaca / Pistacho',
                'alergenos': ['nuts.svg', 'milk.svg', 'fish.svg']
            },
            {
                'nombre': 'Ensalada de Tomate Confitado y Burrata Ahumada',
                'precio': '10.00',
                'categoria': 'ENSALADAS',
                'descripcion': 'Tomate confitado con burrata ahumada',
                'alergenos': ['nuts.svg', 'milk.svg']
            },
            
            # MARISCOS
            {
                'nombre': 'Gamba Roja a la Plancha',
                'precio': '16.00',
                'categoria': 'MARISCOS',
                'descripcion': 'Gambas rojas frescas a la plancha',
                'alergenos': ['crustaceans.svg']
            },
            {
                'nombre': 'Langostinos a la plancha',
                'precio': '12.00',
                'categoria': 'MARISCOS',
                'descripcion': 'Langostinos frescos a la plancha',
                'alergenos': ['crustaceans.svg']
            },
            {
                'nombre': 'Zamburiñas a la plancha',
                'precio': '15.00',
                'categoria': 'MARISCOS',
                'descripcion': 'Zamburiñas gallegas a la plancha',
                'alergenos': ['shellfish.svg']
            },
            {
                'nombre': 'Langostinos Crujientes',
                'precio': '12.00',
                'categoria': 'MARISCOS',
                'descripcion': 'Langostinos con rebozado crujiente',
                'alergenos': ['gluten.svg', 'crustaceans.svg']
            },
            {
                'nombre': 'Vieiras del Mar a la Tierra',
                'precio': '14.00',
                'categoria': 'MARISCOS',
                'descripcion': 'Vieira / Pure de Patata / Cebolla Caramelizada / Jamón',
                'alergenos': ['milk.svg', 'shellfish.svg']
            },
            
            # CARNES (selección representativa)
            {
                'nombre': 'Churrasco de Cerdo',
                'precio': '12.00',
                'categoria': 'CARNES',
                'descripcion': 'Churrasco de cerdo a la parrilla',
                'alergenos': ['sulfites.svg']
            },
            {
                'nombre': 'Churrasco de Ternera',
                'precio': '12.80',
                'categoria': 'CARNES',
                'descripcion': 'Churrasco de ternera a la parrilla',
                'alergenos': []
            },
            {
                'nombre': 'Secreto Ibérico',
                'precio': '16.00',
                'categoria': 'CARNES',
                'descripcion': 'Secreto ibérico a la parrilla',
                'alergenos': []
            },
            {
                'nombre': 'Chuletón de Vaca Gallega',
                'precio': '54.00',
                'categoria': 'CARNES',
                'descripcion': 'Chuletón de vaca gallega - Maduración de 60 días (precio por kg)',
                'alergenos': []
            },
            {
                'nombre': 'Entrecot de Wagyu',
                'precio': '105.00',
                'categoria': 'CARNES',
                'descripcion': 'Entrecot de Wagyu - Pieza de 300gr',
                'alergenos': []
            },
            
            # PESCADOS
            {
                'nombre': 'Bacalao a la plancha',
                'precio': '17.50',
                'categoria': 'PESCADOS',
                'descripcion': 'Bacalao fresco a la plancha',
                'alergenos': ['fish.svg']
            },
            {
                'nombre': 'Bacalao a la gallega',
                'precio': '17.50',
                'categoria': 'PESCADOS',
                'descripcion': 'Bacalao preparado al estilo gallego',
                'alergenos': ['fish.svg']
            },
            {
                'nombre': 'Brocheta de Rape con Langostino',
                'precio': '18.50',
                'categoria': 'PESCADOS',
                'descripcion': 'Brocheta de rape y langostinos',
                'alergenos': ['fish.svg', 'crustaceans.svg']
            },
            
            # ARROCES
            {
                'nombre': 'Arroz a Banda',
                'precio': '40.00',
                'categoria': 'ARROCES',
                'descripcion': 'Arroz a banda para 2 personas - Calamar / Rape / Gamba',
                'alergenos': ['shellfish.svg', 'crustaceans.svg', 'fish.svg']
            },
            {
                'nombre': 'Arroz de Vieiras y Pulpo',
                'precio': '42.00',
                'categoria': 'ARROCES',
                'descripcion': 'Arroz de vieiras y pulpo para 2 personas',
                'alergenos': ['shellfish.svg', 'crustaceans.svg', 'fish.svg']
            },
            {
                'nombre': 'Arroz de Choco en su Tinta',
                'precio': '42.00',
                'categoria': 'ARROCES',
                'descripcion': 'Arroz de choco en su tinta para 2 personas',
                'alergenos': ['shellfish.svg', 'crustaceans.svg', 'fish.svg']
            },
            {
                'nombre': 'Arroz de Carabinero',
                'precio': '48.00',
                'categoria': 'ARROCES',
                'descripcion': 'Arroz de carabinero para 2 personas',
                'alergenos': ['shellfish.svg', 'crustaceans.svg', 'fish.svg']
            },
            
            # POSTRES CASEROS
            {
                'nombre': 'Tiramisú',
                'precio': '6.00',
                'categoria': 'POSTRES CASEROS',
                'descripcion': 'Tiramisú casero',
                'alergenos': ['gluten.svg', 'nuts.svg', 'milk.svg', 'soy.svg', 'egg.svg']
            },
            {
                'nombre': 'Flan',
                'precio': '5.00',
                'categoria': 'POSTRES CASEROS',
                'descripcion': 'Flan casero',
                'alergenos': ['milk.svg', 'egg.svg']
            },
            {
                'nombre': 'Flan de queso',
                'precio': '5.50',
                'categoria': 'POSTRES CASEROS',
                'descripcion': 'Flan de queso casero',
                'alergenos': ['milk.svg', 'egg.svg']
            },
            {
                'nombre': 'Tarta de la Abuela',
                'precio': '6.00',
                'categoria': 'POSTRES CASEROS',
                'descripcion': 'Tarta tradicional de la abuela',
                'alergenos': ['gluten.svg', 'nuts.svg', 'milk.svg', 'soy.svg']
            },
            {
                'nombre': 'Tarta de Tres Chocolates',
                'precio': '6.00',
                'categoria': 'POSTRES CASEROS',
                'descripcion': 'Tarta de tres chocolates',
                'alergenos': ['gluten.svg', 'nuts.svg', 'milk.svg', 'soy.svg']
            },
            {
                'nombre': 'Tarta de Queso Cremosa y Helado',
                'precio': '7.00',
                'categoria': 'POSTRES CASEROS',
                'descripcion': 'Tarta de queso cremosa con helado',
                'alergenos': ['gluten.svg', 'nuts.svg', 'milk.svg', 'soy.svg']
            },
            {
                'nombre': 'Arroz con leche',
                'precio': '5.50',
                'categoria': 'POSTRES CASEROS',
                'descripcion': 'Arroz con leche casero',
                'alergenos': ['milk.svg']
            },
            {
                'nombre': 'Bannoffee',
                'precio': '6.00',
                'categoria': 'POSTRES CASEROS',
                'descripcion': 'Tarta Bannoffee',
                'alergenos': ['gluten.svg', 'milk.svg', 'nuts.svg']
            },
            {
                'nombre': 'Tarta de piña fría',
                'precio': '6.00',
                'categoria': 'POSTRES CASEROS',
                'descripcion': 'Tarta fría de piña',
                'alergenos': ['gluten.svg', 'milk.svg']
            },
            {
                'nombre': 'Tarta de Queso Fría',
                'precio': '6.00',
                'categoria': 'POSTRES CASEROS',
                'descripcion': 'Tarta de queso fría',
                'alergenos': ['gluten.svg', 'nuts.svg', 'milk.svg', 'soy.svg']
            },
            {
                'nombre': 'Tarta de Queso con Membrillo',
                'precio': '6.00',
                'categoria': 'POSTRES CASEROS',
                'descripcion': 'Tarta de queso con membrillo',
                'alergenos': ['gluten.svg', 'nuts.svg', 'milk.svg', 'soy.svg']
            },
            {
                'nombre': 'Tarta de Queso A Ferreira',
                'precio': '7.00',
                'categoria': 'POSTRES CASEROS',
                'descripcion': 'Tarta de Queso al Horno sobre Brownie',
                'alergenos': ['gluten.svg', 'nuts.svg', 'milk.svg', 'soy.svg', 'egg.svg']
            }
        ]
        
        return platos_data
    
    def save_to_database(self, platos_data: List[Dict]):
        """Guarda los platos en la base de datos"""
        saved_count = 0
        error_count = 0
        
        for plato_data in platos_data:
            try:
                # Verificar si el plato ya existe
                existing = self.session.execute(
                    select(Plato).where(Plato.nombre == plato_data['nombre'])
                ).scalar_one_or_none()
                
                if existing:
                    print(f"⚠️  Plato '{plato_data['nombre']}' ya existe, saltando...")
                    continue
                
                # Extraer precio
                precio = self.extract_price(plato_data['precio'])
                if precio is None:
                    precio = Decimal('0.00')  # Precio por defecto para "S/Mercado"
                
                # Obtener categoría
                categoria_id = self.get_categoria_id(plato_data['categoria'])
                
                # Obtener alérgenos
                alergenos_ids = self.extract_allergens_from_icons(plato_data.get('alergenos', []))
                
                # Crear el plato
                nuevo_plato = Plato(
                    nombre=plato_data['nombre'],
                    precio=precio,
                    descripcion=plato_data.get('descripcion', ''),
                    categoria_id=categoria_id
                )
                
                self.session.add(nuevo_plato)
                self.session.flush()  # Para obtener el ID
                
                # Agregar alérgenos
                if alergenos_ids:
                    alergenos = self.session.execute(
                        select(Alergeno).where(Alergeno.id.in_(alergenos_ids))
                    ).scalars().all()
                    nuevo_plato.alergenos = list(alergenos)
                
                self.session.commit()
                saved_count += 1
                print(f"✅ Guardado: {plato_data['nombre']} - {precio}€")
                
            except Exception as e:
                self.session.rollback()
                error_count += 1
                print(f"❌ Error guardando '{plato_data['nombre']}': {e}")
        
        print(f"\n📊 Resumen:")
        print(f"✅ Platos guardados: {saved_count}")
        print(f"❌ Errores: {error_count}")
    
    def run(self):
        """Ejecuta el proceso completo"""
        try:
            print("🚀 Iniciando extracción de datos de Asador A Ferreira...")
            
            # Obtener datos parseados manualmente
            platos_data = self.parse_restaurant_data()
            print(f"📋 Extraídos {len(platos_data)} platos de la carta")
            
            # Guardar en base de datos
            self.save_to_database(platos_data)
            
            print("🎉 ¡Proceso completado!")
            
        except Exception as e:
            print(f"❌ Error general: {e}")
        finally:
            self.session.close()

if __name__ == "__main__":
    extractor = RestaurantDataExtractor()
    extractor.run()
