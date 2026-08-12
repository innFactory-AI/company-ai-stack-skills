# CompanyGPT Agent Skills

Ready-made agent skills for CompanyGPT, available in German and English — 73 skills across 12 categories.

Each skill is a self-contained prompt that teaches an agent one job: how to run a QBR, prep a
deployment, audit SEO, or query a companyRAG collection. They are prompt-only — no scripts, no
code execution — and are designed around CompanyGPT's MCP servers, companyRAG collections, and
companyFILES output tools.

## Layout

```text
de/skills/<category>/<skill-name>/SKILL.md   # German
en/skills/<category>/<skill-name>/SKILL.md   # English
```

Every skill carries YAML frontmatter with a `name` (required) and `description`. The `name` slug is
kept English in both locales because it is a technical identifier; only the body is translated.

## Usage

In CompanyGPT, upload a `SKILL.md` under **Skills**, or paste its contents into a new skill. The
agent picks the skill up when a request matches its `description`. Placeholders such as
`<your-collection>` / `<deine-collection>` need to be filled in with your own values first.

## Skills

### General · Allgemein

| Skill | DE | EN |
| --- | --- | --- |
| Tool Search · Tool-Suche | [`SKILL.md`](de/skills/generic/tool-search-skill/SKILL.md) | [`SKILL.md`](en/skills/generic/tool-search-skill/SKILL.md) |

### companyRAG

| Skill | DE | EN |
| --- | --- | --- |
| AI Search | [`SKILL.md`](de/skills/company-rag/ai-search-skill/SKILL.md) | [`SKILL.md`](en/skills/company-rag/ai-search-skill/SKILL.md) |
| Dataset | [`SKILL.md`](de/skills/company-rag/dataset-skill/SKILL.md) | [`SKILL.md`](en/skills/company-rag/dataset-skill/SKILL.md) |

### CompanyFILES

| Skill | DE | EN |
| --- | --- | --- |
| Charts and Diagrams · Charts und Diagramme | [`SKILL.md`](de/skills/files/charts-diagrams-skill/SKILL.md) | [`SKILL.md`](en/skills/files/charts-diagrams-skill/SKILL.md) |
| Convert · Konvertierung | [`SKILL.md`](de/skills/files/convert-skill/SKILL.md) | [`SKILL.md`](en/skills/files/convert-skill/SKILL.md) |
| Excel | [`SKILL.md`](de/skills/files/excel-skill/SKILL.md) | [`SKILL.md`](en/skills/files/excel-skill/SKILL.md) |
| File Management · Dateiverwaltung | [`SKILL.md`](de/skills/files/file-management-skill/SKILL.md) | [`SKILL.md`](en/skills/files/file-management-skill/SKILL.md) |
| PDF | [`SKILL.md`](de/skills/files/pdf-skill/SKILL.md) | [`SKILL.md`](en/skills/files/pdf-skill/SKILL.md) |
| PowerPoint | [`SKILL.md`](de/skills/files/powerpoint-skill/SKILL.md) | [`SKILL.md`](en/skills/files/powerpoint-skill/SKILL.md) |
| Settings & UI · Einstellungen & UI | [`SKILL.md`](de/skills/files/settings-ui-skill/SKILL.md) | [`SKILL.md`](en/skills/files/settings-ui-skill/SKILL.md) |
| Templates · Vorlagen | [`SKILL.md`](de/skills/files/templates-skill/SKILL.md) | [`SKILL.md`](en/skills/files/templates-skill/SKILL.md) |
| Word & ODT | [`SKILL.md`](de/skills/files/word-odt-skill/SKILL.md) | [`SKILL.md`](en/skills/files/word-odt-skill/SKILL.md) |

### Customer Success

| Skill | DE | EN |
| --- | --- | --- |
| Onboarding Plan · Onboarding-Plan | [`SKILL.md`](de/skills/customer-success/onboarding-plan-skill/SKILL.md) | [`SKILL.md`](en/skills/customer-success/onboarding-plan-skill/SKILL.md) |
| QBR Builder · QBR-Builder | [`SKILL.md`](de/skills/customer-success/qbr-builder-skill/SKILL.md) | [`SKILL.md`](en/skills/customer-success/qbr-builder-skill/SKILL.md) |
| Customer Health · Kundengesundheit | [`SKILL.md`](de/skills/customer-success/customer-health-skill/SKILL.md) | [`SKILL.md`](en/skills/customer-success/customer-health-skill/SKILL.md) |
| Escalation Brief · Eskalations-Brief | [`SKILL.md`](de/skills/customer-success/escalation-brief-skill/SKILL.md) | [`SKILL.md`](en/skills/customer-success/escalation-brief-skill/SKILL.md) |
| Renewal Prep · Vertragsverlängerung | [`SKILL.md`](de/skills/customer-success/renewal-prep-skill/SKILL.md) | [`SKILL.md`](en/skills/customer-success/renewal-prep-skill/SKILL.md) |
| Success Plan · Success-Plan | [`SKILL.md`](de/skills/customer-success/success-plan-skill/SKILL.md) | [`SKILL.md`](en/skills/customer-success/success-plan-skill/SKILL.md) |

