import chromadb
import ollama

# Load ChromaDB
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_collection(name="portal-angular")  # More generic name

def search_code(query):
    # Retrieve top 3 relevant snippets
    results = collection.query(query_texts=[query], n_results=3, include=["documents", "metadatas"])

    # 🔍 Debug: Print ChromaDB response
    # print("🔍 ChromaDB Query Response:", results)

    # Check if any documents were found
    if not results.get("documents") or len(results["documents"]) == 0:
        return "❌ No relevant code snippets found. Try a different query."

    # Extract relevant code snippets
    code_snippets = "\n\n---\n\n".join([doc for doc_list in results["documents"] for doc in doc_list])

    # 🔥 Generic prompt that adapts to any codebase
    prompt = (
        f"I retrieved these relevant code snippets:\n\n"
        f"{code_snippets}\n\n"
        f"Now, using these examples, generate the requested implementation.\n"
        f"- Follow the project's coding style.\n"
        f"- Use best practices based on the retrieved code.\n"
        f"- Return complete files (e.g., .ts, .js, .html, .py, etc.), depending on context.\n"
        f"- Do NOT explain the code; just return it directly."
    )

    # Query LLM (Mistral via Ollama)
    response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])

    return response['message']['content']

# Test it
query = input("🔍 Enter your question: ")
answer = search_code(query)
print("\n💡 Response:\n", answer)
