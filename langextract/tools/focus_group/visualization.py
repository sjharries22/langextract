# Copyright 2025 Google LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Visualization utilities for focus group analysis."""

from __future__ import annotations

import collections
import html
import json
from typing import Any

from langextract.tools.focus_group.types import (
    AnalysisResult,
    ExtractionType,
    Sentiment,
    ThemeSummary,
)

# Color palette for extraction types
EXTRACTION_COLORS = {
    ExtractionType.SENTIMENT.value: "#4285F4",  # Blue
    ExtractionType.THEME.value: "#34A853",  # Green
    ExtractionType.PAIN_POINT.value: "#EA4335",  # Red
    ExtractionType.FEATURE_REQUEST.value: "#FBBC04",  # Yellow
    ExtractionType.QUOTE.value: "#9C27B0",  # Purple
    ExtractionType.INSIGHT.value: "#00BCD4",  # Cyan
    ExtractionType.QUESTION.value: "#FF9800",  # Orange
    ExtractionType.AGREEMENT.value: "#8BC34A",  # Light green
    ExtractionType.DISAGREEMENT.value: "#F44336",  # Light red
    ExtractionType.SUGGESTION.value: "#3F51B5",  # Indigo
    ExtractionType.EXPERIENCE.value: "#607D8B",  # Blue grey
    ExtractionType.EXPECTATION.value: "#795548",  # Brown
    ExtractionType.COMPARISON.value: "#009688",  # Teal
    ExtractionType.EMOTION.value: "#E91E63",  # Pink
}

# Sentiment colors
SENTIMENT_COLORS = {
    Sentiment.VERY_POSITIVE.value: "#1B5E20",  # Dark green
    Sentiment.POSITIVE.value: "#4CAF50",  # Green
    Sentiment.NEUTRAL.value: "#9E9E9E",  # Grey
    Sentiment.NEGATIVE.value: "#F44336",  # Red
    Sentiment.VERY_NEGATIVE.value: "#B71C1C",  # Dark red
    Sentiment.MIXED.value: "#FF9800",  # Orange
}

