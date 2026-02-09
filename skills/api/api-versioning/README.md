# API Versioning Patterns

API versioning strategies — URL path, header, query param, content negotiation — with breaking change classification, deprecation timelines, migration patterns, and multi-version support. Use when evolving APIs, planning breaking changes, or managing version lifecycles.

## What's Inside

- Versioning Strategies — URL path, query param, header, content negotiation comparison
- URL Path Versioning and Header Versioning implementation examples
- Semantic Versioning for APIs (MAJOR, MINOR, PATCH)
- Breaking vs Non-Breaking Changes classification
- Deprecation Strategy — announce, sunset period, removal timeline
- Sunset HTTP Header (RFC 8594) usage
- Migration Patterns — adapter, facade, versioned controllers, API gateway routing
- Multi-Version Support architecture and principles
- Client Communication — changelogs, migration guides, SDK versioning
- Anti-Patterns and common mistakes

## When to Use

- Evolving APIs with breaking changes
- Planning API deprecation and sunset timelines
- Implementing multi-version API support
- Writing migration guides for API consumers
- Choosing a versioning strategy for a new API

## Installation

```bash
skills add api-versioning
```

### Manual Installation

Copy this directory to your project:

```bash
# Cursor
cp -r ~/.skills/ai/skills/api/api-versioning .cursor/rules/api-versioning

# Claude Code  
cp -r ~/.skills/ai/skills/api/api-versioning .agents/skills/api-versioning
```

## Related Skills

- `api-design` — Resource modeling, HTTP semantics, pagination, error formats
- `api-development` — Full API development lifecycle orchestration

---

Part of the [API](..) skill category.
