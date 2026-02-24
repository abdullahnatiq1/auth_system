# Auth System

My Auth system is build in FastAPI help the user to store data in any Login page

## Get Started

### Prerequisites

- We need PostGreSQL for this project

### Setting up the Environment

First create .env file in the root of the project and add PostgreSQL database URL

```bash
DATABASE_URL=your_Db_connection_string
```

### Create and Activate Virtual Environment

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Server

```bash
uvicorn main:app --reload
```
