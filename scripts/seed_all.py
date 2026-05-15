"""
Script para cargar todos los datos iniciales de demostración en la base de datos.
Ejecuta todos los seeds de una vez para inicializar el sistema.

Uso:
    python scripts/seed_all.py
"""

import sys
import os
from pathlib import Path

# Agregar el directorio padre al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.core.database import SessionLocal, engine, Base


def seed_eps():
    """Carga datos de ejemplo para EPS."""
    from sqlalchemy import text
    db = SessionLocal()
    try:
        # Verificar si ya existen datos
        result = db.execute(text("SELECT COUNT(*) as count FROM eps")).scalar()
        if result > 0:
            print("✓ EPS ya existen en la base de datos")
            return
        
        # Insertar datos de ejemplo
        eps_data = [
            ("Salud Total", "EPS Salud Total", 1),
            ("Famisanar", "EPS Famisanar", 1),
            ("Coomeva", "EPS Coomeva", 1),
            ("Axa", "EPS Axa Colpatria", 1),
            ("Aliansalud", "EPS Aliansalud", 1),
        ]
        
        for nombre, descripcion, estado in eps_data:
            db.execute(text(
                f"INSERT INTO eps (nombre, descripcion, estado) VALUES ('{nombre}', '{descripcion}', {estado})"
            ))
        
        db.commit()
        print(f"✓ {len(eps_data)} EPS creadas")
    except Exception as e:
        db.rollback()
        print(f"✗ Error al cargar EPS: {str(e)}")
    finally:
        db.close()


def seed_regimenes():
    """Carga datos de ejemplo para Regímenes."""
    from sqlalchemy import text
    db = SessionLocal()
    try:
        result = db.execute(text("SELECT COUNT(*) as count FROM regimenes")).scalar()
        if result > 0:
            print("✓ Regímenes ya existen en la base de datos")
            return
        
        regimenes_data = [
            ("Contributivo", "Régimen de trabajadores afiliados", 1),
            ("Subsidiado", "Régimen para población sin recursos", 1),
            ("Especial", "Régimen para fuerzas armadas y otros", 1),
        ]
        
        for nombre, descripcion, estado in regimenes_data:
            db.execute(text(
                f"INSERT INTO regimenes (nombre, descripcion, estado) VALUES ('{nombre}', '{descripcion}', {estado})"
            ))
        
        db.commit()
        print(f"✓ {len(regimenes_data)} Regímenes creados")
    except Exception as e:
        db.rollback()
        print(f"✗ Error al cargar Regímenes: {str(e)}")
    finally:
        db.close()


def seed_especialidades():
    """Carga datos de ejemplo para Especialidades médicas."""
    from sqlalchemy import text
    db = SessionLocal()
    try:
        result = db.execute(text("SELECT COUNT(*) as count FROM especialidades")).scalar()
        if result > 0:
            print("✓ Especialidades ya existen en la base de datos")
            return
        
        especialidades_data = [
            ("Medicina General", "Consultas de medicina general", 1),
            ("Cardiología", "Enfermedades del corazón", 1),
            ("Pediatría", "Atención de niños", 1),
            ("Dermatología", "Enfermedades de la piel", 1),
            ("Oftalmología", "Enfermedades de los ojos", 1),
            ("Ortopedia", "Enfermedades óseas y articulares", 1),
            ("Psicología", "Atención en salud mental", 1),
        ]
        
        for nombre, descripcion, estado in especialidades_data:
            db.execute(text(
                f"INSERT INTO especialidades (nombre, descripcion, estado) VALUES ('{nombre}', '{descripcion}', {estado})"
            ))
        
        db.commit()
        print(f"✓ {len(especialidades_data)} Especialidades creadas")
    except Exception as e:
        db.rollback()
        print(f"✗ Error al cargar Especialidades: {str(e)}")
    finally:
        db.close()


def seed_servicios():
    """Carga datos de ejemplo para Servicios médicos."""
    from sqlalchemy import text
    db = SessionLocal()
    try:
        result = db.execute(text("SELECT COUNT(*) as count FROM servicios")).scalar()
        if result > 0:
            print("✓ Servicios ya existen en la base de datos")
            return
        
        servicios_data = [
            ("Consulta General", "Consulta médica general", 50000.00, 1),
            ("Consulta Especializada", "Consulta con especialista", 100000.00, 1),
            ("Laboratorio Clínico", "Análisis de sangre y orina", 30000.00, 1),
            ("Ecografía", "Estudio por ultrasonido", 150000.00, 1),
            ("Radiografía", "Estudio radiológico", 80000.00, 1),
        ]
        
        for nombre, descripcion, precio, estado in servicios_data:
            db.execute(text(
                f"INSERT INTO servicios (nombre, descripcion, precio, estado) VALUES ('{nombre}', '{descripcion}', {precio}, {estado})"
            ))
        
        db.commit()
        print(f"✓ {len(servicios_data)} Servicios creados")
    except Exception as e:
        db.rollback()
        print(f"✗ Error al cargar Servicios: {str(e)}")
    finally:
        db.close()


def main():
    """Ejecuta todos los seeds."""
    print("\n" + "="*60)
    print("CARGANDO DATOS INICIALES - SGCM Backend")
    print("="*60 + "\n")
    
    try:
        # Crear todas las tablas
        print("Creando tablas...")
        Base.metadata.create_all(bind=engine)
        print("✓ Tablas sincronizadas\n")
        
        # Ejecutar seeds
        print("Cargando catálogos...\n")
        seed_eps()
        seed_regimenes()
        seed_especialidades()
        seed_servicios()
        
        print("\n" + "="*60)
        print("✓ Datos iniciales cargados exitosamente")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n✗ Error crítico: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
