from flask import Flask, render_template, request, jsonify
from generation.ollamagen import generate_response
from src.file_loader import MainLoader
from src.vectorizer import Vectorizer
from src.retrieval import mainretriever
from src.chunking import chunker
from generation.gemini_gen import main

ml = MainLoader()
doc = ml.document_loader()
ch = chunker(doc)
ro = ch.recursive_overlap()

vt=Vectorizer(ro)
vector_db=vt.dense_vector()
rt = mainretriever()




app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
# def ask():
#     query = request.form.get("query", "")
#     print(query)
#     # ---------------------------------------------------------
#     # No response logic here. Put your answer manually below.
#     context=rt.Topkretriever(query,vector_db,5)
#     sys_prompt=f"You are a senior advisor of Real estate give answer based on the context below. if the question be answered using the context below, if you dont know the answer give response that please visit the office.{context} this is context to answer this {query}.  "
#     response = generate_response(sys_prompt)# <-- assign your answer here
#     # ---------------------------------------------------------

#     return jsonify({"query": query, "response": response})
def ask():
    query = request.form.get("query", "")
    print(query)
    # ---------------------------------------------------------
    # No response logic here. Put your answer manually below.
    context=rt.Topkretriever(query,vector_db,5)
    sys_prompt=f"You are a senior advisor of Real estate give answer based on the context below. if the question be answered using the context below, if you dont know the answer give response that please visit the office.{context} this is context to answer this {query}.  "
    response = (sys_prompt)# <-- assign your answer here
    # ---------------------------------------------------------

    return jsonify({"query": query, "response": response})



if __name__ == "__main__":
    app.run(debug=True)
