import os
import chromadb
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Initialize vector store
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="code_repository")

# Configure chunking
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

def extract_code_chunks(root_dir):
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(('.ts', '.html', '.scss')):  # Include TypeScript, HTML, SCSS
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                chunks = text_splitter.split_text(content)
                
                # Store chunks in ChromaDB
                for i, chunk in enumerate(chunks):
                    collection.add(
                        ids=[f"{file_path}_{i}"],
                        documents=[chunk],
                        metadatas=[{"file": file_path}]
                    )

# Run chunking
extract_code_chunks("./path-to-your-repository")  # Change to your project path
print("✅ Code chunks stored in ChromaDB.")
