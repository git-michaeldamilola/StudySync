# Testing and Validation Record
 
## Environment Checks
 
- `python manage.py check`: reported 0 issues.

- `python manage.py showmigrations`: migrations applied for `admin`, `auth`, `authtoken`, `contenttypes`, `projects`, and `sessions`. The `users` app showed no migrations.
 
## Manual Functional Checks
 
- Registration, including duplicate username/email validation.

- Login and token issuance.

- Project creation and owner access.

- Member addition, member access, and membership listing.

- Task creation, retrieval, update, assignment, and status change.

- Task marked `Completed`: the project response reported 1 total task, 1 completed, and 100% progress.

- Overdue indicator checked (`false` for the completed test task).

- Member removal, then re-addition.
 
## Access Checks
 
- Outsider project list and task list returned no accessible records.

- Outsider direct task access and deletion were rejected.

- Member task deletion was rejected (owner-only).

- Member attempt at membership management was rejected (owner-only).
 
## Development Test Data
 
Do not expose credentials or tokens.
 
| Item | Value |

|---|---|

| Project | ID 2: StudySync MVP Project |

| Owner test account | `studysync_test` (User ID 2) |

| Member test account | `team_test` (User ID 4) |

| Task | ID 1 |
 
Membership record IDs may change when recreated.
 
## Limitations
 
Manual tests were recorded. A comprehensive automated test suite is not confirmed. The following remain unvalidated:
 
- Production deployment

- MySQL migration

- CORS configuration

- Full React integration

- Formal security audit
 