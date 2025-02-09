# Code-RAG: Local Code Retrieval and Generation

This repository provides a simple **local RAG system** that allows you to retrieve and generate code based on your existing project files. It uses **ChromaDB** for storing code snippets and **Ollama with Mistral 7B** to generate responses.

---

## 🔧 Setup Instructions

### **1️⃣ Create a Python Virtual Environment**
Before installing dependencies, it's recommended to create a virtual environment:
```bash
python -m venv venv  # Create virtual environment
source venv/bin/activate  # Activate on macOS/Linux
venv\Scripts\activate  # Activate on Windows
```

### **2️⃣ Install Required Packages**
Once inside the virtual environment, install the necessary dependencies:
```bash
pip install langchain chromadb ollama
```

---

## 🚀 Usage

### **1️⃣ Modify `chunk_code.py` for Your Project**
Before running, update the **project path** in `chunk_code.py`:
```python
extract_code_chunks("./portal-angular")  # Change this to your project path
```
Optionally, modify the **database name** in:
```python
collection = chroma_client.get_or_create_collection(name="angular_code")
```

### **2️⃣ Extract Code Chunks**
Run the script to store project files in ChromaDB:
```bash
python chunk_code.py
```

### **3️⃣ Run the Code Chat**
To query the stored code, run:
```bash
python chat.py
```
Then, enter a query such as:
```
🔍 Your question: Show me TypeScript code that fetches data from a service.
```
The script will retrieve relevant snippets and generate a response.

---

## 📌 Switching to Another LLM
By default, this repo uses **Mistral 7B**. To use a different model, change this line in `chat.py`:
```python
response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
```
To use **CodeLlama**, update it to:
```python
response = ollama.chat(model="codellama", messages=[{"role": "user", "content": prompt}])
```
To check installed models:
```bash
ollama list
```
To download a new model:
```bash
ollama pull codellama
```
---

## 📜 License
This project is open-source and free to use under the MIT License.
