from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from fastapi.middleware.trustedhost import TrustedHostMiddleware

from fastapi.middleware.cors import CORSMiddleware
from app.config import settings

from app.core.templates import templates


app = FastAPI()

'''@app.get("/")
def home():
    return "hi"'''

#Templates (app/templates)
# templates = Jinja2Templates(directory="app/templates")
#Archivos estaticos desde app/statics
app.mount("/static", StaticFiles(directory="app/static"), name="static")

    ######CORS##########

#middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],   
    allow_headers=["*"],            
)

#Headers de seguridad
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"]) #cambiar en produccion: secure=True - en cookies.

#Importar routers
from app.routers.auth_router import router as auth_router
from app.routers.school_router import router as school_router
from app.routers.posts_router import router as posts_router
from app.routers.views_index_router import router as views_index_router
from app.routers.post_views_router import router as post_views_router


app.include_router(auth_router)
app.include_router(school_router)
app.include_router(posts_router)
app.include_router(views_index_router)
app.include_router(post_views_router)



 
