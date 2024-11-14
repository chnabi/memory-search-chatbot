# builtin 
import random 
import time
import asyncio
from contextlib import asynccontextmanager

# external  
from pinecone import Pinecone 
from fastapi import FastAPI 
from openai import AsyncOpenAI, completions
from fastapi.middleware.cors import CORSMiddleware

# internal 
from src.globals.environment import Environment 
from src.api.conversation.routes import chatter_router
from src.modules.chatter import BrainModule

def setup_clients(app: FastAPI): #always call through app.state
    environment: Environment = app.state.environment 
    openai_client: AsyncOpenAI = AsyncOpenAI(api_key= app.state.environment.OPENAI_KEY)
    app.state.openai_client = openai_client 
    pc_client: Pinecone = Pinecone(api_key=app.state.environment.PINECONE_KEY)
    app.state.pc_client = pc_client 
    index = app.state.pc_client.Index(name = "memory-chatbot", host="https://chatbot-deliv.vercel.app/")

def setup_globals(app:FastAPI):
    enviornment: Environment = Environment()
    app.state.environment =enviornment
    

def setup_modules(app: FastAPI): 
    chatter_module:BrainModule = BrainModule(openai_client=app.state.openai_client, pc_client=app.state.pc_client)
    app.state.chatter_module =chatter_module

@asynccontextmanager
async def lifespan(app: FastAPI):
    # setup
    setup_globals(app =app)
    setup_clients(app=app)
    setup_modules(app=app)
    yield  

app: FastAPI = FastAPI(lifespan=lifespan)

origins = [
    "https://chatbot-deliv.vercel.app/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)

app.include_router(chatter_router)



