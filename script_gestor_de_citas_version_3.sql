CREATE DATABASE sistema_citas_medicas;
USE sistema_citas_medicas;
CREATE TABLE regimenes(
    id_regimen INT NOT NULL AUTO_INCREMENT,
    tipo_regimen VARCHAR(45) NOT NULL,
    PRIMARY KEY(id_regimen)
);

CREATE TABLE eps(
    id_eps INT NOT NULL AUTO_INCREMENT,
    nit_eps VARCHAR(45) NOT NULL,
    nombre_eps VARCHAR(45) NOT NULL,
    PRIMARY KEY(id_eps)
);

CREATE TABLE pacientes(
    id_paciente INT NOT NULL AUTO_INCREMENT,
    numero_identificacion VARCHAR(45) NOT NULL UNIQUE,
    nombre VARCHAR(45) NOT NULL,
    primer_apellido VARCHAR(45) NOT NULL,
    segundo_apellido VARCHAR(45) NULL,
    direccion VARCHAR(100),
    fecha_de_nacimiento DATE,
    id_eps_fk INT,
    id_regimen_fk INT,
    sexo ENUM('M','F'),
    tipo_sangre ENUM('A+','A-','B+','B-','O+','O-','AB+','AB-'),
    PRIMARY KEY(id_paciente),
    CONSTRAINT pacientes_eps_fk FOREIGN KEY(id_eps_fk) REFERENCES eps(id_eps),
    CONSTRAINT pacientes_regimenes_fk FOREIGN KEY(id_regimen_fk) REFERENCES regimenes(id_regimen)
);

CREATE TABLE historias_clinicas(
    id_historia_clinica INT NOT NULL AUTO_INCREMENT,
    resumen TEXT,
    fecha_apertura DATE,
    id_paciente_fk INT UNIQUE,
    antecedentes_personales TEXT,
    antecedentes_familiares TEXT,
    PRIMARY KEY(id_historia_clinica),

    CONSTRAINT historias_clinicas_pacientes_fk 
        FOREIGN KEY(id_paciente_fk) 
        REFERENCES pacientes(id_paciente)
);

CREATE TABLE medicos(
    id_medico INT NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(45) NOT NULL,
    primer_apellido VARCHAR(45) NOT NULL,
    segundo_apellido VARCHAR(45) NULL,
    tarjeta_profesional VARCHAR(100) NOT NULL UNIQUE,
    estado ENUM('Activo','Inactivo') DEFAULT 'Activo',
    PRIMARY KEY(id_medico)
);

CREATE TABLE contactos(
    id_contacto INT NOT NULL AUTO_INCREMENT,
    tipo ENUM('celular','fijo','email','whatsapp'),
    dato_contacto VARCHAR(100) NOT NULL,
    id_paciente_fk INT,
    id_medico_fk INT,
    PRIMARY KEY(id_contacto),
    CONSTRAINT contactos_pacientes_fk FOREIGN KEY(id_paciente_fk) REFERENCES pacientes(id_paciente),
    CONSTRAINT contactos_medicos_fk FOREIGN KEY(id_medico_fk) REFERENCES medicos(id_medico)
);

CREATE TABLE especialidades(
    id_especialidad INT NOT NULL AUTO_INCREMENT,
    nombre_especialidad VARCHAR(60) NOT NULL,
    descripcion VARCHAR(200) NULL,
    PRIMARY KEY(id_especialidad)
);

CREATE TABLE especialidades_medicos(
    id_medico_fk INT,
    id_especialidad_fk INT,
    PRIMARY KEY(id_medico_fk, id_especialidad_fk),
    CONSTRAINT especialidades_medicos_medicos_fk FOREIGN KEY(id_medico_fk) REFERENCES medicos(id_medico),
    CONSTRAINT especialidades_medicos_especialidades_fk FOREIGN KEY(id_especialidad_fk) REFERENCES especialidades(id_especialidad)
);

CREATE TABLE horarios_medicos(
    id_horario_medico INT NOT NULL AUTO_INCREMENT,
    dia_semana ENUM('Lunes','Martes','Miércoles','Jueves','Viernes','Sábado') NOT NULL,
    fecha_vigencia_inicio DATE NOT NULL,
    fecha_vigencia_fin DATE NULL,
    hora_inicial TIME NOT NULL,
    hora_final TIME NOT NULL,
    id_medico_fk INT,
    PRIMARY KEY(id_horario_medico),
    CONSTRAINT horarios_medicos_medicos_fk FOREIGN KEY(id_medico_fk) REFERENCES medicos(id_medico)
);

