from app.modules.pacientes.model import Paciente
from app.modules.pacientes.schema import PacienteCrearRequest
from app.modules.pacientes.contracts import IPacienteRepository
from app.shared.exceptions.errors import SGCMConflictError


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