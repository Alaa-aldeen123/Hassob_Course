import os
import sys
import openai
from langchain_community.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.llms import OpenAI as langChainOpenAI  # Updated import
import warnings

warnings.filterwarnings("ignore")

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
#OPENAI_API_KEY ="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")

# Get user query from command-line arguments
prompt = sys.argv[1]

# Load data from a text file
loader = TextLoader("data.txt")
loader.load()

# Set up embeddings and create an index
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002", api_key=openai.api_key)
index = VectorstoreIndexCreator(embedding=embeddings).from_loaders([loader])

# Initialize the language model
llm = langChainOpenAI(api_key=openai.api_key, temperature=0)

# Query the index
result = index.query(prompt, llm=llm, retriever_kwargs={ "search_kwargs": {"k": 1}})
print(result)
