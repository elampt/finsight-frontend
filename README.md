# FinSight

Smart Portfolio Tracker and News Sentiment Analyzer.

FinSight empowers retail investors by providing a comprehensive dashboard that tracks portfolio holdings, fetches real-time financial news, and evaluates sentiment using FinBERT—all within an intuitive Streamlit interface backed by FastAPI and PostgreSQL.

---

## 🚀 Live Implementation
🔗 [Interact with FinSight](https://finsightpro.streamlit.app)

---

## 🏗️ Architecture Overview

```
                                  +----------------------------+
                                  |     Frontend (Streamlit)   |
                                  |  [User Interface Layer]    |
                                  +-------------+--------------+
                                                |
                                                ▼
                                  +-------------+--------------+
                                  |         FastAPI Backend     |
                                  |  [Users, Holdings, News,    |
                                  |   Sentiment APIs - Modular] |
                                  +-------------+--------------+
                                                |
                         +----------+-----------+----------------------+
                         |          |                                  |
                         ▼          ▼                                  ▼
                +----------------+  +------------------+           +------------------+
                |  PostgreSQL DB |  | Yahoo Finance API|           |  FinBERT Model   |
                | (User data,    |  | (Stock prices,   |           | (Financial Sent. |
                | Holdings, etc.)|  | historical data) |           | Analysis - HF)   |
                +----------------+  +------------------+           +------------------+
```

## Key Features & Architecture

### Database

- **PostgreSQL**, initially local, then migrated to **Neon Server-less Postgres** for scalable, server-less cloud hosting.

**Tables:**
- `users`: username, email, password (hashed)    
- `holdings`: stock_id, purchase_cost, quantity, date
- `stocks`: pre-populated list of US stock tickers

### [Backend](https://github.com/elampt/finsight-backend) (FastAPI + Docker + Hugging Face Space)

**Authentication (JWT)**:
- `/users/signup`, `/users/login`
- JWT-based token authentication used for securing all user endpoints and to extract current user details from the token itself

 **Holdings Management**:
- `POST /holdings/add`, `DELETE /holdings/delete/{id}`, `PUT /holdings/update/{id}`
- `GET /holdings/by-symbol`, `GET /holdings/profit-loss`

**Stock List**:
- `GET /stocks/symbols`
- Real-time stock info via `yfinance`

**News & Sentiment API**:
- `GET /holdings/news-sentiment`
- Retrieves 5 news headlines per stock (via yfinance)
 - Sentiment analysis via **FinBERT (finbert-tone)** model on Hugging Face

**API End-points explained:** 
- `signup` - Users enter their name, email and password (These details will get stored in the `users` table) to sign up. Password will be hashed before getting stored into the db
- `login` - Users enter their email and password to login. Upon login, the `JWT Bearer Token` will be generated which has to be used for further API endpoint accessing
- `me` - Returns the `id` of the current logged in user
- `add` - Used to add a new holding to an user's portfolio
- `delete/{holding_id}` - Used to delete user holdings
- `update/{holding_id}` - Used to update user holdings
- `stocks/symbols` - Returns the list of all unique stock symbols in the database
- `by-symbol` - Used to get the holdings list for an user for a particular stock
- `profit-loss` - Used to get the entire user portfolio holdings status (Profit, loss etc.)
- `news-sentimet` - Gives 5 news headlines with URL for every stock the user holds along with the sentiment for that particular news (Positive, Negative or Neutral)

### Backend (Docker + Hugging Face Space)
I used a **Dockerfile** for my FastAPI backend deployment on **Hugging Face Spaces** to ensure a consistent and isolated environment. Since Hugging Face also offers container-based deployment for backend services, Docker was the ideal choice.

By using the Dockerfile:
- I specified the **Python version** and installed all dependencies from `requirements.txt`, ensuring the app runs the same everywhere.
- I set the working directory and copied all project files into the container.
- I defined how the app should run using `uvicorn` on port `7860`, which is the default for Hugging Face Spaces.

This approach made my backend portable, reliable, and cloud-friendly — a clean solution for production deployment.

### Frontend (Streamlit Cloud)
- Clean UI with JWT token-based login
- Add/update/delete holdings
- Profit/loss dashboard (with live price updates)
- Per-stock news sentiment dashboard

### NLP Integration
**FinBERT (finbert-tone) - Huggingface model**:
* A financial-domain BERT model fine-tuned on ~10k sentiment-labeled analyst statements
* Gives output sentiment labels for the news titles passsed: **Positive**, **Negative**, or **Neutral** 

---
## Deployment: Why I Chose a Multi-Platform Strategy
While working on the FinSight project, I aimed to deploy it with a **realistic, cloud-ready architecture** — similar to what you'd find in modern production environments.

### Initial Plan: Full Deployment on AWS

I first attempted a full deployment on **AWS**, using:
- **Amazon RDS (PostgreSQL)** for the database
- **EC2 (Ubuntu)** instance for the FastAPI backend
- **Streamlit Cloud** for the frontend

#### Why I Dropped It

Even though I was well within the **AWS Free Tier**, I started noticing charges for:
- RDS storage and backup service costs, charges for the VPC Public IPv4 Addresses

To avoid incurring unexpected costs during development, I pivoted to **a cost-effective and scalable alternative**.

### Final Deployment Strategy (Free, Efficient, Modular)

| Component         | Platform                 | Reason                                                                        |
| ----------------- | ------------------------ | ----------------------------------------------------------------------------- |
| **Frontend (UI)** | Streamlit Cloud          | Simple, free deployment for Streamlit apps with custom domain support         |
| **Backend (API)** | Hugging Face Spaces      | FastAPI deployed via Docker; free-tier includes GPU/CPU and public API access |
| **Database**      | Neon Serverless Postgres | Free-tier serverless PostgreSQL with generous limits and fast setup           |
### Why This Modular Approach?

- **Streamlit Cloud** does not support background tasks or API routing — making it unsuitable for a full-stack app. It can only run frontend logic.

- **FastAPI**, when hosted via **Hugging Face Spaces** (using Docker), gives me full control over the API stack, including `uvicorn`, CORS, and JWT auth.

- **Neon** offers **PostgreSQL-as-a-Service** with built-in autoscaling, branches for versioning, and no cold start — perfect for hobby projects and even multi-tenant architectures.

--- 

## Lessons Learned from this project development

- **Cost-awareness is critical** even when using cloud “free tiers”; always monitor billing dashboards.

- **Decoupling the app** (frontend, backend, DB) leads to easier debugging, flexibility, and platform-optimized deployments.

- Using **Docker** ensures portability — I can move the backend to AWS, Azure, or GCP in minutes without changing the code.

- **Cloud-native, server-less options** like Hugging Face and Neon are incredible for fast prototyping with zero infrastructure headaches.

## 📸 Project Screenshots
#### Home Page
<img width="1470" alt="Screenshot 2025-05-15 at 12 49 09 PM" src="https://github.com/user-attachments/assets/4f492e31-9c12-481c-a560-e6e6c6d8de70" />

#### Dashboard Page with Portfolio Summary
<img width="1470" alt="Screenshot 2025-05-15 at 1 08 47 PM" src="https://github.com/user-attachments/assets/bbe56d8f-a40e-44a9-ab4a-3652c67a56a0" />


#### Holdings Page with individual Stock Summary
<img width="1470" alt="Screenshot 2025-05-15 at 1 04 49 PM" src="https://github.com/user-attachments/assets/6a947c66-0cb4-40b4-b06b-652cf29de3a1" />

#### Holdings Page with the `Add New Holding` feature
<img width="1470" alt="Screenshot 2025-05-15 at 1 06 16 PM" src="https://github.com/user-attachments/assets/650f5771-4ed4-4f18-afd7-77b12bd9b500" />

### News Sentiment page
<img width="1470" alt="Screenshot 2025-05-15 at 1 08 26 PM" src="https://github.com/user-attachments/assets/f302ff47-6549-4a8a-b033-1806e91a0f45" />

