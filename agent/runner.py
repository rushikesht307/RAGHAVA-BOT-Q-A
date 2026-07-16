import json
from generation.gemini_gen import geminigen
from agent.tools import create_pdf, create_text_file, send_email
from src.retrieval import mainretriever
from src.vectorizer import Vectorizer
from src.file_loader import MainLoader
from src.chunking import chunker


print("Loading Vector Database...")

# vectorizer = Vectorizer()
# vector_db = vectorizer.dense_vector()
# retriever = mainretriever()

ml = MainLoader()
doc = ml.document_loader()
ch = chunker(doc)
ro = ch.recursive_overlap()

vt=Vectorizer(ro)
vector_db=vt.dense_vector()
rt = mainretriever()

print("Vector Database Loaded Successfully!")


def execute_tool(tool_call):

    tool_name = tool_call["tool"]

    if tool_name == "create_pdf":
        return create_pdf(tool_call["content"])

    elif tool_name == "create_text_file":
        return create_text_file(tool_call["content"])

    elif tool_name == "send_email":
        return send_email(
            tool_call["receiver_email"],
            tool_call["content"]
        )

    return f"Unknown tool: {tool_name}"


def main():

    with open("agent/logs.json", "r", encoding="utf-8") as file:
        tools_metadata = json.load(file)

    while True:

        user_query = input("\nUser: ")

        if user_query.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        context = rt.Topkretriever(
            question=user_query,
            vector_db=vector_db,
            TOP_K=4
        )

        sys_prompt = f"""
You are an AI Agent that has access to a company knowledge base.

Knowledge Base Context:
{context}

Available Tools:
{json.dumps(tools_metadata, indent=2)}

User Query:
{user_query}

Instructions:
1. Read the retrieved context carefully.
2. Use only the retrieved context to generate the content.
3. Select the appropriate tool.
4. Return ONLY valid JSON.
5. Do not return markdown.
6. Do not explain your reasoning.

Examples:

{{
    "tool": "create_pdf",
    "content": "Generated content using the retrieved context."
}}

{{
    "tool": "create_text_file",
    "content": "Generated content using the retrieved context."
}}

{{
    "tool": "send_email",
    "receiver_email": "abc@gmail.com",
    "content": "Generated email using the retrieved context."
}}
"""

        response = geminigen(sys_prompt)

        print("\nGemini Response:")
        print(response)

        tool_call = json.loads(response)

        result = execute_tool(tool_call)

        print("\nResult:")
        print(result)


if __name__ == "__main__":
    main()