from app.modules.citas.repository import CitaRepository


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