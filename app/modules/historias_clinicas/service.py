from datetime import date
from app.modules.historias_clinicas.model import HistoriaClinica
from app.modules.historias_clinicas.schema import HistoriaClinicaCrearRequest
from app.modules.historias_clinicas.contracts import IHistoriaClinicaRepository


class HistoriaClinicaService:

    def __init__(self, repositorio: IHistoriaClinicaRepository):
        self.repositorio = repositorio

    def obtener_por_paciente(self, id_paciente_fk: int):
        return self.repositorio.obtener_por_paciente(id_paciente_fk)

    def crear_o_retornar_historia(self, datos: HistoriaClinicaCrearRequest) -> HistoriaClinica:
        
        # Si ya existe una historia para ese paciente, retornarla sin crear duplicado
        existente = self.repositorio.obtener_por_paciente(datos.id_paciente_fk)
        if existente:
            return existente
        
        # Si no existe, crear una nueva
        nueva_historia = HistoriaClinica(
            id_paciente_fk=datos.id_paciente_fk,
            resumen=datos.resumen,
            fecha_apertura=datos.fecha_apertura or date.today(),
        )
        
        return self.repositorio.crear_historia_clinica(nueva_historia)