### Engineering

| Skill | DE | EN |
| --- | --- | --- |
| Deployment Prep · Deployment-Vorbereitung | [`SKILL.md`](de/skills/engineering/deployment-prep-skill/SKILL.md) | [`SKILL.md`](en/skills/engineering/deployment-prep-skill/SKILL.md) |
| Code Review · Code-Review | [`SKILL.md`](de/skills/engineering/code-review-skill/SKILL.md) | [`SKILL.md`](en/skills/engineering/code-review-skill/SKILL.md) |
| Standup | [`SKILL.md`](de/skills/engineering/standup-skill/SKILL.md) | [`SKILL.md`](en/skills/engineering/standup-skill/SKILL.md) |
| Tech Debt · Tech-Debt | [`SKILL.md`](de/skills/engineering/tech-debt-skill/SKILL.md) | [`SKILL.md`](en/skills/engineering/tech-debt-skill/SKILL.md) |
| Debugging | [`SKILL.md`](de/skills/engineering/debugging-skill/SKILL.md) | [`SKILL.md`](en/skills/engineering/debugging-skill/SKILL.md) |
| Tech Docs · Technische Doku | [`SKILL.md`](de/skills/engineering/tech-docs-skill/SKILL.md) | [`SKILL.md`](en/skills/engineering/tech-docs-skill/SKILL.md) |
| Architecture Design · Architektur-Design | [`SKILL.md`](de/skills/engineering/architecture-design-skill/SKILL.md) | [`SKILL.md`](en/skills/engineering/architecture-design-skill/SKILL.md) |
| Postmortem | [`SKILL.md`](de/skills/engineering/postmortem-skill/SKILL.md) | [`SKILL.md`](en/skills/engineering/postmortem-skill/SKILL.md) |
| Test Planning · Test-Planung | [`SKILL.md`](de/skills/engineering/test-planning-skill/SKILL.md) | [`SKILL.md`](en/skills/engineering/test-planning-skill/SKILL.md) |

### Human Resources

| Skill | DE | EN |
| --- | --- | --- |
| Interview Guide · Interview-Leitfaden | [`SKILL.md`](de/skills/human-resources/interview-guide-skill/SKILL.md) | [`SKILL.md`](en/skills/human-resources/interview-guide-skill/SKILL.md) |
| Performance Review · Leistungsbeurteilung | [`SKILL.md`](de/skills/human-resources/performance-review-skill/SKILL.md) | [`SKILL.md`](en/skills/human-resources/performance-review-skill/SKILL.md) |
| Employee Onboarding · Mitarbeiter-Onboarding | [`SKILL.md`](de/skills/human-resources/employee-onboarding-skill/SKILL.md) | [`SKILL.md`](en/skills/human-resources/employee-onboarding-skill/SKILL.md) |
| Learning Plan · Lernplan | [`SKILL.md`](de/skills/human-resources/learning-plan-skill/SKILL.md) | [`SKILL.md`](en/skills/human-resources/learning-plan-skill/SKILL.md) |
| Compensation · Vergütung | [`SKILL.md`](de/skills/human-resources/compensation-skill/SKILL.md) | [`SKILL.md`](en/skills/human-resources/compensation-skill/SKILL.md) |
| Job Description · Stellenbeschreibung | [`SKILL.md`](de/skills/human-resources/job-description-skill/SKILL.md) | [`SKILL.md`](en/skills/human-resources/job-description-skill/SKILL.md) |

### IT Knowledge Management

