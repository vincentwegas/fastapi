#Create Virtual VENV
# py -3 -m venv venv

#Activate VENV in Terminal
#venv\Scripts\activate.bat 

#install fastapi
# pip install fastapi[all]

#install sqlalchemy
#pip install sqlalchemy

#check pip installations 
#pip freeze

from fastapi import FastAPI, APIRouter
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import Settings
from fastapi.middleware.cors import CORSMiddleware



router = APIRouter()



#models.Base.metadata.create_all(bind=engine)

#set up FastAPI
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "Hello World my Friend!!!!"}

@router.get("/login")
def login():
    return {"message": "Please Login"}

#Start webserver
#uvicorn app.main:app --reload


#See the Docs by Swagger UI
#http://127.0.0.1:8000/docs

#See the Docs by Redoc
#http://127.0.0.1:8000/redoc