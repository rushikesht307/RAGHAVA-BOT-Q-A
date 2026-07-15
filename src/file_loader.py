from langchain_community.document_loaders import DirectoryLoader,PyPDFLoader, Docx2txtLoader, TextLoader, JSONLoader

class MainLoader:
    def __init__(self,path="data"):
        self.documents=[]
        self.path=path
    
    def document_loader(self):
        self.documents+= DirectoryLoader(
            self.path,glob="**/*.pdf",
            loader_cls=PyPDFLoader
        ).load()
        print("PDF File loaded successfully")

        self.documents+= DirectoryLoader(
            self.path,glob="**/*.docx",
            loader_cls=Docx2txtLoader
        ).load()
        print("Doc File loaded successfully")

        self.documents+= DirectoryLoader(
            self.path,glob="**/*.txt",
            loader_cls=TextLoader, 
            loader_kwargs={"encoding":"utf-8"}
        ).load()
        print("Text File loaded successfully")

        self.documents+= DirectoryLoader(
            self.path,glob="**/*.json",
            loader_cls=JSONLoader,
            loader_kwargs={
                "jq_schema":".",
                "text_content":False
            },
        ).load()
        print("JSON File loaded successfully")

        print("all files loaded successfully")
        return self.documents