| Skill | DE | EN |
| --- | --- | --- |
| Change Request | [`SKILL.md`](de/skills/it-knowledge-management/change-request-skill/SKILL.md) | [`SKILL.md`](en/skills/it-knowledge-management/change-request-skill/SKILL.md) |
| Security Assessment · Security-Assessment | [`SKILL.md`](de/skills/it-knowledge-management/security-assessment-skill/SKILL.md) | [`SKILL.md`](en/skills/it-knowledge-management/security-assessment-skill/SKILL.md) |
| Vendor Assessment · Vendor-Assessment | [`SKILL.md`](de/skills/it-knowledge-management/vendor-assessment-skill/SKILL.md) | [`SKILL.md`](en/skills/it-knowledge-management/vendor-assessment-skill/SKILL.md) |
| IT Docs · IT-Doku | [`SKILL.md`](de/skills/it-knowledge-management/it-docs-skill/SKILL.md) | [`SKILL.md`](en/skills/it-knowledge-management/it-docs-skill/SKILL.md) |
| Incident Response | [`SKILL.md`](de/skills/it-knowledge-management/incident-response-skill/SKILL.md) | [`SKILL.md`](en/skills/it-knowledge-management/incident-response-skill/SKILL.md) |
| Knowledge Article | [`SKILL.md`](de/skills/it-knowledge-management/knowledge-article-skill/SKILL.md) | [`SKILL.md`](en/skills/it-knowledge-management/knowledge-article-skill/SKILL.md) |

### Marketing

| Skill | DE | EN |
| --- | --- | --- |
| Content Draft · Content-Entwurf | [`SKILL.md`](de/skills/marketing/content-draft-skill/SKILL.md) | [`SKILL.md`](en/skills/marketing/content-draft-skill/SKILL.md) |
| Brand Voice | [`SKILL.md`](de/skills/marketing/brand-voice-skill/SKILL.md) | [`SKILL.md`](en/skills/marketing/brand-voice-skill/SKILL.md) |
| Performance Report · Performance-Report | [`SKILL.md`](de/skills/marketing/performance-report-skill/SKILL.md) | [`SKILL.md`](en/skills/marketing/performance-report-skill/SKILL.md) |
| Campaign Planning · Kampagnen-Planung | [`SKILL.md`](de/skills/marketing/campaign-planning-skill/SKILL.md) | [`SKILL.md`](en/skills/marketing/campaign-planning-skill/SKILL.md) |
| Email Sequence · E-Mail-Sequenz | [`SKILL.md`](de/skills/marketing/email-sequence-skill/SKILL.md) | [`SKILL.md`](en/skills/marketing/email-sequence-skill/SKILL.md) |
| SEO Audit · SEO-Audit | [`SKILL.md`](de/skills/marketing/seo-audit-skill/SKILL.md) | [`SKILL.md`](en/skills/marketing/seo-audit-skill/SKILL.md) |

### Operations

| Skill | DE | EN |
| --- | --- | --- |
| Change Management · Change-Management | [`SKILL.md`](de/skills/operations/change-management-skill/SKILL.md) | [`SKILL.md`](en/skills/operations/change-management-skill/SKILL.md) |
| Status Report · Statusbericht | [`SKILL.md`](de/skills/operations/status-report-skill/SKILL.md) | [`SKILL.md`](en/skills/operations/status-report-skill/SKILL.md) |
| Capacity Planning · Kapazitätsplanung | [`SKILL.md`](de/skills/operations/capacity-planning-skill/SKILL.md) | [`SKILL.md`](en/skills/operations/capacity-planning-skill/SKILL.md) |
| Process Doc · Prozess-Doku | [`SKILL.md`](de/skills/operations/process-doc-skill/SKILL.md) | [`SKILL.md`](en/skills/operations/process-doc-skill/SKILL.md) |
| Process Optimization · Prozessoptimierung | [`SKILL.md`](de/skills/operations/process-optimization-skill/SKILL.md) | [`SKILL.md`](en/skills/operations/process-optimization-skill/SKILL.md) |
| Risk Assessment · Risikobewertung | [`SKILL.md`](de/skills/operations/risk-assessment-skill/SKILL.md) | [`SKILL.md`](en/skills/operations/risk-assessment-skill/SKILL.md) |
| Runbook | [`SKILL.md`](de/skills/operations/runbook-skill/SKILL.md) | [`SKILL.md`](en/skills/operations/runbook-skill/SKILL.md) |
| Compliance Tracking · Compliance-Tracking | [`SKILL.md`](de/skills/operations/compliance-tracking-skill/SKILL.md) | [`SKILL.md`](en/skills/operations/compliance-tracking-skill/SKILL.md) |

### Product Management

