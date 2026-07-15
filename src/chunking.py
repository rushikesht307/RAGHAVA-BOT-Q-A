from langchain_text_splitters import RecursiveCharacterTextSplitter,CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_experimental.text_splitter import SemanticChunker


class chunker:

    def __init__(self,documents):
        self.documents = documents

    def recursive_overlap(self):
        splitter = RecursiveCharacterTextSplitter(
            chunk_size = 1000,
            chunk_overlap = 200
        )

        chunks = splitter.split_documents(self.documents)
        print("Recursive Chunks Created")
        return chunks
    
    def sementic_chunk(self):
        embedding = HuggingFaceEmbeddings(
            model_name = "sentence-transformers/all-MiniLM-L6-v2"
        )

        splitter = SemanticChunker(
            embeddings = embedding,
            breakpoint_threshold_type = "percentile"
        )

        chunks = splitter.split_documents(self.documents)
        print("Sementic Chunks Created")
        return chunks
    

    def para_chunk(self):
        splitter=CharacterTextSplitter(separator="\n\n",chunk_size=4000)
        chunks=splitter.split_documents(self.documents)
        #paragraph=self.documents.split("\n\n")
        #chunks=[p.strip() for p in paragraph if p.stri()]
        print("para chunks created")
        return chunks 
    
    def fixed_chunk(self):
        splitter=CharacterTextSplitter(chunk_size=500)
        chunks=splitter.split_documents(self.documents)
        print("char chunks created")
        return chunks
        
        
        
    def para_chunk(self):
        splitter=CharacterTextSplitter(separator="\n\n",chunk_size=4000)
        chunks=splitter.split_documents(self.documents)
        #paragraph=self.documents.split("\n\n")
        #chunks=[p.strip() for p in paragraph if p.stri()]
        print("para chunks created")
        return chunks 
    
    def fixed_chunk(self):
        splitter=CharacterTextSplitter(chunk_size=500)
        chunks=splitter.split_documents(self.documents)
        print("char chunks created")
        return chunks
    




    
