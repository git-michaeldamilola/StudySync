# Security and Deployment Notes
 
## Behavior Tested at the MVP Checkpoint
 
- Authentication is required for project and task API endpoints.

- Project access is scoped to the creator or project members.

- Project membership management is restricted to owners.

- Owner membership cannot be removed through the member removal endpoint.

- Task deletion is restricted to the project owner.

- Task assignment is checked against project membership.

- Outsider access to project and task endpoints was rejected in manual checks.
 
## Before Deployment
 
- [ ] Rotate or invalidate development tokens that were exposed during testing.

- [ ] Remove or reset test users and test data as appropriate.

- [ ] Never commit passwords, tokens, `.env` files, or secrets.

- [ ] Use environment variables for secrets and database credentials.

- [ ] Set `DEBUG=False` and configure `ALLOWED_HOSTS`.

- [ ] Configure HTTPS and CORS explicitly for the frontend origin.

- [ ] Choose and configure the production database (MySQL migration if required).

- [ ] Review serializers, permissions, validation, authentication, and error handling.

- [ ] Add automated tests, including permission tests.

- [ ] Plan backups and recovery, and review dependencies.
 
## Disclaimer
 
This is an MVP validation record, not a security audit or production-readiness certification.
 