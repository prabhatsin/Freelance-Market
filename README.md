# Freelance Marketplace — Backend

A mini freelance marketplace API built with **FastAPI**, **PostgreSQL**, and **JWT authentication**. Clients can post projects and hire freelancers; freelancers can browse projects and submit proposals.

**Live API:** https://freelance-market-production.up.railway.app
**Interactive docs (Swagger UI):** https://freelance-market-production.up.railway.app/docs
**Frontend:** https://freelancemarket.prabhatsingh.dev

---

## Tech stack

| Layer | Tool |
|---|---|
| Framework | FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Auth | JWT (python-jose), bcrypt password hashing |
| Validation | Pydantic |
| Hosting | Railway (API + managed Postgres) |

---

## Features

- Role-based accounts: **client** and **freelancer**
- Password hashing with bcrypt — no plaintext passwords stored
- JWT-based authentication — required on every endpoint except signup/login
- Clients can post projects and review/accept proposals
- Freelancers can browse open projects and submit proposals
- A freelancer cannot submit more than one proposal per project
- Accepting a proposal atomically: marks it `accepted`, rejects all other proposals on that project, flips the project to `in_progress`, and creates a `Contract`
- A client can only view proposals for projects they own (enforced server-side, not just hidden in the UI)

---

## Project structure

```
.
├── api/
│   ├── main.py          # app entrypoint, router registration, CORS, startup hook
│   ├── auth.py           # signup / login routes
│   ├── projects.py       # create / list project routes
│   └── proposals.py      # submit / list / accept proposal routes
├── core/
│   └── security.py       # password hashing, JWT create/verify, get_current_user deps
├── db/
│   └── database.py        # SQLAlchemy engine, session, Base
├── models/                # SQLAlchemy models (User, Project, Proposals, Contracts)
├── schema/                # Pydantic request/response schemas
├── requirements.txt
└── .env                   # local only — never committed
```

---

## Environment variables

Create a `.env` file in the project root (never commit this — it's gitignored):

```
DATABASE_URL=postgresql://<user>:<password>@<host>:<port>/<database>
SECRET_KEY=<a long random string>
ALGORITHM=HS256
```

Generate a strong `SECRET_KEY` with:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

In production (Railway), these are set directly in the service's **Variables** tab instead of a `.env` file. `DATABASE_URL` there is a reference to Railway's own managed Postgres instance.

---

## Running locally

```bash
# 1. Clone and enter the repo
git clone https://github.com/prabhatsin/Freelance-Market.git
cd Freelance-Market

# 2. Create and activate a virtual environment
python -m venv myenv
source myenv/bin/activate      # Windows: myenv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up your .env file (see above)

# 5. Run the server
uvicorn api.main:app --reload
```

The API will be live at `http://localhost:8000`, with interactive docs at `http://localhost:8000/docs`.

Tables are created automatically on startup via a FastAPI startup hook (`Base.metadata.create_all`) — no manual migration step needed for this project.

---

## Authentication

Every endpoint except `POST /api/auth/signup` and `POST /api/auth/login` requires a JWT, sent as:
```
Authorization: Bearer <token>
```
The token payload contains `user_id`, `role`, and `name`. Role-specific endpoints use FastAPI dependencies (`get_current_client`, `get_current_freelancer`) to enforce that only the correct role can call them.

---

## API Endpoints

### Auth

**`POST /api/auth/signup`**
Creates a new user. Password is hashed before storage.
```json
{
  "name": "Rahul",
  "email": "rahul@example.com",
  "password": "password123",
  "role": "freelancer"
}
```

**`POST /api/auth/login`**
Authenticates and returns a JWT.
```json
{
  "email": "rahul@example.com",
  "password": "password123"
}
```
Response:
```json
{
  "access_token": "...",
  "token_type": "bearer"
}
```

### Projects

**`POST /api/projects`** — *client only*
Creates a project. Validates `budget_max >= budget_min` and `deadline` is in the future.
```json
{
  "project_title": "Build an E-commerce Website",
  "project_description": "Need a full-stack e-commerce application",
  "category": "Web Development",
  "budget_min": 50000,
  "budget_max": 100000,
  "deadline": "2026-09-15"
}
```

**`GET /api/projects`**
Returns all open projects. Optional query filters: `category`, `budget_min`, `budget_max`.

### Proposals

**`POST /api/projects/{project_id}/proposals`** — *freelancer only*
Submits a proposal. Rejects if the project doesn't exist (404), isn't open (400), or the freelancer already proposed on it (409).
```json
{
  "cover_letter": "I have 3 years of experience...",
  "proposed_price": 75000,
  "estimated_duration": 20
}
```

**`GET /api/projects/{project_id}/proposals`** — *client, project owner only*
Returns all proposals for a project. Returns 403 if the requesting client doesn't own the project.

**`PUT /api/proposals/{proposal_id}/accept`** — *client, project owner only*
Accepts a proposal. Within a single transaction:
1. Marks the accepted proposal as `accepted`
2. Marks all other proposals on that project as `rejected`
3. Sets the project's status to `in_progress`
4. Creates a `Contract` linking the client, freelancer, project, and agreed price

Returns 404 if the proposal doesn't exist, 400 if it was already processed, 403 if the project doesn't belong to the requesting client.

---

## Deployment

Hosted on **Railway**, connected to this GitHub repo — any push to `main` triggers an automatic rebuild and redeploy. Railway also hosts the managed PostgreSQL instance used in production; its connection string is injected into the backend service via a variable reference, not hardcoded.

CORS is configured in `api/main.py` to explicitly allow the deployed frontend origins (Vercel URL and custom domain) alongside `localhost:5173` for local development.

---

## Known limitations

- No endpoint to list all contracts for a user — contract data is currently only returned inline at the moment a proposal is accepted, not retrievable afterward. A `GET /api/contracts` endpoint would be a natural next addition.
- No automated tests yet.