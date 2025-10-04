#!/usr/bin/env python3
"""
Script para cargar datos desde archivos JSON en la base de datos.

Este script permite cargar datos estructurados desde archivos JSON,
útil para migrar datos o cargar datasets específicos.

Uso:
    python scripts-examples/load_from_json.py data/sample_data.json
    
O desde código:
    from scripts_examples.load_from_json import load_data_from_json
    load_data_from_json("data/sample_data.json")
"""
import sys
import json
from pathlib import Path
from decimal import Decimal
from datetime import datetime
from typing import Dict, List, Any, Optional
import bcrypt  # Añadir esta importación

# Agregar el directorio raíz al path para importar módulos
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from src.core.config import settings
    from src.entities.plato import Plato
    from src.entities.vino import Vino
    from src.entities.categoria_plato import CategoriaPlato
    from src.entities.categoria_vino import CategoriaVino
    from src.entities.alergeno import Alergeno
    from src.entities.bodega import Bodega
    from src.entities.denominacion_origen import DenominacionOrigen
    from src.entities.enologo import Enologo
    from src.entities.uva import Uva
    from src.entities.user import User
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    print("💡 Asegúrate de:")
    print("   1. Estar en el directorio raíz del proyecto")
    print("   2. Tener instaladas las dependencias: pip install -r requirements.txt")
    print("   3. Tener configurada la base de datos en src/core/config.py")
    sys.exit(1)

def create_session():
    """Crea una sesión de base de datos"""
    engine = create_engine(settings.sync_dsn, echo=False)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    return SessionLocal()

def load_categorias_platos(db, data: List[Dict[str, Any]]) -> Dict[str, CategoriaPlato]:
    """Carga categorías de platos"""
    print("📂 Cargando categorías de platos...")
    categorias = {}
    
    for categoria_data in data:
        existing = db.query(CategoriaPlato).filter_by(nombre=categoria_data["nombre"]).first()
        if not existing:
            categoria = CategoriaPlato(
                nombre=categoria_data["nombre"]
            )
            db.add(categoria)
            db.flush()  # Para obtener el ID
            categorias[categoria.nombre] = categoria
        else:
            categorias[existing.nombre] = existing
    
    db.commit()
    print(f"✅ {len(categorias)} categorías de platos cargadas")
    return categorias

def load_categorias_vinos(db, data: List[Dict[str, Any]]) -> Dict[str, CategoriaVino]:
    """Carga categorías de vinos"""
    print("🍷 Cargando categorías de vinos...")
    categorias = {}
    
    for categoria_data in data:
        existing = db.query(CategoriaVino).filter_by(nombre=categoria_data["nombre"]).first()
        if not existing:
            categoria = CategoriaVino(
                nombre=categoria_data["nombre"]
            )
            db.add(categoria)
            db.flush()
            categorias[categoria.nombre] = categoria
        else:
            categorias[existing.nombre] = existing
    
    db.commit()
    print(f"✅ {len(categorias)} categorías de vinos cargadas")
    return categorias

def load_alergenos(db, data: List[Dict[str, Any]]) -> Dict[str, Alergeno]:
    """Carga alérgenos"""
    print("⚠️ Cargando alérgenos...")
    alergenos = {}
    
    for alergeno_data in data:
        existing = db.query(Alergeno).filter_by(nombre=alergeno_data["nombre"]).first()
        if not existing:
            alergeno = Alergeno(
                nombre=alergeno_data["nombre"]
            )
            db.add(alergeno)
            db.flush()
            alergenos[alergeno.nombre] = alergeno
        else:
            alergenos[existing.nombre] = existing
    
    db.commit()
    print(f"✅ {len(alergenos)} alérgenos cargados")
    return alergenos

def load_bodegas(db, data: List[Dict[str, Any]]) -> Dict[str, Bodega]:
    """Carga bodegas"""
    print("🏭 Cargando bodegas...")
    bodegas = {}
    
    for bodega_data in data:
        existing = db.query(Bodega).filter_by(nombre=bodega_data["nombre"]).first()
        if not existing:
            # Solo usar campos que existen en la entidad Bodega
            bodega_kwargs = {
                "nombre": bodega_data["nombre"]
            }
            
            # Agregar campos opcionales solo si existen en la entidad
            if "region" in bodega_data:
                bodega_kwargs["region"] = bodega_data["region"]
            
            # Remover descripcion ya que no existe en Bodega
            bodega = Bodega(**bodega_kwargs)
            db.add(bodega)
            db.flush()
            bodegas[bodega.nombre] = bodega
        else:
            bodegas[existing.nombre] = existing
    
    db.commit()
    print(f"✅ {len(bodegas)} bodegas cargadas")
    return bodegas

