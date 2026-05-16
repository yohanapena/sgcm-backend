from app.modules.pacientes.model import Paciente
from app.modules.pacientes.schema import PacienteCrearRequest, PacienteActualizarRequest
from app.modules.pacientes.contracts import IPacienteRepository
from app.shared.exceptions.errors import SGCMConflictError, SGCMNotFoundError

class PacienteService:

    def __init__(self, repositorio: IPacienteRepository):
        self.repositorio = repositorio

    def registrar_paciente(self, datos: PacienteCrearRequest) -> Paciente:
        
        # Verificar si ya existe un paciente con ese número de identificación
        existe = self.repositorio.obtener_por_identificacion(datos.numero_identificacion)
        
        if existe:
            raise SGCMConflictError(
                f"El número de identificación {datos.numero_identificacion} ya existe en el sistema"
            )
        
        # Crea el objeto Paciente con los datos recibidos
        nuevo_paciente = Paciente(
            numero_identificacion=datos.numero_identificacion,
            nombre=datos.nombre,
            primer_apellido=datos.primer_apellido,
            segundo_apellido=datos.segundo_apellido,
            direccion=datos.direccion,
            fecha_de_nacimiento=datos.fecha_de_nacimiento,
            id_eps_fk=datos.id_eps_fk,
            id_regimen_fk=datos.id_regimen_fk,
            sexo=datos.sexo,
            tipo_sangre=datos.tipo_sangre,
        )
        
        # Guardar en la base de datos y retornar
        return self.repositorio.crear_paciente(nuevo_paciente)
    
    def actualizar_paciente(self, id_paciente: int, datos: PacienteActualizarRequest) -> Paciente:
        
        # Verificar que el paciente existe
        existe = self.repositorio.obtener_por_id(id_paciente)
        
        if not existe:
            raise SGCMNotFoundError(
                f"No se encontró un paciente con id {id_paciente}"
            )
        
        # Convertir solo los campos que llegaron (ignorar los None)
        datos_actualizar = {
            campo: valor 
            for campo, valor in datos.model_dump().items() 
            if valor is not None and valor != ""
        }
        
        return self.repositorio.actualizar_paciente(id_paciente, datos_actualizar)
    
    def buscar_pacientes(self, criterio: str) -> list:
        resultados = self.repositorio.buscar_pacientes(criterio)
        
        if not resultados:
            raise SGCMNotFoundError(
                f"No se encontraron pacientes con el criterio '{criterio}'"
            )
        
        return resultados
    
    def obtener_por_id(self, id_paciente: int) -> Paciente:
        paciente = self.repositorio.obtener_por_id(id_paciente)
        
        if not paciente:
            raise SGCMNotFoundError(
                f"No se encontró un paciente con id {id_paciente}"
            )
        
        return paciente
    
    def agregar_alergia(self, id_paciente: int, alergia: str) -> dict:
        # Verificar que el paciente existe
        existe = self.repositorio.obtener_por_id(id_paciente)
        if not existe:
            raise SGCMNotFoundError(f"No se encontró un paciente con id {id_paciente}")
        
        return self.repositorio.agregar_alergia(id_paciente, alergia)

    def listar_alergias(self, id_paciente: int) -> list:
        # Verificar que el paciente existe
        existe = self.repositorio.obtener_por_id(id_paciente)
        if not existe:
            raise SGCMNotFoundError(f"No se encontró un paciente con id {id_paciente}")
        
        return self.repositorio.listar_alergias(id_paciente)

    def eliminar_alergia(self, id_paciente: int, id_alergia: int) -> dict:
        # Verificar que la alergia pertenece al paciente
        eliminado = self.repositorio.eliminar_alergia(id_alergia, id_paciente)
        if not eliminado:
            raise SGCMNotFoundError(f"No se encontró la alergia con id {id_alergia} para este paciente")
        
        return {"deleted": True}