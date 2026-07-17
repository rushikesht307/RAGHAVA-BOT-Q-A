import json
from generation.gemini_gen import geminigen
from agent.tools import create_pdf, create_text_file, send_email
from src.retrieval import mainretriever
from src.vectorizer import Vectorizer
from src.file_loader import MainLoader
from src.chunking import chunker


print("Loading Vector Database...")

ml = MainLoader()
doc = ml.document_loader()

ch = chunker(doc)
ro = ch.recursive_overlap()

vt = Vectorizer(ro)
vector_db = vt.dense_vector()

rt = mainretriever()

print("Vector Database Loaded Successfully!")


def execute_tool(actions):

    results = []

    for action in actions:

        tool_name = action["tool"]

        if tool_name == "create_pdf":

            result = create_pdf(
                action["content"]
            )

        elif tool_name == "create_text_file":

            result = create_text_file(
                action["content"]
            )

        elif tool_name == "send_email":

            result = send_email(
                receiver_email=action["receiver_email"],
                content=action["content"],
                attachments=action.get("attachments", [])
            )

        else:

            result = f"Unknown tool: {tool_name}"

        results.append(
            {
                "tool": tool_name,
                "result": result
            }
        )

    return results


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

1. Use ONLY the retrieved context.
2. Decide which tools are needed.
3. A user may require one or multiple tools.
4. If email contains attachments, always create the files BEFORE sending email.
5. Return ONLY valid JSON.
6. Do NOT return markdown.
7. Do NOT explain reasoning.

Examples:

PDF only:

{{
    "actions": [
        {{
            "tool": "create_pdf",
            "content": "generated content"
        }}
    ]
}}

Text File only:

{{
    "actions": [
        {{
            "tool": "create_text_file",
            "content": "generated content"
        }}
    ]
}}

Email only:

{{
    "actions": [
        {{
            "tool": "send_email",
            "receiver_email": "abc@gmail.com",
            "content": "generated content"
        }}
    ]
}}

PDF + Email:

{{
    "actions": [
        {{
            "tool": "create_pdf",
            "content": "generated content"
        }},
        {{
            "tool": "send_email",
            "receiver_email": "abc@gmail.com",
            "content": "generated content",
            "attachments": [
                "output.pdf"
            ]
        }}
    ]
}}

PDF + TXT + Email:

{{
    "actions": [
        {{
            "tool": "create_pdf",
            "content": "generated content"
        }},
        {{
            "tool": "create_text_file",
            "content": "generated content"
        }},
        {{
            "tool": "send_email",
            "receiver_email": "abc@gmail.com",
            "content": "Please find the attached files.",
            "attachments": [
                "output.pdf",
                "output.txt"
            ]
        }}
    ]
}}
"""

        response = geminigen(sys_prompt)

        print("\nGemini Response:")
        print(response)

        response_json = json.loads(response)

        results = execute_tool(
            response_json["actions"]
        )

        print("\nResults:")

        for result in results:
            print(result)


if __name__ == "__main__":
    main()