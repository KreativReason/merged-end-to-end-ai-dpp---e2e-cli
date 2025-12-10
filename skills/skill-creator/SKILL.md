# Skill Creator Skill

## Purpose

Create new skills for the KreativReason E2E CLI plugin, following the standard skill structure and conventions.

## When to Use

- Adding new capabilities to the plugin
- Creating project-specific skills
- Extending plugin functionality

## Skill Structure

```
skills/
└── my-new-skill/
    ├── my-new-skill.md    # Documentation
    ├── index.ts           # Entry point (optional)
    └── templates/         # Templates (optional)
```

## Skill Template

```markdown
# [Skill Name] Skill

## Purpose

[One-sentence description of what this skill does]

## Capabilities

- Capability 1
- Capability 2
- Capability 3

## Usage

### Basic Usage

```javascript
// Example code
```

### Advanced Usage

```javascript
// More complex example
```

## Configuration

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `option1` | `string` | `'default'` | Description |

## Output Schema

```json
{
  "status": "success",
  "data": {}
}
```

## Integration

Used by:
- [Agent or command that uses this skill]
```

## Creating a New Skill

### Step 1: Define Purpose

Clearly articulate:
- What problem does this skill solve?
- Who will use it?
- How does it fit with existing skills?

### Step 2: Design Interface

```typescript
interface SkillInput {
  // Input parameters
}

interface SkillOutput {
  status: 'success' | 'error';
  data: {
    // Output data
  };
}
```

### Step 3: Create Files

```bash
mkdir -p skills/my-skill
touch skills/my-skill/my-skill.md
```

### Step 4: Document

Follow the template above.

### Step 5: Register

Add to plugin.json if needed.

## Output Schema

```json
{
  "artifact_type": "skill_created",
  "status": "success",
  "data": {
    "skill_name": "my-new-skill",
    "directory": "skills/my-new-skill/",
    "files_created": [
      "skills/my-new-skill/my-new-skill.md"
    ],
    "next_steps": [
      "Implement skill logic",
      "Add to plugin.json",
      "Test with agents"
    ]
  }
}
```

## Best Practices

### Do
- Keep skills focused on one capability
- Provide clear documentation
- Include usage examples
- Define clear input/output schemas

### Don't
- Create skills that overlap with existing ones
- Add skills without documentation
- Make skills too broad in scope

## Integration

Skills can be used by:
- Agents (via skill invocation)
- Commands (via skill calls)
- Other skills (composition)

## Example: Creating a "Code Metrics" Skill

```bash
/kreativreason:create-skill name:"code-metrics" purpose:"Calculate code complexity and quality metrics"
```

Generated structure:
```
skills/
└── code-metrics/
    ├── code-metrics.md
    └── index.ts
```

Generated documentation:
```markdown
# Code Metrics Skill

## Purpose
Calculate code complexity and quality metrics for codebases.

## Capabilities
- Cyclomatic complexity calculation
- Lines of code counting
- Function/method length analysis
- Dependency counting

...
```
