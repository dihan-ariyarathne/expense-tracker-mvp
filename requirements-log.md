# 📒 Requirements Log – Personal Expense Tracker

**Project:** AI-Assisted Expense Tracker (Web MVP)  
**Team:** D.R Ariyarathne, Meedum Keerthisir, Supul Wickramasinghe  
**Version:** 0.1  

---

## 1. Functional Requirements (User Stories)

| ID | User Story | Acceptance Criteria | Priority |
|----|------------|---------------------|----------|
| FR1 | As a user, I want to **add an expense** with amount, category, and note so that I can track my spending. | - Expense form includes amount, category dropdown, and optional note. <br> - Saving inserts into DB. <br> - Invalid input (empty amount, negative number) is rejected. | High |
| FR2 | As a user, I want to **add income entries** so that I can track money coming in. | - Form supports type = income. <br> - Saved in DB with positive balance effect. | High |
| FR3 | As a user, I want to **view all transactions** in a list so I can see my history. | - Transactions displayed in table with date, type, category, amount, note. <br> - Sorted newest first. | High |
| FR4 | As a user, I want to **categorize expenses** so I can group spending by type. | - Category dropdown has defaults (Food, Transport, Bills, Other). <br> - User must pick one. | Medium |
| FR5 | As a user, I want to **see a summary of balance** so I know my financial position. | - Summary shows: total income, total expense, current balance. | High |
| FR6 | As a user, I want to **filter transactions by month or category** so I can analyze spending. | - Simple filter box/dropdown. <br> - Refreshes table. | Low (optional MVP+) |

---

## 2. Non-Functional Requirements

| ID | Requirement | Acceptance Criteria |
|----|-------------|---------------------|
| NFR1 | **Performance** | Transaction list loads under 2 seconds with <100 entries. |
| NFR2 | **Usability** | Simple 2-page app: Dashboard (list + summary) and Add Transaction form. |
| NFR3 | **Portability** | Runs in browser via free hosting (Replit/Render). |
| NFR4 | **Reliability** | Database persists data between sessions. |
| NFR5 | **Maintainability** | Code organized into `app.py`, `/templates`, `/static`. Comments + docstrings added. |

---

## 3. Data Requirements

- **Transactions Table**  
  - `id (PK, int, autoincrement)`  
  - `type (string: income/expense)`  
  - `amount (float)`  
  - `category (string)`  
  - `note (string, optional)`  
  - `date_created (datetime)`  

- **Categories Table (optional)**  
  - `id (PK, int, autoincrement)`  
  - `name (string)`  

---

## 4. Constraints

- Must use **AI-assisted coding tools** (Replit Ghostwriter, Codeium, GitHub Copilot, etc.).  
- Must deliver an **MVP web app** hosted for free.  
- Limited to **2–3 weeks** timeline for coursework.  

---

## 5. Open Questions

- Should categories be editable by the user or fixed defaults for MVP?  
- Do we need authentication (likely out of scope for MVP)?  
- Should balance be calculated dynamically or stored in DB?  
