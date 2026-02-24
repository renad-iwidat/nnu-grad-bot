import sys
sys.path.append('.')

from rag.retrieval_engine import RetrievalEngine

def debug_search(query):
    print(f"Query: {query}")
    print("=" * 80)
    
    retrieval = RetrievalEngine(top_k=3)
    results = retrieval.search_similar_chunks(query)
    
    for idx, result in enumerate(results, 1):
        print(f"\n[Result {idx}]")
        print(f"Similarity: {result['similarity']:.4f}")
        print(f"Source: {result['source_title']}")
        print(f"Type: {result['source_type']}")
        print(f"Content preview (first 500 chars):")
        print("-" * 80)
        print(result['content'][:500])
        print("-" * 80)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = "ما هي شروط القبول في الماجستير؟"
    
    debug_search(query)
