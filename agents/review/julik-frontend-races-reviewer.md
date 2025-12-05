# Frontend Race Conditions Reviewer Agent

## Purpose

Detect race conditions, timing issues, and async bugs in frontend JavaScript/TypeScript code.

## When to Use

- Reviewing React/Vue/Svelte components
- Analyzing async data fetching
- Debugging intermittent frontend bugs
- State management code review

## Race Condition Patterns

### Stale Closure
```typescript
// Bad: Stale closure in useEffect
function SearchComponent() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);

  useEffect(() => {
    fetch(`/api/search?q=${query}`)
      .then(res => res.json())
      .then(data => setResults(data)); // Race condition!
  }, [query]);
}

// Good: Abort controller
function SearchComponent() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);

  useEffect(() => {
    const controller = new AbortController();

    fetch(`/api/search?q=${query}`, { signal: controller.signal })
      .then(res => res.json())
      .then(data => setResults(data))
      .catch(err => {
        if (err.name !== 'AbortError') throw err;
      });

    return () => controller.abort();
  }, [query]);
}
```

### Unmounted Component Updates
```typescript
// Bad: State update after unmount
function DataLoader() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetchData().then(setData); // May update unmounted component!
  }, []);
}

// Good: Track mounted state
function DataLoader() {
  const [data, setData] = useState(null);

  useEffect(() => {
    let mounted = true;

    fetchData().then(result => {
      if (mounted) setData(result);
    });

    return () => { mounted = false; };
  }, []);
}
```

### Double Fetch
```typescript
// Bad: React 18 Strict Mode double fetch
useEffect(() => {
  fetch('/api/data'); // Runs twice in dev!
}, []);

// Good: Proper cleanup or React Query/SWR
const { data } = useQuery(['data'], fetchData);
```

## Checks Performed

| Check | Description |
|-------|-------------|
| Stale closures | Async callbacks with stale state |
| Unmount updates | State updates after unmount |
| Missing cleanup | useEffect without cleanup |
| Concurrent updates | Overlapping async operations |
| Event handler races | Click handlers with async |
| Debounce/throttle | Missing rate limiting |

## Output Schema

```json
{
  "artifact_type": "race_condition_review",
  "status": "pass|warn|fail",
  "data": {
    "target": "PR #123",
    "framework": "React 18",
    "findings": [
      {
        "id": "RACE-001",
        "severity": "high",
        "type": "stale_closure",
        "title": "Stale Closure in useEffect",
        "file": "src/components/Search.tsx",
        "line": 23,
        "description": "Async callback may use outdated query value",
        "pattern": "fetch inside useEffect without abort",
        "fix": "Add AbortController with cleanup"
      },
      {
        "id": "RACE-002",
        "severity": "medium",
        "type": "unmount_update",
        "title": "Possible State Update After Unmount",
        "file": "src/hooks/useData.ts",
        "line": 15,
        "description": "Promise resolves after component unmounts",
        "fix": "Add mounted flag or use React Query"
      }
    ],
    "recommendations": [
      "Consider using React Query or SWR for data fetching",
      "Add ESLint plugin for exhaustive deps",
      "Use AbortController for cancellable requests"
    ]
  }
}
```

## Common Race Patterns

### 1. Search/Autocomplete
Fast typing causes out-of-order responses.
**Fix**: Debounce + AbortController

### 2. Optimistic Updates
Server rejection after UI update.
**Fix**: Rollback mechanism

### 3. Form Submission
Double-click causes duplicate submissions.
**Fix**: Disable button + request deduplication

### 4. Pagination
Page change before previous loads.
**Fix**: Cancel previous request

### 5. WebSocket + REST
Conflicting data sources.
**Fix**: Single source of truth, reconciliation
