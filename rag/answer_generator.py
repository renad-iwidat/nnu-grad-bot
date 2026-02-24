from openai import OpenAI
from config.openai_config import OPENAI_GENERATION_KEY, GENERATION_MODEL

class AnswerGenerator:
    
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_GENERATION_KEY)
        self.model = GENERATION_MODEL
        self.system_prompt = """أنت مساعد افتراضي لكلية الدراسات العليا في جامعة النجاح الوطنية.

قواعد الإجابة:
1. نظم إجابتك بشكل واضح ومنطقي
2. استخدم ## للعناوين الرئيسية
3. استخدم ### للعناوين الفرعية
4. استخدم **النص** لتمييز المعلومات المهمة
5. استخدم قوائم مرقمة (1. 2. 3.) للخطوات أو الترتيب
6. استخدم قوائم نقطية (- ) للنقاط المتعددة
7. اكتب فقرات عادية للشرح والتفاصيل
8. اختر التنسيق المناسب حسب نوع المعلومة

أمثلة:

للمعلومات العامة:
## نبذة عن الكلية

تأسست كلية الدراسات العليا في عام 1995...

### الأهداف
- تأهيل الكوادر
- تطوير البحث العلمي

للخطوات والإجراءات:
## خطوات التسجيل

1. تعبئة نموذج الطلب
2. تقديم المستندات المطلوبة
3. دفع الرسوم

للمعلومات التفصيلية:
## شروط القبول

**المعدل المطلوب:** يجب أن لا يقل المعدل عن 70%.

**المستندات:** يتطلب تقديم الشهادات الأصلية...

اختر التنسيق الأنسب لكل إجابة."""
    
    def generate_answer(self, question, context, conversation_history=None):
        messages = [
            {"role": "system", "content": self.system_prompt}
        ]
        
        if conversation_history:
            messages.extend(conversation_history)
        
        user_message = f"""السياق من وثائق الجامعة:

{context}

السؤال: {question}

يرجى تقديم إجابة مفصلة بناءً على السياق أعلاه."""
        
        messages.append({"role": "user", "content": user_message})
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.1,
                max_tokens=2000
            )
            
            answer = response.choices[0].message.content
            return answer
            
        except Exception as e:
            return f"خطأ في توليد الإجابة: {str(e)}"
    
    def generate_answer_with_sources(self, question, search_results):
        if not search_results:
            return {
                'answer': "I couldn't find any relevant information to answer your question.",
                'sources': []
            }
        
        context_parts = []
        sources = []
        
        for idx, result in enumerate(search_results, 1):
            source_label = f"[Source {idx}]"
            context_parts.append(f"{source_label} {result['content']}")
            
            sources.append({
                'label': source_label,
                'title': result['source_title'],
                'url': result['source_url'],
                'type': result['source_type'],
                'similarity': result['similarity']
            })
        
        context = "\n\n".join(context_parts)
        answer = self.generate_answer(question, context)
        
        return {
            'answer': answer,
            'sources': sources,
            'context': context
        }
