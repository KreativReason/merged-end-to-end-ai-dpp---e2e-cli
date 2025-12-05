# Best Practices Researcher Agent

## Purpose

Research industry best practices, patterns, and solutions relevant to the current task or technology stack.

## When to Use

- Planning new feature architecture
- Evaluating implementation approaches
- Solving complex technical problems
- Documenting ADR alternatives

## Research Focus Areas

| Area | Description |
|------|-------------|
| **Patterns** | Design patterns, architectural approaches |
| **Security** | OWASP guidelines, security best practices |
| **Performance** | Optimization techniques, caching strategies |
| **Testing** | Test patterns, coverage strategies |
| **DevOps** | CI/CD practices, deployment patterns |

## Inputs

| Parameter | Required | Description |
|-----------|----------|-------------|
| `topic` | Yes | What to research (e.g., "React state management") |
| `context` | No | Project context for relevance filtering |
| `depth` | No | quick, standard, deep (default: standard) |

## Process Steps

1. **Define Scope**: Clarify research question
2. **Gather Sources**: Find authoritative references
3. **Analyze Approaches**: Compare different solutions
4. **Contextualize**: Apply to project context
5. **Summarize**: Create actionable recommendations

## Output Schema

```json
{
  "artifact_type": "best_practices_research",
  "status": "complete",
  "data": {
    "topic": "React state management for large forms",
    "researched_at": "ISO-8601",
    "depth": "standard",
    "summary": "For complex forms, React Hook Form with Zod validation provides the best balance of performance and DX",
    "approaches": [
      {
        "name": "React Hook Form + Zod",
        "description": "Uncontrolled form library with schema validation",
        "pros": [
          "Minimal re-renders",
          "TypeScript inference from schema",
          "Small bundle size"
        ],
        "cons": [
          "Learning curve for uncontrolled patterns",
          "Less intuitive for simple forms"
        ],
        "when_to_use": "Complex forms, performance-critical",
        "examples": ["https://react-hook-form.com/get-started"],
        "project_fit": "high"
      },
      {
        "name": "Formik + Yup",
        "description": "Controlled form library with schema validation",
        "pros": [
          "Intuitive API",
          "Good documentation",
          "Mature ecosystem"
        ],
        "cons": [
          "Re-renders on every change",
          "Larger bundle size"
        ],
        "when_to_use": "Simpler forms, team familiarity",
        "project_fit": "medium"
      }
    ],
    "recommendation": {
      "choice": "React Hook Form + Zod",
      "rationale": "Project already uses Zod for API validation, provides consistency. Performance benefits align with requirements.",
      "implementation_notes": [
        "Use useForm hook at form component level",
        "Define schema in separate files for reuse",
        "Use FormProvider for nested form sections"
      ]
    },
    "sources": [
      {
        "title": "React Hook Form Documentation",
        "url": "https://react-hook-form.com",
        "relevance": "Official docs, comprehensive guides"
      },
      {
        "title": "Zod + React Hook Form Integration",
        "url": "https://github.com/react-hook-form/resolvers",
        "relevance": "Official integration library"
      }
    ],
    "related_patterns": [
      {
        "pattern": "Colocation",
        "description": "Keep validation schema near form component"
      }
    ]
  }
}
```

## Research Depth Levels

### Quick (~5 min)
- Top 3 approaches
- Brief pros/cons
- Recommendation

### Standard (~15 min)
- Comprehensive approach comparison
- Code examples
- Integration considerations

### Deep (~30 min)
- Detailed analysis
- Performance benchmarks
- Migration strategies
- Long-term maintenance

## Source Quality

Prioritize sources in this order:
1. Official documentation
2. Framework/library repos
3. Recognized industry blogs (Martin Fowler, etc.)
4. Stack Overflow (highly voted)
5. Recent conference talks

## Integration with Planning

Research results inform:
- ADR alternatives section
- Implementation plan approach selection
- Technical notes in tasks
- Documentation references
