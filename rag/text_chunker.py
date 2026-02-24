class TextChunker:
    
    def __init__(self, chunk_size=1000, chunk_overlap=200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def chunk_text(self, text):
        if not text or len(text.strip()) == 0:
            return []
        
        text = text.strip()
        text_length = len(text)
        
        if text_length <= self.chunk_size:
            return [text]
        
        chunks = []
        position = 0
        
        while position < text_length:
            chunk_end = position + self.chunk_size
            
            if chunk_end >= text_length:
                chunk = text[position:].strip()
                if chunk and len(chunk) > 50:
                    chunks.append(chunk)
                break
            
            last_period = text.rfind('.', position, chunk_end)
            last_newline = text.rfind('\n', position, chunk_end)
            
            if last_period > position + 100:
                chunk_end = last_period + 1
            elif last_newline > position + 100:
                chunk_end = last_newline + 1
            
            chunk = text[position:chunk_end].strip()
            if chunk and len(chunk) > 50:
                chunks.append(chunk)
            
            position = chunk_end - self.chunk_overlap
            
            if position <= len(chunks) * 10:
                position = chunk_end
        
        return chunks
    
    def chunk_html_page(self, page_data):
        page_id, title, content, language, url, scraped_at = page_data
        
        full_text = f"{title}\n\n{content}" if title else content
        
        print(f"Chunking page {page_id}: {title[:50] if title else 'No title'}...")
        
        chunks = self.chunk_text(full_text)
        
        chunked_data = []
        for index, chunk in enumerate(chunks):
            chunked_data.append({
                'content': chunk,
                'source_type': 'html_page',
                'source_id': page_id,
                'source_url': url,
                'source_title': title,
                'chunk_index': index,
                'metadata': {
                    'language': language,
                    'scraped_at': str(scraped_at) if scraped_at else None
                }
            })
        
        print(f"Created {len(chunked_data)} chunks for page {page_id}")
        
        return chunked_data
    
    def chunk_pdf_file(self, pdf_data):
        pdf_id, file_name, extracted_text, total_pages, url, downloaded_at = pdf_data
        
        chunks = self.chunk_text(extracted_text)
        
        chunked_data = []
        for index, chunk in enumerate(chunks):
            chunked_data.append({
                'content': chunk,
                'source_type': 'pdf_file',
                'source_id': pdf_id,
                'source_url': url,
                'source_title': file_name,
                'chunk_index': index,
                'metadata': {
                    'total_pages': total_pages,
                    'downloaded_at': str(downloaded_at) if downloaded_at else None
                }
            })
        
        return chunked_data
