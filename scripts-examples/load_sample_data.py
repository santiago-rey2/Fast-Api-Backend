#!/usr/bin/env python3
"""
Script para cargar datos de ejemplo en la base de datos.

Este script carga datos de ejemplo realistas para platos y vinos,
útil para desarrollo y testing.

Prerrequisitos:
- La base de datos debe estar inicializada con datos por defecto
- Ejecutar primero: python scripts-examples/reset_database.py

Uso:
    python scripts-examples/load_sample_data.py
"""

import sys
import os
from pathlib import Path
from decimal import Decimal
from typing import List

# Agregar el directorio raíz al path para importar módulos
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy import create_engine, text
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

def create_session():
    """Crea una sesión de base de datos"""
    engine = create_engine(settings.sync_dsn, echo=False)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    return SessionLocal()

def load_sample_bodegas(db):
    """Carga bodegas de ejemplo"""
    print("🏭 Cargando bodegas de ejemplo...")
    
    bodegas_data = [
        {"nombre": "Marqués de Riscal", "region": "La Rioja"},
        {"nombre": "Vega Sicilia", "region": "Castilla y León"},
        {"nombre": "Torres", "region": "Cataluña"},
        {"nombre": "Martín Códax", "region": "Galicia"},
        {"nombre": "González Byass", "region": "Andalucía"},
        {"nombre": "Artadi", "region": "País Vasco"},
        {"nombre": "Alvear", "region": "Andalucía"},
        {"nombre": "Can Feixes", "region": "Cataluña"},
    ]
    
    bodegas_creadas = []
    for bodega_data in bodegas_data:
        # Verificar si ya existe
        existing = db.query(Bodega).filter(Bodega.nombre == bodega_data["nombre"]).first()
        if not existing:
            bodega = Bodega(**bodega_data)
            db.add(bodega)
            bodegas_creadas.append(bodega_data["nombre"])
    
    db.commit()
    print(f"✅ {len(bodegas_creadas)} bodegas creadas")

def load_sample_enologos(db):
    """Carga enólogos de ejemplo"""
    print("👨‍🔬 Cargando enólogos de ejemplo...")
    
    enologos_data = [
        {"nombre": "Miguel Torres Maczassek", "experiencia_anos": 35},
        {"nombre": "Álvaro Palacios", "experiencia_anos": 30},
        {"nombre": "Telmo Rodríguez", "experiencia_anos": 28},
        {"nombre": "Mariano García", "experiencia_anos": 45},
        {"nombre": "Josep Lluís Pérez", "experiencia_anos": 40},
        {"nombre": "Rafael Palacios", "experiencia_anos": 25},
    ]
    
    enologos_creados = []
    for enologo_data in enologos_data:
        # Verificar si ya existe
        existing = db.query(Enologo).filter(Enologo.nombre == enologo_data["nombre"]).first()
        if not existing:
            enologo = Enologo(**enologo_data)
            db.add(enologo)
            enologos_creados.append(enologo_data["nombre"])
    
    db.commit()
    print(f"✅ {len(enologos_creados)} enólogos creados")

