import os
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
import pickle
import json

def load_chatbot():
    # Load Memory (if applicable)
    memory_path = "memory.pkl"
    if os.path.exists(memory_path):
        with open(memory_path, "rb") as memory_file:
            memory_state = pickle.load(memory_file)
    else:
        memory_state = {}

    # Initialize Memory
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    if memory_state:
        memory.save_context({"input": "Restored state"}, memory_state)

    # Load OpenAI Embeddings
    openai_api_key = os.getenv("OPENAI_API_KEY")
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

    # Load Chroma Vector Store
    vector_store = Chroma(
        collection_name="diet-coach",
        embedding_function=embeddings,
        persist_directory="chroma_data"  # Directory containing the persisted vector store
    )

    # Load Chain Configurations
    with open("chain_config.json", "r") as config_file:
        chain_config = json.load(config_file)

    # Recreate Prompt Template
    custom_prompt = PromptTemplate(
        template=chain_config["prompt_template"],
        input_variables=chain_config["input_variables"],
    )

    # Initialize Chat Model
    chat_model = ChatOpenAI(model="gpt-4", openai_api_key=openai_api_key)

    # Create Retrieval Chain
    retrieval_chain = ConversationalRetrievalChain.from_llm(
        llm=chat_model,
        retriever=vector_store.as_retriever(),
        memory=memory,
        combine_docs_chain_kwargs={"prompt": custom_prompt},
    )

    return retrieval_chain
