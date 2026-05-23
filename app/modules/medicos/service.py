from fastapi import HTTPException

from app.modules.medicos.repository import (
    MedicoRepository
)


class MedicoService:

    def __init__(self):

        self.repository = MedicoRepository()

    def registrar_medico(self, medico):

        medico_existente = (
            self.repository.buscar_tarjeta_profesional(
                medico.tarjeta_profesional
            )
        )

        if medico_existente:

            raise HTTPException(
                status_code=409,
                detail="La tarjeta profesional ya existe"
            )

        id_medico = self.repository.crear_medico(
            medico
        )

        for id_especialidad in medico.especialidades:

            self.repository.agregar_especialidad(
                id_medico,
                id_especialidad
            )

        return {
            "id_medico": id_medico,
            "nombre": medico.nombre,
            "primer_apellido": medico.primer_apellido,
            "segundo_apellido": medico.segundo_apellido,
            "tarjeta_profesional": medico.tarjeta_profesional,
            "estado": "Activo"
        }
    
    def agregar_horario(
        self,
        id_medico,
        horario
    ):

        horario_existente = (
            self.repository.verificar_superposicion(
                id_medico,
                horario.dia_semana,
                horario.hora_inicial,
                horario.hora_final
            )
        )

        if horario_existente:

            raise HTTPException(
                status_code=409,
                detail="El horario se superpone con otro existente"
            )

        return self.repository.crear_horario(
            id_medico,
            horario
        )
    
    def obtener_horarios(
        self,
        id_medico
    ):

        return self.repository.obtener_horarios(
            id_medico
        )
    
    def actualizar_medico(self, id_medico, medico):

        medico_existente = self.repository.obtener_medico_por_id(
            id_medico
        )

        if not medico_existente:

            raise HTTPException(
                status_code=404,
                detail="Medico no encontrado"
            )

        medico_actualizado = self.repository.actualizar_medico(
            id_medico,
            medico
        )

        return {
            "data": medico_actualizado
        }
    
    def cambiar_estado(self, id_medico, datos):

        medico = self.repository.obtener_medico_por_id(id_medico)

        if not medico:
            raise HTTPException(
                status_code=404,
                detail="Médico no encontrado"
            )

        if datos.estado not in ["Activo", "Inactivo"]:
            raise HTTPException(
                status_code=422,
                detail="estado debe ser Activo o Inactivo"
            )

        return self.repository.cambiar_estado(
            id_medico,
            datos.estado
        )