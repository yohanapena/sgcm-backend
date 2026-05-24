from app.modules.citas.repository import CitaRepository
from fastapi import HTTPException

class SGCMConflictError(Exception):
    pass


class CitaService:

    def __init__(self):

        self.repository = CitaRepository()


    def agendar_cita(self, cita):

        cita_existente = (
            self.repository.verificar_disponibilidad(
                cita.fecha,
                cita.hora,
                cita.id_horario_medico_fk
            )
        )

        if cita_existente:

            raise SGCMConflictError(
                "El horario ya está ocupado"
            )

        return self.repository.crear_cita(cita)
    
    def cancelar_cita(self, id_cita: int, motivo: str):
        cita = self.repository.obtener_cita(id_cita)

        if not cita:
            raise HTTPException(
                status_code=404,
                detail="La cita no existe"
            )

        if cita["estado"] == "Cancelada":
            raise HTTPException(
                status_code=400,
                detail="La cita ya está cancelada"
            )

        self.repository.registrar_historial(
            id_cita=id_cita,
            estado_anterior=cita["estado"],
            estado_nuevo="Cancelada",
            motivo=motivo
        )

        self.repository.cancelar_cita(id_cita)

        return {
            "message": "Cita cancelada correctamente"
        }