# Real-Time Systems

Skills for building real-time features including WebSocket servers, event streaming, resilient connections, and live React UIs. Covers the full stack from dual-stream event publishing through to client-side hooks.

## Skills

| Skill | Description |
|-------|-------------|
| [dual-stream-architecture](dual-stream-architecture/) | Dual-stream event publishing combining Kafka for durability with Redis Pub/Sub for real-time delivery |
| [realtime-react-hooks](realtime-react-hooks/) | React hooks for real-time data with SSE, WebSocket, and SWR integration |
| [resilient-connections](resilient-connections/) | Patterns for resilient API clients and connections with retry logic, circuit breakers, and graceful degradation |
| [websocket-hub-patterns](websocket-hub-patterns/) | Horizontally-scalable WebSocket hub pattern with lazy Redis subscriptions and connection registry |

## Installation

```bash
# Add individual skills
npx add https://github.com/wpank/ai/tree/main/skills/realtime/dual-stream-architecture
npx add https://github.com/wpank/ai/tree/main/skills/realtime/realtime-react-hooks
npx add https://github.com/wpank/ai/tree/main/skills/realtime/resilient-connections
npx add https://github.com/wpank/ai/tree/main/skills/realtime/websocket-hub-patterns
```

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install dual-stream-architecture
npx clawhub@latest install realtime-react-hooks
npx clawhub@latest install resilient-connections
npx clawhub@latest install websocket-hub-patterns
```

## See Also

- [All Skills](../) — Complete skills catalog
- [Agents](../../agents/) — Workflow agents
