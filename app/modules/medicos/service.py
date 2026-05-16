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