def load_denominaciones(db, data: List[Dict[str, Any]]) -> Dict[str, DenominacionOrigen]:
    """Carga denominaciones de origen"""
    print("🎯 Cargando denominaciones de origen...")
    denominaciones = {}
    
    for denominacion_data in data:
        existing = db.query(DenominacionOrigen).filter_by(nombre=denominacion_data["nombre"]).first()
        if not existing:
            # Solo usar campos que existen en la entidad DenominacionOrigen
            denominacion_kwargs = {
                "nombre": denominacion_data["nombre"]
            }
            
            # Agregar campos opcionales solo si existen en la entidad
            if "region" in denominacion_data:
                denominacion_kwargs["region"] = denominacion_data["region"]
            
            # Remover descripcion si no existe en DenominacionOrigen
            denominacion = DenominacionOrigen(**denominacion_kwargs)
            db.add(denominacion)
            db.flush()
            denominaciones[denominacion.nombre] = denominacion
        else:
            denominaciones[existing.nombre] = existing
    
    db.commit()
    print(f"✅ {len(denominaciones)} denominaciones cargadas")
    return denominaciones

def load_enologos(db, data: List[Dict[str, Any]]) -> Dict[str, Enologo]:
    """Carga enólogos"""
    print("👨‍🔬 Cargando enólogos...")
    enologos = {}
    
    for enologo_data in data:
        existing = db.query(Enologo).filter_by(nombre=enologo_data["nombre"]).first()
        if not existing:
            # Solo usar campos que existen en la entidad Enologo
            enologo_kwargs = {
                "nombre": enologo_data["nombre"]
            }
            
            # Agregar biografia solo si existe en los datos y en la entidad
            if "biografia" in enologo_data:
                enologo_kwargs["biografia"] = enologo_data["biografia"]
            
            enologo = Enologo(**enologo_kwargs)
            db.add(enologo)
            db.flush()
            enologos[enologo.nombre] = enologo
        else:
            enologos[existing.nombre] = existing
    
    db.commit()
    print(f"✅ {len(enologos)} enólogos cargados")
    return enologos

def load_uvas(db, data: List[Dict[str, Any]]) -> Dict[str, Uva]:
    """Carga variedades de uva"""
    print("🍇 Cargando variedades de uva...")
    uvas = {}
    
    for uva_data in data:
        existing = db.query(Uva).filter_by(nombre=uva_data["nombre"]).first()
        if not existing:
            # Solo usar campos que existen en la entidad Uva
            uva_kwargs = {
                "nombre": uva_data["nombre"]
            }
            
            # Agregar campos opcionales solo si existen
            if "tipo" in uva_data:
                uva_kwargs["tipo"] = uva_data["tipo"]
            if "descripcion" in uva_data:
                uva_kwargs["descripcion"] = uva_data["descripcion"]
            
            uva = Uva(**uva_kwargs)
            db.add(uva)
            db.flush()
            uvas[uva.nombre] = uva
        else:
            uvas[existing.nombre] = existing
    
    db.commit()
    print(f"✅ {len(uvas)} variedades de uva cargadas")
    return uvas

