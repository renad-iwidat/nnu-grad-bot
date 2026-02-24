from database.queries import DatabaseQueries

class DataLoader:
    
    @staticmethod
    def load_html_pages(limit=None):
        query = """
        SELECT 
            hp.id,
            hp.title,
            hp.content,
            hp.language,
            u.url,
            hp.scraped_at
        FROM html_pages hp
        JOIN urls u ON hp.url_id = u.id
        WHERE hp.content IS NOT NULL AND hp.content != ''
        """
        if limit:
            query += f" LIMIT {limit}"
        
        return DatabaseQueries.execute_query(query)
    
    @staticmethod
    def load_pdf_files(limit=None):
        query = """
        SELECT 
            pf.id,
            pf.file_name,
            pf.extracted_text,
            pf.total_pages,
            u.url,
            pf.downloaded_at
        FROM pdf_files pf
        JOIN urls u ON pf.url_id = u.id
        WHERE pf.extracted_text IS NOT NULL AND pf.extracted_text != ''
        """
        if limit:
            query += f" LIMIT {limit}"
        
        return DatabaseQueries.execute_query(query)
    
    @staticmethod
    def get_total_html_pages():
        query = "SELECT COUNT(*) FROM html_pages WHERE content IS NOT NULL"
        result = DatabaseQueries.execute_query(query)
        return result[0][0] if result else 0
    
    @staticmethod
    def get_total_pdf_files():
        query = "SELECT COUNT(*) FROM pdf_files WHERE extracted_text IS NOT NULL"
        result = DatabaseQueries.execute_query(query)
        return result[0][0] if result else 0
