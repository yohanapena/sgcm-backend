# 🏥 SGCM — Backend | Sistema Gestor de Citas Médicas

API REST para el Sistema Gestor de Citas Médicas de hospitales de nivel I. Maneja autenticación, gestión de pacientes, médicos, citas, consultas e historias clínicas con control de acceso por roles.

> Proyecto académico — Universidad Industrial de Santander  
> Facultad de Ingenierías Físico-Mecánicas — Abril 2026

**Autores:**
- Andrea Yohana Peña Peña — 2245625
- Yulieth Vanesa Rojas Cáceres — 2245617
- Yefferson Andrey López Pita — 2245511

**Docente:** Fabián Ferney Roa Prada

---

## 🔗 Repositorios del proyecto

| Parte | Link |
|-------|------|
| ⚙️ Backend (este repo) | `https://github.com/yohanapena/sgcm-backend.git` |
| 🎨 Frontend | `https://github.com/yohanapena/sgcm_frontend.git` |

---

## 🛠️ Tecnologías

- **Lenguaje:** Python
- **Framework:** FastAPI
- **Servidor:** Uvicorn
- **Base de datos:** MySQL (mysql-connector-python con pooling)
- **Autenticación:** JWT (PyJWT) + bcrypt
- **Validación:** Pydantic
- **Variables de entorno:** python-dotenv

---

## 🏗️ Arquitectura

Organización por módulos con separación en capas:

```
Routes → Service → Repository → Model/Schema
```

```
backend/
├── app/
│   ├── main.py
│   ├── core/           # database, security, dependencies
│   ├── modules/        # auth, pacientes, medicos, citas, consultas,
│   │                   # historias_clinicas, signos_vitales, catalogos
│   ├── shared/         # exceptions, responses, utils
│   └── tests/
├── migrations/
├── scripts/            # seed_all.py
└── requirements.txt
```

---

## 🚀 Instalación y ejecución

```bash
# 1. Crear y activar entorno virtual
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar variables de entorno (ver sección .env)

# 4. Ejecutar el servidor
uvicorn app.main:app --reload
```

Servidor disponible en: `http://localhost:8000`  
Documentación automática en: `http://localhost:8000/docs`

---

## 🔑 Variables de entorno

Crear un archivo `.env` en la raíz del proyecto:

```env
# Base de datos
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=tu_contraseña
DB_NAME=sistema_citas_medicas

# JWT
JWT_SECRET_KEY=tu_clave_secreta
JWT_ALGORITHM=HS256
JWT_EXPIRES_MINUTES=60

# CORS
FRONTEND_URL=http://localhost:5500
```

---

## 📡 Endpoints principales

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/auth/login` | Iniciar sesión |
| GET | `/auth/me` | Usuario autenticado |
| GET/POST | `/pacientes` | Listar / registrar pacientes |
| GET/POST | `/medicos` | Listar / registrar médicos |
| POST | `/medicos/{id}/horarios` | Agregar horario a médico |
| GET/POST | `/citas` | Listar / agendar citas |
| PUT | `/citas/{id}/cancelar` | Cancelar cita |
| POST | `/consultas` | Registrar consulta médica |
| GET | `/consultas/historia-clinica/paciente/{id}` | Historia clínica del paciente |
| GET | `/signos_vitales` | Signos vitales |
| GET | `/dashboard/admin/summary` | Resumen administrativo |

---

## 🗄️ Base de datos

**Motor:** MySQL 8.0+  
**Nombre:** `sistema_citas_medicas`

### Importar desde MySQL Workbench

1. Ir a **Server → Data Import**
2. Seleccionar el archivo `script_gestor_de_citas_version_3.sql`
3. Ejecutar

### Importar desde terminal

```bash
mysql -u root -p < script_gestor_de_citas_version_3.sql
```

### Tablas

`regimenes` · `eps` · `pacientes` · `historias_clinicas` · `medicos` · `contactos` · `especialidades` · `especialidades_medicos` · `horarios_medicos` · `citas` · `historial_citas` · `consultas` · `servicios` · `consultas_servicios` · `usuarios` · `signos_vitales` · `paciente_alergias`

---

## 👥 Roles del sistema

| Rol | Acceso |
|-----|--------|
| Administrativo | Pacientes, médicos, horarios, citas |
| Médico | Sus citas, consultas, historia clínica |
| Administrador del Sistema | Usuarios y roles |

---

## 🚀 Orden de ejecución recomendado

1. Importar la base de datos en MySQL
2. Configurar el `.env` y ejecutar el backend
3. Abrir el frontend en el navegador