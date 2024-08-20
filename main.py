# we are importing the packages, which are AzureOpenAI, AzureOpenAIEmbeddings
#langchain is a python library for exploring generative AI
from langchain_openai import AzureOpenAI, AzureOpenAIEmbeddings, AzureChatOpenAI
from langchain.schema import HumanMessage
from langchain.prompts import ChatPromptTemplate
from langchain_community.document_loaders import AzureAIDocumentIntelligenceLoader
from langchain_community.vectorstores import FAISS
import os
from dotenv import load_dotenv
load_dotenv()

llm = AzureChatOpenAI(
    azure_endpoint = ('https://ict-llm.openai.azure.com/'), #if it doesn't work, use the actual value and run the code.
    openai_api_version="2023-03-15-preview",
    model = 'llm-ict',
    openai_api_key= ('929631d081584305804d7d4be3431c61'),
    openai_api_type = "azure"
)
embedding = AzureOpenAIEmbeddings(azure_endpoint = ('https://ict-llm.openai.azure.com/'),
    openai_api_version="2023-03-15-preview",
    model = 'embedding-ict',
    openai_api_key= ('929631d081584305804d7d4be3431c61'),
    openai_api_type = "azure")
#create a function to load the documents
def load_document(file_path):
    loader = AzureAIDocumentIntelligenceLoader(
        api_endpoint = ('https://ict-documentloader.cognitiveservices.azure.com/'),
        api_key = ('6aa69bf49be54cecb16e7615fd9a4b88'),
        api_model = "prebuilt-layout", # This is the specific api model that we have used for layout extraction, this helps to identify whether it's a paragraph,image or table.
        file_path = file_path # it's just a file path, from where the file will be loaded.
    )
    return loader.load()



def vector_store(file_path):
    docs = load_document(file_path)
    #print(docs)
    db = FAISS.from_documents(docs, embedding)
    return db

def query(query, db):
    docs = db.similarity_search(query)
    prompt = ChatPromptTemplate.from_messages(

        [
            ('system',
             'You are an useful AI assistant, you need to answer the queries I send you, using the context provided'),
            ('human', 'query: {query}, context:{context} elaborate it as much as you can')
        ]
    )
    chain = prompt | llm
    result = (chain.invoke({'query': query, 'context': str(docs)}))
    return result.content





