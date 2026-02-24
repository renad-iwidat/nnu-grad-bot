class IntentClassifier:
    
    GENERAL_QUESTIONS = [
        'من انت', 'من أنت', 'مرحبا', 'مرحباً', 'السلام عليكم',
        'شكرا', 'شكراً', 'وداعا', 'وداعاً', 'مع السلامة',
        'كيف حالك', 'ما اسمك', 'اتصل', 'تواصل', 'رقم', 'هاتف', 'ايميل', 'بريد'
    ]
    
    GENERAL_RESPONSES = {
        'identity': """أنا مساعد افتراضي لكلية الدراسات العليا في جامعة النجاح الوطنية.
أستطيع مساعدتك في:
- معلومات عن برامج الماجستير والدكتوراه
- شروط القبول والتسجيل
- تعليمات الدراسة والامتحانات
- معلومات عن الكلية ورؤيتها ورسالتها

كيف يمكنني مساعدتك؟""",
        
        'greeting': """مرحباً بك! أنا مساعد كلية الدراسات العليا في جامعة النجاح الوطنية.
كيف يمكنني مساعدتك اليوم؟""",
        
        'thanks': """العفو! سعيد بمساعدتك. إذا كان لديك أي أسئلة أخرى، لا تتردد في السؤال.""",
        
        'goodbye': """وداعاً! أتمنى أن أكون قد ساعدتك. يمكنك العودة في أي وقت.""",
        
        'status': """أنا بخير، شكراً لسؤالك! كيف يمكنني مساعدتك اليوم؟""",
        
        'contact': """للتواصل مع كلية الدراسات العليا:

📍 العنوان: نابلس، فلسطين

📞 هاتف: 970+ (0) 92345113-
   داخلي: 4538

📠 فاكس: 970+ (0) 92345982-

📧 البريد الإلكتروني: fgs@najah.edu

يمكنك التواصل معنا خلال أوقات الدوام الرسمي."""
    }
    
    @staticmethod
    def is_general_question(question):
        question_lower = question.lower().strip()
        
        for general_q in IntentClassifier.GENERAL_QUESTIONS:
            if general_q in question_lower:
                return True
        
        return False
    
    @staticmethod
    def get_general_response(question):
        question_lower = question.lower().strip()
        
        identity_keywords = ['من انت', 'من أنت', 'ما اسمك']
        greeting_keywords = ['مرحبا', 'مرحباً', 'السلام عليكم']
        thanks_keywords = ['شكرا', 'شكراً']
        goodbye_keywords = ['وداعا', 'وداعاً', 'مع السلامة']
        status_keywords = ['كيف حالك']
        contact_keywords = ['اتصل', 'تواصل', 'رقم', 'هاتف', 'ايميل', 'بريد']
        
        for keyword in contact_keywords:
            if keyword in question_lower:
                return IntentClassifier.GENERAL_RESPONSES['contact']
        
        for keyword in identity_keywords:
            if keyword in question_lower:
                return IntentClassifier.GENERAL_RESPONSES['identity']
        
        for keyword in greeting_keywords:
            if keyword in question_lower:
                return IntentClassifier.GENERAL_RESPONSES['greeting']
        
        for keyword in thanks_keywords:
            if keyword in question_lower:
                return IntentClassifier.GENERAL_RESPONSES['thanks']
        
        for keyword in goodbye_keywords:
            if keyword in question_lower:
                return IntentClassifier.GENERAL_RESPONSES['goodbye']
        
        for keyword in status_keywords:
            if keyword in question_lower:
                return IntentClassifier.GENERAL_RESPONSES['status']
        
        return IntentClassifier.GENERAL_RESPONSES['greeting']