CREATE TABLE citas(
    id_cita INT NOT NULL AUTO_INCREMENT,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,    
    estado ENUM('Agendada','Cancelada','Atendida') DEFAULT 'Agendada',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    observacion VARCHAR(200),
    id_horario_medico_fk INT,
    id_paciente_fk INT,
    PRIMARY KEY(id_cita),
    CONSTRAINT citas_horarios_medicos_fk FOREIGN KEY(id_horario_medico_fk) REFERENCES horarios_medicos(id_horario_medico),
    CONSTRAINT citas_pacientes_fk FOREIGN KEY(id_paciente_fk) REFERENCES pacientes(id_paciente)
);

CREATE TABLE historial_citas(
    id_historial INT NOT NULL AUTO_INCREMENT,
    estado_anterior ENUM('Agendada','Cancelada','Atendida'),
    estado_nuevo ENUM('Agendada','Cancelada','Atendida'),
    fecha_cambio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    motivo VARCHAR(200),
    id_cita_fk INT,
    PRIMARY KEY(id_historial),
    CONSTRAINT historial_citas_fk FOREIGN KEY(id_cita_fk) REFERENCES citas(id_cita)
);

CREATE TABLE consultas(
    id_consulta INT NOT NULL AUTO_INCREMENT,
    observacion TEXT,
    diagnostico TEXT,
    id_cita_fk INT UNIQUE,
    id_historia_clinica_fk INT,
    PRIMARY KEY(id_consulta),
    CONSTRAINT consultas_citas_fk FOREIGN KEY(id_cita_fk) REFERENCES citas(id_cita),
    CONSTRAINT consultas_historias_clinicas_fk FOREIGN KEY(id_historia_clinica_fk) REFERENCES historias_clinicas(id_historia_clinica)
);

CREATE TABLE servicios(
    id_servicio INT NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    PRIMARY KEY(id_servicio)
);

CREATE TABLE consultas_servicios(
    id_servicio_fk INT,
    id_consulta_fk INT,
    PRIMARY KEY(id_servicio_fk, id_consulta_fk),
    CONSTRAINT consultas_servicios_servicios_fk FOREIGN KEY(id_servicio_fk) REFERENCES servicios(id_servicio),
    CONSTRAINT consultas_servicios_consultas_fk FOREIGN KEY(id_consulta_fk) REFERENCES consultas(id_consulta)
);

CREATE TABLE usuarios(
    id_usuario INT NOT NULL AUTO_INCREMENT,
    usuario VARCHAR(45) NOT NULL UNIQUE,
    contrasena VARCHAR(255) NOT NULL,
    rol ENUM('Administrativo','Medico') NOT NULL,
    estado ENUM('Activo','Inactivo') DEFAULT 'Activo',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_medico_fk INT NULL,
    PRIMARY KEY(id_usuario),
    CONSTRAINT usuarios_medicos_fk  FOREIGN KEY(id_medico_fk) REFERENCES medicos(id_medico));


CREATE TABLE signos_vitales(
   id_signo INT NOT NULL AUTO_INCREMENT,
   peso DECIMAL(5,2),
   estatura DECIMAL(4,2),
   temperatura DECIMAL(4,1),
   presion_arterial VARCHAR(10),
   frecuencia_cardiaca DECIMAL(5,2),
   saturacion_oxigeno DECIMAL(5,2),
   fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   id_historia_clinica_fk INT NOT NULL,
   id_consulta_fk INT,

   PRIMARY KEY(id_signo),

   CONSTRAINT signos_vitales_consulta_fk
      FOREIGN KEY(id_consulta_fk)
      REFERENCES consultas(id_consulta),

   CONSTRAINT signos_vitales_historia_fk
      FOREIGN KEY(id_historia_clinica_fk)
      REFERENCES historias_clinicas(id_historia_clinica)
);
 
 CREATE TABLE paciente_alergias(
    id INT NOT NULL AUTO_INCREMENT,
    id_paciente_fk INT NOT NULL,
    alergia VARCHAR(255) NOT NULL,
    PRIMARY KEY(id),

    CONSTRAINT paciente_alergias_ibfk_1
        FOREIGN KEY(id_paciente_fk)
        REFERENCES pacientes(id_paciente)
);