#Declaracion de librerias
import os
import collections
import re
from softtek_llm.chatbot import Chatbot
from softtek_llm.models import OpenAI
from softtek_llm.cache import Cache
from softtek_llm.vectorStores import PineconeVectorStore
from softtek_llm.embeddings import OpenAIEmbeddings
from softtek_llm.schemas import Filter
from dotenv import load_dotenv

# Inicialización de las variables env
load_dotenv()

# Verifica si existe las variables en el env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY is None:
    raise ValueError("OPENAI_API_KEY not found in .env file")

OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")
if OPENAI_API_BASE is None:
    raise ValueError("OPENAI_API_BASE not found in .env file")

OPENAI_EMBEDDINGS_MODEL_NAME = os.getenv("OPENAI_EMBEDDINGS_MODEL_NAME")
if OPENAI_EMBEDDINGS_MODEL_NAME is None:
    raise ValueError("OPENAI_EMBEDDINGS_MODEL_NAME not found in .env file")

OPENAI_CHAT_MODEL_NAME = os.getenv("OPENAI_CHAT_MODEL_NAME")
if OPENAI_CHAT_MODEL_NAME is None:
    raise ValueError("OPENAI_CHAT_MODEL_NAME not found in .env file")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
if PINECONE_API_KEY is None:
    raise ValueError("PINECONE_API_KEY not found in .env file")

PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
if PINECONE_ENVIRONMENT is None:
    raise ValueError("PINECONE_ENVIRONMENT not found in .env file")

PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
if PINECONE_INDEX_NAME is None:
    raise ValueError("PINECONE_INDEX_NAME not found in .env file")

# Variables globales
text = str()

# Declaracion del modelo y sus variables usando el SDK
model = OpenAI(
    api_key=OPENAI_API_KEY,
    model_name=OPENAI_CHAT_MODEL_NAME,
    api_type="azure",
    api_base=OPENAI_API_BASE,
)

embeddings_model = OpenAIEmbeddings(
    api_key=OPENAI_API_KEY,
    model_name=OPENAI_EMBEDDINGS_MODEL_NAME,
    api_type="azure",
    api_base=OPENAI_API_BASE,
)

# Declaración de filtros para el chatbot

filters = [
Filter(
    type="DENY",
    case="Any curses or bad words in any language",
),
Filter(
    type="DENY",
    case="Any offensive comentaries or sentences against any person or topic",
),
]

# Declacion de la cache

vector_store = PineconeVectorStore(
    api_key=PINECONE_API_KEY,
    environment=PINECONE_ENVIRONMENT,
    index_name=PINECONE_INDEX_NAME,
)

cache = Cache(
    vector_store=vector_store,
    embeddings_model= embeddings_model,
)

# Declaración del chatbot
chatbot = Chatbot(
    model=model,
    description="You are a very helpful and polite chatbot",
    filters=filters,
    cache=cache,
    verbose=True,
)


def correctText():
    print("retorna el texto del archivo de entrada corregido")
    # equisdeqeuidxe ya me conecye
    # SIZE XL como lo mueve esa muchachona
    # Esta en lad beinbow y la rebota
    
def suggestText():
    print("retorna la retroalimentación del archivo de entrada")
    
    # Hola
    
# Hace un conteo del top 5 palabras más repetidas y retorna una lista de tuplas 
def contador():
    res = list()
    words = re.findall(r'\w+', text.lower())
    count = collections.Counter(words)
    most_repeated_words = count.most_common(5)
    for each, frec in most_repeated_words:
        res.append((each, frec)) 
    return res

def traductor(language: str):
    print("traducir el texto")
    response = chatbot.chat(
        str("Translate the text of the file in ", language), 
        print_cache_score=True, 
        cache_kwargs={"namespace": "chatbot-test"}
                            )
    type(response)
    



