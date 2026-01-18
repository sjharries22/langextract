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

"""Visualization utilities for population health focus group analysis."""

from __future__ import annotations

import collections
import html
import json
from typing import Any

from langextract.tools.focus_group.types import (
    AlignmentStatus,
    AnalysisResult,
    ExtractionType,
    HealthDomain,
    SDOHCategory,
    Sentiment,
    ThemeSummary,
)

# Color palette for health-focused extraction types
EXTRACTION_COLORS = {
    # Health concerns
    ExtractionType.HEALTH_CONCERN.value: "#E53935",  # Red
    ExtractionType.HEALTH_CONDITION.value: "#D32F2F",  # Dark red
    ExtractionType.SYMPTOM.value: "#EF5350",  # Light red
    # Barriers and access
    ExtractionType.BARRIER_TO_CARE.value: "#FF7043",  # Deep orange
    ExtractionType.ACCESS_ISSUE.value: "#FF8A65",  # Light orange
    ExtractionType.RESOURCE_GAP.value: "#FFAB91",  # Pale orange
    # SDOH factors
    ExtractionType.SDOH_FACTOR.value: "#7E57C2",  # Purple
    ExtractionType.HOUSING_ISSUE.value: "#9575CD",  # Light purple
    ExtractionType.FOOD_ACCESS.value: "#4DB6AC",  # Teal
    ExtractionType.TRANSPORTATION_ISSUE.value: "#4DD0E1",  # Cyan
    ExtractionType.ECONOMIC_FACTOR.value: "#FFB74D",  # Amber
    ExtractionType.SAFETY_CONCERN.value: "#F06292",  # Pink
    ExtractionType.ENVIRONMENTAL_FACTOR.value: "#81C784",  # Light green
    # Healthcare experiences
    ExtractionType.HEALTHCARE_EXPERIENCE.value: "#64B5F6",  # Blue
    ExtractionType.PROVIDER_INTERACTION.value: "#42A5F5",  # Medium blue
    ExtractionType.CARE_QUALITY.value: "#2196F3",  # Primary blue
    ExtractionType.TRUST_ISSUE.value: "#1976D2",  # Dark blue
    # Community factors
    ExtractionType.COMMUNITY_STRENGTH.value: "#66BB6A",  # Green
    ExtractionType.SOCIAL_SUPPORT.value: "#81C784",  # Light green
    ExtractionType.CULTURAL_FACTOR.value: "#A1887F",  # Brown
    # Needs and suggestions
    ExtractionType.UNMET_NEED.value: "#FFA726",  # Orange
    ExtractionType.COMMUNITY_SUGGESTION.value: "#29B6F6",  # Light blue
    ExtractionType.PRIORITY_AREA.value: "#AB47BC",  # Purple
    # General
    ExtractionType.QUOTE.value: "#78909C",  # Blue grey
    ExtractionType.INSIGHT.value: "#26A69A",  # Teal
    ExtractionType.SENTIMENT.value: "#5C6BC0",  # Indigo
    ExtractionType.AGREEMENT.value: "#9CCC65",  # Light green
    ExtractionType.DISAGREEMENT.value: "#EF5350",  # Red
}

# Health domain colors
HEALTH_DOMAIN_COLORS = {
    HealthDomain.CHRONIC_DISEASE.value: "#E53935",
    HealthDomain.MENTAL_HEALTH.value: "#7E57C2",
    HealthDomain.MATERNAL_CHILD_HEALTH.value: "#EC407A",
    HealthDomain.INFECTIOUS_DISEASE.value: "#FFA726",
    HealthDomain.SUBSTANCE_USE.value: "#8D6E63",
    HealthDomain.ORAL_HEALTH.value: "#26C6DA",
    HealthDomain.NUTRITION.value: "#66BB6A",
    HealthDomain.PHYSICAL_ACTIVITY.value: "#42A5F5",
    HealthDomain.ENVIRONMENTAL_HEALTH.value: "#9CCC65",
    HealthDomain.AGING.value: "#78909C",
}

