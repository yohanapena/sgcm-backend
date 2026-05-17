import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.shared.exceptions.handlers import registrar_handlers



app = FastAPI(
    title="SGCM Backend",
    description="Backend del Gestor de Citas Médicas",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL", "*")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

registrar_handlers(app)


@app.get("/", tags=["salud"])
def read_root():
    return {"success": True, "message": "SGCM Backend está funcionando"}


# Routers de los módulos principales.
from app.modules.auth.routes import router as auth_router
from app.modules.usuarios.routes import router as usuarios_router

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(usuarios_router, prefix="/usuarios", tags=["usuarios"])

# from app.modules.pacientes.routes import router as pacientes_router
# app.include_router(pacientes_router, prefix="/pacientes", tags=["pacientes"])

# from app.modules.historias_clinicas.routes import router as historias_clinicas_router
# app.include_router(historias_clinicas_router, prefix="/historias_clinicas", tags=["historias_clinicas"])

# from app.modules.signos_vitales.routes import router as signos_vitales_router
# app.include_router(signos_vitales_router, prefix="/signos_vitales", tags=["signos_vitales"])

# from app.modules.medicos.routes import router as medicos_router
# app.include_router(medicos_router, prefix="/medicos", tags=["medicos"])

# from app.modules.citas.routes import router as citas_router
# app.include_router(citas_router, prefix="/citas", tags=["citas"])

# from app.modules.consultas.routes import router as consultas_router
# app.include_router(consultas_router, prefix="/consultas", tags=["consultas"])
