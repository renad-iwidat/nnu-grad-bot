from rag.retrieval_engine import RetrievalEngine
from rag.answer_generator import AnswerGenerator
from rag.intent_classifier import IntentClassifier

class QueryPipeline:
    
    def __init__(self, top_k=10):
        self.retrieval_engine = RetrievalEngine(top_k=top_k)
        self.answer_generator = AnswerGenerator()
        self.conversation_history = []
    
    def query(self, question, include_context=False, debug=False):
        if IntentClassifier.is_out_of_scope(question):
            return {
                'question': question,
                'answer': IntentClassifier.GENERAL_RESPONSES['out_of_scope'],
                'sources': [],
                'search_results_count': 0,
                'is_out_of_scope': True
            }
        
        if IntentClassifier.is_general_question(question):
            general_response = IntentClassifier.get_general_response(question)
            return {
                'question': question,
                'answer': general_response,
                'sources': [],
                'search_results_count': 0,
                'is_general': True
            }
        
        print(f"Question: {question}")
        print("Searching for relevant information...")
        
        search_results = self.retrieval_engine.search_similar_chunks(question)
        
        if not search_results:
            result = self.answer_generator.generate_answer_with_sources(question, search_results)
            return {
                'question': question,
                'answer': result['answer'],
                'sources': result['sources'],
                'search_results_count': 0
            }
        
        print(f"Found {len(search_results)} relevant chunks")
        
        if debug:
            print("\n" + "="*80)
            print("DEBUG: Context being sent to LLM:")
            print("="*80)
            for idx, result in enumerate(search_results, 1):
                print(f"\n[Chunk {idx}] Similarity: {result['similarity']:.4f}")
                print(result['content'][:300])
            print("="*80 + "\n")
        
        print("Generating answer...")
        
        result = self.answer_generator.generate_answer_with_sources(
            question, 
            search_results
        )
        
        response = {
            'question': question,
            'answer': result['answer'],
            'sources': result['sources'],
            'search_results_count': len(search_results)
        }
        
        if include_context:
            response['context'] = result['context']
            response['search_results'] = search_results
        
        return response
    
    def query_with_conversation(self, question):
        search_results = self.retrieval_engine.search_similar_chunks(question)
        
        if not search_results:
            result = self.answer_generator.generate_answer_with_sources(question, search_results)
            self.conversation_history.append({"role": "user", "content": question})
            self.conversation_history.append({"role": "assistant", "content": result['answer']})
            return {
                'question': question,
                'answer': result['answer'],
                'sources': []
            }
        
        context = self.retrieval_engine.get_context_from_results(search_results)
        answer = self.answer_generator.generate_answer(
            question, 
            context, 
            self.conversation_history
        )
        
        self.conversation_history.append({"role": "user", "content": question})
        self.conversation_history.append({"role": "assistant", "content": answer})
        
        sources = []
        for idx, result in enumerate(search_results, 1):
            sources.append({
                'label': f"[Source {idx}]",
                'title': result['source_title'],
                'url': result['source_url'],
                'type': result['source_type']
            })
        
        return {
            'question': question,
            'answer': answer,
            'sources': sources
        }
    
    def clear_conversation(self):
        self.conversation_history = []
    
    def get_conversation_history(self):
        return self.conversation_history
