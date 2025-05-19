---
marp: true
theme: default
paginate: true
---

# Cloudflare Workers Configuration
## wrangler.toml Example

---

# Basic Configuration

```toml
# Project name (will be used as subdomain)
name = "mcp-server-authless"

# Main entry point
main = "src/index.ts"

# Cloudflare Workers compatibility date
compatibility_date = "2024-01-01"

# Build configuration
[build]
command = "npm run build"
```

---

# What Each Section Does

- `name`: Your project's name and subdomain
- `main`: Entry point for your Worker
- `compatibility_date`: Ensures consistent behavior
- `[build]`: Build configuration for deployment

---

# Additional Common Options

```toml
# Environment variables
[vars]
API_KEY = "your-api-key"

# Custom domains
routes = [
  { pattern = "example.com/*", zone_name = "example.com" }
]

# KV Namespaces
[[kv_namespaces]]
binding = "MY_KV"
id = "xxx"
```

---

# Development Settings

```toml
# Local development
[dev]
port = 8787
local_protocol = "http"

# Environment-specific settings
[env.production]
name = "prod-worker"
```

---

# Questions?

- Visit [Cloudflare Workers Documentation](https://developers.cloudflare.com/workers/)
- Check [Wrangler CLI Reference](https://developers.cloudflare.com/workers/wrangler/commands/) 