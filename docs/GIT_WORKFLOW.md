# Git Workflow Guide for ServiceHub Team

## Branch Strategy

```
main (protected)
├── person-a-auth           (Person A: Backend Lead)
├── person-b-booking        (Person B: Backend)
├── person-c-frontend-auth  (Person C: Frontend Lead)
└── person-d-frontend-booking (Person D: Frontend)
```

---

## Initial Setup (For All Team Members)

### 1. Clone Repository

```bash
git clone https://github.com/YOUR_ORG/servicehub.git
cd servicehub
```

### 2. Create Your Feature Branch

```bash
# Person A
git checkout -b person-a-auth

# Person B
git checkout -b person-b-booking

# Person C
git checkout -b person-c-frontend-auth

# Person D
git checkout -b person-d-frontend-booking
```

### 3. Push Your Branch

```bash
git push -u origin YOUR_BRANCH_NAME
```

---

## Daily Workflow

### Morning: Sync with Main

```bash
# Switch to main branch
git checkout main

# Pull latest changes
git pull origin main

# Switch back to your feature branch
git checkout YOUR_BRANCH_NAME

# Merge main into your branch (to get teammates' updates)
git merge main

# Resolve any conflicts if they occur
# Then push updated branch
git push origin YOUR_BRANCH_NAME
```

### During Development: Commit Often

```bash
# Check status
git status

# Stage changes
git add .
# Or stage specific files
git add path/to/file.py

# Commit with meaningful message
git commit -m "feat(auth): add JWT token generation"

# Push to your branch
git push origin YOUR_BRANCH_NAME
```

---

## Commit Message Format

Follow conventional commits format:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, no logic change)
- **refactor**: Code refactoring
- **test**: Adding or updating tests
- **chore**: Maintenance tasks

### Examples

```bash
# Good commit messages
git commit -m "feat(auth): implement JWT authentication"
git commit -m "fix(booking): prevent overlapping bookings"
git commit -m "docs(readme): update setup instructions"
git commit -m "refactor(providers): optimize distance calculation"

# Bad commit messages (avoid these)
git commit -m "fixed stuff"
git commit -m "update"
git commit -m "asdf"
```

---

## Creating a Pull Request

### When Your Feature is Ready

```bash
# 1. Make sure all changes are committed
git status

# 2. Push final changes
git push origin YOUR_BRANCH_NAME

# 3. Go to GitHub repository
# 4. Click "Compare & pull request"
# 5. Fill out PR template:
```

### PR Title Format

```
<type>: <description>

Example: "feat: implement authentication system"
```

### PR Description Template

```markdown
## What does this PR do?

Brief description of changes

## Checklist

- [ ] Code follows project style guidelines
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No console errors
- [ ] Tested locally

## Related Issues

Closes #123

## Screenshots (if applicable)

[Add screenshots for UI changes]
```

### Request Review

Assign reviewers:
- Backend PRs: Request review from another backend teammate
- Frontend PRs: Request review from another frontend teammate
- Critical changes: Request review from team lead

---

## Handling Merge Conflicts

### When You See Conflicts

```bash
# 1. Pull latest main
git checkout main
git pull origin main

# 2. Switch to your branch
git checkout YOUR_BRANCH_NAME

# 3. Merge main (this will show conflicts)
git merge main

# 4. Open conflicted files and resolve
# Look for markers:
# <<<<<<< HEAD (your changes)
# =======
# >>>>>>> main (incoming changes)

# 5. After resolving, stage files
git add path/to/resolved/file.py

# 6. Complete merge
git commit -m "merge: resolve conflicts with main"

# 7. Push
git push origin YOUR_BRANCH_NAME
```

---

## Code Review Process

### As a PR Author

1. Create PR with clear description
2. Assign reviewers
3. Address review comments
4. Push updates to same branch (PR auto-updates)
5. Request re-review after changes

### As a Reviewer

1. Review code for:
   - Correctness
   - Follows project conventions
   - No obvious bugs
   - Adequate error handling
2. Leave constructive comments
3. Approve or request changes
4. Re-review after updates

---

## Integration Checkpoints

### Hour 8 Checkpoint

**All team members:**

```bash
# Sync with team changes
git checkout main
git pull origin main
git checkout YOUR_BRANCH_NAME
git merge main
git push origin YOUR_BRANCH_NAME
```

**Test integration locally:**
```bash
docker-compose down
docker-compose up --build
```

### Hour 16 Checkpoint

Same as Hour 8, plus:
- Test end-to-end flow
- Fix critical bugs
- Merge urgent fixes to main

---

## Emergency Procedures

### Accidentally Committed to Main

```bash
# If you haven't pushed yet
git reset HEAD~1

# If you already pushed (DON'T DO THIS - contact team lead)
# Team lead will need to force push or revert
```

### Need to Undo Last Commit

```bash
# Keep changes, undo commit
git reset --soft HEAD~1

# Discard changes and commit
git reset --hard HEAD~1  # ⚠️ Use with caution!
```

### Need to Sync Fork (if using forks)

```bash
# Add upstream remote (one-time setup)
git remote add upstream https://github.com/ORIGINAL_ORG/servicehub.git

# Fetch upstream changes
git fetch upstream

# Merge into your main
git checkout main
git merge upstream/main
git push origin main
```

---

## Best Practices

### ✅ DO

- Commit frequently with meaningful messages
- Pull from main daily
- Keep PRs focused and small
- Test locally before pushing
- Review your own diff before creating PR
- Respond to review comments promptly

### ❌ DON'T

- Commit directly to main
- Force push to shared branches
- Commit secrets or .env files
- Leave commented-out code
- Commit large binary files
- Ignore merge conflicts

---

## Useful Git Commands

### Viewing History

```bash
# View commit log
git log --oneline --graph --all

# View changes in last commit
git show HEAD

# View changes between branches
git diff main..YOUR_BRANCH_NAME
```

### Stashing Changes

```bash
# Save uncommitted changes
git stash

# List stashes
git stash list

# Apply last stash
git stash pop

# Apply specific stash
git stash apply stash@{0}
```

### Branch Management

```bash
# List all branches
git branch -a

# Delete local branch
git branch -d branch-name

# Delete remote branch
git push origin --delete branch-name

# Rename current branch
git branch -m new-name
```

---

## Getting Help

- **Git documentation**: https://git-scm.com/doc
- **GitHub guides**: https://guides.github.com/
- **Team Slack**: #servicehub-dev
- **Ask Person A (Backend Lead)** for git issues

---

**Remember: Communication is key! Always let the team know if you're blocked or need help.**

*Last updated: December 10, 2025*
