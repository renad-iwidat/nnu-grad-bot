from database.queries import DatabaseQueries
from rag.embedding_generator import EmbeddingGenerator

class RetrievalEngine:
    
    def __init__(self, top_k=5):
        self.embedding_generator = EmbeddingGenerator()
        self.top_k = top_k
    
    def search_similar_chunks(self, query_text, top_k=None):
        if top_k is None:
            top_k = self.top_k
        
        query_embedding = self.embedding_generator.generate_embedding(query_text)
        
        if query_embedding is None:
            return []
        
        query_vector = str(query_embedding)
        
        search_query = """
        SELECT 
            id,
            content,
            source_type,
            source_id,
            source_url,
            source_title,
            chunk_index,
            1 - (embedding <=> %s::vector) as similarity
        FROM embeddings
        ORDER BY embedding <=> %s::vector
        LIMIT %s
        """
        
        results = DatabaseQueries.execute_query(
            search_query, 
            (query_vector, query_vector, top_k)
        )
        
        formatted_results = []
        for row in results:
            formatted_results.append({
                'id': row[0],
                'content': row[1],
                'source_type': row[2],
                'source_id': row[3],
                'source_url': row[4],
                'source_title': row[5],
                'chunk_index': row[6],
                'similarity': float(row[7])
            })
        
        return formatted_results
    
    def get_context_from_results(self, results):
        context_parts = []
        
        for idx, result in enumerate(results, 1):
            source_info = f"Source {idx}: {result['source_title']}"
            if result['source_url']:
                source_info += f" ({result['source_url']})"
            
            context_parts.append(f"{source_info}\n{result['content']}")
        
        return "\n\n---\n\n".join(context_parts)
