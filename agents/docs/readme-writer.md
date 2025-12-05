# README Writer Agent

## Purpose

Generate and maintain high-quality README documentation following best practices for open source projects.

## When to Use

- Creating README for new projects
- Updating documentation after major changes
- Standardizing project documentation
- Onboarding documentation improvements

## README Structure

### Essential Sections

1. **Title & Badges** - Project name, status badges
2. **Description** - What the project does (1-2 sentences)
3. **Features** - Key capabilities
4. **Installation** - How to install
5. **Quick Start** - Get running in < 5 minutes
6. **Usage** - Common use cases with examples
7. **API/Configuration** - Detailed reference
8. **Contributing** - How to contribute
9. **License** - License information

### Optional Sections

- Screenshots/GIFs
- Roadmap
- Changelog
- Acknowledgments
- FAQ

## Quality Criteria

### Good README Characteristics

- **Scannable**: Headers, bullets, code blocks
- **Example-driven**: Working code examples
- **Complete**: Answers common questions
- **Current**: Matches actual code
- **Accessible**: No assumed knowledge

### Common Issues

| Issue | Fix |
|-------|-----|
| No quick start | Add 5-minute getting started |
| Outdated examples | Verify examples work |
| Missing prerequisites | List all requirements |
| No badges | Add build/coverage status |
| Wall of text | Add structure and formatting |

## Output Schema

```json
{
  "artifact_type": "readme_generation",
  "status": "complete",
  "data": {
    "project_name": "my-project",
    "analyzed_at": "ISO-8601",
    "existing_readme": {
      "exists": true,
      "completeness_score": 65,
      "missing_sections": ["quick_start", "badges", "contributing"]
    },
    "generated_sections": [
      {
        "section": "badges",
        "content": "![Build Status](...) ![Coverage](...)"
      },
      {
        "section": "quick_start",
        "content": "## Quick Start\n\n```bash\nnpm install my-project\n```"
      }
    ],
    "recommendations": [
      "Add GIF showing main feature",
      "Include troubleshooting section",
      "Add link to API documentation"
    ],
    "full_readme": "# Project Name\n\n..."
  }
}
```

## Template

```markdown
# Project Name

[![Build Status](badge-url)](link)
[![Coverage](badge-url)](link)
[![License](badge-url)](link)

Brief, compelling description of what this project does and why it matters.

## Features

- ✅ Feature one
- ✅ Feature two
- ✅ Feature three

## Installation

```bash
npm install project-name
```

### Prerequisites

- Node.js >= 18
- npm >= 9

## Quick Start

```javascript
import { something } from 'project-name';

// Minimal working example
const result = something();
console.log(result);
```

## Usage

### Basic Usage

```javascript
// Example with explanation
```

### Advanced Usage

```javascript
// More complex example
```

## Configuration

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `option1` | `string` | `'default'` | What it does |

## API Reference

### `functionName(param)`

Description of what it does.

**Parameters:**
- `param` (Type): Description

**Returns:** Type - Description

**Example:**
```javascript
functionName('value');
```

## Contributing

Contributions welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) first.

## License

MIT © [Author Name](link)
```

## Integration

- Part of project scaffolding
- Can be invoked for documentation updates
- Works with `/kreativreason:work` for doc tasks
