# 📒 Requirements Log — Personal Expense Tracker (Auth + Analytics)

**Project:** Personal Expense Tracker (Web)  
**Approach:** Vibe Coding (AI‑assisted)  
**Version:** 1.0 (MVP scope)  
**Date:** 14/09/2025 
**Owner:** D. R. Ariyarathne, S. T. Wickramasinghe, M. Keerthisiri

---

## 0) Scope & Goals
A web app where a user can **sign up / log in** with email + password (also capture **name** and **age**), add **income/expense** transactions, and view a **dashboard** that shows:
- **Last transaction**
- **Current balance** (all‑time income − expense)
- **Today’s totals**: total income today, total expense today
- **Pie chart** of **expense categories** for **day / week / month** (toggle)
- **Line chart** of **daily expense trends** for past **week / month / year** (toggle)

MVP focuses on a **single user account per sign‑in** (no multi‑tenant admin) and **simple, clear UI**.

---

## 1) Functional Requirements (FR)

| ID | Requirement | Acceptance Criteria | Priority |
|----|-------------|---------------------|----------|
| FR1 | **Sign up** with name, age, email, password | - Form collects name (text), age (integer), email, password (min 8). <br> - Email must be unique. <br> - Password stored **hashed**. <br> - On success, redirect to login or auto‑login to dashboard. | High |
| FR2 | **Log in / Log out** | - Correct email+password signs in, creates a session. <br> - Wrong credentials show error (no detail which field). <br> - Log out ends session and redirects to login. | High |
| FR3 | **Add transaction** | - Form fields: type (**income/expense**), **category** (string from dropdown), **amount** (positive), optional note. <br> - **Timestamp auto‑captured** (server time); stored in UTC. <br> - Persists with authenticated user id. | High |
| FR4 | **Dashboard overview** | - Shows **last transaction** for the signed‑in user. <br> - Shows **current balance** = sum(income) − sum(expense) for the user. <br> - Shows **today’s totals** (income and expense) based on user’s local day (see assumptions). | High |
| FR5 | **Pie chart: expense categories** | - Toggle **day / week / month**. <br> - Computes total **expense** per category over selected range. <br> - Renders as a pie/doughnut chart. | High |
| FR6 | **Line chart: daily expense trend** | - Toggle **past week / month / year**. <br> - Computes **expense per day** for the selected period. <br> - Renders as a line chart with date labels. | High |
| FR7 | **Categories presets** | - Income: at least **Salary, Gifts, Sales Revenue, Other**. <br> - Expense: at least **Food, Travel, Rent, Utilities, Other**. | Medium |
| FR8 | **Basic validation & UX** | - All required fields validated. <br> - Friendly error messages. <br> - Flash confirmations on success. | Medium |
| FR9 | **Session protection** | - Dashboard and add‑transaction routes require auth. <br> - CSRF protection for forms (MVP: Flask‑WTF or simple token). | Medium |
| FR10 | **Mobile‑friendly UI** | - Layout is responsive; cards stack on small screens. | Low |

---

## 2) Non‑Functional Requirements (NFR)

| ID | Requirement | Acceptance Criteria |
|----|-------------|---------------------|
| NFR1 | Performance | Dashboard loads < 2s with ≤ 2k transactions; charts render < 1s after data load. |
| NFR2 | Security | Passwords hashed; sessions secured; no secrets in repo; use env var for SECRET_KEY. |
| NFR3 | Privacy | Only the signed‑in user can see their data. |
| NFR4 | Portability | Runs on Replit free tier; can deploy via Replit URL. |
| NFR5 | Maintainability | Clear file structure; docstrings; README with run steps. |
| NFR6 | Accessibility | Form labels, keyboard navigable controls for chart toggles. |

---

## 3) Data Model (ERD — textual)

**users**  
- id (PK, int, autoincrement)  
- name (text, 1–80)  
- age (int, ≥ 13)  
- email (text, unique, valid format)  
- password_hash (text)  
- created_at (datetime, UTC)

