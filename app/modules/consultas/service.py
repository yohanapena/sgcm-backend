from app.modules.consultas.contracts import IConsultaService
from app.modules.consultas.repository import ConsultaRepository
from app.modules.citas.repository import CitaRepository
from app.modules.signos_vitales.repository import SignosVitalesRepository

class ConsultaService(IConsultaService):

    def __init__(self):

        self.repository = ConsultaRepository()
        self.cita_repository = CitaRepository()
        self.signos_repository = SignosVitalesRepository()

    def registrar_consulta(
            self,
            consulta
        ):

        id_consulta = self.repository.crear_consulta(
            consulta
        )

        if consulta.signos_vitales:

            try:

                self.signos_repository.crear_signos_vitales({
                    "peso": consulta.signos_vitales.peso,
                    "estatura": consulta.signos_vitales.estatura,
                    "temperatura": consulta.signos_vitales.temperatura,
                    "presion_arterial": consulta.signos_vitales.presion,
                    "frecuencia_cardiaca": consulta.signos_vitales.frecuenciaCardiaca,
                    "saturacion_oxigeno": consulta.signos_vitales.saturacion,
                    "id_historia_clinica_fk": consulta.id_historia_clinica_fk,
                    "id_consulta_fk": id_consulta
                })

            except Exception as e:

                print("Error registrando signos vitales:", e)

        for servicio_id in consulta.servicios_ids:

            self.repository.agregar_servicio(id_consulta, servicio_id)

            self.cita_repository.marcar_atendida(consulta.id_cita_fk)
            self.cita_repository.registrar_historial(
                id_cita=consulta.id_cita_fk,
                estado_anterior="Agendada",
                estado_nuevo="Atendida",
                motivo="Consulta registrada"
            )
            return {"mensaje": "Consulta registrada"}

    def obtener_consultas(
        self,
        id_historia_clinica_fk
    ):

        return self.repository.obtener_por_historia(
            id_historia_clinica_fk
        )
    
    def obtener_servicios_consulta(
        self,
        id_consulta
    ):

        return self.repository.obtener_servicios_consulta(
            id_consulta
        )
        
    def obtener_historia_clinica_paciente(
        self,
        id_paciente: int
    ):
        # Obtener historia clínica con JOIN a pacientes
        historia = self.repository.obtener_historia_clinica(id_paciente)
        
        if not historia:
            return {"paciente": None, "historia": None, "consultas": []}
        
        # Obtener consultas ordenadas por fecha DESC
        consultas = self.repository.obtener_consultas_historia(
            historia["id_historia_clinica"]
        )
        # Normalizar alergias del paciente: puede venir como string, array o null
        paciente = {
            "nombre": historia.get("nombre") or "",
            "primer_apellido": historia.get("primer_apellido") or "",
            "numero_identificacion": historia.get("numero_identificacion") or "",
        }

        alergias_raw = historia.get("alergias", None)
        if isinstance(alergias_raw, str):
            paciente["alergias"] = [a.strip() for a in alergias_raw.split(",") if a.strip()]
        elif isinstance(alergias_raw, list):
            paciente["alergias"] = alergias_raw
        else:
            paciente["alergias"] = []

        # Normalizar campos de historia y asegurar valores por defecto
        historia_obj = {
            "antecedentes_personales": historia.get("antecedentes_personales") or "",
            "antecedentes_familiares": historia.get("antecedentes_familiares") or "",
            "resumen": historia.get("resumen"),
            "fecha_apertura": historia.get("fecha_apertura"),
            "id_historia_clinica": historia.get("id_historia_clinica"),
        }

        # Anidar signos vitales por consulta y limpiar propiedades raíz
        consultas_normalizadas = []
        for c in consultas:
            consulta = dict(c)  # copy
            id_consulta = consulta.get("id_consulta") or consulta.get("id_consulta")

            # Obtener signos asociados a la consulta (puede venir lista)
            signos_list = self.signos_repository.obtener_por_consulta(id_consulta)
            signos_vitales = None
            if signos_list:
                # Tomar el primer registro (si hay varios)
                s = signos_list[0]
                signos_vitales = {}
                for key in ("peso", "estatura", "temperatura", "presion_arterial", "frecuencia_cardiaca", "saturacion_oxigeno"):
                    if key in s:
                        signos_vitales[key] = s.get(key)

            # Eliminar posibles campos de signos del nivel raíz si existieran
            for key in ("peso", "estatura", "temperatura", "presion_arterial", "frecuencia_cardiaca", "saturacion_oxigeno"):
                if key in consulta:
                    consulta.pop(key, None)

            consulta["signos_vitales"] = signos_vitales or {}

            consultas_normalizadas.append(consulta)

        return {
            "paciente": paciente,
            "historia": historia_obj,
            "consultas": consultas_normalizadas,
        }