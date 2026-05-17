from typing import Optional
from app.core.database import get_connection
from app.modules.historias_clinicas.model import HistoriaClinica
from app.modules.historias_clinicas.contracts import IHistoriaClinicaRepository


class HistoriaClinicaRepository(IHistoriaClinicaRepository):

    def obtener_por_paciente(self, id_paciente_fk: int) -> Optional[HistoriaClinica]:
        conexion = get_connection()
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM historias_clinicas WHERE id_paciente_fk = %s",
                (id_paciente_fk,)
            )
            fila = cursor.fetchone()
            if not fila:
                return None
            return HistoriaClinica(**fila)
        finally:
            cursor.close()
            conexion.close()

    def crear_historia_clinica(self, historia: HistoriaClinica) -> HistoriaClinica:
        conexion = get_connection()
        try:
            cursor = conexion.cursor()
            cursor.execute(
                """
                INSERT INTO historias_clinicas (
                    id_paciente_fk, resumen, fecha_apertura,
                    antecedentes_personales, antecedentes_familiares
                ) VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    historia.id_paciente_fk,
                    historia.resumen,
                    historia.fecha_apertura,
                    historia.antecedentes_personales,
                    historia.antecedentes_familiares,
                )
            )
            conexion.commit()
            historia.id_historia_clinica = cursor.lastrowid
            return historia
        finally:
            cursor.close()
            conexion.close()
            
            
    def actualizar_historia_clinica(self, id_historia_clinica: int, datos: dict) -> Optional[HistoriaClinica]:
        conexion = get_connection()
        try:
            campos = ", ".join(f"{campo} = %s" for campo in datos.keys())
            valores = list(datos.values())
            valores.append(id_historia_clinica)
            cursor = conexion.cursor()
            cursor.execute(
                f"UPDATE historias_clinicas SET {campos} WHERE id_historia_clinica = %s",
                valores
            )
            conexion.commit()
            # Obtener la historia actualizada
            cursor2 = conexion.cursor(dictionary=True)
            cursor2.execute(
                "SELECT * FROM historias_clinicas WHERE id_historia_clinica = %s",
                (id_historia_clinica,)
            )
            fila = cursor2.fetchone()
            if not fila:
                return None
            return HistoriaClinica(**fila)
        finally:
            cursor.close()
            conexion.close()