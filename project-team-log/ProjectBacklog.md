# CLP API Project Backlog

*Note: This project backlog was initially developed through personal discussions and planning sessions among team members. It was later formalized and migrated to GitHub.*

### Planning and Design
- [x] Document project description.
- [x] Document API endpoints.
- [x] Distribute and document team roles and responsibilities.

### Setup and Configuration
- [x] Set up Poetry.
- [x] Create Docker configuration.
- [x] Write Makefile.
- [x] Configure GitHub Actions CI.
- [x] Define request/response data contracts (Pydantic models).
- [x] Develop `sqlalchemy` models.

### Security and Authentication
- [x] Implement JWT features in `security.py`.
- [x] Develop utility code validating headers of requests.
- [x] Test implemented features.
### Endpoints Implementation
#### Develop endpoints and DB interaction functions for:
- [x] `/application`.
- [x] `/user`.
- [x] `/orders`.

### Unit Tests
#### Write unit tests for the endpoints of:
- [x] `/application`.
- [x] `/user`.
- [x] `/orders`.

*Note: mock all the DB interactions. Test coverage must be >= 80%.*

### Functional Tests
- [x] Develop utility code of general fixtures.
#### Develop functional tests for the endpoints of:
- [x] `/application`.
- [x] `/user`.
- [x] `/orders`.

*Note: tests must interact with a running database.  Test coverage must be >= 80%.*

### Refinement
- [x] Refactor the code with respect to the open GitHub technical debt issues.
- [x] Edit GitHub repository (create ReadMe, edit file names).

### Project Retrospective
- [x] Review team interaction successes and challenges.
