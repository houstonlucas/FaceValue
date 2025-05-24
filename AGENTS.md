### Instructions for maintaining this repo
- Maintain this `AGENTS.md` file with design decisions, future tasks, feature roadmaps, etc.
- Make sure to divide tasks into managable sizes.
- Make sure to add tests for new features.
- Keep the Current Tasks list below updated when tasks are completed.
- If all tasks have been completed suggest some to the user and update the list with their decisions.

### Future Considerations
- An initial MVP will be created running entirely locally, but eventually a migration into aws will occur.
  - Design decisions should take this into account

### Current Tasks
- Integrate puzzle rating models (Puzzle, Review) into the database
- Implement CRUD views for puzzles and reviews
- Add search functionality for puzzles by brand and type
- Configure PostgreSQL for production environment
- Set up GitHub Actions CI pipeline for tests and linting
- Plan and implement user roles and permissions (Admin, Moderator, Normie(?) (Names to be refined later as well)) with appropriate access levels and group-based permissions.