# HTML template for the dashboard
DASHBOARD_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Focus Group Analysis Dashboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto,
                         Oxygen, Ubuntu, sans-serif;
            background: #f5f5f5;
            color: #333;
            line-height: 1.6;
        }
        .dashboard {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 12px;
            margin-bottom: 20px;
        }
        .header h1 {
            font-size: 2rem;
            margin-bottom: 10px;
        }
        .header .stats {
            display: flex;
            gap: 30px;
            flex-wrap: wrap;
        }
        .header .stat {
            text-align: center;
        }
        .header .stat-value {
            font-size: 2rem;
            font-weight: bold;
        }
        .header .stat-label {
            font-size: 0.9rem;
            opacity: 0.9;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 20px;
        }
        .card {
            background: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .card h2 {
            font-size: 1.2rem;
            margin-bottom: 15px;
            color: #333;
            border-bottom: 2px solid #eee;
            padding-bottom: 10px;
        }
        .sentiment-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            color: white;
            font-weight: 500;
            font-size: 0.9rem;
        }
        .theme-list {
            list-style: none;
        }
        .theme-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 0;
            border-bottom: 1px solid #eee;
        }
        .theme-item:last-child {
            border-bottom: none;
        }
        .theme-name {
            font-weight: 500;
        }
        .theme-bar {
            height: 8px;
            background: #e0e0e0;
            border-radius: 4px;
            flex: 1;
            margin: 0 15px;
            overflow: hidden;
        }
        .theme-bar-fill {
            height: 100%;
            background: linear-gradient(90deg, #4285F4, #34A853);
            border-radius: 4px;
        }
        .theme-count {
            font-size: 0.9rem;
            color: #666;
            min-width: 40px;
            text-align: right;
        }
        .finding {
            padding: 12px;
            margin-bottom: 10px;
            background: #f8f9fa;
            border-left: 4px solid #4285F4;
            border-radius: 0 8px 8px 0;
        }
        .participant-card {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 10px;
        }
        .participant-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }
        .participant-id {
            font-weight: 600;
            color: #333;
        }
        .participant-count {
            font-size: 0.85rem;
            color: #666;
        }
        .extraction-type-legend {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-bottom: 15px;
        }
        .legend-item {
            display: flex;
            align-items: center;
            gap: 5px;
            font-size: 0.85rem;
        }
        .legend-color {
            width: 12px;
            height: 12px;
            border-radius: 3px;
        }
        .quote-card {
            background: #fff;
            border: 1px solid #e0e0e0;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 10px;
            position: relative;
        }
        .quote-card::before {
            content: '"';
            font-size: 3rem;
            color: #e0e0e0;
            position: absolute;
            top: -10px;
            left: 10px;
        }
        .quote-text {
            padding-left: 30px;
            font-style: italic;
            color: #555;
        }
        .quote-meta {
            padding-left: 30px;
            margin-top: 10px;
            font-size: 0.85rem;
            color: #888;
        }
        .chart-container {
            height: 200px;
            display: flex;
            align-items: flex-end;
            gap: 10px;
            padding: 20px 0;
        }
        .chart-bar-wrapper {
            flex: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .chart-bar {
            width: 100%;
            max-width: 60px;
            border-radius: 4px 4px 0 0;
            transition: height 0.3s ease;
        }
        .chart-label {
            margin-top: 8px;
            font-size: 0.75rem;
            text-align: center;
            color: #666;
        }
        .chart-value {
            font-size: 0.85rem;
            font-weight: 500;
            margin-bottom: 5px;
        }
        .pain-point {
            background: #ffebee;
            border-left: 4px solid #EA4335;
            padding: 12px;
            margin-bottom: 10px;
            border-radius: 0 8px 8px 0;
        }
        .pain-point-severity {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 500;
            margin-left: 10px;
        }
        .severity-critical { background: #B71C1C; color: white; }
        .severity-high { background: #F44336; color: white; }
        .severity-medium { background: #FF9800; color: white; }
        .severity-low { background: #FFC107; color: #333; }
        .feature-request {
            background: #FFF8E1;
            border-left: 4px solid #FBBC04;
            padding: 12px;
            margin-bottom: 10px;
            border-radius: 0 8px 8px 0;
        }
        .transcript-view {
            font-family: 'Courier New', monospace;
            font-size: 0.9rem;
            line-height: 1.8;
            white-space: pre-wrap;
            background: #fafafa;
            padding: 20px;
            border-radius: 8px;
            max-height: 500px;
            overflow-y: auto;
        }
        .highlight {
            padding: 2px 4px;
            border-radius: 3px;
            cursor: pointer;
        }
        .highlight:hover {
            opacity: 0.8;
        }
        .tooltip {
            position: absolute;
            background: #333;
            color: white;
            padding: 8px 12px;
            border-radius: 6px;
            font-size: 0.85rem;
            max-width: 300px;
            z-index: 1000;
            display: none;
        }
        .tabs {
            display: flex;
            gap: 5px;
            margin-bottom: 15px;
            border-bottom: 2px solid #eee;
        }
        .tab {
            padding: 10px 20px;
            cursor: pointer;
            border: none;
            background: none;
            font-size: 0.95rem;
            color: #666;
            border-bottom: 2px solid transparent;
            margin-bottom: -2px;
        }
        .tab:hover {
            color: #333;
        }
        .tab.active {
            color: #4285F4;
            border-bottom-color: #4285F4;
        }
        .tab-content {
            display: none;
        }
        .tab-content.active {
            display: block;
        }
        @media (max-width: 768px) {
            .grid {
                grid-template-columns: 1fr;
            }
            .header .stats {
                gap: 15px;
            }
        }
    </style>
</head>
<body>
    <div class="dashboard">
        {header}
        <div class="grid">
            {cards}
        </div>
    </div>
    <div class="tooltip" id="tooltip"></div>
    <script>
        // Tab functionality
        document.querySelectorAll('.tab').forEach(tab => {
            tab.addEventListener('click', () => {
                const tabGroup = tab.closest('.card');
                tabGroup.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
                tabGroup.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
                tab.classList.add('active');
                const contentId = tab.dataset.tab;
                document.getElementById(contentId).classList.add('active');
            });
        });

        // Tooltip functionality
        const tooltip = document.getElementById('tooltip');
        document.querySelectorAll('.highlight').forEach(el => {
            el.addEventListener('mouseenter', (e) => {
                const data = JSON.parse(el.dataset.info || '{}');
                let content = '<strong>' + (data.type || 'Extraction') + '</strong>';
                if (data.participant) content += '<br>Participant: ' + data.participant;
                if (data.sentiment) content += '<br>Sentiment: ' + data.sentiment;
                if (data.topic) content += '<br>Topic: ' + data.topic;
                tooltip.innerHTML = content;
                tooltip.style.display = 'block';
                tooltip.style.left = e.pageX + 10 + 'px';
                tooltip.style.top = e.pageY + 10 + 'px';
            });
            el.addEventListener('mouseleave', () => {
                tooltip.style.display = 'none';
            });
        });
    </script>
</body>
</html>"""


def _escape_html(text: str) -> str:
  """Escape HTML special characters."""
  return html.escape(text)


def _get_extraction_color(extraction_class: str) -> str:
  """Get color for an extraction type."""
  return EXTRACTION_COLORS.get(extraction_class, "#9E9E9E")


def _get_sentiment_color(sentiment: str | Sentiment) -> str:
  """Get color for a sentiment."""
  if isinstance(sentiment, Sentiment):
    sentiment = sentiment.value
  return SENTIMENT_COLORS.get(sentiment, "#9E9E9E")


def _render_header(result: AnalysisResult) -> str:
  """Render the dashboard header."""
  sentiment_color = _get_sentiment_color(result.overall_sentiment)

  stats_html = f"""
    <div class="stat">
        <div class="stat-value">{result.total_extractions}</div>
        <div class="stat-label">Total Insights</div>
    </div>
    <div class="stat">
        <div class="stat-value">{len(result.themes)}</div>
        <div class="stat-label">Themes</div>
    </div>
    <div class="stat">
        <div class="stat-value">{len(result.participant_summaries)}</div>
        <div class="stat-label">Participants</div>
    </div>
    <div class="stat">
        <span class="sentiment-badge" style="background: {sentiment_color}">
            {result.overall_sentiment.value.replace('_', ' ').title()}
        </span>
        <div class="stat-label">Overall Sentiment</div>
    </div>
  """

  return f"""
    <div class="header">
        <h1>Focus Group Analysis Dashboard</h1>
        <div class="stats">{stats_html}</div>
    </div>
  """


def _render_key_findings(result: AnalysisResult) -> str:
  """Render the key findings card."""
  if not result.key_findings:
    return ""

  findings_html = "\n".join(
      f'<div class="finding">{_escape_html(finding)}</div>'
      for finding in result.key_findings
  )

  return f"""
    <div class="card">
        <h2>Key Findings</h2>
        {findings_html}
    </div>
  """


def _render_themes_chart(themes: list[ThemeSummary]) -> str:
  """Render themes as a bar chart."""
  if not themes:
    return ""

  max_freq = max(t.frequency for t in themes) if themes else 1
  top_themes = themes[:10]

  theme_items = ""
  for theme in top_themes:
    width_pct = (theme.frequency / max_freq) * 100
    theme_items += f"""
      <div class="theme-item">
          <span class="theme-name">{_escape_html(theme.theme_name)}</span>
          <div class="theme-bar">
              <div class="theme-bar-fill" style="width: {width_pct}%"></div>
          </div>
          <span class="theme-count">{theme.frequency}</span>
      </div>
    """

  return f"""
    <div class="card">
        <h2>Top Themes</h2>
        <ul class="theme-list">{theme_items}</ul>
    </div>
  """


def _render_extraction_distribution(result: AnalysisResult) -> str:
  """Render extraction type distribution chart."""
  counts = result.extraction_type_counts
  if not counts:
    return ""

  max_count = max(counts.values()) if counts else 1

  bars_html = ""
  for ext_type, count in sorted(
      counts.items(), key=lambda x: x[1], reverse=True
  )[:8]:
    height_pct = (count / max_count) * 150
    color = _get_extraction_color(ext_type)
    label = ext_type.replace("_", " ").title()
    bars_html += f"""
      <div class="chart-bar-wrapper">
          <div class="chart-value">{count}</div>
          <div class="chart-bar" style="height: {height_pct}px; background: {color}"></div>
          <div class="chart-label">{label[:10]}</div>
      </div>
    """

  return f"""
    <div class="card">
        <h2>Insight Distribution</h2>
        <div class="chart-container">{bars_html}</div>
    </div>
  """


def _render_pain_points(result: AnalysisResult) -> str:
  """Render pain points card."""
  pain_points = result.get_extractions_by_type(ExtractionType.PAIN_POINT)
  if not pain_points:
    return ""

  items_html = ""
  for pp in pain_points[:10]:
    severity = "medium"
    if pp.attributes:
      severity = pp.attributes.get("severity", "medium")

    severity_class = f"severity-{severity}"
    items_html += f"""
      <div class="pain-point">
          {_escape_html(pp.extraction_text)}
          <span class="pain-point-severity {severity_class}">
              {severity.upper()}
          </span>
      </div>
    """

  return f"""
    <div class="card">
        <h2>Pain Points ({len(pain_points)})</h2>
        {items_html}
    </div>
  """


def _render_feature_requests(result: AnalysisResult) -> str:
  """Render feature requests card."""
  feature_requests = result.get_extractions_by_type(
      ExtractionType.FEATURE_REQUEST
  )
  if not feature_requests:
    return ""

  items_html = ""
  for fr in feature_requests[:10]:
    items_html += f"""
      <div class="feature-request">
          {_escape_html(fr.extraction_text)}
      </div>
    """

  return f"""
    <div class="card">
        <h2>Feature Requests ({len(feature_requests)})</h2>
        {items_html}
    </div>
  """


def _render_participant_summary(result: AnalysisResult) -> str:
  """Render participant summaries."""
  if not result.participant_summaries:
    return ""

  items_html = ""
  for ps in result.participant_summaries[:6]:
    sentiment_html = ""
    for sent, count in ps.sentiment_distribution.items():
      color = _get_sentiment_color(sent)
      sentiment_html += f"""
        <span style="color: {color}; margin-right: 10px;">
            {sent}: {count}
        </span>
      """

    themes_html = ", ".join(ps.themes_discussed[:3]) if ps.themes_discussed else "N/A"

    items_html += f"""
      <div class="participant-card">
          <div class="participant-header">
              <span class="participant-id">{_escape_html(ps.participant_id)}</span>
              <span class="participant-count">{ps.total_contributions} contributions</span>
          </div>
          <div style="font-size: 0.85rem; color: #666;">
              Themes: {_escape_html(themes_html)}
          </div>
          <div style="font-size: 0.85rem; margin-top: 5px;">
              {sentiment_html}
          </div>
      </div>
    """

  return f"""
    <div class="card">
        <h2>Participant Summary</h2>
        {items_html}
    </div>
  """


def _render_quotes(result: AnalysisResult) -> str:
  """Render notable quotes."""
  quotes = result.get_extractions_by_type(ExtractionType.QUOTE)

  # Also include insights if no quotes
  if not quotes:
    quotes = result.get_extractions_by_type(ExtractionType.INSIGHT)

  if not quotes:
    return ""

  items_html = ""
  for quote in quotes[:5]:
    participant = ""
    if quote.attributes:
      participant = quote.attributes.get("participant", "")

    items_html += f"""
      <div class="quote-card">
          <div class="quote-text">{_escape_html(quote.extraction_text)}</div>
          <div class="quote-meta">— {_escape_html(participant) if participant else 'Anonymous'}</div>
      </div>
    """

  return f"""
    <div class="card">
        <h2>Notable Quotes</h2>
        {items_html}
    </div>
  """


def _render_sentiment_breakdown(result: AnalysisResult) -> str:
  """Render sentiment breakdown chart."""
  sentiment_counts: dict[str, int] = collections.Counter()

  for doc in result.annotated_documents:
    for extraction in doc.extractions or []:
      if extraction.attributes:
        sentiment = extraction.attributes.get("sentiment")
        if sentiment:
          sentiment_counts[sentiment] += 1

  if not sentiment_counts:
    return ""

  total = sum(sentiment_counts.values())
  max_count = max(sentiment_counts.values())

  bars_html = ""
  for sentiment in [
      "very_positive",
      "positive",
      "neutral",
      "negative",
      "very_negative",
  ]:
    count = sentiment_counts.get(sentiment, 0)
    height_pct = (count / max_count) * 150 if max_count > 0 else 0
    color = _get_sentiment_color(sentiment)
    pct = (count / total) * 100 if total > 0 else 0
    label = sentiment.replace("_", " ").title()

    bars_html += f"""
      <div class="chart-bar-wrapper">
          <div class="chart-value">{pct:.0f}%</div>
          <div class="chart-bar" style="height: {height_pct}px; background: {color}"></div>
          <div class="chart-label">{label}</div>
      </div>
    """

  return f"""
    <div class="card">
        <h2>Sentiment Breakdown</h2>
        <div class="chart-container">{bars_html}</div>
    </div>
  """


def create_dashboard(result: AnalysisResult) -> str:
  """Create an interactive HTML dashboard for analysis results.

  Args:
    result: AnalysisResult from focus group analysis.

  Returns:
    HTML string containing the interactive dashboard.
  """
  header = _render_header(result)

  cards = []
  cards.append(_render_key_findings(result))
  cards.append(_render_themes_chart(result.themes))
  cards.append(_render_sentiment_breakdown(result))
  cards.append(_render_extraction_distribution(result))
  cards.append(_render_pain_points(result))
  cards.append(_render_feature_requests(result))
  cards.append(_render_participant_summary(result))
  cards.append(_render_quotes(result))

  # Filter out empty cards
  cards = [c for c in cards if c]

  return DASHBOARD_TEMPLATE.format(header=header, cards="\n".join(cards))


def create_highlighted_transcript(
    result: AnalysisResult,
    document_index: int = 0,
) -> str:
  """Create HTML with highlighted extractions in the transcript.

  Args:
    result: AnalysisResult from focus group analysis.
    document_index: Index of the document to visualize.

  Returns:
    HTML string with highlighted transcript.
  """
  if document_index >= len(result.annotated_documents):
    return "<p>Document not found</p>"

  doc = result.annotated_documents[document_index]
  if not doc.text:
    return "<p>No text available</p>"

  # Sort extractions by position
  extractions = sorted(
      doc.extractions or [],
      key=lambda e: (
          e.char_interval.start_pos if e.char_interval else float("inf")
      ),
  )

  # Build highlighted text
  text = doc.text
  result_parts = []
  last_end = 0

  for extraction in extractions:
    if not extraction.char_interval:
      continue

    start = extraction.char_interval.start_pos or 0
    end = extraction.char_interval.end_pos or start

    if start < last_end:
      continue  # Skip overlapping

    # Add text before this extraction
    if start > last_end:
      result_parts.append(_escape_html(text[last_end:start]))

    # Add highlighted extraction
    color = _get_extraction_color(extraction.extraction_class)
    info = {
        "type": extraction.extraction_class,
    }
    if extraction.attributes:
      info.update(extraction.attributes)

    info_json = _escape_html(json.dumps(info))
    highlighted_text = _escape_html(text[start:end])

    result_parts.append(
        f'<span class="highlight" style="background: {color}33; '
        f'border-bottom: 2px solid {color};" '
        f"data-info='{info_json}'>{highlighted_text}</span>"
    )

    last_end = end

  # Add remaining text
  if last_end < len(text):
    result_parts.append(_escape_html(text[last_end:]))

  transcript_html = "".join(result_parts)

  return f"""
    <div class="transcript-view">{transcript_html}</div>
    <div class="tooltip" id="tooltip"></div>
    <script>
        const tooltip = document.getElementById('tooltip');
        document.querySelectorAll('.highlight').forEach(el => {{
            el.addEventListener('mouseenter', (e) => {{
                const data = JSON.parse(el.dataset.info || '{{}}');
                let content = '<strong>' + (data.type || 'Extraction') + '</strong>';
                for (const [key, value] of Object.entries(data)) {{
                    if (key !== 'type') {{
                        content += '<br>' + key + ': ' + value;
                    }}
                }}
                tooltip.innerHTML = content;
                tooltip.style.display = 'block';
                tooltip.style.left = e.pageX + 10 + 'px';
                tooltip.style.top = e.pageY + 10 + 'px';
            }});
            el.addEventListener('mouseleave', () => {{
                tooltip.style.display = 'none';
            }});
        }});
    </script>
  """


def export_to_json(result: AnalysisResult) -> dict[str, Any]:
  """Export analysis result to JSON-serializable format.

  Args:
    result: AnalysisResult from focus group analysis.

  Returns:
    Dictionary suitable for JSON serialization.
  """
  return {
      "summary": {
          "total_extractions": result.total_extractions,
          "extraction_type_counts": result.extraction_type_counts,
          "overall_sentiment": result.overall_sentiment.value,
          "key_findings": result.key_findings,
      },
      "themes": [
          {
              "name": t.theme_name,
              "frequency": t.frequency,
              "sentiment_distribution": t.sentiment_distribution,
              "sample_quotes": t.sample_quotes,
              "participants": list(t.participants_mentioned),
              "avg_sentiment_score": t.avg_sentiment_score,
          }
          for t in result.themes
      ],
      "participants": [
          {
              "id": p.participant_id,
              "contributions": p.total_contributions,
              "sentiment_distribution": p.sentiment_distribution,
              "themes": p.themes_discussed,
              "key_quotes": p.key_quotes,
              "avg_sentiment_score": p.avg_sentiment_score,
          }
          for p in result.participant_summaries
      ],
      "insight_clusters": [
          {
              "id": c.cluster_id,
              "theme": c.theme,
              "sentiment": c.sentiment.value,
              "confidence": c.confidence.value,
              "quotes": c.supporting_quotes,
              "participant_count": c.participant_count,
          }
          for c in result.insight_clusters
      ],
      "metadata": result.metadata,
  }


def save_dashboard(result: AnalysisResult, file_path: str) -> None:
  """Save the dashboard to an HTML file.

  Args:
    result: AnalysisResult from focus group analysis.
    file_path: Path to save the HTML file.
  """
  html_content = create_dashboard(result)
  with open(file_path, "w", encoding="utf-8") as f:
    f.write(html_content)


def save_json_report(result: AnalysisResult, file_path: str) -> None:
  """Save the analysis as a JSON report.

  Args:
    result: AnalysisResult from focus group analysis.
    file_path: Path to save the JSON file.
  """
  data = export_to_json(result)
  with open(file_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
