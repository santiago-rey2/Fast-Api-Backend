"""
Script para probar el endpoint de carga CSV
"""
import requests
import json

def test_admin_endpoints():
    """Prueba los endpoints de administración"""
    base_url = "http://127.0.0.1:8000/api/v1/admin"
    
    print("🧪 Probando endpoints de administración...")
    
    # Test 1: Obtener categorías
    try:
        response = requests.get(f"{base_url}/categorias")
        print(f"✅ GET /categorias - Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   📊 Categorías encontradas: {len(data)}")
    except Exception as e:
        print(f"❌ Error en GET /categorias: {e}")
    
    # Test 2: Crear nueva categoría
    try:
        nueva_categoria = {"nombre": "Tapas Especiales"}
        response = requests.post(
            f"{base_url}/categorias",
            json=nueva_categoria
        )
        print(f"✅ POST /categorias - Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   🆕 Nueva categoría creada: {data['nombre']} (ID: {data['id']})")
    except Exception as e:
        print(f"❌ Error en POST /categorias: {e}")
    
    # Test 3: Obtener alérgenos
    try:
        response = requests.get(f"{base_url}/alergenos")
        print(f"✅ GET /alergenos - Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   📊 Alérgenos encontrados: {len(data)}")
    except Exception as e:
        print(f"❌ Error en GET /alergenos: {e}")

def test_csv_upload():
    """Prueba la carga de CSV"""
    base_url = "http://127.0.0.1:8000/api/v1/admin"
    
    print("\n📤 Probando carga de CSV...")
    
    # Preparar archivo CSV de prueba
    csv_content = """nombre
Cocina Creativa
Fusion Asiática
Mediterráneo
Cocina Molecular"""
    
    try:
        # Crear archivo temporal
        with open("test_categorias.csv", "w", encoding="utf-8") as f:
            f.write(csv_content)
        
        # Subir archivo
        with open("test_categorias.csv", "rb") as f:
            files = {"file": ("test_categorias.csv", f, "text/csv")}
            params = {"entity_type": "categorias"}
            response = requests.post(
                f"{base_url}/upload-csv",
                files=files,
                params=params
            )
        
        print(f"✅ POST /upload-csv - Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   📊 Total filas: {data['total_rows']}")
            print(f"   ✅ Creadas: {data['created_count']}")
            print(f"   ❌ Errores: {data['error_count']}")
            if data['errors']:
                for error in data['errors']:
                    print(f"      ⚠️  {error}")
        
        # Limpiar archivo temporal
        import os
        os.remove("test_categorias.csv")
        
    except Exception as e:
        print(f"❌ Error en carga CSV: {e}")

def test_platos_endpoints():
    """Prueba los endpoints de platos"""
    base_url = "http://127.0.0.1:8000/api/v1"
    
    print("\n🍽️ Probando endpoints de platos...")
    
    try:
        response = requests.get(f"{base_url}/platos/?limit=5")
        print(f"✅ GET /platos - Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   📊 Total platos: {data['total']}")
            print(f"   📋 Platos mostrados: {len(data['platos'])}")
            if data['platos']:
                primer_plato = data['platos'][0]
                print(f"   🍽️ Primer plato: {primer_plato['nombre']} - {primer_plato['precio']}€")
    except Exception as e:
        print(f"❌ Error en GET /platos: {e}")

if __name__ == "__main__":
    print("🚀 Iniciando pruebas de la API...")
    print("⏳ Asegúrate de que el servidor esté ejecutándose en http://127.0.0.1:8000")
    print()
    
    test_admin_endpoints()
    test_csv_upload()
    test_platos_endpoints()
    
    print("\n🎉 ¡Pruebas completadas!")
