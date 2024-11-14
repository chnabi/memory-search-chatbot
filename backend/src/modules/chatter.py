# builtin 
import time 
# external 
from fastapi import APIRouter,Request
from openai import AsyncOpenAI
from pinecone import Pinecone 
# internal 
from src.models import  QueryGPTInput, Message, EmbedIntoPinconeInput, Embedding, PineconeEmbeddings, UpsertInput, MemorizeInput, RespondToChatOutput, MemorizeOutput

class BrainModule: 
    def __init__(self, openai_client: AsyncOpenAI, pc_client: Pinecone): 
        self.openai_client = openai_client 
        self.pc_client = pc_client
        self.index = pc_client.Index(name = "memory-chatbot", host="https://memory-chatbot-4j6ue9i.svc.aped-4627-b74a.pinecone.io")

    async def upsert_into_pincone(self, input: UpsertInput):
        vectors = []  
        for d,e in zip(input.data, input.embeddings):
            vectors.append({
                "id":str(time.time()),
                "values": e,
                "metadata": {'text': d}
            })      
        self.index.upsert(
        vectors=vectors,
        namespace="ns1"
        )
        
    async def query_chatgpt(self, prompt: QueryGPTInput):
        completion = await self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=prompt.messages
        )
        gpt_output: str = completion.choices[0].message.content 
        return gpt_output

    async def embed_into_pinecone(self, docs: EmbedIntoPinconeInput) -> PineconeEmbeddings:
        res = await self.openai_client.embeddings.create(
            input= docs.data,
            model = "text-embedding-ada-002"
        )
        doc_embeds =[r.embedding for r in res.data]
        output: PineconeEmbeddings = PineconeEmbeddings(embeddings=doc_embeds)
        return output

    async def query_pinecone(self, query: str) -> list[dict[str,str]]:
        data: EmbedIntoPinconeInput = EmbedIntoPinconeInput(data= [query])
        embeddings:PineconeEmbeddings = await self.embed_into_pinecone(data)
        results = self.index.query(
            namespace="ns1",
            vector=embeddings.embeddings[0],
            top_k=3,
            include_values=False,
            include_metadata=True
        )
        texts = [r['metadata']['text'] for r in results['matches']]
        context_pieces: list[dict[str,str]] = [{'role': 'system', 'content': text} for text in texts]
        # output: dict[str,str] ={'role':'system', 'content':texts[0]}
        return context_pieces
    
    async def handle_chat(self, chat_input: str): 
        prompt: list[dict[str,str]] = await self.query_pinecone(chat_input)
        msg: dict[str,str] = {'role':'user', 'content':chat_input}
        print(msg['content'])
        prompt.append(msg)
        gpt_prompt: QueryGPTInput = QueryGPTInput(messages=prompt)
        response:str  = await self.query_chatgpt(gpt_prompt)
        print(response)
        bot_response: RespondToChatOutput = RespondToChatOutput(response=response)
        return bot_response
    
    async def handle_memorize(self, memorize_input: list[str]):
        data_to_embed: EmbedIntoPinconeInput = EmbedIntoPinconeInput(data=memorize_input)
        embeds: PineconeEmbeddings = await self.embed_into_pinecone(data_to_embed)
        data_to_upsert: UpsertInput =UpsertInput(data=memorize_input, embeddings=embeds.embeddings)
        await self.upsert_into_pincone(data_to_upsert)
        return_status:MemorizeOutput = MemorizeOutput(status="Memory Updated")
        return return_status
   
