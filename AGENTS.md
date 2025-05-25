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
- Configure PostgreSQL for production environment
- Set up GitHub Actions CI pipeline for tests and linting
- Plan and implement user roles and permissions (Admin, Moderator, Normie(?) (Names to be refined later as well)) with appropriate access levels and group-based permissions.

# User Profile & Personal Dashboard enhancements
- Implement a “My Profile” page for authenticated users with the following features:
  0. Access & Navigation:
     - Reachable by clicking your username or avatar in the main nav.
     - Clicking any user’s profile picture (e.g. next to a post or comment) opens that user’s profile page.
     - When viewing another user’s profile, show stats in read-only mode; your own profile remains editable.
  1. Recent Activity Stats:
     - Display the user’s most recent post or review, including title/link and timestamp.
     - Indicate the date/time of last activity.
  2. Overall Stats Summary:
     - Show aggregate counts (e.g. total posts, total reviews).
     - Compute and display metrics like average words per post and time since signup/last login.
  3. Profile Picture Management:
     - Allow users to upload, crop, and change a profile avatar.
     - Store and serve the avatar image for display next to their posts and comments.
  4. Notifications Center:
     - Track replies to the user’s reviews (mark as seen/unseen).
     - Show a notification badge on the user-nav link when there are unread replies.
     - Provide a page or dropdown listing recent replies with “mark as read” actions.
