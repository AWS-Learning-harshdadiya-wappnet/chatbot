# 🧠 Groq‑Powered Chatbot Demo

Tiny FastAPI backend + Streamlit UI, deployed with GitHub Actions → Amazon App Runner.  Uses Groq’s OpenAI‑compatible API.

---

## 🚀 Features

* **FastAPI** backend (`/chat`) calling Groq via the `openai` client.
* **Streamlit** one‑page UI.
* **Dockerised** backend (optional UI container).
* **CI/CD** – GitHub Actions → ECR → App Runner via OIDC (no static AWS keys).

---

## 🏃‍♂️ Quick Start (local)

```bash
python -m venv .venv && source .venv/bin/activate
cp .env.example .env           # add your GROQ_API_KEY
pip install -r requirements.txt

# Backend
uvicorn app.main:app --reload   # ➜ http://localhost:8000
# Frontend
streamlit run app/frontend.py   # ➜ http://localhost:8501
```

Test the API directly:

```bash
curl -X POST http://localhost:8000/chat \
     -H "Content-Type: application/json" \
     -d '{"message": "Hello"}'
```

---

## 🐳 Docker (local)

```bash
# Build & run backend
docker build -t chatbot-backend -f Dockerfile .
docker run -p 8000:8000 --env-file .env chatbot-backend

# Build & run UI (optional)
docker build -t chatbot-ui -f Dockerfile.streamlit .
docker run -p 8501:8501 chatbot-ui
```

---

## 🌩️ Deploy to AWS

1. **Create** an ECR repo named `chatbot-demo`:

   ```bash
   aws ecr create-repository --repository-name chatbot-demo
   ```
2. **Create** an App Runner service:

   ```bash
   aws apprunner create-service \
     --service-name chatbot-demo-svc \
     --source-configuration "ImageRepository={ImageIdentifier=$(aws ecr describe-repositories --repository-names chatbot-demo --query 'repositories[0].repositoryUri' --output text):latest,ImageRepositoryType=ECR},AutoDeploymentsEnabled=true"
   ```
3. **Create** IAM role `GitHubOIDCRole` with ECR + App Runner perms.
4. Push to `main` → GitHub Actions builds, pushes, and updates the service 🚀.

---

## 📂 Project Structure

```
chatbot-demo/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI
│   └── frontend.py      # Streamlit
├── tests/
│   └── test_main.py
├── .env.example
├── requirements.txt
├── Dockerfile
├── Dockerfile.streamlit
└── .github/workflows/ci-cd.yml
```

---

## 🙋‍♀️ Need Help?

Open an issue or ping me – happy to assist!