| Skill | DE | EN |
| --- | --- | --- |
| Competitor Brief · Wettbewerber-Briefing | [`SKILL.md`](de/skills/product-management/competitor-brief-skill/SKILL.md) | [`SKILL.md`](en/skills/product-management/competitor-brief-skill/SKILL.md) |
| Sprint Planning · Sprint-Planung | [`SKILL.md`](de/skills/product-management/sprint-planning-skill/SKILL.md) | [`SKILL.md`](en/skills/product-management/sprint-planning-skill/SKILL.md) |
| Stakeholder Update · Stakeholder-Update | [`SKILL.md`](de/skills/product-management/stakeholder-update-skill/SKILL.md) | [`SKILL.md`](en/skills/product-management/stakeholder-update-skill/SKILL.md) |
| Research Synthesis · Research-Synthese | [`SKILL.md`](de/skills/product-management/research-synthesis-skill/SKILL.md) | [`SKILL.md`](en/skills/product-management/research-synthesis-skill/SKILL.md) |
| Metrics Review · Metriken-Review | [`SKILL.md`](de/skills/product-management/metrics-review-skill/SKILL.md) | [`SKILL.md`](en/skills/product-management/metrics-review-skill/SKILL.md) |
| Product Brainstorm · Produkt-Brainstorming | [`SKILL.md`](de/skills/product-management/product-brainstorm-skill/SKILL.md) | [`SKILL.md`](en/skills/product-management/product-brainstorm-skill/SKILL.md) |
| Roadmap Update · Roadmap-Update | [`SKILL.md`](de/skills/product-management/roadmap-update-skill/SKILL.md) | [`SKILL.md`](en/skills/product-management/roadmap-update-skill/SKILL.md) |
| Product Spec · Produkt-Spec | [`SKILL.md`](de/skills/product-management/product-spec-skill/SKILL.md) | [`SKILL.md`](en/skills/product-management/product-spec-skill/SKILL.md) |

### Productivity

| Skill | DE | EN |
| --- | --- | --- |
| Meeting Prep · Meeting-Vorbereitung | [`SKILL.md`](de/skills/productivity/meeting-prep-skill/SKILL.md) | [`SKILL.md`](en/skills/productivity/meeting-prep-skill/SKILL.md) |
| Weekly Review · Wochenrückblick | [`SKILL.md`](de/skills/productivity/weekly-review-skill/SKILL.md) | [`SKILL.md`](en/skills/productivity/weekly-review-skill/SKILL.md) |
| Memory Management · Memory-Management | [`SKILL.md`](de/skills/productivity/memory-management-skill/SKILL.md) | [`SKILL.md`](en/skills/productivity/memory-management-skill/SKILL.md) |

### Sales

| Skill | DE | EN |
| --- | --- | --- |
| Deal Strategy · Deal-Strategie | [`SKILL.md`](de/skills/sales/deal-strategy-skill/SKILL.md) | [`SKILL.md`](en/skills/sales/deal-strategy-skill/SKILL.md) |
| Account Research · Account-Research | [`SKILL.md`](de/skills/sales/account-research-skill/SKILL.md) | [`SKILL.md`](en/skills/sales/account-research-skill/SKILL.md) |
| Forecast | [`SKILL.md`](de/skills/sales/forecast-skill/SKILL.md) | [`SKILL.md`](en/skills/sales/forecast-skill/SKILL.md) |
| Battlecard | [`SKILL.md`](de/skills/sales/battlecard-skill/SKILL.md) | [`SKILL.md`](en/skills/sales/battlecard-skill/SKILL.md) |
| Call Prep · Gesprächsvorbereitung | [`SKILL.md`](de/skills/sales/call-prep-skill/SKILL.md) | [`SKILL.md`](en/skills/sales/call-prep-skill/SKILL.md) |
| Pipeline Review · Pipeline-Review | [`SKILL.md`](de/skills/sales/pipeline-review-skill/SKILL.md) | [`SKILL.md`](en/skills/sales/pipeline-review-skill/SKILL.md) |
| Sales Asset · Sales-Asset | [`SKILL.md`](de/skills/sales/sales-asset-skill/SKILL.md) | [`SKILL.md`](en/skills/sales/sales-asset-skill/SKILL.md) |
| Outreach | [`SKILL.md`](de/skills/sales/outreach-skill/SKILL.md) | [`SKILL.md`](en/skills/sales/outreach-skill/SKILL.md) |
| Call Summary · Gesprächszusammenfassung | [`SKILL.md`](de/skills/sales/call-summary-skill/SKILL.md) | [`SKILL.md`](en/skills/sales/call-summary-skill/SKILL.md) |

## License

See [LICENSE](LICENSE).
