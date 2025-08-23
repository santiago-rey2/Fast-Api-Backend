"""
Script para inicializar la base de datos con datos semilla
"""
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import select
from src.database import SessionLocal, init_db
from src.entities import (
    CategoriaPlato, Alergeno, Plato,
    CategoriaVino, Bodega, DenominacionOrigen, Enologo, Uva, Vino
)

def create_initial_data():
    """Crea datos iniciales en la base de datos"""
    db = SessionLocal()
    
    try:
        # Crear categorías de platos con IDs específicos
        categorias_platos = [
            CategoriaPlato(id=0, nombre="Sin categoría"),
            CategoriaPlato(id=1, nombre="Entrantes"),
            CategoriaPlato(id=2, nombre="Platos principales"),
            CategoriaPlato(id=3, nombre="Postres")
        ]
        
        for categoria in categorias_platos:
            existing = db.execute(
                select(CategoriaPlato).where(CategoriaPlato.id == categoria.id)
            ).scalar_one_or_none()
            if not existing:
                db.add(categoria)
        
        # Crear alérgenos con IDs específicos
        alergenos = [
            Alergeno(id=0, nombre="Sin alérgenos"),
            Alergeno(id=1, nombre="Gluten"),
            Alergeno(id=2, nombre="Lácteos"),
            Alergeno(id=3, nombre="Huevos"),
            Alergeno(id=4, nombre="Frutos secos"),
            Alergeno(id=5, nombre="Mariscos"),
            Alergeno(id=6, nombre="Pescado")
        ]
        
        for alergeno in alergenos:
            existing = db.execute(
                select(Alergeno).where(Alergeno.id == alergeno.id)
            ).scalar_one_or_none()
            if not existing:
                db.add(alergeno)
        
        # Crear categorías de vinos con IDs específicos
        categorias_vinos = [
            CategoriaVino(id=0, nombre="Sin categoría"),
            CategoriaVino(id=1, nombre="Vinos Blancos"),
            CategoriaVino(id=2, nombre="Vinos Tintos"),
            CategoriaVino(id=3, nombre="Vinos Dulces")
        ]
        
        for categoria in categorias_vinos:
            existing = db.execute(
                select(CategoriaVino).where(CategoriaVino.id == categoria.id)
            ).scalar_one_or_none()
            if not existing:
                db.add(categoria)
        
        # Crear bodegas con IDs específicos
        bodegas = [
            Bodega(id=0, nombre="Sin bodega"),
            Bodega(id=1, nombre="Bodegas Marqués de Riscal"),
            Bodega(id=2, nombre="Bodegas Vega Sicilia"),
            Bodega(id=3, nombre="Bodegas Torres")
        ]
        
        for bodega in bodegas:
            existing = db.execute(
                select(Bodega).where(Bodega.id == bodega.id)
            ).scalar_one_or_none()
            if not existing:
                db.add(bodega)
        
        # Crear denominaciones de origen con IDs específicos
        denominaciones = [
            DenominacionOrigen(id=0, nombre="Sin denominación"),
            DenominacionOrigen(id=1, nombre="D.O. Rioja"),
            DenominacionOrigen(id=2, nombre="D.O. Ribera del Duero"),
            DenominacionOrigen(id=3, nombre="D.O. Penedès")
        ]
        
        for denominacion in denominaciones:
            existing = db.execute(
                select(DenominacionOrigen).where(DenominacionOrigen.id == denominacion.id)
            ).scalar_one_or_none()
            if not existing:
                db.add(denominacion)
        
        # Crear enólogos con IDs específicos
        enologos = [
            Enologo(id=0, nombre="Sin enólogo"),
            Enologo(id=1, nombre="Álvaro Palacios"),
            Enologo(id=2, nombre="Mariano García"),
            Enologo(id=3, nombre="Miguel Torres")
        ]
        
        for enologo in enologos:
            existing = db.execute(
                select(Enologo).where(Enologo.id == enologo.id)
            ).scalar_one_or_none()
            if not existing:
                db.add(enologo)
        
        # Crear tipos de uva con IDs específicos
        uvas = [
            Uva(id=0, nombre="Sin uva específica"),
            Uva(id=1, nombre="Tempranillo"),
            Uva(id=2, nombre="Garnacha"),
            Uva(id=3, nombre="Albariño"),
            Uva(id=4, nombre="Verdejo"),
            Uva(id=5, nombre="Chardonnay"),
            Uva(id=6, nombre="Cabernet Sauvignon")
        ]
        
        for uva in uvas:
            existing = db.execute(
                select(Uva).where(Uva.id == uva.id)
            ).scalar_one_or_none()
            if not existing:
                db.add(uva)
        
        db.commit()
        print("✅ Datos iniciales creados correctamente")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error creando datos iniciales: {e}")
        raise
    finally:
        db.close()

def main():
    """Punto de entrada principal"""
    print("🚀 Inicializando base de datos...")
    
    # Crear tablas
    init_db()
    print("✅ Tablas creadas")
    
    # Crear datos iniciales
    create_initial_data()
    
    print("🎉 Inicialización completada")

if __name__ == "__main__":
    main()
