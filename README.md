# AI Recruitment Platform

## 🚀 Overview

The AI Recruitment Platform is a modular, AI-powered system designed to automate and enhance the recruitment process. It streamlines CV parsing, candidate-job matching, ranking, interview selection, and communication through intelligent agents.

This project simulates a real-world Applicant Tracking System (ATS) enhanced with AI-driven decision-making.

---

## 🎯 Problem It Solves

Traditional recruitment processes are:
- Time-consuming
- Manual and repetitive
- Prone to bias and inconsistency
- Difficult to scale

This system solves these issues by:
- Automating CV analysis
- Matching candidates to job descriptions intelligently
- Ranking candidates using semantic similarity
- Automating recruiter communication (emails, reports)
- Centralizing recruitment workflows

---

## 🧠 Key Features

- 📄 AI-powered CV parsing and analysis
- 🧩 Job description understanding
- 🔍 Semantic candidate-job matching (FAISS)
- 📊 Candidate ranking system
- 📬 Automated email notifications (shortlist, rejection, interview)
- 📑 PDF report generation
- 🧠 Modular AI agent architecture
- 🔐 Authentication and user management
- 📈 Analytics and recruitment history tracking

---

## 🏗️ System Architecture

CV → CV Agent → Job Agent → Matching Engine → Ranking System → Interview Agent → Email Dispatcher → Report Generator

---

## 🛠️ Tech Stack

- Python
- FAISS (Vector Search)
- SMTP Email Automation
- SQLite / Database Layer
- Modular AI Agent Design
- FastAPI / Backend services (if applicable)
- Git & GitHub

---

## 📂 Project Structure
agents/ - AI agents (CV, Job, Matching, Interview, etc.)
auth/ - Authentication system
database/ - Database layer and repositories
models/ - AI/LLM models
nodes/ - Workflow execution nodes
services/ - Email and business logic services
utils/ - Helper functions (FAISS, parsing, embeddings)
templates/ - Email templates
pages/ - Dashboard / UI pages
pipeline.py - Main workflow pipeline
app.py - Application entry point

---

## 📸 Screenshots
*

- Candidate ranking output
- Email automation
- Dashboard views
- Report generation

---

## ⚙️ Setup Instructions

```bash
# Clone repository
git clone git@github.com:KeletsoNIT/ai-recruitment-platform.git

# Navigate into project
cd ai-recruitment-platform

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py
