"""Standalone interactive HTML5 report exporter with embedded CSS and Mermaid.js support."""

from __future__ import annotations

import html
from pathlib import Path

from forge.schemas.report import EngineeringReport


class HTMLExporter:
    """Exports EngineeringReport instances into a modern, self-contained interactive HTML document."""

    @classmethod
    def generate_html(cls, report: EngineeringReport) -> str:
        """Render complete HTML5 document from an EngineeringReport."""
        status_color = "#10B981" if report.final_status.value == "APPROVED" else "#F59E0B"
        if report.final_status.value == "FAILED":
            status_color = "#EF4444"

        # Generate Mermaid diagram for components and data flows
        mermaid_lines = ["graph LR"]
        for comp in report.architecture.components:
            cid = comp.component_id.replace("-", "_")
            mermaid_lines.append(f'    {cid}["{comp.name}<br/><i>{comp.technology}</i>"]')
        for df in report.architecture.data_flows:
            src = df.source_component_id.replace("-", "_")
            dst = df.target_component_id.replace("-", "_")
            proto = df.protocol or "calls"
            mermaid_lines.append(f'    {src} -->|"{proto}"| {dst}')

        mermaid_code = "\n".join(mermaid_lines)

        components_rows = "".join(
            f"<tr><td><code>{html.escape(c.component_id)}</code></td>"
            f"<td><b>{html.escape(c.name)}</b></td>"
            f"<td>{html.escape(c.technology)}</td>"
            f"<td>{html.escape(c.responsibility)}</td></tr>"
            for c in report.architecture.components
        )

        threats_rows = "".join(
            f"<tr><td><code>{html.escape(t.threat_id)}</code></td>"
            f"<td><span class='badge'>{html.escape(t.category.value if hasattr(t.category, 'value') else str(t.category))}</span></td>"
            f"<td><b>{html.escape(t.attack_scenario[:80] + '...' if len(t.attack_scenario) > 80 else t.attack_scenario)}</b></td>"
            f"<td><span class='severity-badge'>{html.escape(t.severity.value if hasattr(t.severity, 'value') else str(t.severity))}</span></td>"
            f"<td>{html.escape(t.mitigation.description if t.mitigation else 'None')}</td></tr>"
            for t in report.threat_model.threats
        )

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FORGE Blueprint: {html.escape(report.architecture.title)}</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <script>mermaid.initialize({{startOnLoad:true, theme: 'neutral'}});</script>
    <style>
        :root {{
            --primary: #2563EB;
            --bg: #F8FAFC;
            --card-bg: #FFFFFF;
            --text: #0F172A;
            --text-muted: #64748B;
            --border: #E2E8F0;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg);
            color: var(--text);
            line-height: 1.6;
            margin: 0;
            padding: 40px 20px;
        }}
        .container {{
            max-width: 1100px;
            margin: 0 auto;
        }}
        .header {{
            background: var(--card-bg);
            padding: 32px;
            border-radius: 12px;
            border: 1px solid var(--border);
            margin-bottom: 24px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }}
        .badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 9999px;
            font-size: 13px;
            font-weight: 600;
            background: #E0E7FF;
            color: #3730A3;
        }}
        .status-badge {{
            background: {status_color};
            color: white;
            padding: 6px 16px;
            border-radius: 9999px;
            font-weight: 700;
            font-size: 14px;
            float: right;
        }}
        .severity-badge {{
            font-weight: 600;
            color: #DC2626;
        }}
        .section {{
            background: var(--card-bg);
            padding: 28px;
            border-radius: 12px;
            border: 1px solid var(--border);
            margin-bottom: 24px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }}
        h1, h2, h3 {{ color: var(--text); margin-top: 0; }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 16px;
        }}
        th, td {{
            padding: 12px 16px;
            text-align: left;
            border-bottom: 1px solid var(--border);
        }}
        th {{
            background: #F1F5F9;
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-muted);
        }}
        code {{
            background: #F1F5F9;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 13px;
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
        }}
        .mermaid {{
            background: #FFFFFF;
            padding: 20px;
            border-radius: 8px;
            border: 1px solid var(--border);
            margin-top: 16px;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <span class="status-badge">{html.escape(report.final_status.value)}</span>
            <h1>{html.escape(report.architecture.title)}</h1>
            <p style="color: var(--text-muted); margin-bottom: 0;">
                Report ID: <code>{html.escape(report.report_id)}</code> &bull;
                Project ID: <code>{html.escape(report.project_id)}</code> &bull;
                Generated: {report.generated_at.strftime('%Y-%m-%d %H:%M:%S UTC')}
            </p>
        </div>

        <div class="section">
            <h2>1. Executive Summary</h2>
            <p>{html.escape(report.executive_summary.overview)}</p>
            <p><strong>Readiness Score:</strong> {report.executive_summary.readiness_score} / 100.0</p>
            <blockquote><em>{html.escape(report.objective)}</em></blockquote>
        </div>

        <div class="section">
            <h2>2. Architectural Topology</h2>
            <div class="mermaid">
{mermaid_code}
            </div>
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Component</th>
                        <th>Technology</th>
                        <th>Responsibility</th>
                    </tr>
                </thead>
                <tbody>
{components_rows}
                </tbody>
            </table>
        </div>

        <div class="section">
            <h2>3. STRIDE Threat Analysis</h2>
            <table>
                <thead>
                    <tr>
                        <th>Threat ID</th>
                        <th>Category</th>
                        <th>Attack Scenario</th>
                        <th>Severity</th>
                        <th>Mitigation</th>
                    </tr>
                </thead>
                <tbody>
{threats_rows}
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>
"""
        return html_content

    @classmethod
    def export_html(cls, report: EngineeringReport, output_path: str | Path) -> None:
        """Write self-contained HTML report to filesystem."""
        target = Path(output_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        content = cls.generate_html(report)
        target.write_text(content, encoding="utf-8")
