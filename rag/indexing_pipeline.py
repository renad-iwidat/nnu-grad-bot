from rag.data_loader import DataLoader
from rag.text_chunker import TextChunker
from rag.embedding_generator import EmbeddingGenerator
from rag.embedding_storage import EmbeddingStorage

class IndexingPipeline:
    
    def __init__(self, chunk_size=1000, chunk_overlap=200):
        self.data_loader = DataLoader()
        self.text_chunker = TextChunker(chunk_size, chunk_overlap)
        self.embedding_generator = EmbeddingGenerator()
        self.embedding_storage = EmbeddingStorage()
    
    def index_html_pages(self, limit=None):
        print("Loading HTML pages from database...")
        html_pages = self.data_loader.load_html_pages(limit)
        print(f"Loaded {len(html_pages)} HTML pages")
        
        print("Chunking HTML pages...")
        all_chunks = []
        for idx, page in enumerate(html_pages, 1):
            page_id, title, content, language, url, scraped_at = page
            print(f"Chunking page {idx}: {title[:50] if title else 'No title'}...")
            
            try:
                chunks = self.text_chunker.chunk_html_page(page)
                all_chunks.extend(chunks)
                print(f"  Created {len(chunks)} chunks")
            except Exception as e:
                print(f"  Error chunking page {page_id}: {str(e)}")
                continue
        
        print(f"Total chunks created: {len(all_chunks)}")
        
        print("Generating embeddings...")
        texts = [chunk['content'] for chunk in all_chunks]
        embeddings = self.embedding_generator.generate_embeddings_batch(texts)
        
        print("Storing embeddings in database...")
        success, failed = self.embedding_storage.store_embeddings_batch(all_chunks, embeddings)
        print(f"Stored {success} embeddings successfully, {failed} failed")
        
        return success, failed
    
    def index_pdf_files(self, limit=None):
        print("Loading PDF files from database...")
        pdf_files = self.data_loader.load_pdf_files(limit)
        print(f"Loaded {len(pdf_files)} PDF files")
        
        print("Chunking PDF files...")
        all_chunks = []
        for idx, pdf in enumerate(pdf_files, 1):
            pdf_id, file_name, extracted_text, total_pages, url, downloaded_at = pdf
            print(f"Chunking PDF {idx}: {file_name[:50] if file_name else 'No name'}...")
            
            try:
                chunks = self.text_chunker.chunk_pdf_file(pdf)
                all_chunks.extend(chunks)
                print(f"  Created {len(chunks)} chunks")
            except Exception as e:
                print(f"  Error chunking PDF {pdf_id}: {str(e)}")
                continue
        
        print(f"Total chunks created: {len(all_chunks)}")
        
        print("Generating embeddings...")
        texts = [chunk['content'] for chunk in all_chunks]
        embeddings = self.embedding_generator.generate_embeddings_batch(texts)
        
        print("Storing embeddings in database...")
        success, failed = self.embedding_storage.store_embeddings_batch(all_chunks, embeddings)
        print(f"Stored {success} embeddings successfully, {failed} failed")
        
        return success, failed
    
    def index_all_data(self, html_limit=None, pdf_limit=None):
        print("Starting full indexing pipeline...")
        print("=" * 50)
        
        html_success, html_failed = self.index_html_pages(html_limit)
        print("=" * 50)
        
        pdf_success, pdf_failed = self.index_pdf_files(pdf_limit)
        print("=" * 50)
        
        total_success = html_success + pdf_success
        total_failed = html_failed + pdf_failed
        
        print(f"Indexing complete!")
        print(f"Total embeddings stored: {total_success}")
        print(f"Total failed: {total_failed}")
        
        return total_success, total_failed
