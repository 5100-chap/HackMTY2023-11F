# Declaración de librerías
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


class TextAssistant:
    def __init__(self):
        # Inicialización de las variables env
        load_dotenv()

        # Verifica si existe las variables en el env
        self._initialize_env_vars()

        # Declaracion del modelo y sus variables usando el SDK
        self.model = OpenAI(
            api_key=self.OPENAI_API_KEY,
            model_name=self.OPENAI_CHAT_MODEL_NAME,
            api_type="azure",
            api_base=self.OPENAI_API_BASE,
        )

        self.embeddings_model = OpenAIEmbeddings(
            api_key=self.OPENAI_API_KEY,
            model_name=self.OPENAI_EMBEDDINGS_MODEL_NAME,
            api_type="azure",
            api_base=self.OPENAI_API_BASE,
        )

        # Declaración de filtros para el chatbot
        self.filters = []

        # Declaración de la cache
        self.vector_store = PineconeVectorStore(
            api_key=self.PINECONE_API_KEY,
            environment=self.PINECONE_ENVIRONMENT,
            index_name=self.PINECONE_INDEX_NAME,
        )

        self.cache = Cache(
            vector_store=self.vector_store, embeddings_model=self.embeddings_model
        )

        # Declaración del chatbot
        self.chatbot = Chatbot(
            model=self.model,
            description="You are a very helpful and polite chatbot",
            filters=self.filters,
            cache=self.cache,
            verbose=True,
        )

    def _initialize_env_vars(self):
        # Verifica si existe las variables en el env
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        if self.OPENAI_API_KEY is None:
            raise ValueError("OPENAI_API_KEY not found in .env file")

        self.OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")
        if self.OPENAI_API_BASE is None:
            raise ValueError("OPENAI_API_BASE not found in .env file")

        self.OPENAI_EMBEDDINGS_MODEL_NAME = os.getenv("OPENAI_EMBEDDINGS_MODEL_NAME")
        if self.OPENAI_EMBEDDINGS_MODEL_NAME is None:
            raise ValueError("OPENAI_EMBEDDINGS_MODEL_NAME not found in .env file")

        self.OPENAI_CHAT_MODEL_NAME = os.getenv("OPENAI_CHAT_MODEL_NAME")
        if self.OPENAI_CHAT_MODEL_NAME is None:
            raise ValueError("OPENAI_CHAT_MODEL_NAME not found in .env file")
        self.PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
        if self.PINECONE_API_KEY is None:
            raise ValueError("PINECONE_API_KEY not found in .env file")

        self.PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
        if self.PINECONE_ENVIRONMENT is None:
            raise ValueError("PINECONE_ENVIRONMENT not found in .env file")

        self.PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
        if self.PINECONE_INDEX_NAME is None:
            raise ValueError("PINECONE_INDEX_NAME not found in .env file")

def correct_text(self, text):
    # Dividir el texto en párrafos manejables
    parrafos = self.dividir_en_parrafos(text)

    # Inicializar una variable para almacenar el texto corregido
    res = ""

    command = "Please review the following text and correct any grammatical or stylistic errors while preserving its original meaning:\n\n"

    # Corregir cada párrafo individualmente
    for parrafo in parrafos:
        promp = command + parrafo
        print(promp)
        response = self.chatbot.chat(
            promp,
            print_cache_score=True,
        )
        res += response.message.content

    # Devolver el texto corregido
    return res


    def suggestText(self, text):
        # Enviar el texto al chatbot para obtener la retroalimentación del archivo de entrada
        res = ""
        for each in text:
            command = "Based on the following text, while preserving its original language, can you suggest three continuations or improvements in bullet points?\n\n" + each + "\n\nSuggestions:\n- "
            response = self.chatbot.chat(
                command,
                print_cache_score=True,
            )
            res += response.message.content

        # Devolver el contenido de la respuesta del chatbot
        return res


    # Hace un conteo del top 5 palabras más repetidas y retorna una lista de tuplas
    def contador(self, text):
        res = list()
        temp = str()
        temp = " ".join(collections.deque(text))
        words = re.findall(r"\w+", temp.lower())
        count = collections.Counter(words)
        most_repeated_words = count.most_common(5)
        for each, frec in most_repeated_words:
            res.append((each, frec))
        return res

    def traductor(self, text, target_language):
        command = (
            f"Please translate the following text into {target_language}. "
            f"Ensure accuracy and maintain the context and nuance of the original content:\n\n"
            f'"{text}"'
        )
        response = self.chatbot.chat(
            command,
            print_cache_score=True,
        )
        return response.message.content
    
    def dividir_por_puntuacion(self, texto, inicio=100):
        fin = inicio + 400

        if fin < len(texto):
            if fin > inicio + 700:
                posibles_puntuaciones = ['.', ',', ';', ':']
            else:
                posibles_puntuaciones = ['.']

            for puntuacion in posibles_puntuaciones:
                posicion = texto.find(puntuacion, fin)
                if posicion != -1:
                    fin = posicion + 1
                    break
            else:
                fin = min(fin + 400, len(texto))

        return texto[inicio:fin], fin

    def dividir_en_parrafos(self, texto):
        parrafos = []
        if '\n\n' or '\n' in texto:
            if '\n' in texto:
                breaker = '\n'
            else:
                breaker = '\n\n'
            temp_parrafos = texto.split(breaker)
            for par in temp_parrafos:
                inicio = 0
                while inicio < len(par):
                    if len(par) > 500:
                        fragmento, inicio = self.dividir_por_puntuacion(par, inicio)
                        parrafos.append(fragmento)
                    else:
                        parrafos.append(par[inicio:])
                        break
        else:
            inicio = 0
            while inicio < len(texto):
                fragmento, inicio = self.dividir_por_puntuacion(texto, inicio)
                parrafos.append(fragmento)

        return parrafos