# SDOH category colors
SDOH_COLORS = {
    SDOHCategory.ECONOMIC_STABILITY.value: "#FFB74D",
    SDOHCategory.EDUCATION_ACCESS.value: "#4FC3F7",
    SDOHCategory.HEALTHCARE_ACCESS.value: "#E57373",
    SDOHCategory.NEIGHBORHOOD_ENVIRONMENT.value: "#81C784",
    SDOHCategory.SOCIAL_COMMUNITY.value: "#BA68C8",
}

# Alignment status colors
ALIGNMENT_COLORS = {
    AlignmentStatus.ALIGNED.value: "#4CAF50",  # Green - data confirms
    AlignmentStatus.PARTIALLY_ALIGNED.value: "#FFC107",  # Amber
    AlignmentStatus.DIVERGENT.value: "#FF9800",  # Orange - emerging issue
    AlignmentStatus.DATA_GAP.value: "#9E9E9E",  # Grey - no data
    AlignmentStatus.EMERGING.value: "#2196F3",  # Blue - new concern
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
    <title>Community Health Analysis Dashboard</title>
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


def _render_health_concerns(result: AnalysisResult) -> str:
  """Render health concerns card."""
  if not result.health_concerns:
    return ""

  items_html = ""
  for concern in result.health_concerns[:8]:
    severity = concern.severity.value if concern.severity else "medium"
    severity_class = f"severity-{severity}"
    domain_html = ""
    if concern.health_domain:
      domain_color = HEALTH_DOMAIN_COLORS.get(
          concern.health_domain.value, "#9E9E9E"
      )
      domain_html = f"""
        <span style="background: {domain_color}; color: white;
                     padding: 2px 8px; border-radius: 4px;
                     font-size: 0.75rem; margin-left: 8px;">
            {concern.health_domain.value.replace('_', ' ').title()}
        </span>
      """

    items_html += f"""
      <div class="pain-point">
          {_escape_html(concern.concern)}
          <span class="pain-point-severity {severity_class}">
              {severity.upper()}
          </span>
          {domain_html}
      </div>
    """

  return f"""
    <div class="card">
        <h2>Health Concerns ({len(result.health_concerns)})</h2>
        {items_html}
    </div>
  """


def _render_barriers_to_care(result: AnalysisResult) -> str:
  """Render barriers to care card."""
  if not result.barriers:
    return ""

  items_html = ""
  for barrier in result.barriers[:8]:
    sdoh_html = ""
    if barrier.sdoh_category:
      sdoh_color = SDOH_COLORS.get(barrier.sdoh_category.value, "#9E9E9E")
      sdoh_html = f"""
        <span style="background: {sdoh_color}; color: white;
                     padding: 2px 8px; border-radius: 4px;
                     font-size: 0.75rem;">
            {barrier.sdoh_category.value.replace('_', ' ').title()}
        </span>
      """

    items_html += f"""
      <div class="feature-request" style="border-left-color: #FF7043;">
          <div style="margin-bottom: 8px;">
              <strong>{_escape_html(barrier.barrier_type)}</strong>
              {sdoh_html}
          </div>
          <div>{_escape_html(barrier.barrier)}</div>
      </div>
    """

  return f"""
    <div class="card">
        <h2>Barriers to Care ({len(result.barriers)})</h2>
        {items_html}
    </div>
  """


def _render_data_comparison(result: AnalysisResult) -> str:
  """Render community voice vs population health data comparison."""
  if not result.data_comparisons:
    return ""

  items_html = ""
  for dc in result.data_comparisons[:10]:
    status_color = ALIGNMENT_COLORS.get(dc.alignment_status.value, "#9E9E9E")
    status_label = {
        AlignmentStatus.ALIGNED.value: "DATA CONFIRMS",
        AlignmentStatus.PARTIALLY_ALIGNED.value: "PARTIAL MATCH",
        AlignmentStatus.DIVERGENT.value: "EMERGING ISSUE",
        AlignmentStatus.DATA_GAP.value: "NO DATA",
        AlignmentStatus.EMERGING.value: "NEW CONCERN",
    }.get(dc.alignment_status.value, dc.alignment_status.value.upper())

    data_html = ""
    if dc.population_indicator:
      ind = dc.population_indicator
      benchmark_html = ""
      if ind.comparison_value:
        diff = ind.value - ind.comparison_value
        diff_sign = "+" if diff > 0 else ""
        benchmark_html = f"""
          <div style="font-size: 0.85rem; color: #666;">
              Benchmark ({ind.comparison_geography}): {ind.comparison_value}{ind.unit}
              <span style="color: {'#E53935' if diff > 0 else '#4CAF50'};">
                  ({diff_sign}{diff:.1f})
              </span>
          </div>
        """

      data_html = f"""
        <div style="background: #f5f5f5; padding: 10px; border-radius: 6px;
                    margin-top: 8px;">
            <div style="font-weight: 500;">{_escape_html(ind.name)}</div>
            <div style="font-size: 1.5rem; font-weight: bold; color: #333;">
                {ind.value}{ind.unit}
            </div>
            {benchmark_html}
            <div style="font-size: 0.75rem; color: #999;">
                Source: {_escape_html(ind.source)} ({ind.year})
            </div>
        </div>
      """

    interpretation_html = ""
    if dc.interpretation:
      interpretation_html = f"""
        <div style="font-size: 0.85rem; color: #555; margin-top: 8px;
                    font-style: italic;">
            {_escape_html(dc.interpretation)}
        </div>
      """

    items_html += f"""
      <div style="border: 1px solid #e0e0e0; border-radius: 8px;
                  padding: 15px; margin-bottom: 12px;
                  border-left: 4px solid {status_color};">
          <div style="display: flex; justify-content: space-between;
                      align-items: center; margin-bottom: 8px;">
              <strong style="font-size: 1.1rem;">
                  {_escape_html(dc.topic)}
              </strong>
              <span style="background: {status_color}; color: white;
                           padding: 4px 10px; border-radius: 4px;
                           font-size: 0.75rem; font-weight: 500;">
                  {status_label}
              </span>
          </div>
          <div style="color: #666;">
              Community mentions: <strong>{dc.community_frequency}</strong>
          </div>
          {data_html}
          {interpretation_html}
      </div>
    """

  return f"""
    <div class="card" style="grid-column: span 2;">
        <h2>Community Voice vs Population Health Data</h2>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 15px;">
            {items_html}
        </div>
    </div>
  """


def _render_community_strengths(result: AnalysisResult) -> str:
  """Render community strengths card."""
  if not result.community_strengths:
    return ""

  items_html = ""
  for strength in result.community_strengths[:6]:
    items_html += f"""
      <div class="finding" style="border-left-color: #4CAF50;">
          {_escape_html(strength)}
      </div>
    """

  return f"""
    <div class="card">
        <h2>Community Strengths</h2>
        {items_html}
    </div>
  """


def _render_priority_areas(result: AnalysisResult) -> str:
  """Render community-identified priority areas card."""
  if not result.priority_areas:
    return ""

  items_html = ""
  for i, priority in enumerate(result.priority_areas[:6], 1):
    items_html += f"""
      <div style="display: flex; align-items: flex-start; gap: 12px;
                  padding: 12px 0; border-bottom: 1px solid #eee;">
          <span style="background: #7E57C2; color: white; width: 28px;
                       height: 28px; border-radius: 50%; display: flex;
                       align-items: center; justify-content: center;
                       font-weight: bold; flex-shrink: 0;">
              {i}
          </span>
          <div>{_escape_html(priority)}</div>
      </div>
    """

  return f"""
    <div class="card">
        <h2>Community-Identified Priorities</h2>
        {items_html}
    </div>
  """


def _render_health_domain_breakdown(result: AnalysisResult) -> str:
  """Render health domain breakdown chart."""
  if not result.health_concerns:
    return ""

  domain_counts: dict[str, int] = collections.Counter()
  for concern in result.health_concerns:
    if concern.health_domain:
      domain_counts[concern.health_domain.value] += 1

  if not domain_counts:
    return ""

  max_count = max(domain_counts.values())

  bars_html = ""
  for domain, count in sorted(
      domain_counts.items(), key=lambda x: x[1], reverse=True
  )[:6]:
    height_pct = (count / max_count) * 150
    color = HEALTH_DOMAIN_COLORS.get(domain, "#9E9E9E")
    label = domain.replace("_", " ").title()

    bars_html += f"""
      <div class="chart-bar-wrapper">
          <div class="chart-value">{count}</div>
          <div class="chart-bar" style="height: {height_pct}px; background: {color}"></div>
          <div class="chart-label">{label[:12]}</div>
      </div>
    """

  return f"""
    <div class="card">
        <h2>Health Domains</h2>
        <div class="chart-container">{bars_html}</div>
    </div>
  """


def _render_sdoh_breakdown(result: AnalysisResult) -> str:
  """Render SDOH category breakdown chart."""
  if not result.barriers:
    return ""

  sdoh_counts: dict[str, int] = collections.Counter()
  for barrier in result.barriers:
    if barrier.sdoh_category:
      sdoh_counts[barrier.sdoh_category.value] += 1

  if not sdoh_counts:
    return ""

  max_count = max(sdoh_counts.values())

  bars_html = ""
  for sdoh, count in sorted(
      sdoh_counts.items(), key=lambda x: x[1], reverse=True
  ):
    height_pct = (count / max_count) * 150
    color = SDOH_COLORS.get(sdoh, "#9E9E9E")
    label = sdoh.replace("_", " ").title()

    bars_html += f"""
      <div class="chart-bar-wrapper">
          <div class="chart-value">{count}</div>
          <div class="chart-bar" style="height: {height_pct}px; background: {color}"></div>
          <div class="chart-label">{label[:12]}</div>
      </div>
    """

  return f"""
    <div class="card">
        <h2>Social Determinants of Health</h2>
        <div class="chart-container">{bars_html}</div>
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

  # Health-specific cards (prioritized if available)
  cards.append(_render_data_comparison(result))
  cards.append(_render_health_concerns(result))
  cards.append(_render_barriers_to_care(result))
  cards.append(_render_health_domain_breakdown(result))
  cards.append(_render_sdoh_breakdown(result))
  cards.append(_render_community_strengths(result))
  cards.append(_render_priority_areas(result))

  # General analysis cards
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
  output = {
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
              "health_domain": t.health_domain.value if t.health_domain else None,
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

  # Add health-specific data
  if result.health_concerns:
    output["health_concerns"] = [
        {
            "concern": c.concern,
            "severity": c.severity.value if c.severity else None,
            "frequency": c.frequency,
            "health_domain": c.health_domain.value if c.health_domain else None,
            "sample_quotes": c.sample_quotes,
        }
        for c in result.health_concerns
    ]

  if result.barriers:
    output["barriers_to_care"] = [
        {
            "barrier": b.barrier,
            "barrier_type": b.barrier_type,
            "frequency": b.frequency,
            "sdoh_category": b.sdoh_category.value if b.sdoh_category else None,
            "sample_quotes": b.sample_quotes,
        }
        for b in result.barriers
    ]

  if result.community_strengths:
    output["community_strengths"] = result.community_strengths

  if result.priority_areas:
    output["priority_areas"] = result.priority_areas

  if result.data_comparisons:
    output["data_comparisons"] = [
        {
            "topic": dc.topic,
            "alignment_status": dc.alignment_status.value,
            "community_frequency": dc.community_frequency,
            "population_indicator": {
                "name": dc.population_indicator.name,
                "value": dc.population_indicator.value,
                "unit": dc.population_indicator.unit,
                "source": dc.population_indicator.source,
                "year": dc.population_indicator.year,
                "comparison_value": dc.population_indicator.comparison_value,
                "comparison_geography": dc.population_indicator.comparison_geography,
            } if dc.population_indicator else None,
            "interpretation": dc.interpretation,
        }
        for dc in result.data_comparisons
    ]

  if result.community_health_gaps:
    output["community_health_gaps"] = [
        {
            "gap_description": g.gap_description,
            "frequency_mentioned": g.frequency_mentioned,
            "severity": g.severity.value if g.severity else None,
            "suggested_data_sources": g.suggested_data_sources,
        }
        for g in result.community_health_gaps
    ]

  return output


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
