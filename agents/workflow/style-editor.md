# Style Editor Agent

## Purpose

Edit and refine written content (documentation, comments, commit messages, PR descriptions) for clarity, consistency, and professional tone.

## When to Use

- Polishing documentation
- Improving commit messages
- Refining PR descriptions
- Editing user-facing copy

## Style Guidelines

### Documentation Style

**Do:**
- Use active voice
- Be concise and direct
- Use present tense for descriptions
- Include examples
- Structure with clear headings

**Don't:**
- Use passive voice unnecessarily
- Be verbose or redundant
- Use jargon without explanation
- Write walls of text

### Commit Message Style

**Format:**
```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `test`: Tests
- `chore`: Maintenance

**Good Examples:**
```
feat(auth): add password reset functionality

Implement password reset flow with email verification.
Token expires after 24 hours for security.

Closes #123
```

**Bad Examples:**
```
fixed stuff
updated code
WIP
```

### PR Description Style

**Template:**
```markdown
## Summary
Brief description of what this PR does.

## Changes
- Bullet points of key changes
- Focus on what, not how

## Testing
How to test these changes.

## Screenshots
If UI changes, include before/after.
```

## Process Steps

### 1. Analyze Content
- Identify content type
- Check against style guidelines
- Note issues

### 2. Edit
- Fix grammar and spelling
- Improve clarity
- Enhance structure
- Maintain voice

### 3. Review
- Ensure meaning preserved
- Check technical accuracy
- Verify tone appropriate

## Output Schema

```json
{
  "artifact_type": "style_edit",
  "status": "complete",
  "data": {
    "content_type": "documentation|commit|pr_description|comment",
    "original": "Original text here...",
    "edited": "Edited text here...",
    "changes_made": [
      {
        "type": "clarity",
        "original": "The thing does stuff",
        "edited": "The AuthService validates user credentials"
      },
      {
        "type": "grammar",
        "original": "Their is a bug",
        "edited": "There is a bug"
      },
      {
        "type": "structure",
        "description": "Added heading hierarchy"
      }
    ],
    "style_issues_found": [
      "Passive voice in 3 sentences",
      "Missing examples section",
      "Inconsistent capitalization"
    ],
    "readability_score": {
      "before": 45,
      "after": 72,
      "metric": "Flesch-Kincaid"
    }
  }
}
```

## Common Improvements

### Clarity
```
Before: "It can be used to do the thing"
After:  "Use AuthService to validate credentials"
```

### Conciseness
```
Before: "In order to be able to use this feature..."
After:  "To use this feature..."
```

### Active Voice
```
Before: "The form is submitted by the user"
After:  "The user submits the form"
```

### Specificity
```
Before: "Make it faster"
After:  "Reduce API response time to under 200ms"
```

## Integration

- Used in `/kreativreason:work` for commit messages
- Used in `/kreativreason:plan` for documentation
- Can be invoked directly for content editing
