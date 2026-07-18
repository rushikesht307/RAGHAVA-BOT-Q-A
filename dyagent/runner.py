import json
import inspect
from generation.gemini_gen import geminigen
import dyagent.tools as tools
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


TOOL_REGISTRY = {
    name: func
    for name, func in inspect.getmembers(
        tools,
        inspect.isfunction
    )
}


def execute_tool(actions):

    results = []
    generated_files = []

    for action in actions:

        action = action.copy()

        tool_name = action.pop("tool")

        tool_function = TOOL_REGISTRY.get(
            tool_name
        )

        import inspect

        print(tool_function)
        print(inspect.signature(tool_function))

        print("/nAction")
        print(action)

        print(tool_name)

        if not tool_function:

            results.append(
                {
                    "tool": tool_name,
                    "result": "Tool Not Found"
                }
            )

            continue

        if tool_name == "send_email":

            action["attachments"] = generated_files

        result = tool_function(**action)

        if isinstance(result, str):

            valid_extensions = (
                ".pdf",
                ".txt",
                ".html",
                ".csv",
                ".json",
                ".md"
            )

            if result.endswith(valid_extensions):

                generated_files.append(
                    result
                )

        results.append(
            {
                "tool": tool_name,
                "result": result
            }
        )

    return results


def main():

    with open(
        "agent/logs.json",
        "r",
        encoding="utf-8"
    ) as file:

        tools_metadata = json.load(file)

    while True:

        user_query = input("\nUser: ")

        if user_query.lower() in [
            "exit",
            "quit"
        ]:

            print("Goodbye!")
            break

        context = rt.Topkretriever(
            question=user_query,
            vector_db=vector_db,
            TOP_K=4
        )

        prompt = f"""
You are an intelligent Real Estate AI Agent.

Knowledge Base Context:
{context}

Available Tools:
{json.dumps(tools_metadata, indent=2)}

User Query:
{user_query}

Rules:

1. Use only the retrieved context.
2. Select one or more tools.
3. If the user specifies a filename, include file_name.
4. If email is requested along with files, create files first and send email last.
5. Do not manually specify attachments.
6. Return ONLY valid JSON.
7. Do not explain.

Example 1:

{{
    "actions": [
        {{
            "tool": "create_pdf",
            "content": "property details",
            "file_name": "property_details.pdf"
        }}
    ]
}}

Example 2:

{{
    "actions": [
        {{
            "tool": "create_pdf",
            "content": "property details",
            "file_name": "property.pdf"
        }},
        {{
            "tool": "create_html_file",
            "content": "property details",
            "file_name": "property.html"
        }},
        {{
            "tool": "send_email",
            "receiver_email": "user@gmail.com",
            "content": "Please find attached files."
        }}
    ]
}}
"""

        response = geminigen(prompt)

        print("\nGemini Response:")
        print(response)

        response_json = json.loads(
            response
        )

        results = execute_tool(
            response_json["actions"]
        )

        print("\nResults:")

        for result in results:
            print(result)


if __name__ == "__main__":
    main()