# USER.md - User Model

Store stable user preferences and profile facts as directives that can guide future sessions.

Use one directive per entry:

```md
<!-- observed: YYYY-MM-DD | status: active -->

- Prefer concise progress updates during implementation work.
```

- Begin each directive with an imperative such as `Always`, `Never`, or `Prefer`.
- Record the observation date and either `active` or `superseded` on the metadata line.
- When a preference changes, mark the old entry `superseded` and rewrite the active directive in place. Never append a contradictory active directive.
- Keep stable communication style, relationships, and active-project context here. Put durable non-profile facts and decisions in `MEMORY.md`.
- Save this file at the workspace root as `USER.md`. It loads every session with a separate 4,000-character budget.

## Directives

Replace the example below with a real directive and a real observation date before you save this file. Never leave a placeholder directive `active`.

<!-- observed: 2026-11-02 | status: active -->
- User name: Acib Abbade de Castro
- Professional background: Pesquisador em tecnologia, formado em Análise e Desenvolvimento de Sistemas
- Expertise: Hardware desde 1997, redes, Linux (Debian 4+, 2004), Python, Kubernetes, Docker, Proxmox, Ubuntu Server
- Current project: Montar uma SaaS para pequenos negócios com empresa de suporte técnico
- Communication style: Casual and direct - no formal titles like "Senhor" or "Vossa Excelência"
<!-- /openclaw:attempt:DYNAMIC -->