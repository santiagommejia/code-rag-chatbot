import chromadb
import ollama

# Load ChromaDB
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_collection(name="code_repository")

# Chat history to maintain conversation context
chat_history = []

def search_code(query):
    # Retrieve top 3 relevant snippets
    results = collection.query(query_texts=[query], n_results=3, include=["documents", "metadatas"])

    # Debug: Print ChromaDB response
    # print("🔍 ChromaDB Query Response:", results)

    # Check if any documents were found
    if not results.get("documents") or len(results["documents"]) == 0:
        return "❌ No relevant code snippets found. Try a different query."

    # Extract relevant code snippets
    code_snippets = "\n\n---\n\n".join([doc for doc_list in results["documents"] for doc in doc_list])

    # 🔥 Build dynamic prompt with context
    conversation_context = "\n".join(chat_history[-3:])  # Keep last 3 messages
    prompt = (
        f"Previous context:\n{conversation_context}\n\n"
        f"New user question: {query}\n\n"
        f"I retrieved these relevant code snippets:\n\n"
        f"{code_snippets}\n\n"
        f"Now, using these examples, provide the best answer.\n"
        f"- Maintain coding style consistency.\n"
        f"- Output full implementation files if needed.\n"
    )

    # Query LLM (Mistral via Ollama)
    response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])

    # Store chat history
    chat_history.append(f"User: {query}")
    chat_history.append(f"AI: {response['message']['content']}")

    return response['message']['content']

# 🚀 Interactive Chat Loop
print("🤖 RAG Chatbot: Ask me anything about your codebase! (Type 'exit' to quit)")

while True:
    query = input("\n🔍 Your question: ")
    if query.lower() == "exit":
        print("👋 Goodbye!")
        break

    answer = search_code(query)
    print("\n💡 Response:\n", answer)
