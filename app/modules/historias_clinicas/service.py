from datetime import date
from app.modules.historias_clinicas.model import HistoriaClinica
from app.modules.historias_clinicas.schema import HistoriaClinicaCrearRequest, HistoriaClinicaActualizarRequest
from app.modules.historias_clinicas.contracts import IHistoriaClinicaRepository
from app.shared.exceptions.errors import SGCMNotFoundError


class HistoriaClinicaService:

    def __init__(self, repositorio: IHistoriaClinicaRepository):
        self.repositorio = repositorio

    def obtener_por_paciente(self, id_paciente_fk: int):
        return self.repositorio.obtener_por_paciente(id_paciente_fk)

    def crear_o_retornar_historia(self, datos: HistoriaClinicaCrearRequest) -> HistoriaClinica:
        
        existente = self.repositorio.obtener_por_paciente(datos.id_paciente_fk)
        if existente:
            return existente
        
        nueva_historia = HistoriaClinica(
            id_paciente_fk=datos.id_paciente_fk,
            resumen=datos.resumen,
            fecha_apertura=datos.fecha_apertura or date.today(),
            antecedentes_personales=datos.antecedentes_personales,
            antecedentes_familiares=datos.antecedentes_familiares,
        )
        
        return self.repositorio.crear_historia_clinica(nueva_historia)
    
    
    def actualizar_historia_clinica(self, id_historia_clinica: int, datos: HistoriaClinicaActualizarRequest) -> HistoriaClinica:
        
        datos_actualizar = {
            campo: valor
            for campo, valor in datos.model_dump().items()
            if valor is not None and valor != ""
        }

        if not datos_actualizar:
            raise SGCMNotFoundError("No se enviaron campos para actualizar")

        resultado = self.repositorio.actualizar_historia_clinica(id_historia_clinica, datos_actualizar)
        
        if not resultado:
            raise SGCMNotFoundError(f"No se encontró historia clínica con id {id_historia_clinica}")
        
        return resultado