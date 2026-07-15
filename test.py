from src.file_loader import MainLoader
from src.chunking import chunker
from src.vectorizer import Vectorizer


a = MainLoader()
doc = a.document_loader()

ch = chunker(doc)
c = ch.recursive_overlap()
ch.sementic_chunk()
ch.para_chunk()


r = Vectorizer(c)
r.dense_vector()
r.sparse_vector()
r.load_or_create_graph_vectorstore()

