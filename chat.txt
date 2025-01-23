import os
from openai import OpenAI
from llama_index.core import StorageContext, load_index_from_storage, Settings
from llama_index.embeddings.dashscope import (
    DashScopeEmbedding,
    DashScopeTextEmbeddingModels,
    DashScopeTextEmbeddingType,
)
from llama_index.postprocessor.dashscope_rerank import DashScopeRerank
from create_kb import *
from llama_index.core.llms import ChatMessage
from llama_index.llms.litellm import LiteLLM

from config.load_key import load_key
load_key()

DB_PATH = "VectorStore"
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

def get_model_response(multi_modal_input, history, model, temperature, max_tokens, history_round, db_name, similarity_threshold, chunk_cnt):
    # prompt = multi_modal_input['text']
    prompt = history[-1][0]
    tmp_files = multi_modal_input['files']
    if os.path.exists(os.path.join("File", TMP_NAME)):
        db_name = TMP_NAME
    else:
        if tmp_files:
            create_tmp_kb(tmp_files)
            db_name = TMP_NAME
    # Get index
    print(f"prompt: {prompt}, tmp_files: {tmp_files}, db_name: {db_name}")
    try:
        dashscope_rerank = DashScopeRerank(top_n=chunk_cnt, return_documents=True)
        storage_context = StorageContext.from_defaults(
            persist_dir=os.path.join(DB_PATH, db_name)
        )
        index = load_index_from_storage(storage_context)
        print("Index retrieval completed")
        retriever_engine = index.as_retriever(
            similarity_top_k=20,
        )
        # Get chunks
        retrieve_chunk = retriever_engine.retrieve(prompt)
        print(f"Original chunks: {retrieve_chunk}")
        try:
            results = dashscope_rerank.postprocess_nodes(retrieve_chunk, query_str=prompt)
            print(f"Rerank successful, reordered chunks: {results}")
        except:
            results = retrieve_chunk[:chunk_cnt]
            print(f"Rerank failed, chunks: {results}")
        chunk_text = ""
        chunk_show = ""
        for i in range(len(results)):
            if results[i].score >= similarity_threshold:
                chunk_text = chunk_text + f"## {i+1}:\n {results[i].text}\n"
                chunk_show = chunk_show + f"## {i+1}:\n {results[i].text}\nscore: {round(results[i].score, 2)}\n"
        print(f"Retrieved chunks: {chunk_text}")
        prompt_template = f"Please refer to the following content: {chunk_text}, and answer the user's question in an appropriate tone: {prompt}. If there are image links in the reference content, please return them directly."
    except Exception as e:
        print(f"Exception: {e}")
        prompt_template = prompt
        chunk_show = ""
    history[-1][-1] = ""
    # client = OpenAI(
    #     api_key=os.getenv("DASHSCOPE_API_KEY"),
    #     base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    # )
    # system_message = {'role': 'system', 'content': 'You are a helpful assistant.'}
    # messages = []
    # history_round = min(len(history), history_round)
    # for i in range(history_round):
    #     messages.append({'role': 'user', 'content': history[-history_round+i][0]})
    #     messages.append({'role': 'assistant', 'content': history[-history_round+i][1]})
    # messages.append({'role': 'user', 'content': prompt_template})
    # messages = [system_message] + messages
    # completion = client.chat.completions.create(
    #     model=model,
    #     messages=messages,
    #     temperature=temperature,
    #     max_tokens=max_tokens,
    #     stream=True
    #     )
    # assistant_response = ""
    # for chunk in completion:
    #     assistant_response += chunk.choices[0].delta.content
    #     history[-1][-1] = assistant_response
    #     yield history, chunk_show
    messages = [
        ChatMessage(
            role="system", content=prompt_template
        ),
        ChatMessage(role="user", content=prompt),
    ]
    print(f"model: {model}")
    if model == 'qwen-plus':
        llm_qwen = LiteLLM(
            model="openai/qwen-plus",
            api_key=os.getenv("DASHSCOPE_API_KEY"),
            api_base="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
        resp = llm_qwen.chat(messages)
    elif model == 'deepseek':
        os.environ["DEEPSEEK_API_KEY"] = "sk-123"
        llm_deepseek = LiteLLM(
            model="deepseek/deepseek-chat",
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            api_base="https://api.deepseek.com",
        )
        resp = llm_deepseek.chat(messages)
    elif model == 'ollama':
        llm_ollama = LiteLLM(
            model="ollama/qwen2.5:7b",
            api_base="http://localhost:11434",
        )
        resp = llm_ollama.chat(messages)

    print(f"resp: {resp.message.content}")
    assistant_response = resp.message.content
    history[-1][-1] = assistant_response
    yield history, chunk_show