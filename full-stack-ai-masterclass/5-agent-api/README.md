## **Setup Instructions (Using Poetry)**

### **1. Install Poetry**

```sh
pip install poetry
```

### **2. Initialize Virtual Environment & Install Dependencies**

```sh
poetry install
```

### **3. Set Up Environment Variables**

Create a `.env` file with the following configuration:

```sh
# API Keys
GROQ_API_KEY=your_groq_key_here
OPENAI_API_KEY=your_openai_key_here
```

### **4. Run the agent (Python)**

```sh
poetry run python agent.py
```

### **5. Run the API (FastAPI)**

```sh
poetry run fastapi dev api.py
```
