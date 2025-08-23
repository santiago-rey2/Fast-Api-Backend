"""
Script para actualizar los precios de los platos existentes en la base de datos
"""
import sys
import os
from decimal import Decimal

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database import SessionLocal
from src.entities.plato import Plato
from sqlalchemy import select

# Precios actualizados para los platos existentes
PRECIOS_ACTUALIZADOS = {
    'Brioche de Carrillera': '14.00',
    'Chuletón de Minhota': '69.00',
    'Chuletón de Old Special Beef': '85.00',
    'Tarta Cremosa de Nocilla': '7.00',
    'Mouse de Limón': '6.50',
    'Chipirones a la plancha': '10.50',
    'Empanada Zamburiñas/Xoubas': '8.50',
    'Tabla Mixta A Ferreira': '24.90',
    'Cecina de Origen con Queso Trufado': '16.50',
    'Croquetas de Carne': '12.00',
    'Croquetas de Marisco o Choco': '14.00',
    'Croquetas Variadas': '13.00',
    'Pan Bao de Cerdo o Marisco con Queso': '15.90',
    'Pan Bao Negro de Calamar': '16.50',
    'Ensalada Grande': '8.50',
    'Ensalada Pequeña': '6.00',
    'Ensalada Mixta Grande': '12.00',
    'Ensalada Mixta Pequeña': '9.50',
    'Ensalada A Ferreira': '16.90',
    'Ensalada templada de Vieira y Langostino': '19.50',
    'Ensalada de tomate y queso burrata': '14.90',
    'Ensalada de Tomate Confitado y Burrata Ahumada': '16.50',
    'Gamba Roja a la Plancha': '32.00',
    'Langostinos a la plancha': '18.50',
    'Zamburiñas a la plancha': '16.90',
    'Langostinos Crujientes': '19.90',
    'Vieiras del Mar a la Tierra': '22.50',
    'Churrasco de Cerdo': '18.50',
    'Churrasco de Ternera': '24.90',
    'Secreto Ibérico': '19.90',
    'Chuletón de Vaca Gallega': '75.00',
    'Entrecot de Wagyu': '45.00',
    'Bacalao a la plancha': '22.50',
    'Bacalao a la gallega': '24.90',
    'Brocheta de Rape con Langostino': '21.50',
    'Arroz a Banda': '32.00',
    'Arroz de Vieiras y Pulpo': '34.50',
    'Arroz de Choco en su Tinta': '29.90',
    'Arroz de Carabinero': '42.00',
    'Tiramisú': '6.50',
    'Flan': '4.50',
    'Flan de queso': '5.50',
    'Tarta de la Abuela': '6.90',
    'Tarta de Tres Chocolates': '7.50',
    'Tarta de Queso Cremosa y Helado': '8.90',
    'Arroz con leche': '5.50',
    'Bannoffee': '7.90',
    'Tarta de piña fría': '6.50',
    'Tarta de Queso Fría': '7.90',
    'Tarta de Queso con Membrillo': '8.50',
    'Tarta de Queso A Ferreira': '9.90'
}

def actualizar_precios():
    """Actualiza los precios de todos los platos en la base de datos"""
    session = SessionLocal()
    
    try:
        print("🔄 Actualizando precios de platos...")
        updated_count = 0
        not_found_count = 0
        
        for nombre_plato, precio_str in PRECIOS_ACTUALIZADOS.items():
            # Buscar el plato
            plato = session.execute(
                select(Plato).where(Plato.nombre == nombre_plato)
            ).scalar_one_or_none()
            
            if plato:
                # Convertir precio
                nuevo_precio = Decimal(precio_str)
                plato.precio = nuevo_precio
                updated_count += 1
                print(f"✅ {nombre_plato}: {nuevo_precio}€")
            else:
                not_found_count += 1
                print(f"❌ No encontrado: {nombre_plato}")
        
        # Confirmar cambios
        session.commit()
        
        print(f"\n📊 Resumen:")
        print(f"✅ Platos actualizados: {updated_count}")
        print(f"❌ Platos no encontrados: {not_found_count}")
        print(f"💰 Total de platos con precios: {updated_count}")
        
    except Exception as e:
        session.rollback()
        print(f"❌ Error actualizando precios: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    actualizar_precios()
    print("\n🎉 ¡Actualización de precios completada!")