def load_platos(db, data: List[Dict[str, Any]], categorias: Dict[str, CategoriaPlato], alergenos: Dict[str, Alergeno]):
    """Carga platos"""
    print("🍽️ Cargando platos...")
    
    loaded_count = 0
    skipped_count = 0
    processed_names = set()  # Para evitar duplicados
    
    for plato_data in data:
        plato_nombre = plato_data["nombre"]
        
        # Evitar duplicados
        if plato_nombre in processed_names:
            print(f"⚠️ Plato duplicado omitido: '{plato_nombre}'")
            skipped_count += 1
            continue
        
        processed_names.add(plato_nombre)
        
        existing = db.query(Plato).filter_by(nombre=plato_nombre).first()
        if not existing:
            # Validar categoría
            categoria = categorias.get(plato_data["categoria"])
            if not categoria:
                print(f"❌ Categoría '{plato_data['categoria']}' no encontrada para plato '{plato_nombre}' - OMITIDO")
                skipped_count += 1
                continue
            
            try:
                # Crear plato
                plato = Plato(
                    nombre=plato_nombre,
                    descripcion=plato_data.get("descripcion"),
                    precio=Decimal(str(plato_data["precio"])),
                    precio_unidad=plato_data.get("precio_unidad"),
                    categoria_id=categoria.id,
                    sugerencias=plato_data.get("sugerencias", False),
                    is_active=plato_data.get("is_active", True)
                )
                
                # Agregar alérgenos con mapeo mejorado
                plato_alergenos = plato_data.get("alergenos", [])
                for alergeno_nombre in plato_alergenos:
                    # Mapeo de nombres inconsistentes
                    alergeno_mapped = mapear_alergeno_nombre(alergeno_nombre)
                    alergeno = alergenos.get(alergeno_mapped)
                    
                    if alergeno:
                        plato.alergenos.append(alergeno)
                    else:
                        print(f"⚠️ Alérgeno '{alergeno_nombre}' (mapeado: '{alergeno_mapped}') no encontrado para plato '{plato_nombre}'")
                
                db.add(plato)
                loaded_count += 1
                
                # Debug info
                print(f"✅ Plato agregado: '{plato_nombre}' - Precio: {plato.precio} - Categoría: {categoria.nombre}")
                
            except Exception as e:
                print(f"❌ Error al crear plato '{plato_nombre}': {e}")
                skipped_count += 1
        else:
            print(f"ℹ️ Plato ya existe: '{plato_nombre}'")
            skipped_count += 1
    
    db.commit()
    print(f"✅ {loaded_count} platos cargados, {skipped_count} omitidos")

def load_vinos(db, data: List[Dict[str, Any]], categorias: Dict[str, CategoriaVino], 
               bodegas: Dict[str, Bodega], denominaciones: Dict[str, DenominacionOrigen],
               enologos: Dict[str, Enologo], uvas: Dict[str, Uva]):
    """Carga vinos"""
    print("🍷 Cargando vinos...")
    
    loaded_count = 0
    skipped_count = 0
    processed_wines = set()  # Para manejar duplicados por nombre+precio+unidad
    
    for vino_data in data:
        # Crear clave única para detectar duplicados
        wine_key = f"{vino_data['nombre']}_{vino_data['precio']}_{vino_data.get('precio_unidad', '')}"
        
        if wine_key in processed_wines:
            print(f"⚠️ Vino duplicado omitido: '{vino_data['nombre']}' ({vino_data['precio']} {vino_data.get('precio_unidad', '')})")
            skipped_count += 1
            continue
        
        processed_wines.add(wine_key)
        
        # Buscar por nombre, precio y unidad para evitar duplicados reales
        existing = db.query(Vino).filter_by(
            nombre=vino_data["nombre"],
            precio=Decimal(str(vino_data["precio"])),
            precio_unidad=vino_data.get("precio_unidad")
        ).first()
        
        if not existing:
            # Validar relaciones obligatorias
            categoria = categorias.get(vino_data["categoria"])
            if not categoria:
                print(f"❌ Categoría '{vino_data['categoria']}' no encontrada para vino '{vino_data['nombre']}' - OMITIDO")
                skipped_count += 1
                continue
            
            bodega = bodegas.get(vino_data["bodega"])
            if not bodega:
                print(f"❌ Bodega '{vino_data['bodega']}' no encontrada para vino '{vino_data['nombre']}' - OMITIDO")
                skipped_count += 1
                continue
            
            try:
                # Validar denominación (opcional)
                denominacion = None
                if vino_data.get("denominacion"):
                    denominacion = denominaciones.get(vino_data["denominacion"])
                    if not denominacion:
                        print(f"⚠️ Denominación '{vino_data['denominacion']}' no encontrada para vino '{vino_data['nombre']}' - continuando sin denominación")
                
                # Crear vino
                vino = Vino(
                    nombre=vino_data["nombre"],
                    precio=Decimal(str(vino_data["precio"])),
                    precio_unidad=vino_data.get("precio_unidad"),
                    categoria_id=categoria.id,
                    bodega_id=bodega.id,
                    denominacion_origen_id=denominacion.id if denominacion else None,
                    is_active=vino_data.get("is_active", True)
                )
                
                # Agregar enólogo (opcional)
                if vino_data.get("enologo"):
                    enologo = enologos.get(vino_data["enologo"])
                    if enologo:
                        vino.enologo_id = enologo.id
                    else:
                        print(f"⚠️ Enólogo '{vino_data['enologo']}' no encontrado para vino '{vino_data['nombre']}'")
                
                # Agregar uvas
                vino_uvas = vino_data.get("uvas", [])
                for uva_nombre in vino_uvas:
                    uva = uvas.get(uva_nombre)
                    if uva:
                        vino.uvas.append(uva)
                    else:
                        print(f"⚠️ Uva '{uva_nombre}' no encontrada para vino '{vino_data['nombre']}'")
                
                db.add(vino)
                loaded_count += 1
                
                # Debug info
                print(f"✅ Vino agregado: '{vino.nombre}' - Precio: {vino.precio} {vino.precio_unidad or ''} - Bodega: {bodega.nombre}")
                
            except Exception as e:
                print(f"❌ Error al crear vino '{vino_data['nombre']}': {e}")
                skipped_count += 1
        else:
            print(f"ℹ️ Vino ya existe: '{vino_data['nombre']}' ({vino_data['precio']} {vino_data.get('precio_unidad', '')})")
            skipped_count += 1
    
    db.commit()
    print(f"✅ {loaded_count} vinos cargados, {skipped_count} omitidos")

