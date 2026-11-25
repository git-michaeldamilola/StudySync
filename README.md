# StudySync Backend
 
StudySync is a university study-planning and task-management application. This repository contains its Django REST API backend, built for integration with the React frontend.
 
## Status
 
MVP backend checkpoint: validated and ready for frontend integration.
 
- Django's system check reported no issues, and migrations were applied.

- Manually tested: registration/login, token authentication, projects, membership, task CRUD/assignment/status, progress/overdue fields, and permission boundaries.

- This is an MVP checkpoint, not a production audit.
 
## Stack
 
- Python 3.13.9 (development environment)

- Django 6.1.3

- Django REST Framework with DRF Token Authentication

- SQLite development database
 
## Setup (macOS)
 
```bash

cd ~/Desktop/StudySync

python3 -m venv .venv

source .venv/bin/activate

python -m pip install --upgrade pip

pip install django djangorestframework

```
 
If `requirements.txt` exists, prefer `pip install -r requirements.txt`.
 
## Run
 
```bash

source .venv/bin/activate

python manage.py migrate

python manage.py runserver

```
 
Local API: <http://127.0.0.1:8000/>
 
## Endpoints
 
| Function | Method | Endpoint |
|---|---|---|
| Register | POST | `/api/users/register/` |
| Login | POST | `/api/users/login/` |
| List/create projects | GET/POST | `/api/projects/` |
| List/add members | GET/POST | `/api/projects/<project_id>/members/` |
| Remove member (owner) | DELETE | `/api/projects/<project_id>/members/<user_id>/` |
| List/create tasks | GET/POST | `/api/projects/tasks/` |
| Retrieve/update/delete task | GET/PUT/PATCH/DELETE | `/api/projects/tasks/<task_id>/` |

Protected requests use the header `Authorization: Token <token>`. See [API_REFERENCE.md](API_REFERENCE.md) for examples.
 
## Documentation
 
- [API_REFERENCE.md](API_REFERENCE.md): endpoints and payloads

- [FRONTEND_HANDOFF.md](FRONTEND_HANDOFF.md): React integration

- [TESTING_AND_VALIDATION.md](TESTING_AND_VALIDATION.md): checkpoint test record

- [DEVELOPMENT_SETUP.md](DEVELOPMENT_SETUP.md): setup and troubleshooting

- [PROJECT_STATUS.md](PROJECT_STATUS.md): scope and next phase

- [SECURITY_NOTES.md](SECURITY_NOTES.md): permissions and deployment cautions

- [HANDOFF_SUMMARY.md](HANDOFF_SUMMARY.md): concise handoff
 
## Database Note
 
SQLite is the current MVP database. MySQL migration and production deployment are not validated.
 