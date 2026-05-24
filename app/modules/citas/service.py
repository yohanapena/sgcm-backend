from app.modules.citas.repository import CitaRepository
from fastapi import HTTPException
from datetime import date

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
                detail="Cita no encontrada"
            )

        if cita["estado"] == "Cancelada":
            raise HTTPException(
                status_code=400,
                detail="La cita ya está cancelada"
            )

        if cita["estado"] == "Atendida":
            raise HTTPException(
                status_code=400,
                detail="No se puede cancelar una cita Atendida"
            )

        self.repository.registrar_historial(
            id_cita=id_cita,
            estado_anterior=cita["estado"],
            estado_nuevo="Cancelada",
            motivo=motivo
        )

        cita_cancelada = self.repository.cancelar_cita(
            id_cita,
            motivo
        )

        return {
            "data": cita_cancelada
        }

    def obtener_citas_paciente(
        self,
        id_paciente,
        fecha_inicio=None,
        fecha_fin=None
    ):

        return self.repository.obtener_por_paciente(
            id_paciente,
            fecha_inicio,
            fecha_fin
        )


    def obtener_citas_medico(
        self,
        id_medico,
        fecha=None
    ):

        return self.repository.obtener_por_medico(
            id_medico,
            fecha
        )
    
    def obtener_citas_dashboard(
        self,
        id_medico,
        fecha=None
    ):

        if fecha is None:
            fecha = date.today()

        citas = self.repository.obtener_citas_medico_fecha(
            id_medico,
            fecha
        )

        return {
            "data": citas
        }
    
    def actualizar_cita(self, id_cita, datos):

        cita = self.repository.obtener_cita_por_id(id_cita)

        if not cita:
            raise HTTPException(
                status_code=404,
                detail="Cita no encontrada"
            )

        if cita["estado"] != "Agendada":
            raise HTTPException(
                status_code=400,
                detail="No se puede modificar una cita en estado Cancelada/Atendida"
            )

        datos_actualizar = {}

        if datos.fecha is not None:
            datos_actualizar["fecha"] = datos.fecha

        if datos.hora is not None:
            datos_actualizar["hora"] = datos.hora

        if datos.observacion is not None:
            datos_actualizar["observacion"] = datos.observacion

        self.repository.actualizar_cita(
            id_cita,
            datos_actualizar
        )

        return {
            "data": {
                "id_cita": id_cita
            }
        }
    
    def obtener_cita(self, id_cita):

        cita = self.repository.obtener_cita_por_id(id_cita)

        if not cita:
            raise HTTPException(
                status_code=404,
                detail="Cita no encontrada"
            )

        return {
            "data": cita
        }
