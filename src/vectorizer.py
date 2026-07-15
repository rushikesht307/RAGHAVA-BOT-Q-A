from pathlib import Path
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import pickle
from langchain_community.retrievers import TFIDFRetriever
from langchain_community.graph_vectorstores import CassandraGraphVectorStore



EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

class Vectorizer:
    def __init__(self,chunks):
        self.chunks = chunks


    def dense_vector(self):
        CHROMA_DIR = "dense_db"
        embedding_model = HuggingFaceEmbeddings(model_name = EMBEDDING_MODEL)

        if Path(CHROMA_DIR).exists():
            print("Loading existing dense Chroma DB...")
            dense_vector_db = Chroma(
                persist_directory = CHROMA_DIR,
                embedding_function = embedding_model,
            )

        else:
            print("Creating new dense Chroma DB...")
            dense_vector_db = Chroma.from_documents(
                documents = self.chunks,
                embedding = embedding_model,
                persist_directory= CHROMA_DIR,
            )

        print("Chroma DB is Created")

        return dense_vector_db
    
    def sparse_vector(self):
        DATA_DIR = "sparsedb"
        retriever = TFIDFRetriever.from_documents(self.chunks)
        with open("tfidf_retrieve.pkl","wb") as f:
            pickle.dump(retriever,f)
            print("Sparse vector created")



    def create_graph_vectorstore(chunks):

        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        graph_store = CassandraGraphVectorStore.from_documents(
            documents=chunks,
            embedding=embeddings
        )
        print("Graph vector Created")
        return graph_store