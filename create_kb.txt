#####################################
######   Create Knowledge Base  #######
#####################################
import gradio as gr
import os
import shutil
from llama_index.core import VectorStoreIndex, Settings, SimpleDirectoryReader
from llama_index.embeddings.dashscope import (
    DashScopeEmbedding,
    DashScopeTextEmbeddingModels,
    DashScopeTextEmbeddingType,
)
from llama_index.core.schema import TextNode
from upload_file import *

DB_PATH = "VectorStore"
STRUCTURED_FILE_PATH = "File/Structured"
UNSTRUCTURED_FILE_PATH = "File/Unstructured"
TMP_NAME = "tmp_abcd"
EMBED_MODEL = DashScopeEmbedding(
    model_name=DashScopeTextEmbeddingModels.TEXT_EMBEDDING_V2,
    text_type=DashScopeTextEmbeddingType.TEXT_TYPE_DOCUMENT,
)

# If using a local embedding model, uncomment the following:
# from langchain_community.embeddings import ModelScopeEmbeddings
# from llama_index.embeddings.langchain import LangchainEmbedding
# embeddings = ModelScopeEmbeddings(model_id="modelscope/iic/nlp_gte_sentence-embedding_chinese-large")
# EMBED_MODEL = LangchainEmbedding(embeddings)

# Set embedding model
Settings.embed_model = EMBED_MODEL

# Refresh knowledge base
def refresh_knowledge_base():
    return os.listdir(DB_PATH)

# Create unstructured vector database
def create_unstructured_db(db_name: str, label_name: list):
    print(f"Knowledge base name: {db_name}, Category names: {label_name}")
    if label_name is None:
        gr.Info("No category selected")
    elif len(db_name) == 0:
        gr.Info("No name provided for the knowledge base")
    # Check if a vector database with the same name already exists
    elif db_name in os.listdir(DB_PATH):
        gr.Info("Knowledge base already exists. Please choose a different name or delete the existing one before creating.")
    else:
        gr.Info("Creating knowledge base. Please wait for the success message before proceeding to RAG Q&A.")
        documents = []
        for label in label_name:
            label_path = os.path.join(UNSTRUCTURED_FILE_PATH, label)
            documents.extend(SimpleDirectoryReader(label_path).load_data())
        index = VectorStoreIndex.from_documents(
            documents
        )
        db_path = os.path.join(DB_PATH, db_name)
        if not os.path.exists(db_path):
            os.mkdir(db_path)
            index.storage_context.persist(db_path)
        elif os.path.exists(db_path):
            pass
        gr.Info("Knowledge base created successfully. You can now proceed to RAG Q&A.")

# Create structured vector database
def create_structured_db(db_name: str, data_table: list):
    print(f"Knowledge base name: {db_name}, Data table names: {data_table}")
    if data_table is None:
        gr.Info("No data table selected")
    elif len(db_name) == 0:
        gr.Info("No name provided for the knowledge base")
    # Check if a vector database with the same name already exists
    elif db_name in os.listdir(DB_PATH):
        gr.Info("Knowledge base already exists. Please choose a different name or delete the existing one before creating.")
    else:
        gr.Info("Creating knowledge base. Please wait for the success message before proceeding to RAG Q&A.")
        documents = []
        for label in data_table:
            label_path = os.path.join(STRUCTURED_FILE_PATH, label)
            documents.extend(SimpleDirectoryReader(label_path).load_data())
        # index = VectorStoreIndex.from_documents(
        #     documents
        # )
        nodes = []
        for doc in documents:
            doc_content = doc.get_content().split('\n')
            for chunk in doc_content:
                node = TextNode(text=chunk)
                node.metadata = {'source': doc.get_doc_id(), 'file_name': doc.metadata['file_name']}
                nodes = nodes + [node]
        index = VectorStoreIndex(nodes)
        db_path = os.path.join(DB_PATH, db_name)
        if not os.path.exists(db_path):
            os.mkdir(db_path)
        index.storage_context.persist(db_path)
        gr.Info("Knowledge base created successfully. You can now proceed to RAG Q&A.")

# Delete knowledge base by name
def delete_db(db_name: str):
    if db_name is not None:
        folder_path = os.path.join(DB_PATH, db_name)
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
            gr.Info(f"Successfully deleted knowledge base {db_name}")
            print(f"Successfully deleted knowledge base {db_name}")
        else:
            gr.Info(f"Knowledge base {db_name} does not exist")
            print(f"Knowledge base {db_name} does not exist")

# Update knowledge base list in real time
def update_knowledge_base():
    return gr.update(choices=os.listdir(DB_PATH))

# Create temporary knowledge base
def create_tmp_kb(files):
    if not os.path.exists(os.path.join("File", TMP_NAME)):
        os.mkdir(os.path.join("File", TMP_NAME))
    for file in files:
        file_name = os.path.basename(file)
        shutil.move(file, os.path.join("File", TMP_NAME, file_name))
    documents = SimpleDirectoryReader(os.path.join("File", TMP_NAME)).load_data()
    index = VectorStoreIndex.from_documents(
        documents
    )
    db_path = os.path.join(DB_PATH, TMP_NAME)
    if not os.path.exists(db_path):
        os.mkdir(db_path)
    index.storage_context.persist(db_path)

# Clear contents of the tmp folder
def clear_tmp():
    if os.path.exists(os.path.join("File", TMP_NAME)):
        shutil.rmtree(os.path.join("File", TMP_NAME))
    if os.path.exists(os.path.join(DB_PATH, TMP_NAME)):
        shutil.rmtree(os.path.join(DB_PATH, TMP_NAME))