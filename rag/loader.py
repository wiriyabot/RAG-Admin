from langchain_core.documents import Document
import os


import re

def load_docs(path='raw_data'):
    all_documents = []
    for filename in os.listdir(path):
        if filename.endswith(".txt"):
            with open(os.path.join(path, filename), encoding="utf-8") as f:
                content = f.read()

            price_match = re.search(r"Price[:：]\s*(.*)", content)
            price = price_match.group(1) if price_match else None

            doc = Document(
                page_content=content,
                metadata={
                    "source": filename,
                    "subject": filename.replace(".txt", ""),
                    "price": price
                }
            )
            all_documents.append(doc)
    return all_documents
