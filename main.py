# Importacion de librerias para pagina principal
import streamlit as st
import pandas as pd
import fitz  # Importar PyMuPDF (Fitz)
from docx import Document
from back import *


# Declaración de clase para el uso de la app web
myclass = TextAssistant()

band = 0
st.markdown(
    "<h1 style='text-align: center;'>TinyWrite.gpt</h1>", unsafe_allow_html=True
)

# Agregar la barra de navegación a la barra lateral
st.sidebar.title("Menú de herramientas")


# Agregar enlaces a diferentes páginas o secciones
pagina_inicio = st.sidebar.button("Correción de textos")
pagina_seccion1 = st.sidebar.button("Sugerencias de mejora de textos")
pagina_seccion2 = st.sidebar.button("Traductor de documentos")


# Función para mostrar el contenido de la página de inicio
def mostrar_inicio():
    st.empty()

    st.markdown(
        "<h3 style='text-align: left;'>Corrección de textos</h3>",
        unsafe_allow_html=True,
    )

    user_input = st.text_input("Introduzca su texto aquí:")

    # Inicializa una variable para almacenar el contenido del archivo o del input del usuario
    contenido = [user_input]

    # Crear un checkbox en Streamlit
    show_content = st.checkbox("¿Desea adjuntar un archivo?")

    if show_content:
        uploaded_file = st.file_uploader(
            "Cargar un archivo:", type=["txt", "pdf", "docx"]
        )

        if uploaded_file is not None:
            st.markdown(
                "<h4 style='text-align: left; text-decoration: underline'> Texto original: </h4>",
                unsafe_allow_html=True,
            )

            file_extension = uploaded_file.name.split(".")[-1].lower()

            if file_extension == "pdf":
                pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
                contenido = [page.get_text() for page_num in range(len(pdf_document)) for page in [pdf_document[page_num]]]
            
            elif file_extension == "docx":
                doc = Document(uploaded_file)
                full_text = '\n'.join([parrafo.text for parrafo in doc.paragraphs if parrafo.text.strip() != ''])
                contenido = [full_text]

            elif file_extension == "txt":
                contenido = [linea_bytes.decode("utf-8").strip("\n") for linea_bytes in uploaded_file]

            st.write(contenido[0])
            
    st.markdown(
        "<h4 style='text-align: left; text-decoration: underline'> Texto corregido: </h4>",
        unsafe_allow_html=True,
    )

    # Asumiendo que la función myclass.correct_text puede manejar el formato de contenido que proporcionamos.
    corrected = myclass.correct_text(contenido[0])
    st.write(corrected)

# Función para mostrar el contenido de la Sección 1
def mostrar_Sugerencia():
    st.empty()

    st.markdown(
        "<h3 style='text-align: left;'> Sugerencias de mejora de redacción de textos</h3>",
        unsafe_allow_html=True,
    )

    


# Función para mostrar el contenido de la Sección 2
def mostrar_Traducción():
    st.empty()
    st.markdown(
        "<h3 style='text-align: left;'> Traducción de textos </h3>",
        unsafe_allow_html=True,
    )



# Verificar qué página se debe mostrar en función de los botones de la navbar
if pagina_inicio:
    band = 1
    mostrar_inicio()
elif pagina_seccion1:
    band = 1
    mostrar_Sugerencia()
elif pagina_seccion2:
    band = 1
    mostrar_Traducción()


if band == 0:
    mostrar_inicio()

else:
    st.empty()
