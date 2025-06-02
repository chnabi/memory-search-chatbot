## Memory Search Chatbot — Personalized RAG System with Pinecone
A personal chatbot built using a Retrieval-Augmented Generation (RAG) pipeline that lets users ask questions and get responses grounded in their own past notes and reflections. 
### Key Features:
  -Personal Context Retrieval: Stores journal-style entries in a Pinecone vector database for fast semantic search.
  
  -RAG Architecture: Combines vector retrieval with a language model to generate responses using relevant personal context.
  
  -Use Case: Acts like a digital memory — useful for recalling past thoughts, tracking progress, or just reflecting over time.

### Tech Stack:
  -Pinecone for vector search
  
  -OpenAI embeddings + GPT for retrieval and generation
  
  -Python backend with basic API integration using FastAPI

Built as for learning and improving skills while combining LLMs with personal knowledge management — and as a step toward making chatbots more genuinely useful and personalized.
