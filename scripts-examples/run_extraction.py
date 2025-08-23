"""
Script simplificado para ejecutar la extracción con precios corregidos
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.scripts.extract_restaurant_data import RestaurantDataExtractor

def main():
    print("🚀 Iniciando extracción de datos del restaurante...")
    print("🔧 Con función de precios actualizada")
    print()
    
    try:
        extractor = RestaurantDataExtractor()
        extractor.extract_and_save()
        print("\n🎉 ¡Extracción completada con éxito!")
    except Exception as e:
        print(f"❌ Error durante la extracción: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
