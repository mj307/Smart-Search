from langchain_core.prompts import PromptTemplate
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Query, Request, Form
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader

app = FastAPI()


# Using Jinja2 for templates
templates = Jinja2Templates(directory="templates")

class QueryModel(BaseModel):
    query: str = Query(..., description="Query to summarize the document")

# Your existing setup code
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=350, chunk_overlap=100, add_start_index=True)
loader = PyPDFLoader("brain.pdf")
docs = loader.load()
all_splits = text_splitter.split_documents(docs)
vectordb = Chroma.from_documents(documents=all_splits, embedding=embeddings, persist_directory="braindb")
llm = Ollama(model="llama3")

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

template = """Use the following pieces of context to answer the question at the end.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
Keep the answer as concise as possible.
{context}
Question: {question}
Answer:"""

custom_rag_prompt = PromptTemplate.from_template(template)
retriever = vectordb.as_retriever()

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | custom_rag_prompt
    | llm
    | StrOutputParser()
)

# Endpoint to serve the HTML form
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# FastAPI endpoint to handle summarization
@app.post("/summarize/", response_class=HTMLResponse)
async def summarize(request: Request, query: str = Form(...)):
    response = ""
    for chunk in rag_chain.stream(query):
        response += chunk
    return templates.TemplateResponse("result.html", {"request": request, "summary": response})



