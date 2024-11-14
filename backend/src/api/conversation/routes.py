# builtin 
import time 
# external 
from fastapi import APIRouter,Request
from openai import AsyncOpenAI
from pinecone import Pinecone 
# internal 
from src.models import ConversationChatInput, QueryGPTInput, Message, EmbedIntoPinconeInput, Embedding, PineconeEmbeddings, UpsertInput, MemorizeInput, RespondToChatOutput, MemorizeOutput
from src.modules.chatter import BrainModule



chatter_router: APIRouter = APIRouter(prefix="/conversation", tags=["conversation"])
        
@chatter_router.post('/chat', response_model=RespondToChatOutput) 
async def chat(user_input:ConversationChatInput, request:Request) -> RespondToChatOutput:
    chatter_module: BrainModule = request.app.state.chatter_module
    response_model: RespondToChatOutput = await chatter_module.handle_chat(user_input.input)
    return response_model

    
@chatter_router.post('/memorize', response_model=MemorizeOutput)
async def memorize_new_info(data_to_memorize: MemorizeInput, request:Request):
    chatter_module: BrainModule = request.app.state.chatter_module
    response_model: MemorizeOutput = await chatter_module.handle_memorize(data_to_memorize.data)
    return response_model