def load_sample_platos(db):
    """Carga platos de ejemplo"""
    print("🍽️ Cargando platos de ejemplo...")
    
    # Obtener categorías y alérgenos
    categorias = {cat.nombre: cat.id for cat in db.query(CategoriaPlato).all()}
    alergenos = {alerg.nombre: alerg.id for alerg in db.query(Alergeno).all()}
    
    platos_data = [
        # Entrantes
        {
            "nombre": "Croquetas de jamón ibérico",
            "precio": Decimal("8.50"),
            "descripcion": "Croquetas caseras con jamón ibérico de bellota",
            "categoria_id": categorias.get("Entrantes", 1),
            "alergenos": ["Cereales que contienen gluten", "Leche", "Huevos"]
        },
        {
            "nombre": "Pulpo a la gallega",
            "precio": Decimal("16.00"),
            "descripcion": "Pulpo cocido con patatas, pimentón dulce y aceite de oliva",
            "categoria_id": categorias.get("Entrantes", 1),
            "alergenos": ["Moluscos"]
        },
        {
            "nombre": "Tabla de quesos manchegos",
            "precio": Decimal("12.50"),
            "descripcion": "Selección de quesos curados de La Mancha con membrillo",
            "categoria_id": categorias.get("Entrantes", 1),
            "alergenos": ["Leche"]
        },
        
        # Platos principales
        {
            "nombre": "Paella valenciana",
            "precio": Decimal("18.00"),
            "descripcion": "Arroz con pollo, conejo, garrofó, judía verde y azafrán",
            "categoria_id": categorias.get("Arroces", 6),
            "alergenos": []
        },
        {
            "nombre": "Cochinillo asado",
            "precio": Decimal("22.00"),
            "descripcion": "Cochinillo segoviano asado en horno de leña",
            "categoria_id": categorias.get("Carnes", 7),
            "alergenos": []
        },
        {
            "nombre": "Lubina a la sal",
            "precio": Decimal("19.50"),
            "descripcion": "Lubina fresca cocinada en costra de sal marina",
            "categoria_id": categorias.get("Pescados", 8),
            "alergenos": ["Pescado"]
        },
        {
            "nombre": "Rabo de toro estofado",
            "precio": Decimal("20.00"),
            "descripcion": "Rabo de toro guisado lentamente con verduras y vino tinto",
            "categoria_id": categorias.get("Carnes", 7),
            "alergenos": ["Dióxido de azufre y sulfitos"]
        },
        
        # Postres
        {
            "nombre": "Torrija con helado de vainilla",
            "precio": Decimal("6.50"),
            "descripcion": "Torrija casera con canela y helado de vainilla artesanal",
            "categoria_id": categorias.get("Postres", 3),
            "alergenos": ["Cereales que contienen gluten", "Leche", "Huevos"]
        },
        {
            "nombre": "Crema catalana",
            "precio": Decimal("5.50"),
            "descripcion": "Crema catalana tradicional con azúcar caramelizado",
            "categoria_id": categorias.get("Postres", 3),
            "alergenos": ["Leche", "Huevos"]
        },
        
        # Tapas
        {
            "nombre": "Patatas bravas",
            "precio": Decimal("4.50"),
            "descripcion": "Patatas fritas con salsa brava y alioli",
            "categoria_id": categorias.get("Tapas", 5),
            "alergenos": ["Huevos"]
        },
        {
            "nombre": "Pimientos de Padrón",
            "precio": Decimal("5.00"),
            "descripcion": "Pimientos verdes fritos con sal gorda",
            "categoria_id": categorias.get("Tapas", 5),
            "alergenos": []
        }
    ]
    
    platos_creados = []
    for plato_data in platos_data:
        # Verificar si ya existe
        existing = db.query(Plato).filter(Plato.nombre == plato_data["nombre"]).first()
        if not existing:
            # Separar alérgenos del resto de datos
            alergenos_nombres = plato_data.pop("alergenos", [])
            
            # Crear plato
            plato = Plato(**plato_data)
            db.add(plato)
            db.flush()  # Para obtener el ID
            
            # Agregar alérgenos
            for alergeno_nombre in alergenos_nombres:
                alergeno_id = alergenos.get(alergeno_nombre)
                if alergeno_id:
                    alergeno = db.query(Alergeno).get(alergeno_id)
                    if alergeno:
                        plato.alergenos.append(alergeno)
            
            platos_creados.append(plato_data["nombre"])
    
    db.commit()
    print(f"✅ {len(platos_creados)} platos creados")

