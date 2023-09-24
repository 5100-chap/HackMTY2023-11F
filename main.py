import streamlit as st
import pandas as pd

import fitz  # Importar PyMuPDF (Fitz)
from docx import Document
import string




st.markdown("<h1 style='text-align: center;'>TinyWrite.gpt</h1>", unsafe_allow_html=True)


user_input = st.text_input("Introduzca su texto aquí:")



# Crear un checkbox en Streamlit
show_content = st.checkbox("¿Desea adjuntar un archivo?")

# Mostrar contenido si el checkbox está marcado
if show_content:
    # Crear un campo de entrada de archivos en Streamlit
    
    uploaded_file = st.file_uploader("Cargar un archivo:", type=[ "txt", "pdf", "docx"])


    if uploaded_file is not None:
        st.write("Archivo cargado con éxito!")
        # Aquí puedes realizar operaciones con el archivo cargado, como leer su contenido o procesarlo.
        
        file_extension = uploaded_file.name.split(".")[-1].lower()

        if file_extension == "pdf":
            # Leer el contenido del archivo PDF
            pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            
            #Crear una lista para almacenar el contenido de cada página del PDF
            pdf_text_array = []
            
            #Iterar a través de las páginas del PDF y agregar el texto de cada página a la lista
            for page_num in range(len(pdf_document)):
                page = pdf_document[page_num]
                pdf_text_array.append(page.get_text())
                
            #Mostrar el contenido del archivo en Streamlit como una lista
            st.write(pdf_text_array)
            
            
        elif file_extension == "docx":
            # Leer el contenido del archivo docxs
             doc = Document(uploaded_file)
             
             # Inicializa una variable para almacenar el contenido del archivo
             contenido = []
             
             #Itera a través de los párrafos del archivo y agrega el texto al contenido
             for parrafo in doc.paragraphs:
                 contenido.append(parrafo.text)
                 
                 # Muestra el contenido en la aplicación

             st.write("\n".join(contenido))


        else:    
            # Leer el contenido del archivo txt
            contenido = []
            
             # Lee el contenido del archivo TXT línea por línea
            for linea_bytes in uploaded_file:
                # Decodifica la línea y elimina caracteres de puntuación
                linea = linea_bytes.decode("utf-8").strip()
                contenido.append(linea)
            
            # Muestra el contenido en la aplicación
            st.write("Texto sin corregir")
            st.write("\n".join(contenido))



        





