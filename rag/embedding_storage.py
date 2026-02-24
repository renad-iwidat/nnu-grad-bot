from database.queries import DatabaseQueries

class EmbeddingStorage:
    
    @staticmethod
    def store_embedding(chunk_data, embedding):
        query = """
        INSERT INTO embeddings 
        (content, embedding, source_type, source_id, source_url, source_title, chunk_index)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING id
        """
        
        params = (
            chunk_data['content'],
            str(embedding),
            chunk_data['source_type'],
            chunk_data['source_id'],
            chunk_data['source_url'],
            chunk_data['source_title'],
            chunk_data['chunk_index']
        )
        
        result = DatabaseQueries.execute_query(query, params, fetch=False)
        return result
    
    @staticmethod
    def store_embeddings_batch(chunks_data, embeddings):
        success_count = 0
        failed_count = 0
        
        for chunk_data, embedding in zip(chunks_data, embeddings):
            if embedding is None:
                failed_count += 1
                continue
            
            try:
                EmbeddingStorage.store_embedding(chunk_data, embedding)
                success_count += 1
            except Exception as e:
                print(f"Error storing embedding: {str(e)}")
                failed_count += 1
        
        return success_count, failed_count
    
    @staticmethod
    def get_embeddings_count():
        query = "SELECT COUNT(*) FROM embeddings"
        result = DatabaseQueries.execute_query(query)
        return result[0][0] if result else 0
    
    @staticmethod
    def clear_all_embeddings():
        query = "DELETE FROM embeddings"
        return DatabaseQueries.execute_query(query, fetch=False)
