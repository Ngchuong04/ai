# Solidity Security

Smart contract security patterns, vulnerability prevention, gas optimization, and audit preparation for Solidity development. Covers the critical vulnerabilities that have caused hundreds of millions in losses.

## What's Inside

- Critical vulnerabilities (reentrancy, integer overflow, access control, front-running, oracle manipulation, signature replay)
- Security patterns (Checks-Effects-Interactions, Pull over Push, Emergency Stop)
- Gas optimization techniques (storage packing, calldata, events)
- Proxy and upgrade safety (EIP-1967, storage gaps, initializer protection)
- Audit preparation checklist by category
- Security analysis tools (Slither, Mythril, Echidna, Foundry)
- Reference files for vulnerability patterns, audit checklists, and real-world exploit breakdowns

## When to Use

- Writing or reviewing smart contracts
- Auditing contracts for vulnerabilities
- Implementing DeFi protocols
- Preventing reentrancy, overflow, and access control issues
- Optimizing gas while maintaining security
- Preparing contracts for professional audits

## Installation

```bash
npx skills add solidity-security
```

### Manual Installation

#### Cursor (per-project)

From your project root:

```bash
mkdir -p .cursor/skills
cp -r ~/.ai-skills/skills/devops/solidity-security .cursor/skills/solidity-security
```

#### Cursor (global)

```bash
mkdir -p ~/.cursor/skills
cp -r ~/.ai-skills/skills/devops/solidity-security ~/.cursor/skills/solidity-security
```

#### Claude Code (per-project)

From your project root:

```bash
mkdir -p .claude/skills
cp -r ~/.ai-skills/skills/devops/solidity-security .claude/skills/solidity-security
```

#### Claude Code (global)

```bash
mkdir -p ~/.claude/skills
cp -r ~/.ai-skills/skills/devops/solidity-security ~/.claude/skills/solidity-security
```

---

Part of the [DevOps](..) skill category.