def mapear_alergeno_nombre(nombre_original: str) -> str:
    """Mapea nombres de alérgenos inconsistentes"""
    mapeo = {
        "Gluten": "gluten",
        "Huevos": "eggs", 
        "Lácteos": "milk",
        "Pescado": "fish",
        "Crustáceos": "crustaceans",
        "Frutos secos": "nuts",
        "Soja": "soybeans",
        "Sésamo": "sesame",
        "Sulfitos": "sulphites",
        "Apio": "celery",
        "Mostaza": "mustard",
        "Altramuces": "lupin",
        "Moluscos": "molluscs",
        "Cacahuetes": "peanuts"
    }
    
    return mapeo.get(nombre_original, nombre_original.lower())

def load_data_from_json(json_file_path: str):
    """Función principal para cargar datos desde JSON"""
    print(f"🚀 Cargando datos desde: {json_file_path}")
    
    # Verificar que el archivo existe
    json_path = Path(json_file_path)
    if not json_path.exists():
        raise FileNotFoundError(f"Archivo JSON no encontrado: {json_file_path}")
    
    # Cargar JSON
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Error al parsear JSON: {e}")
    
    # Validar estructura básica
    required_sections = ["categorias_platos", "categorias_vinos", "alergenos"]
    for section in required_sections:
        if section not in data:
            raise ValueError(f"Sección requerida '{section}' no encontrada en JSON")
    
    # Crear sesión de base de datos
    db = create_session()
    
    try:
        # Cargar datos en orden de dependencias
        print("📦 Iniciando carga de datos...")
        
        # 1. Datos básicos (sin dependencias)
        categorias_platos = load_categorias_platos(db, data["categorias_platos"])
        categorias_vinos = load_categorias_vinos(db, data["categorias_vinos"])
        alergenos = load_alergenos(db, data["alergenos"])
        
        # 2. Datos de vinos (con dependencias)
        bodegas = {}
        denominaciones = {}
        enologos = {}
        uvas = {}
        
        if "bodegas" in data and data["bodegas"]:
            bodegas = load_bodegas(db, data["bodegas"])
        if "denominaciones_origen" in data and data["denominaciones_origen"]:
            denominaciones = load_denominaciones(db, data["denominaciones_origen"])
        if "enologos" in data and data["enologos"]:
            enologos = load_enologos(db, data["enologos"])
        if "uvas" in data and data["uvas"]:
            uvas = load_uvas(db, data["uvas"])
        
        # 3. Platos y vinos
        if "platos" in data and data["platos"]:
            print(f"📊 Procesando {len(data['platos'])} platos...")
            load_platos(db, data["platos"], categorias_platos, alergenos)
        
        if "vinos" in data and data["vinos"]:
            print(f"📊 Procesando {len(data['vinos'])} vinos...")
            load_vinos(db, data["vinos"], categorias_vinos, bodegas, denominaciones, enologos, uvas)
        
        # 4. Usuarios (opcional)
        if "users" in data and data["users"]:
            load_users(db, data["users"])
        
        # Verificar resultados finales
        print("\n📊 RESUMEN FINAL DE CARGA:")
        print(f"   📂 Categorías platos: {db.query(CategoriaPlato).count()}")
        print(f"   🍷 Categorías vinos: {db.query(CategoriaVino).count()}")
        print(f"   ⚠️  Alérgenos: {db.query(Alergeno).count()}")
        print(f"   🏭 Bodegas: {db.query(Bodega).count()}")
        print(f"   🎯 Denominaciones: {db.query(DenominacionOrigen).count()}")
        print(f"   👨‍🔬 Enólogos: {db.query(Enologo).count()}")
        print(f"   🍇 Uvas: {db.query(Uva).count()}")
        print(f"   🍽️  Platos: {db.query(Plato).count()}")
        print(f"   🍷 Vinos: {db.query(Vino).count()}")
        print(f"   👤 Usuarios: {db.query(User).count()}")
        
        print("🎉 ¡Datos cargados exitosamente desde JSON!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error durante la carga: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        db.close()

def create_sample_json():
    """Crea un archivo JSON de ejemplo con la estructura correcta"""
    sample_data = {
        "categorias_platos": [
            {"nombre": "Entrantes"},
            {"nombre": "Principales"},
            {"nombre": "Postres",}
        ],
        "categorias_vinos": [
            {"nombre": "Tinto joven"},
            {"nombre": "Tinto crianza"},
            {"nombre": "Blanco joven"}
        ],
        "alergenos": [
            {"nombre": "Gluten"},
            {"nombre": "Lácteos"},
            {"nombre": "Huevos"},
            {"nombre": "Pescado"}
        ],
        "bodegas": [
            {"nombre": "Marqués de Riscal", "region": "Rioja"},
            {"nombre": "Torres", "region": "Penedès"}
        ],
        "denominaciones_origen": [
            {"nombre": "D.O. Rioja", "region": "La Rioja"},
            {"nombre": "D.O. Penedès", "region": "Cataluña"}
        ],
        "enologos": [
            {"nombre": "Francisco Hurtado de Amézaga"},
            {"nombre": "Miguel Torres Maczassek"}
        ],
        "uvas": [
            {"nombre": "Tempranillo", "tipo": "Tinta"},
            {"nombre": "Albariño", "tipo": "Blanca"}
        ],
        "platos": [
            {
                "nombre": "Ensalada César",
                "descripcion": "Lechuga romana con salsa césar",
                "precio": 12.50,
                "categoria": "Entrantes",
                "sugerencias": True,
                "is_active": True,
                "alergenos": ["Gluten", "Huevos", "Lácteos"]
            }
        ],
        "vinos": [
            {
                "nombre": "Marqués de Riscal Reserva",
                "precio": 15.90,
                "categoria": "Tinto crianza",
                "bodega": "Marqués de Riscal",
                "denominacion": "D.O. Rioja",
                "enologo": "Francisco Hurtado de Amézaga",
                "is_active": True,
                "uvas": ["Tempranillo"]
            }
        ],
        "users": [
            {
                "email": "admin@restaurant.com",
                "username": "admin",
                "password": "admin123",
                "is_admin": True,
                "is_active": True
            }
        ]
    }
    
    with open("data/sample_data.json", "w", encoding="utf-8") as f:
        json.dump(sample_data, f, indent=2, ensure_ascii=False)
    
    print("📝 Archivo de ejemplo creado en: data/sample_data.json")

def main():
    """Función principal"""
    if len(sys.argv) < 2:
        print("❌ Uso: python scripts-examples/load_from_json.py <archivo.json>")
        print("\n💡 Para crear un archivo de ejemplo:")
        print("   python scripts-examples/load_from_json.py --create-sample")
        sys.exit(1)
    
    if sys.argv[1] == "--create-sample":
        # Crear directorio data si no existe
        Path("data").mkdir(exist_ok=True)
        create_sample_json()
        return
    
    json_file = sys.argv[1]
    
    try:
        load_data_from_json(json_file)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()