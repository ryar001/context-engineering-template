**Note:** This tool works with `GEMINI.md` or Other context file and is triggered by commands starting with `:ai-tracker`.

## Core Function

This utility monitors, summarizes, and documents changes in a software project. It analyzes file modifications and appends a categorized summary to `UPDATES.md` at the project root. Then it will also do a commit with relevant message.

## Workflow

1.  Stage changes using `git add -A`.
2.  The tool uses `git diff` to find staged changes.
    - Then use the result of `git diff` for summarization and categorization.
    - The summary is appended to `UPDATES.md`.
    - the latest update is always at the top of the file.
    - The commit message generate the summary based on the `UPDATES.md`.
    - ignore spaces, newlines, and other whitespace changes or non-code changes when generating the summary.

## Usage

### Generate or update `UPDATES.md`:

```bash
# Analyze staged changes and write to UPDATES.md
:ai-tracker update
```

### Compare against a specific commit or branch:

```bash
# Compare against a specific commit
:ai-tracker update --ref <commit-hash>

# Compare against another branch
:ai-tracker update --ref <branch-name>
```

## `UPDATES.md` Format

Changes are grouped by date, category, and then file.

### Example:

```markdown
# Project Updates

## 2023-10-27

### What's New

#### `src/features/auth.js`

- Implemented the core logic for the new user authentication flow.
- Added a new component for the login form.

### Bugfix

#### `src/components/Header.js`

- Fixed a layout issue where the logo would overlap navigation links on smaller screens.
```