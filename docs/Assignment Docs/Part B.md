# Team JOHTO Project: Part B - Alumni Network AI Dashboard

---

## 1. Decompose User Stories into Tasks

### User Story 1: Alumni (Assigned: Brandon Medina)

“As an alumnus of CGU, I want to give back by mentoring a student. I want to be able to create an account, log in, and see a dashboard of students I match with that have similar classes I took, or are interested in the industry I work in, or have the same degree concentration as me, or are in my location, so that I can connect with them.”

**Tasks**

1. **Define database requirements** – 3 hrs
   - Alumni, Student, Classes Taken, Industry, Degree Concentration, Job Location
2. **Build database schema SQL** – 6 hrs
   - Tables: `alumni`, `students`, `classes`, `alumni_classes`, `student_classes`, `industries`, `degree_concentrations`, `job_locations`
3. **Create HTML skeleton & base** – 5 hrs
   - `main.py`, `index.html`, `base.html`, `login.html`, `register.html`, `dashboard.html`, `profile.html`
4. **Connect Flask with database** – 6 hrs
   - Write `seed_db.py`, `empty_db.py`, helper DB functions, sample queries
5. **Implement login route** – 5 hrs
   - Validate credentials, query DB, password hash check, sessions, flash messages
6. **Implement logout route** – 2 hrs
   - Clear session, redirect, flash message
7. **Implement registration route** – 5 hrs
   - Form validation, insert new users, hash password, redirect to login
8. **Build profile route** – 4 hrs
   - Display profile, update/edit button
9. **Add profile edit constraints** – 4 hrs
   - Allow edits only on alumni-specific fields (industry, concentration, job location, LinkedIn)
10. **Create dashboard page** – 6 hrs
    - Display matched students by role
11. **Implement matching system** – 8 hrs
    - Define criteria weights, join alumni ↔ students, return sorted matches
12. **Implement connection feature** – 7 hrs
    - Connections table, pending requests, accept/reject workflow
13. **Testing & dataset validation** – 8 hrs
    - Unit + integration tests, synthetic dataset, manual UI testing
14. **Create tasks/issues on JIRA** – 2 hrs
    - JIRA project, Kanban board, dependencies, due dates

---

### User Story 2: Student Mentor Suggestions (Assigned: PJ, Nihaad)

- Create synthetic student profiles
- Implement AI matching logic
- Connect RAG/SQL backend
- Define system prompt and few-shot examples
- Service endpoints for ranked mentors & connection requests
- Wire student dashboard (Find Mentors, Connect)
- Handle login/role checks, empty states, and test queries

---

### User Story 3: Administrator Dashboard (Assigned: Alex)

“As a university administrator I want to view alumni data visualizations on a dashboard using synthetic data during development so I can explore and validate how the system will display insights before connecting to real alumni records.”

**Tasks**

1. **Setup environment** (3–5 hrs)
   - Create frontend folder, install visualization libraries (plotly, dash, matplotlib, seaborn)
2. **Synthetic data organization** (8 hrs)
   - Load dataset, create REST API endpoints, simulate real-time updates
3. **Dashboard visualizations** (10 hrs)
   - Industry distribution, geographic spread, career timeline, mentorship opt-in stats, engagement trends
4. **Integration & interactivity** (10 hrs)
   - Connect charts to backend API, add filtering, tooltips, dashboard tabs
5. **Testing & validation** (10 hrs)
   - Unit tests, API validation, chart rendering checks
6. **Documentation** (10 hrs)
   - Instructions, screenshots, dataset regeneration notes

---

### User Story 4: Project Management (Assigned: Jin, Nihaad)

“As a project developer responsible for analytics, I want to integrate alumni and student data into a dashboard prototype so that administrators and alumni can visualize distributions, trends, and mentorship participation during development, ensuring the system’s insights are validated before connecting to real data.”

**Tasks**

1. Environment Setup & Structure (4 hrs)
2. Dashboard Prototype Layout (6 hrs)
3. Visualization Components (8 hrs)
4. Data Integration (6 hrs)
5. Documentation & Testing (4 hrs)

---

### Optional User Story: Developer RAG Integration

- Set up RAG pipeline or SQL fallback
- Connect 10 profiles
- Validate retrieval quality

---

## 2. Milestone 1.0 Features

- Search functionality (Admin view)
- Alumni and student profile creation
- Analytics dashboard prototype (basic charts)
- GitHub repo with functional + test code

---

## 3. Iterations for Milestone 1.0

**Iteration 1 (30 days, 100 hrs total):**

- Database setup
- API & backend logic
- Synthetic dataset + profiles
- Basic dashboard integration

**Iteration 2 (60 days, 200 hrs total):**

- AI matching logic
- Dashboard analytics prototype
- Profile opt-in implementation
- Testing & refinement
- Sync with AI Squared

_Total work = 200 hrs, completed in 60 days (velocity = 20 hrs/week/team member)._

---

## 4. Task Allocation

- **Brandon**: Database schema, RAG setup, alumni profiles
- **Alexander**: Python backend logic, mentor suggestion engine
- **Haoran**: Dashboard integration, analytics prototype
- **Prajwal**: API development, AI matching support
- **Nihaad**: Sync with AI Squared, documentation, manage repo, synthetic student profiles, AI matching logic, RAG/SQL backend

---

## 5. Burn Down Chart

_(Attach chart image in repo, e.g., `docs/burndown.png`)_

---

## 6. Stand-Up Meetings

- Frequency: **2x/week (Tuesdays & Thursdays)**
- Logs/Agenda stored in repo (`docs/standups/`)
- Example agenda: Progress updates, blockers, reallocation
- Meeting notes uploaded as Markdown files

---

## 7. Development & Testing Environment

- GitHub repo initialized with `README.md`, `requirements.txt`, and `tests/`
- Python virtual environment created
- Synthetic alumni/student dataset in `/data`
- Basic search API and test queries implemented
- CI/CD pipeline setup for automated testing in GitHub Actions
