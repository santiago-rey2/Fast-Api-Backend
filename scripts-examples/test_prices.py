"""
Script para probar la extracción de precios
"""
import sys
import os
import re
from decimal import Decimal
from typing import Optional

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def extract_price(price_text: str) -> Optional[Decimal]:
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

# Casos de prueba
test_cases = [
    "14.00",
    "69.00",
    "10.50", 
    "6.50",
    "15.90€",
    "22,50€",
    "S/Mercado",
    "",
    "12€",
    "8,75€"
]

print("🧪 Probando extracción de precios...")
print()

for case in test_cases:
    result = extract_price(case)
    status = "✅" if result is not None else "❌"
    print(f"{status} '{case}' -> {result}")

print()
print("🎯 Los precios deberían extraerse correctamente ahora")
