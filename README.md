# مساعد كلية الدراسات العليا - جامعة النجاح الوطنية
# Najah Graduate Studies Chatbot

نظام ذكاء اصطناعي للإجابة على الأسئلة المتعلقة ببرامج الدراسات العليا في جامعة النجاح الوطنية باستخدام تقنية RAG (Retrieval-Augmented Generation).

## المميزات

- 🤖 إجابات ذكية باستخدام GPT-4o-mini
- 📚 بحث دلالي في قاعدة بيانات الجامعة
- 🎨 واجهة مستخدم عربية جميلة وسهلة الاستخدام
- 🌙 وضع داكن وفاتح
- 📱 تصميم متجاوب يعمل على جميع الأجهزة
- ⚡ استجابة سريعة مع عرض المصادر

## البنية التقنية

```
.
├── api/                    # FastAPI Backend
│   ├── main.py            # API endpoints
│   └── models.py          # Pydantic models
├── config/                # Configuration files
│   ├── database.py        # Database config
│   └── openai_config.py   # OpenAI config
├── database/              # Database layer
│   ├── connection.py      # Connection pool
│   └── queries.py         # Query functions
├── frontend/              # Frontend files
│   ├── index.html         # Main HTML
│   ├── styles.css         # Styling
│   ├── script.js          # JavaScript
│   └── assets/            # Images and assets
├── rag/                   # RAG System
│   ├── data_loader.py     # Load data from DB
│   ├── text_chunker.py    # Split text into chunks
│   ├── embedding_generator.py  # Generate embeddings
│   ├── embedding_storage.py    # Store embeddings
│   ├── indexing_pipeline.py    # Full indexing pipeline
│   ├── retrieval_engine.py     # Search embeddings
│   ├── answer_generator.py     # Generate answers
│   ├── intent_classifier.py    # Classify intents
│   └── query_pipeline.py       # Full query pipeline
├── scripts/               # Utility scripts
│   ├── run_indexing.py    # Index data
│   └── run_query.py       # Test queries
├── .env                   # Environment variables
├── .env.example          # Example env file
├── requirements.txt      # Python dependencies
└── run_api.py           # Run the API server
```

## المتطلبات

- Python 3.11+
- PostgreSQL with pgvector extension
- OpenAI API keys

## التثبيت

### 1. تثبيت المكتبات

```bash
pip install -r requirements.txt
```

### 2. إعداد قاعدة البيانات

تأكد من تثبيت pgvector extension:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

### 3. إعداد ملف البيئة

```bash
cp .env.example .env
```

عدل ملف `.env` وأضف المعلومات الصحيحة:

```env
# Database
DB_HOST=your_host
DB_PORT=5432
DB_NAME=your_database
DB_USER=your_user
DB_PASSWORD=your_password

# OpenAI
OPENAI_EMBEDDING_KEY=sk-...
OPENAI_GENERATION_KEY=sk-...
```

### 4. فهرسة البيانات

```bash
python scripts/run_indexing.py
```

هذا سيقوم بـ:
- تحميل البيانات من قاعدة البيانات
- تقسيم النصوص إلى أجزاء
- توليد embeddings باستخدام OpenAI
- تخزين embeddings في قاعدة البيانات

## التشغيل

### تشغيل الـ API

```bash
python run_api.py
```

الـ API سيعمل على: `http://localhost:8000`

التوثيق التفاعلي: `http://localhost:8000/docs`

### تشغيل الـ Frontend

افتح ملف `frontend/index.html` في المتصفح مباشرة.

## API Endpoints

### GET /
معلومات عن الـ API

### GET /health
فحص صحة النظام وعدد الـ embeddings

### POST /query
إرسال سؤال والحصول على إجابة

```json
{
  "question": "ما هي شروط القبول؟",
  "session_id": "optional-session-id",
  "include_context": false
}
```

Response:
```json
{
  "question": "ما هي شروط القبول؟",
  "answer": "الإجابة المفصلة...",
  "sources": [
    {
      "label": "[Source 1]",
      "title": "عنوان المصدر",
      "url": "رابط المصدر",
      "type": "html_page",
      "similarity": 0.85
    }
  ],
  "search_results_count": 10,
  "is_general": false,
  "session_id": "session-id"
}
```

### POST /query/conversation
سؤال مع تاريخ المحادثة

### DELETE /session/{session_id}
حذف جلسة محادثة

## التقنيات المستخدمة

### Backend
- **FastAPI**: إطار عمل API سريع وحديث
- **PostgreSQL + pgvector**: قاعدة بيانات مع دعم vector search
- **OpenAI API**: 
  - `text-embedding-3-small` للـ embeddings
  - `gpt-4o-mini` لتوليد الإجابات
- **psycopg2**: للاتصال بقاعدة البيانات

### Frontend
- **HTML5/CSS3/JavaScript**: واجهة مستخدم نظيفة
- **Cairo Font**: خط عربي جميل
- **Responsive Design**: يعمل على جميع الأحجام

### RAG System
- **Chunking**: تقسيم النصوص إلى أجزاء 1000 حرف مع تداخل 200 حرف
- **Embeddings**: 1536 بُعد باستخدام text-embedding-3-small
- **Retrieval**: بحث cosine similarity مع top-k=10
- **Generation**: GPT-4o-mini مع temperature=0.1

## الاختبار

### اختبار الاتصال بقاعدة البيانات

```bash
python test_connection.py
```

### اختبار الاستعلام

```bash
python scripts/run_query.py
```

## الإنتاج (Production)

### تحديثات مطلوبة للإنتاج:

1. **CORS Settings**: عدل `api/main.py` لتحديد الـ origins المسموحة
2. **Environment**: استخدم متغيرات بيئة آمنة
3. **HTTPS**: استخدم SSL certificate
4. **Rate Limiting**: أضف حدود للطلبات
5. **Monitoring**: أضف logging ومراقبة
6. **Caching**: أضف Redis للـ caching

## المساهمة

تم تطوير هذا المشروع بواسطة وحدة ليمينال التابعة لمركز الإعلام في جامعة النجاح الوطنية.

## الترخيص

هذا المشروع خاص بجامعة النجاح الوطنية.
