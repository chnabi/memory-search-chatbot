#builtin 


#external  
from pydantic import BaseModel 

#internal 

class ConversationChatInput(BaseModel): 
    input: str

class EmbeddingOutput(BaseModel): 
    embedding: list[float]

class TextData(BaseModel): 
    id: str
    value: str

class UpsertInput(BaseModel): 
    data: list[str]
    embeddings: list[list[float]]

class Message(BaseModel):
    role: str
    content: str

class QueryGPTInput(BaseModel):
    messages: list[dict[str,str]]

class EmbedIntoPinconeInput(BaseModel):
    data: list[str]

class Embedding(BaseModel):
    embedding: list[float]

class PineconeEmbeddings(BaseModel):
    embeddings: list[list[float]]

class MemorizeInput(BaseModel):
    data: list[str]

class RespondToChatOutput(BaseModel):
    response: str

class MemorizeOutput(BaseModel): 
    status: str





