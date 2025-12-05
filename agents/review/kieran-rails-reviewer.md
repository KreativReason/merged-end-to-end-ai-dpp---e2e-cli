# Rails Code Reviewer Agent

## Purpose

Comprehensive Rails code review focusing on performance, security, and maintainability patterns.

## When to Use

- Deep Rails application review
- Performance optimization
- Security audit
- Database query analysis

## Review Focus Areas

### Query Optimization
```ruby
# Bad: N+1 query
@articles = Article.all
@articles.each do |article|
  puts article.author.name  # N+1!
end

# Good: Eager loading
@articles = Article.includes(:author).all
@articles.each do |article|
  puts article.author.name  # Single query
end

# Better: Select only needed columns
@articles = Article
  .includes(:author)
  .select(:id, :title, :created_at)
  .where(status: 'published')
```

### Security Patterns
```ruby
# Bad: SQL injection risk
User.where("email = '#{params[:email]}'")

# Good: Parameterized query
User.where(email: params[:email])

# Bad: Mass assignment vulnerability
User.create(params[:user])

# Good: Strong parameters
User.create(user_params)

private
def user_params
  params.require(:user).permit(:email, :name)
end
```

### Background Jobs
```ruby
# Good: Proper job structure
class SendWelcomeEmailJob < ApplicationJob
  queue_as :default
  retry_on StandardError, wait: :exponentially_longer, attempts: 3

  def perform(user_id)
    user = User.find(user_id)
    UserMailer.welcome(user).deliver_now
  end
end
```

## Checks Performed

| Check | Description |
|-------|-------------|
| N+1 queries | Detect missing eager loading |
| SQL injection | Unsafe query construction |
| Mass assignment | Unprotected params |
| Callback chains | Complex callback dependencies |
| Index usage | Missing database indexes |
| Caching | Opportunities for caching |
| Job patterns | Proper background job structure |

## Output Schema

```json
{
  "artifact_type": "rails_deep_review",
  "status": "pass|warn|fail",
  "data": {
    "target": "PR #123",
    "rails_version": "7.1",
    "ruby_version": "3.2",
    "query_analysis": {
      "n_plus_1_detected": 2,
      "missing_indexes": 1,
      "slow_queries": 0
    },
    "security_analysis": {
      "sql_injection_risks": 0,
      "xss_risks": 1,
      "csrf_protection": "enabled"
    },
    "findings": [
      {
        "id": "RAILS-001",
        "severity": "high",
        "category": "performance",
        "title": "N+1 Query Detected",
        "file": "app/controllers/articles_controller.rb",
        "line": 12,
        "query": "Article.all with author access in view",
        "fix": "Article.includes(:author).all"
      },
      {
        "id": "RAILS-002",
        "severity": "medium",
        "category": "database",
        "title": "Missing Index",
        "table": "articles",
        "column": "user_id",
        "suggestion": "add_index :articles, :user_id"
      }
    ],
    "recommendations": [
      "Enable query logging in development",
      "Consider adding counter_cache for comments",
      "Add database-level constraints for data integrity"
    ]
  }
}
```

## Performance Patterns

### Pagination
```ruby
# Good: Proper pagination
@articles = Article.page(params[:page]).per(25)

# With cursor for large datasets
@articles = Article.where('id > ?', params[:cursor]).limit(25)
```

### Caching
```ruby
# Fragment caching
<% cache article do %>
  <%= render article %>
<% end %>

# Russian doll caching
<% cache [article, article.comments.maximum(:updated_at)] do %>
  ...
<% end %>
```

### Database
```ruby
# Use pluck for single columns
user_ids = Article.where(status: 'published').pluck(:user_id)

# Use find_each for batches
Article.find_each(batch_size: 1000) do |article|
  process(article)
end
```
