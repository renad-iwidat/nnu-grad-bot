import os
from dotenv import load_dotenv
import certifi

load_dotenv()

os.environ['SSL_CERT_FILE'] = certifi.where()

OPENAI_EMBEDDING_KEY = os.getenv('OPENAI_EMBEDDING_KEY', '')
OPENAI_GENERATION_KEY = os.getenv('OPENAI_GENERATION_KEY', '')
EMBEDDING_MODEL = 'text-embedding-3-small'
EMBEDDING_DIMENSION = 1536
GENERATION_MODEL = 'gpt-4o-mini'
