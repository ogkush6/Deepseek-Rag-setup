
# src/rag_engine.py
import ollama
from typing import List, Dict
from .embeddings import VectorStore

class RAGEngine:
    def __init__(self, vector_store: VectorStore, model_name: str = "deepseek-r1:7b"):
        self.vector_store = vector_store
        self.model_name = model_name
        
        # Test Ollama connection
        try:
            ollama.list()
        except Exception as e:
            raise RuntimeError(f"Failed to connect to Ollama. Is it running? Error: {e}")
        
    def get_context(self, query: str, k: int = 3) -> str:
        results = self.vector_store.search(query, k=k)
        if not results['documents'][0]:
            return "No relevant context found in the documents."
            
        contexts = []
        for doc, metadata in zip(results['documents'][0], results['metadatas'][0]):
            source = metadata.get('source', 'Unknown source')
            contexts.append(f"From {source}:\n{doc}")
            
        return "\n\n---\n\n".join(contexts)
        
    async def generate_response(self, query: str) -> str:
        try:
            print ("Getting Context")
            context = self.get_context(query)
            print (f"context received: {context[:1000]}...")


            # prompt = f"""You are a helpful assistant with access to specific document contents.
            #             Use ONLY the following context to answer the question. If the context doesn't contain
            #             relevant information, say so. Do not make up information.
            prompt = f"""You are a helpful assistant. If the provided context is relevant to the question, 
                        use it to answer. If the question is general and doesn't require the context, you can answer based 
                        on your general knowledge.

                        Context:
                        {context}

                        Question: {query}

                        :"""

            try:
                print(f"Attempting to call ollama with model: {self.model_name}")
                response = ollama.chat(
                    model=self.model_name,
                    messages=[
                        {
                            'role': 'system',
                            'content': 'You are a helpful assistant that answers questions based only on the provided context.'
                        },
                        {
                            'role': 'user',
                            'content': prompt
                        }
                    ],
                    options={
                        'temperature': 0.7,
                        'top_k': 10,
                        'top_p': 0.95,
                    }
                )
                
             #   return response['message']['content']
                return {
                'content': response['message']['content'],
                'metrics': {
                    'total_duration': response.get('total_duration'),
                    'load_duration': response.get('load_duration'),
                    'prompt_eval_count': response.get('prompt_eval_count'),
                    'eval_count': response.get('eval_count'),
                    'eval_duration': response.get('eval_duration')
                }
            }
                
            except Exception as e:
                error_msg = f"Error generating response: {str(e)}"
                print(error_msg)
                return f"I encountered an error while processing your query. Please ensure Ollama is running and the model '{self.model_name}' is available."
    
        except Exception as e:
            error_msg = f"Error generating response: {str(e)}"
            print(error_msg)
            return error_msg