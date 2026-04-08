---
apiVersion: processkit.projectious.work/v1
kind: Skill
metadata:
  id: SKILL-threat-modeling
  name: threat-modeling
  version: "1.1.0"
  created: 2026-04-06T00:00:00Z
spec:
  description: "Threat modeling with STRIDE — data flow diagrams, trust boundaries, risk."
  category: security
  layer: null
  when_to_use: "Use when designing a new system, reviewing architecture for security, conducting a security review, or prioritizing security work by risk."
---

# Threat Modeling

## Level 1 — Intro

A threat model is a structured analysis of how a system could be
attacked. STRIDE walks each component and data flow through six
threat categories, producing a prioritized list of risks and
mitigations.

## Level 2 — Overview

### STRIDE categories

| Category                   | Threat                        | Property violated |
|----------------------------|-------------------------------|-------------------|
| **S**poofing               | Pretending to be someone else | Authentication    |
| **T**ampering              | Modifying data or code        | Integrity         |
| **R**epudiation            | Denying an action occurred    | Non-repudiation   |
| **I**nformation Disclosure | Exposing data                 | Confidentiality   |
| **D**enial of Service      | Making the system unavailable | Availability      |
| **E**levation of Privilege | Gaining unauthorized access   | Authorization     |

### Step 1 — Draw a data flow diagram

Map processes, data stores, data flows, and external entities. Mark
trust boundaries where data crosses between trust levels.

```
                    Trust Boundary
                    +---------------------------------+
  [User Browser] ---|---> [Web Server] ---> [App Server] ---> [Database]
                    |         |                  |
                    |         v                  v
                    |    [Static Files]    [Cache (Redis)]
                    +---------------------------------+
                           |
                           v
                    [External Auth Provider]
```

- **Processes** — web server, app server, background workers.
- **Data stores** — database, cache, file system, message queue.
- **Data flows** — HTTP requests, database queries, API calls.
- **External entities** — users, third-party services, admins.
- **Trust boundaries** — network segments, process boundaries,
  privilege levels.

### Step 2 — Identify trust boundaries

Each crossing is a potential attack point:

- Internet to DMZ.
- DMZ to internal network.
- Application to database.
- Service to service in a microservice mesh.
- Regular user vs admin privilege levels.

### Step 3 — Apply STRIDE to each element

For every process, data store, and data flow, ask:

- **Spoofing** — can an attacker impersonate a legitimate entity?
- **Tampering** — can data be modified in transit or at rest?
- **Repudiation** — can a user deny performing an action?
- **Information disclosure** — can sensitive data leak?
- **Denial of service** — can this component be overwhelmed?
- **Elevation of privilege** — can a user gain higher privileges?

### Step 4 — Risk assessment

Rate each threat by likelihood and impact:

| Rating | Likelihood                      | Impact                           |
|--------|---------------------------------|----------------------------------|
| High   | Exploitable with public tools   | Data breach, full compromise     |
| Medium | Requires some skill or access   | Partial data exposure, downtime  |
| Low    | Requires insider access or luck | Minor data exposure, degradation |

**Risk = Likelihood × Impact**

| Likelihood \ Impact | High     | Medium | Low    |
|---------------------|----------|--------|--------|
| High                | Critical | High   | Medium |
| Medium              | High     | Medium | Low    |
| Low                 | Medium   | Low    | Low    |

### Step 5 — Mitigations

Map each STRIDE category to common mitigations:

| STRIDE category        | Common mitigations                                |
|------------------------|---------------------------------------------------|
| Spoofing               | MFA, certificate pinning, mutual TLS              |
| Tampering              | Digital signatures, checksums, immutable logs     |
| Repudiation            | Audit logging, tamper-evident logs, signatures    |
| Information Disclosure | Encryption (TLS, AES), access controls, masking   |
| Denial of Service      | Rate limiting, autoscaling, CDN, circuit breakers |
| Elevation of Privilege | Least privilege, input validation, sandboxing     |

## Level 3 — Full reference

### Attack surface mapping

Enumerate every entry point an attacker could use:

- **Network** — open ports, exposed services, public endpoints.
- **Application** — API endpoints, file upload, search, user input
  fields.
- **Authentication** — login, password reset, session management.
- **Data** — database access, file storage, backups, logs.
- **Infrastructure** — cloud console, CI/CD pipeline, container
  registry.
- **Human** — phishing targets, social engineering, insider threats.

### Output format

Structure the threat model as a single document:

```
## Threat Model: [System Name]

### System Description
Brief description of the system and its purpose.

### Data Flow Diagram
ASCII diagram showing components and trust boundaries.

### Assets
List of valuable data and resources to protect.

### Threats
| ID | STRIDE | Component | Threat | Risk | Mitigation |
|----|--------|-----------|--------|------|------------|
| T1 | S      | Login API | Credential stuffing | High | Rate limiting, MFA |
| T2 | I      | Database  | SQL injection leaks PII | Critical | Parameterized queries |

### Recommendations
Prioritized list of security improvements.
```

### When to threat model

- During initial design of any system handling sensitive data.
- Before adding a new external integration or trust boundary.
- After an incident, to find adjacent risks.
- On a periodic schedule for high-value systems (annually or per
  major release).

### Anti-patterns

- Threat modeling once at design time and never revisiting.
- Skipping the data flow diagram and going straight to a threat list.
- Treating "low likelihood" as "ignore forever".
- Producing a document nobody reads. The output should drive a
  prioritized punch list of work, not sit in a wiki.
- Modeling abstract systems instead of the actual architecture in
  production.

### Tips for sharper models

- Walk the diagram with someone who didn't build the system; gaps
  surface fast.
- Track every mitigation back to a ticket or commit. A mitigation
  with no owner is a mitigation that won't happen.
- Re-rate risks after mitigations land — residual risk is what
  matters for prioritization.
