import sys
sys.path.append('.')

from rag.query_pipeline import QueryPipeline
import json

def print_separator():
    print("=" * 80)

def print_answer(response):
    print_separator()
    print(f"Question: {response['question']}")
    print_separator()
    print(f"\nAnswer:\n{response['answer']}\n")
    
    if response.get('sources'):
        print_separator()
        print("Sources:")
        for source in response['sources']:
            print(f"\n{source['label']}")
            print(f"  Title: {source['title']}")
            if source.get('url'):
                print(f"  URL: {source['url']}")
            print(f"  Type: {source['type']}")
            if source.get('similarity'):
                print(f"  Similarity: {source['similarity']:.4f}")
    
    print_separator()

def interactive_mode():
    print("Najah Graduate Studies Chatbot - Interactive Mode")
    print_separator()
    print("Commands:")
    print("  - Type your question and press Enter")
    print("  - Type 'clear' to clear conversation history")
    print("  - Type 'exit' or 'quit' to exit")
    print_separator()
    
    pipeline = QueryPipeline(top_k=8)
    
    while True:
        try:
            question = input("\nYour question: ").strip()
            
            if not question:
                continue
            
            if question.lower() in ['exit', 'quit']:
                print("Goodbye!")
                break
            
            if question.lower() == 'clear':
                pipeline.clear_conversation()
                print("Conversation history cleared.")
                continue
            
            response = pipeline.query(question)
            print_answer(response)
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {str(e)}")

def single_query_mode(question, debug=False):
    print("Najah Graduate Studies Chatbot - Single Query Mode")
    print_separator()
    
    pipeline = QueryPipeline(top_k=8)
    response = pipeline.query(question, include_context=False, debug=debug)
    print_answer(response)

def main():
    debug = '--debug' in sys.argv
    if debug:
        sys.argv.remove('--debug')
    
    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
        single_query_mode(question, debug=debug)
    else:
        interactive_mode()

if __name__ == "__main__":
    main()
