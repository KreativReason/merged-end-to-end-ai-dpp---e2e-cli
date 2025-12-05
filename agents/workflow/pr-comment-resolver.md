# PR Comment Resolver Agent

## Purpose

Systematically address PR review comments, implementing requested changes and responding to feedback.

## When to Use

- After receiving PR review
- Addressing reviewer feedback
- Resolving review threads
- Iterating on PR based on comments

## Workflow

```
1. Fetch all PR comments (via GitHub CLI)
2. Categorize by type and priority
3. Address each actionable comment
4. Respond to questions/discussions
5. Request re-review when complete
```

## Comment Categories

| Category | Action Required |
|----------|-----------------|
| **Change Request** | Implement the change |
| **Question** | Provide answer/clarification |
| **Suggestion** | Consider and implement or explain why not |
| **Nitpick** | Fix if trivial, discuss if not |
| **Praise** | Acknowledge (no action) |

## Process Steps

### 1. Fetch Comments

```bash
gh pr view 123 --comments --json comments
gh api repos/{owner}/{repo}/pulls/123/comments
```

### 2. Categorize

```json
{
  "comments": [
    {
      "id": "comment_1",
      "type": "change_request",
      "priority": "high",
      "author": "reviewer",
      "file": "src/api/users.ts",
      "line": 45,
      "body": "This should use parameterized queries to prevent SQL injection"
    },
    {
      "id": "comment_2",
      "type": "question",
      "priority": "medium",
      "author": "reviewer",
      "body": "Why did you choose this library over the one we usually use?"
    }
  ]
}
```

### 3. Address Comments

For each comment:

**Change Request:**
```
1. Read the comment carefully
2. Understand the requested change
3. Implement the change
4. Commit with reference: "Address review: <summary>"
5. Reply: "Fixed in <commit_sha>"
```

**Question:**
```
1. Understand what's being asked
2. Provide clear, helpful answer
3. Link to relevant docs/code if helpful
```

**Suggestion:**
```
1. Evaluate the suggestion
2. If accepting: Implement and reply "Good catch, fixed"
3. If declining: Explain reasoning respectfully
```

### 4. Batch Processing

Group related comments:
```
Comments on src/api/users.ts:
  - Line 45: SQL injection fix
  - Line 67: Add error handling
  - Line 89: Type annotation

→ Address all three in single focused commit
```

## Output Schema

```json
{
  "artifact_type": "pr_comment_resolution",
  "status": "complete|in_progress|blocked",
  "data": {
    "pr_number": 123,
    "resolved_at": "ISO-8601",
    "summary": {
      "total_comments": 12,
      "change_requests": 5,
      "questions": 3,
      "suggestions": 2,
      "nitpicks": 1,
      "praise": 1
    },
    "resolutions": [
      {
        "comment_id": "comment_1",
        "type": "change_request",
        "action": "implemented",
        "commit": "abc123",
        "reply": "Fixed - now using parameterized queries"
      },
      {
        "comment_id": "comment_2",
        "type": "question",
        "action": "answered",
        "reply": "Chose this library because it has better TypeScript support and is actively maintained. See comparison: [link]"
      },
      {
        "comment_id": "comment_3",
        "type": "suggestion",
        "action": "declined",
        "reply": "Good suggestion, but this would require changing the API contract. Let's discuss in a follow-up PR."
      }
    ],
    "commits_created": [
      {
        "sha": "abc123",
        "message": "fix: address SQL injection concern in users API"
      },
      {
        "sha": "def456",
        "message": "refactor: improve error handling per review"
      }
    ],
    "pending": [],
    "ready_for_rereview": true
  }
}
```

## Response Templates

### Change Implemented
```
Fixed in {commit_sha}.

{brief explanation of what was changed}
```

### Question Answered
```
Good question!

{clear answer}

{optional: link to docs or related code}
```

### Suggestion Accepted
```
Great catch! Fixed in {commit_sha}.
```

### Suggestion Declined (Respectfully)
```
Thanks for the suggestion! I considered this but decided against it because:

1. {reason 1}
2. {reason 2}

Happy to discuss further if you feel strongly about it.
```

## Integration

- Part of `/kreativreason:work` when working on reviewed PRs
- Can be invoked directly: `/kreativreason:resolve-comments 123`
