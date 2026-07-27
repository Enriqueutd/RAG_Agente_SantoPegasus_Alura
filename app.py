import os
import streamlit as st
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

try:
    from langchain.chains import create_retrieval_chain
    from langchain.chains.combine_documents import create_stuff_documents_chain
except ModuleNotFoundError:
    from langchain_classic.chains import create_retrieval_chain
    from langchain_classic.chains.combine_documents import create_stuff_documents_chain

# Configurar la página en Streamlit
st.set_page_config(
    page_title="Asistente IA - Santo Pegasus Soluciones",
    page_icon="🦄",
    layout="centered"
)

st.title("🦄 Asistente Técnico - Santo Pegasus Soluciones")
st.caption("Consulta la documentación interna de ingeniería, incidentes y microservicios.")

# Obtener la API Key desde el entorno (.env)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Si no está en el .env, permite ingresarla manualmente por UI
if not GROQ_API_KEY:
    GROQ_API_KEY = st.sidebar.text_input("Ingresa tu Groq API Key:", type="password")

if GROQ_API_KEY:
    os.environ["GROQ_API_KEY"] = GROQ_API_KEY

    @st.cache_resource
    def inicializar_rag():
        ruta_carpeta = "documentos_pegasus"
        if not os.path.exists(ruta_carpeta):
            os.makedirs(ruta_carpeta)
            
        loader = PyPDFDirectoryLoader(ruta_carpeta)
        docs = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
        splits = text_splitter.split_documents(docs)

        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)
        retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

        system_prompt = (
            "Eres el asistente virtual interno de desarrollo e ingeniería para 'Santo Pegasus Soluciones'. "
            "Responde a las preguntas utilizando ÚNICAMENTE la información de los documentos provistos. "
            "Si la información no está registrada, indica amablemente que no se encuentra en la documentación oficial.\n\n"
            "{context}"
        )

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}"),
        ])

        llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
        question_answer_chain = create_stuff_documents_chain(llm, prompt)
        return create_retrieval_chain(retriever, question_answer_chain)

    try:
        rag_chain = inicializar_rag()

        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt_usuario := st.chat_input("Escribe tu pregunta sobre la documentación..."):
            st.session_state.messages.append({"role": "user", "content": prompt_usuario})
            with st.chat_message("user"):
                st.markdown(prompt_usuario)

            with st.chat_message("assistant"):
                with st.spinner("Buscando en la base de conocimientos..."):
                    respuesta = rag_chain.invoke({"input": prompt_usuario})
                    st.markdown(respuesta["answer"])

            st.session_state.messages.append({"role": "assistant", "content": respuesta["answer"]})

    except Exception as e:
        st.error(f"Error al inicializar el sistema RAG: {e}")

else:
    st.warning("⚠️ Por favor, define GROQ_API_KEY en tu archivo .env o escríbela en la barra lateral.")