from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .config.database import init_db
from .controllers import auth_controller, links_controller, categories_controller

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Iniciando servidor...")
    init_db()
    print("✅ Banco de dados inicializado!")
    yield
    print("👋 Encerrando servidor...")

app = FastAPI(
    title="DevLink API",
    description="API para gerenciamento de links de desenvolvimento",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_controller.router)
app.include_router(links_controller.router)
app.include_router(categories_controller.router)

@app.get("/")
def root():
    return {
        "message": "DevLink API está rodando! 🚀",
        "docs": "/docs",
        "version": "1.0.0"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "database": "connected"}