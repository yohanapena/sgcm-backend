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
                    id_paciente_fk, resumen, fecha_apertura
                ) VALUES (%s, %s, %s)
                """,
                (
                    historia.id_paciente_fk,
                    historia.resumen,
                    historia.fecha_apertura,
                )
            )
            conexion.commit()
            historia.id_historia_clinica = cursor.lastrowid
            return historia
        finally:
            cursor.close()
            conexion.close()