**transactions**  
- id (PK, int, autoincrement)  
- user_id (FK → users.id)  
- t_type (text: 'income' or 'expense')  
- category (text)  # e.g., Food, Travel, Rent or Salary, Gifts  
- amount (numeric, > 0)  
- note (text, optional)  
- ts (datetime, UTC)  # transaction timestamp (auto at insert)  
- created_at (datetime, UTC default now)

**Indexes**  
- idx_tx_user_ts (user_id, ts desc)  
- idx_tx_user_type (user_id, t_type)  
- idx_tx_user_category (user_id, category)

*(Optional) categories table if you want per‑user custom categories later.*

---

## 4) API / Pages (MVP)

**Pages (server‑rendered Jinja):**  
- `GET /auth/signup` — sign‑up form  
- `POST /auth/signup` — create user  
- `GET /auth/login` — login form  
- `POST /auth/login` — authenticate  
- `POST /auth/logout` — logout (or GET if you prefer)  
- `GET /dashboard` — main dashboard (requires auth)  
- `GET /transactions/new` — add transaction (requires auth)  
- `POST /transactions` — create transaction (requires auth)

**JSON endpoints for charts (consumed by Chart.js):**  
- `GET /api/pie?range=day|week|month` → `{ labels: [cat], data: [sum] }` (expense only)  
- `GET /api/trends?period=week|month|year` → `{ labels: [dates], data: [daily_expense] }`

---

## 5) Analytics Definitions

- **Current balance:** sum(amount where t_type='income') − sum(amount where t_type='expense'), across **all time** for the signed‑in user.  
- **Today’s totals:** totals where the transaction timestamp falls **between today 00:00 and now** in user’s time zone (*MVP assumption below*).  
- **Pie (range=day/week/month):** expense totals grouped by `category` within the selected **rolling** range ending today.  
- **Line (period=week/month/year):** series of **daily** expense totals for the past N days ending today (7 / ~30 / 365).

---

## 6) Validation & Rules

- Email must be unique and valid.  
- Password min 8 chars; store hash (e.g., Werkzeug).  
- Age must be integer ≥ 13 (MVP assumption).  
- Transaction amount > 0; t_type ∈ {income, expense}; category is required.  
- Timestamp `ts` is auto‑captured by server on insert (UTC).  
- All data access must be filtered by `user_id` in queries.

---

## 7) Assumptions

- Time zone: for MVP, compute “today/week/month/year” using **Asia/Colombo** local time or treat server local time consistently; store all timestamps in **UTC** and convert for display/aggregation.  
- Single currency; no exchange rates.  
- No file uploads/receipts.  
- Single‑device sign‑in flows; no email verification (could add later).

---

## 8) Out of Scope (MVP)

- Multi‑currency, budgets, recurring transactions, sharing accounts, export to CSV/PDF, password reset via email, 2FA, admin panel.

---

## 9) Acceptance Test Checklist (Sampling)

- ✅ Sign up with valid data → user saved, password hashed, redirect to dashboard/login.  
- ✅ Duplicate email → error shown, no user created.  
- ✅ Login with correct credentials → dashboard visible; incorrect → error.  
- ✅ Add income 100 and expense 40 → dashboard balance = 60.  
- ✅ Today’s totals reflect transactions added today.  
- ✅ Pie toggles day/week/month update data correctly.  
- ✅ Line toggles week/month/year render distinct series lengths.  
- ✅ Unauthorized user cannot access /dashboard or /transactions routes.

---

## 10) Risks & Mitigations

- **Authentication mistakes** → use Flask‑Login and secure password hashing.  
- **Time zone confusion** → store UTC and standardize conversions; document rule.  
- **Chart performance** → aggregate in SQL and return compact JSON.  
- **Data leakage** → always filter by `user_id` on queries.

---

## 11) Milestones

1) Auth + users table  
2) Transactions + add form (timestamp auto)  
3) Dashboard summary (last tx, balance, today totals)  
4) Pie endpoint + UI toggle (day/week/month)  
5) Line endpoint + UI toggle (week/month/year)  
6) Polish + tests + deploy (Replit)
