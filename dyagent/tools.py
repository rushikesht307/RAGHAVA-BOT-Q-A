# tools.py

import os
import csv
import json
import mimetypes
import smtplib

from email.message import EmailMessage
from dotenv import load_dotenv

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

load_dotenv()


def create_pdf(content, file_name="output.pdf"):
    """
    Creates a PDF file.
    """

    pdf = canvas.Canvas(
        file_name,
        pagesize=letter
    )

    y = 750

    for line in content.split("\n"):
        pdf.drawString(50, y, line)
        y -= 20

    pdf.save()

    print(f"PDF Created: {file_name}")

    return file_name


def create_text_file(
    content,
    file_name="output.txt"
):
    """
    Creates a text file.
    """

    with open(
        file_name,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(content)

    print(f"TXT Created: {file_name}")

    return file_name


def create_html_file(
    content,
    file_name="output.html"
):
    """
    Creates an HTML file.
    """

    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Generated Content</title>
</head>
<body>
    <h1>Generated Content</h1>
    <pre>{content}</pre>
</body>
</html>
"""

    with open(
        file_name,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(html_content)

    print(f"HTML Created: {file_name}")

    return file_name


def create_json_file(
    content,
    file_name="output.json"
):
    """
    Creates a JSON file.
    """

    with open(
        file_name,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            {"content": content},
            file,
            indent=4
        )

    print(f"JSON Created: {file_name}")

    return file_name


def create_csv_file(
    content,
    file_name="output.csv"
):
    """
    Creates a CSV file.
    """

    with open(
        file_name,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        for line in content.split("\n"):
            writer.writerow([line])

    print(f"CSV Created: {file_name}")

    return file_name


def create_markdown_file(
    content,
    file_name="output.md"
):
    """
    Creates a Markdown file.
    """

    with open(
        file_name,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(content)

    print(f"Markdown Created: {file_name}")

    return file_name


def save_backup(
    content,
    file_name="backup.txt"
):
    """
    Creates a backup text file.
    """

    with open(
        file_name,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(content)

    print(f"Backup Created: {file_name}")

    return file_name


def create_log_file(
    content,
    file_name="output.log"
):
    """
    Creates a log file.
    """

    with open(
        file_name,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(content)

    print(f"Log Created: {file_name}")

    return file_name


def create_xml_file(
    content,
    file_name="output.xml"
):
    """
    Creates an XML file.
    """

    xml_content = f"""
<?xml version="1.0" encoding="UTF-8"?>
<data>
    <content>{content}</content>
</data>
"""

    with open(
        file_name,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(xml_content)

    print(f"XML Created: {file_name}")

    return file_name


def create_property_brochure(
    content,
    file_name="property_brochure.pdf"
):
    """
    Creates a property brochure.
    """

    pdf = canvas.Canvas(
        file_name,
        pagesize=letter
    )

    pdf.setFont(
        "Helvetica-Bold",
        18
    )

    pdf.drawString(
        50,
        750,
        "Property Brochure"
    )

    pdf.setFont(
        "Helvetica",
        12
    )

    y = 700

    for line in content.split("\n"):
        pdf.drawString(
            50,
            y,
            line
        )
        y -= 20

    pdf.save()

    print(f"Brochure Created: {file_name}")

    return file_name


def word_count(content):
    """
    Returns total words.
    """

    return len(content.split())


def character_count(content):
    """
    Returns total characters.
    """

    return len(content)


def send_email(
    receiver_email,
    content,
    attachments=None
):
    """
    Sends email with attachments.
    """

    sender_email = os.getenv(
        "SENDER_EMAIL"
    )

    sender_password = os.getenv(
        "SENDER_PASSWORD"
    )

    if not sender_email:
        raise ValueError(
            "SENDER_EMAIL not found in .env"
        )

    if not sender_password:
        raise ValueError(
            "SENDER_PASSWORD not found in .env"
        )

    msg = EmailMessage()

    msg["Subject"] = "Generated Content"
    msg["From"] = sender_email
    msg["To"] = receiver_email

    msg.set_content(content)

    if attachments:

        print(
            "Attachments Received:",
            attachments
        )

        for file_path in attachments:

            if not os.path.isfile(file_path):

                print(
                    f"File Not Found: {file_path}"
                )

                continue

            mime_type, _ = mimetypes.guess_type(
                file_path
            )

            if mime_type:
                maintype, subtype = (
                    mime_type.split("/", 1)
                )
            else:
                maintype = "application"
                subtype = "octet-stream"

            with open(
                file_path,
                "rb"
            ) as file:

                msg.add_attachment(
                    file.read(),
                    maintype=maintype,
                    subtype=subtype,
                    filename=os.path.basename(
                        file_path
                    )
                )

                print(
                    f"Attached: {file_path}"
                )

    with smtplib.SMTP(
        "smtp.gmail.com",
        587
    ) as server:

        server.starttls()

        server.login(
            sender_email,
            sender_password
        )

        server.send_message(msg)

    return "Email Sent Successfully"

if __name__ == "__main__":
    content = """
    This is sample content generated by an LLM.
    It can be written to a PDF, text file,
    or sent through email.
    """

    create_pdf(content)
    create_text_file(content)