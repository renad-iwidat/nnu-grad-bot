import sys
sys.path.append('.')

from rag.indexing_pipeline import IndexingPipeline
from rag.data_loader import DataLoader
from rag.embedding_storage import EmbeddingStorage

def main():
    print("Najah Graduate Studies Chatbot - Data Indexing")
    print("=" * 60)
    
    data_loader = DataLoader()
    total_html = data_loader.get_total_html_pages()
    total_pdf = data_loader.get_total_pdf_files()
    
    print(f"Total HTML pages in database: {total_html}")
    print(f"Total PDF files in database: {total_pdf}")
    print(f"Current embeddings count: {EmbeddingStorage.get_embeddings_count()}")
    print("=" * 60)
    
    choice = input("Do you want to index all data? (yes/no): ").strip().lower()
    
    if choice != 'yes':
        print("Indexing cancelled.")
        return
    
    pipeline = IndexingPipeline(chunk_size=1000, chunk_overlap=200)
    
    pipeline.index_all_data()
    
    print("=" * 60)
    print(f"Final embeddings count: {EmbeddingStorage.get_embeddings_count()}")

if __name__ == "__main__":
    main()
