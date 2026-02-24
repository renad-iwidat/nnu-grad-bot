from openai import OpenAI
from config.openai_config import OPENAI_EMBEDDING_KEY, EMBEDDING_MODEL

class EmbeddingGenerator:
    
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_EMBEDDING_KEY)
        self.model = EMBEDDING_MODEL
    
    def generate_embedding(self, text):
        try:
            response = self.client.embeddings.create(
                input=text,
                model=self.model
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"Error generating embedding: {str(e)}")
            return None
    
    def generate_embeddings_batch(self, texts, batch_size=100):
        embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            
            try:
                response = self.client.embeddings.create(
                    input=batch,
                    model=self.model
                )
                
                batch_embeddings = [item.embedding for item in response.data]
                embeddings.extend(batch_embeddings)
                
                print(f"Processed {min(i + batch_size, len(texts))}/{len(texts)} embeddings")
                
            except Exception as e:
                print(f"Error in batch {i}-{i+batch_size}: {str(e)}")
                embeddings.extend([None] * len(batch))
        
        return embeddings