def load_sample_vinos(db):
    """Carga vinos de ejemplo"""
    print("🍷 Cargando vinos de ejemplo...")
    
    # Obtener datos de referencia
    categorias = {cat.nombre: cat.id for cat in db.query(CategoriaVino).all()}
    bodegas = {bod.nombre: bod.id for bod in db.query(Bodega).all()}
    denominaciones = {do.nombre: do.id for do in db.query(DenominacionOrigen).all()}
    enologos = {enol.nombre: enol.id for enol in db.query(Enologo).all()}
    uvas = {uva.nombre: uva.id for uva in db.query(Uva).all()}
    
    vinos_data = [
        {
            "nombre": "Marqués de Riscal Reserva",
            "precio": Decimal("15.50"),
            "categoria_id": categorias.get("Tinto reserva", 3),
            "bodega_id": bodegas.get("Marqués de Riscal"),
            "denominacion_origen_id": denominaciones.get("D.O. Rioja", 1),
            "enologo_id": None,
            "uvas": ["Tempranillo", "Garnacha"]
        },
        {
            "nombre": "Vega Sicilia Único",
            "precio": Decimal("320.00"),
            "categoria_id": categorias.get("Tinto gran reserva", 4),
            "bodega_id": bodegas.get("Vega Sicilia"),
            "denominacion_origen_id": denominaciones.get("D.O. Ribera del Duero", 2),
            "enologo_id": enologos.get("Mariano García"),
            "uvas": ["Tempranillo", "Cabernet Sauvignon", "Merlot"]
        },
        {
            "nombre": "Torres Sangre de Toro",
            "precio": Decimal("8.90"),
            "categoria_id": categorias.get("Tinto joven", 1),
            "bodega_id": bodegas.get("Torres"),
            "denominacion_origen_id": denominaciones.get("D.O. Penedès", 3),
            "enologo_id": enologos.get("Miguel Torres Maczassek"),
            "uvas": ["Garnacha", "Monastrell"]
        },
        {
            "nombre": "Martín Códax Albariño",
            "precio": Decimal("12.50"),
            "categoria_id": categorias.get("Blanco joven", 5),
            "bodega_id": bodegas.get("Martín Códax"),
            "denominacion_origen_id": denominaciones.get("D.O. Rías Baixas", 4),
            "enologo_id": None,
            "uvas": ["Albariño"]
        },
        {
            "nombre": "González Byass Tío Pepe",
            "precio": Decimal("9.50"),
            "categoria_id": categorias.get("Generoso", 10),
            "bodega_id": bodegas.get("González Byass"),
            "denominacion_origen_id": denominaciones.get("D.O. Jerez", 5),
            "enologo_id": None,
            "uvas": ["Albariño"]  # Usando Albariño como proxy para Palomino
        },
        {
            "nombre": "Artadi Viñas de Gain",
            "precio": Decimal("18.00"),
            "categoria_id": categorias.get("Tinto crianza", 2),
            "bodega_id": bodegas.get("Artadi"),
            "denominacion_origen_id": denominaciones.get("D.O. Rioja", 1),
            "enologo_id": None,
            "uvas": ["Tempranillo"]
        }
    ]
    
    vinos_creados = []
    for vino_data in vinos_data:
        # Verificar si ya existe
        existing = db.query(Vino).filter(Vino.nombre == vino_data["nombre"]).first()
        if not existing:
            # Separar uvas del resto de datos
            uvas_nombres = vino_data.pop("uvas", [])
            
            # Crear vino
            vino = Vino(**vino_data)
            db.add(vino)
            db.flush()  # Para obtener el ID
            
            # Agregar uvas
            for uva_nombre in uvas_nombres:
                uva_id = uvas.get(uva_nombre)
                if uva_id:
                    uva = db.query(Uva).get(uva_id)
                    if uva:
                        vino.uvas.append(uva)
            
            vinos_creados.append(vino_data["nombre"])
    
    db.commit()
    print(f"✅ {len(vinos_creados)} vinos creados")

def verify_sample_data(db):
    """Verifica que los datos de ejemplo se hayan cargado correctamente"""
    print("\n🔍 Verificando datos de ejemplo...")
    
    checks = [
        ("Bodegas", db.query(Bodega).count()),
        ("Enólogos", db.query(Enologo).count()),
        ("Platos", db.query(Plato).count()),
        ("Vinos", db.query(Vino).count()),
    ]
    
    for name, count in checks:
        print(f"   ✅ {name}: {count} registros")

def main():
    """Función principal"""
    print("=" * 60)
    print("🎭 CARGA DE DATOS DE EJEMPLO")
    print("=" * 60)
    
    # Verificar que la base de datos esté inicializada
    db = create_session()
    
    try:
        # Verificar que existan datos básicos
        categoria_count = db.query(CategoriaPlato).count()
        if categoria_count == 0:
            print("❌ Error: La base de datos no está inicializada")
            print("💡 Ejecuta primero: python scripts-examples/reset_database.py")
            return
        
        print(f"✅ Base de datos inicializada ({categoria_count} categorías encontradas)")
        
        # Cargar datos de ejemplo
        load_sample_bodegas(db)
        load_sample_enologos(db)
        load_sample_platos(db)
        load_sample_vinos(db)
        
        # Verificar resultado
        verify_sample_data(db)
        
        print("\n🎉 ¡Datos de ejemplo cargados exitosamente!")
        print("\n💡 Ahora puedes:")
        print("   • Iniciar el servidor: python -m uvicorn src.main:app --reload")
        print("   • Ver la documentación: http://localhost:8000/docs")
        print("   • Probar los endpoints públicos: GET /api/v1/platos/")
        
    except Exception as e:
        print(f"❌ Error durante la carga: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()
