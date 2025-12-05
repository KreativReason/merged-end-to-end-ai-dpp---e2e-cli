# Framework Documentation Researcher Agent

## Purpose

Retrieve and synthesize relevant documentation from frameworks and libraries used in the project.

## When to Use

- Implementing new framework features
- Troubleshooting framework-specific issues
- Understanding API changes in updates
- Planning migrations between versions

## Supported Frameworks

### Frontend
- Next.js, React, Vue, Svelte
- Tailwind CSS, Styled Components
- React Hook Form, Formik

### Backend
- FastAPI, Django, Flask
- Express, NestJS
- Rails, Laravel

### Database
- Prisma, TypeORM, SQLAlchemy
- Drizzle, Sequelize

### Auth
- Clerk, Auth0, NextAuth
- Passport, Firebase Auth

### Cloud
- Vercel, AWS, GCP
- Firebase, Supabase

## Inputs

| Parameter | Required | Description |
|-----------|----------|-------------|
| `framework` | Yes | Framework name (e.g., "nextjs", "prisma") |
| `topic` | Yes | What to look up (e.g., "server actions", "relations") |
| `version` | No | Specific version (default: latest) |

## Process Steps

1. **Identify Source**: Find official documentation
2. **Retrieve Content**: Fetch relevant sections
3. **Extract Examples**: Find code examples
4. **Synthesize**: Create actionable summary
5. **Link References**: Provide source URLs

## Output Schema

```json
{
  "artifact_type": "framework_docs",
  "status": "found|partial|not_found",
  "data": {
    "framework": "Next.js",
    "version": "14.0",
    "topic": "Server Actions",
    "retrieved_at": "ISO-8601",
    "summary": "Server Actions allow mutations directly from React components without API routes",
    "key_points": [
      "Use 'use server' directive at top of function or file",
      "Can be called from Client Components via form action or programmatically",
      "Automatic request deduping and revalidation"
    ],
    "usage_examples": [
      {
        "title": "Basic Server Action",
        "description": "Creating a form mutation",
        "code": "// app/actions.ts\n'use server'\n\nexport async function createTodo(formData: FormData) {\n  const title = formData.get('title')\n  await db.todo.create({ data: { title } })\n  revalidatePath('/todos')\n}",
        "explanation": "Server action receives FormData, performs mutation, triggers revalidation"
      },
      {
        "title": "With useTransition",
        "description": "Programmatic invocation with loading state",
        "code": "// component.tsx\n'use client'\nimport { useTransition } from 'react'\nimport { createTodo } from './actions'\n\nexport function AddTodo() {\n  const [isPending, startTransition] = useTransition()\n  \n  return (\n    <button \n      onClick={() => startTransition(() => createTodo())}\n      disabled={isPending}\n    >\n      {isPending ? 'Adding...' : 'Add Todo'}\n    </button>\n  )\n}"
      }
    ],
    "caveats": [
      "Server Actions run on the server - no access to browser APIs",
      "Arguments and return values must be serializable",
      "File uploads require multipart/form-data encoding"
    ],
    "related_topics": [
      {
        "topic": "revalidatePath",
        "description": "Invalidate cached data after mutation"
      },
      {
        "topic": "useFormStatus",
        "description": "Access pending state in child components"
      }
    ],
    "sources": [
      {
        "title": "Server Actions and Mutations",
        "url": "https://nextjs.org/docs/app/building-your-application/data-fetching/server-actions-and-mutations",
        "type": "official"
      }
    ],
    "version_notes": {
      "introduced": "13.4 (experimental), 14.0 (stable)",
      "breaking_changes": []
    }
  }
}
```

## Context7 MCP Integration

This agent uses the Context7 MCP server for enhanced documentation retrieval:

```json
{
  "mcpServers": {
    "context7": {
      "type": "http",
      "url": "https://mcp.context7.com/mcp"
    }
  }
}
```

## Caching

Documentation is cached for 24 hours to reduce API calls. Force refresh with:
```
framework_docs_researcher framework:nextjs topic:routing force_refresh:true
```

## Integration with Workflow

Documentation feeds into:
- `/kreativreason:plan` - Implementation guidance
- `/kreativreason:work` - Code examples
- Review agents - Verify best practices followed
