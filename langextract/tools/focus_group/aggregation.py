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

"""Aggregation and summary utilities for focus group analysis."""

from __future__ import annotations

import collections
from collections.abc import Sequence
from typing import Any

from langextract.core.data import AnnotatedDocument, Extraction
from langextract.tools.focus_group.types import (
    AnalysisResult,
    Confidence,
    ExtractionType,
    InsightCluster,
    ParticipantSummary,
    Sentiment,
    ThemeSummary,
)

# Sentiment scoring for aggregation
SENTIMENT_SCORES = {
    "very_positive": 2.0,
    "positive": 1.0,
    "neutral": 0.0,
    "negative": -1.0,
    "very_negative": -2.0,
    "mixed": 0.0,
}


def _get_sentiment_score(sentiment: str) -> float:
  """Convert sentiment string to numerical score."""
  return SENTIMENT_SCORES.get(sentiment.lower(), 0.0)


def _classify_overall_sentiment(avg_score: float) -> Sentiment:
  """Classify overall sentiment based on average score."""
  if avg_score >= 1.5:
    return Sentiment.VERY_POSITIVE
  elif avg_score >= 0.5:
    return Sentiment.POSITIVE
  elif avg_score >= -0.5:
    return Sentiment.NEUTRAL
  elif avg_score >= -1.5:
    return Sentiment.NEGATIVE
  else:
    return Sentiment.VERY_NEGATIVE


def extract_themes(
    documents: Sequence[AnnotatedDocument],
) -> list[ThemeSummary]:
  """Extract and summarize themes from annotated documents.

  Args:
    documents: Sequence of annotated documents with extractions.

  Returns:
    List of ThemeSummary objects sorted by frequency.
  """
  theme_data: dict[str, dict[str, Any]] = collections.defaultdict(
      lambda: {
          "count": 0,
          "sentiments": collections.Counter(),
          "quotes": [],
          "participants": set(),
      }
  )

  for doc in documents:
    for extraction in doc.extractions or []:
      theme = None

      # Get theme from extraction class or attributes
      if extraction.extraction_class == ExtractionType.THEME.value:
        theme = extraction.attributes.get("theme") if extraction.attributes else None
        if not theme:
          theme = extraction.extraction_text.strip()
      elif extraction.attributes:
        theme = extraction.attributes.get("topic")

      if theme:
        theme = theme.lower().strip()
        theme_data[theme]["count"] += 1

        # Track sentiment
        if extraction.attributes:
          sentiment = extraction.attributes.get("sentiment", "neutral")
          theme_data[theme]["sentiments"][sentiment] += 1

          # Track participant
          participant = extraction.attributes.get("participant")
          if participant:
            theme_data[theme]["participants"].add(participant)

        # Collect sample quotes
        if len(theme_data[theme]["quotes"]) < 5:
          theme_data[theme]["quotes"].append(extraction.extraction_text)

  # Convert to ThemeSummary objects
  summaries = []
  for theme_name, data in theme_data.items():
    sentiment_dist = dict(data["sentiments"])
    sentiment_scores = [
        _get_sentiment_score(s) * count
        for s, count in sentiment_dist.items()
    ]
    total_sentiment_count = sum(sentiment_dist.values())
    avg_score = (
        sum(sentiment_scores) / total_sentiment_count
        if total_sentiment_count > 0
        else None
    )

    summaries.append(
        ThemeSummary(
            theme_name=theme_name,
            frequency=data["count"],
            sentiment_distribution=sentiment_dist,
            sample_quotes=data["quotes"],
            participants_mentioned=data["participants"],
            avg_sentiment_score=avg_score,
        )
    )

  # Sort by frequency
  summaries.sort(key=lambda x: x.frequency, reverse=True)
  return summaries


def extract_participant_summaries(
    documents: Sequence[AnnotatedDocument],
) -> list[ParticipantSummary]:
  """Extract summaries for each participant.

  Args:
    documents: Sequence of annotated documents with extractions.

  Returns:
    List of ParticipantSummary objects.
  """
  participant_data: dict[str, dict[str, Any]] = collections.defaultdict(
      lambda: {
          "count": 0,
          "sentiments": collections.Counter(),
          "themes": set(),
          "quotes": [],
      }
  )

  for doc in documents:
    for extraction in doc.extractions or []:
      if not extraction.attributes:
        continue

      participant = extraction.attributes.get("participant")
      if not participant:
        continue

      participant_data[participant]["count"] += 1

      # Track sentiment
      sentiment = extraction.attributes.get("sentiment")
      if sentiment:
        participant_data[participant]["sentiments"][sentiment] += 1

      # Track themes
      topic = extraction.attributes.get("topic") or extraction.attributes.get(
          "theme"
      )
      if topic:
        participant_data[participant]["themes"].add(topic.lower())

      # Collect key quotes
      if extraction.extraction_class == ExtractionType.QUOTE.value:
        if len(participant_data[participant]["quotes"]) < 5:
          participant_data[participant]["quotes"].append(
              extraction.extraction_text
          )
      elif len(participant_data[participant]["quotes"]) < 3:
        participant_data[participant]["quotes"].append(
            extraction.extraction_text
        )

  # Convert to ParticipantSummary objects
  summaries = []
  for participant_id, data in participant_data.items():
    sentiment_dist = dict(data["sentiments"])
    sentiment_scores = [
        _get_sentiment_score(s) * count
        for s, count in sentiment_dist.items()
    ]
    total_sentiment_count = sum(sentiment_dist.values())
    avg_score = (
        sum(sentiment_scores) / total_sentiment_count
        if total_sentiment_count > 0
        else None
    )

    summaries.append(
        ParticipantSummary(
            participant_id=participant_id,
            total_contributions=data["count"],
            sentiment_distribution=sentiment_dist,
            themes_discussed=sorted(data["themes"]),
            key_quotes=data["quotes"],
            avg_sentiment_score=avg_score,
        )
    )

  # Sort by total contributions
  summaries.sort(key=lambda x: x.total_contributions, reverse=True)
  return summaries


def cluster_insights(
    documents: Sequence[AnnotatedDocument],
    min_cluster_size: int = 2,
) -> list[InsightCluster]:
  """Cluster related insights together.

  Args:
    documents: Sequence of annotated documents with extractions.
    min_cluster_size: Minimum number of extractions to form a cluster.

  Returns:
    List of InsightCluster objects.
  """
  # Group extractions by theme/topic
  theme_extractions: dict[str, list[Extraction]] = collections.defaultdict(list)

  for doc in documents:
    for extraction in doc.extractions or []:
      if not extraction.attributes:
        continue

      # Determine theme
      theme = (
          extraction.attributes.get("topic")
          or extraction.attributes.get("theme")
          or extraction.attributes.get("category")
      )

      if theme:
        theme_extractions[theme.lower()].append(extraction)

  # Create clusters
  clusters = []
  cluster_id = 0

  for theme, extractions in theme_extractions.items():
    if len(extractions) < min_cluster_size:
      continue

    cluster_id += 1

    # Calculate cluster sentiment
    sentiments = []
    participants = set()
    quotes = []

    for extraction in extractions:
      if extraction.attributes:
        sentiment = extraction.attributes.get("sentiment")
        if sentiment:
          sentiments.append(sentiment)

        participant = extraction.attributes.get("participant")
        if participant:
          participants.add(participant)

      quotes.append(extraction.extraction_text)

    # Determine overall cluster sentiment
    sentiment_counts = collections.Counter(sentiments)
    if sentiment_counts:
      most_common = sentiment_counts.most_common(1)[0][0]
      try:
        cluster_sentiment = Sentiment(most_common)
      except ValueError:
        cluster_sentiment = Sentiment.NEUTRAL
    else:
      cluster_sentiment = Sentiment.NEUTRAL

    # Determine confidence based on cluster size
    if len(extractions) >= 5:
      confidence = Confidence.HIGH
    elif len(extractions) >= 3:
      confidence = Confidence.MEDIUM
    else:
      confidence = Confidence.LOW

    clusters.append(
        InsightCluster(
            cluster_id=f"cluster_{cluster_id}",
            theme=theme,
            insights=extractions,
            sentiment=cluster_sentiment,
            confidence=confidence,
            supporting_quotes=quotes[:5],  # Limit quotes
            participant_count=len(participants),
        )
    )

  # Sort by participant count (more participants = more significant)
  clusters.sort(key=lambda x: x.participant_count, reverse=True)
  return clusters


def calculate_overall_sentiment(
    documents: Sequence[AnnotatedDocument],
) -> Sentiment:
  """Calculate overall sentiment across all documents.

  Args:
    documents: Sequence of annotated documents with extractions.

  Returns:
    Overall Sentiment classification.
  """
  sentiment_scores = []

  for doc in documents:
    for extraction in doc.extractions or []:
      if not extraction.attributes:
        continue

      sentiment = extraction.attributes.get("sentiment")
      if sentiment:
        sentiment_scores.append(_get_sentiment_score(sentiment))

  if not sentiment_scores:
    return Sentiment.NEUTRAL

  avg_score = sum(sentiment_scores) / len(sentiment_scores)
  return _classify_overall_sentiment(avg_score)


def generate_key_findings(
    documents: Sequence[AnnotatedDocument],
    max_findings: int = 10,
) -> list[str]:
  """Generate key findings from the analysis.

  Args:
    documents: Sequence of annotated documents with extractions.
    max_findings: Maximum number of findings to generate.

  Returns:
    List of key finding strings.
  """
  findings = []

  # Count extraction types
  type_counts: dict[str, int] = collections.Counter()
  pain_points: list[str] = []
  feature_requests: list[str] = []
  positive_sentiments: list[str] = []
  negative_sentiments: list[str] = []

  for doc in documents:
    for extraction in doc.extractions or []:
      type_counts[extraction.extraction_class] += 1

      if extraction.extraction_class == ExtractionType.PAIN_POINT.value:
        pain_points.append(extraction.extraction_text)
      elif extraction.extraction_class == ExtractionType.FEATURE_REQUEST.value:
        feature_requests.append(extraction.extraction_text)
      elif extraction.attributes:
        sentiment = extraction.attributes.get("sentiment", "")
        if sentiment in ("positive", "very_positive"):
          positive_sentiments.append(extraction.extraction_text)
        elif sentiment in ("negative", "very_negative"):
          negative_sentiments.append(extraction.extraction_text)

  # Generate findings
  total_extractions = sum(type_counts.values())
  if total_extractions > 0:
    findings.append(
        f"Identified {total_extractions} insights across "
        f"{len(type_counts)} categories"
    )

  if pain_points:
    findings.append(
        f"Found {len(pain_points)} pain points - "
        f"top concern: \"{pain_points[0][:100]}...\""
        if len(pain_points[0]) > 100
        else f"Found {len(pain_points)} pain points - "
        f"top concern: \"{pain_points[0]}\""
    )

  if feature_requests:
    findings.append(
        f"Captured {len(feature_requests)} feature requests"
    )

  # Sentiment balance
  positive_count = len(positive_sentiments)
  negative_count = len(negative_sentiments)
  if positive_count + negative_count > 0:
    positive_pct = positive_count / (positive_count + negative_count) * 100
    findings.append(
        f"Sentiment distribution: {positive_pct:.0f}% positive, "
        f"{100 - positive_pct:.0f}% negative"
    )

  # Most discussed topics
  themes = extract_themes(documents)
  if themes:
    top_themes = [t.theme_name for t in themes[:3]]
    findings.append(f"Top themes: {', '.join(top_themes)}")

  # Participant engagement
  participants = extract_participant_summaries(documents)
  if participants:
    findings.append(
        f"Analyzed contributions from {len(participants)} participants"
    )

  return findings[:max_findings]


def aggregate_by_attribute(
    documents: Sequence[AnnotatedDocument],
    attribute_name: str,
) -> dict[str, list[Extraction]]:
  """Group extractions by a specific attribute value.

  Args:
    documents: Sequence of annotated documents with extractions.
    attribute_name: Name of the attribute to group by.

  Returns:
    Dictionary mapping attribute values to lists of extractions.
  """
  grouped: dict[str, list[Extraction]] = collections.defaultdict(list)

  for doc in documents:
    for extraction in doc.extractions or []:
      if extraction.attributes:
        value = extraction.attributes.get(attribute_name)
        if value:
          if isinstance(value, list):
            for v in value:
              grouped[str(v)].append(extraction)
          else:
            grouped[str(value)].append(extraction)

  return dict(grouped)


def calculate_sentiment_over_time(
    documents: Sequence[AnnotatedDocument],
) -> list[tuple[int, float]]:
  """Calculate sentiment progression through the document.

  Args:
    documents: Sequence of annotated documents with extractions.

  Returns:
    List of (extraction_index, sentiment_score) tuples.
  """
  sentiment_progression = []

  for doc in documents:
    for extraction in doc.extractions or []:
      if extraction.attributes and extraction.extraction_index is not None:
        sentiment = extraction.attributes.get("sentiment")
        if sentiment:
          score = _get_sentiment_score(sentiment)
          sentiment_progression.append((extraction.extraction_index, score))

  sentiment_progression.sort(key=lambda x: x[0])
  return sentiment_progression


def create_analysis_result(
    annotated_documents: Sequence[AnnotatedDocument],
    metadata: dict[str, Any] | None = None,
) -> AnalysisResult:
  """Create a complete AnalysisResult from annotated documents.

  Args:
    annotated_documents: Sequence of annotated documents with extractions.
    metadata: Optional metadata to include in the result.

  Returns:
    Complete AnalysisResult object.
  """
  return AnalysisResult(
      annotated_documents=annotated_documents,
      themes=extract_themes(annotated_documents),
      participant_summaries=extract_participant_summaries(annotated_documents),
      insight_clusters=cluster_insights(annotated_documents),
      overall_sentiment=calculate_overall_sentiment(annotated_documents),
      key_findings=generate_key_findings(annotated_documents),
      metadata=metadata,
  )


def compare_sessions(
    results: Sequence[AnalysisResult],
) -> dict[str, Any]:
  """Compare multiple analysis sessions.

  Args:
    results: Sequence of AnalysisResult objects to compare.

  Returns:
    Dictionary containing comparison metrics.
  """
  comparison = {
      "session_count": len(results),
      "total_extractions": 0,
      "sentiment_by_session": [],
      "common_themes": collections.Counter(),
      "common_pain_points": collections.Counter(),
      "all_feature_requests": [],
  }

  for i, result in enumerate(results):
    comparison["total_extractions"] += result.total_extractions
    comparison["sentiment_by_session"].append({
        "session": i + 1,
        "sentiment": result.overall_sentiment.value,
    })

    # Track themes
    for theme in result.themes:
      comparison["common_themes"][theme.theme_name] += theme.frequency

    # Track pain points and feature requests
    pain_points = result.get_extractions_by_type(ExtractionType.PAIN_POINT)
    for pp in pain_points:
      comparison["common_pain_points"][pp.extraction_text] += 1

    feature_requests = result.get_extractions_by_type(
        ExtractionType.FEATURE_REQUEST
    )
    for fr in feature_requests:
      comparison["all_feature_requests"].append(fr.extraction_text)

  # Convert counters to sorted lists
  comparison["common_themes"] = [
      {"theme": theme, "count": count}
      for theme, count in comparison["common_themes"].most_common(10)
  ]
  comparison["common_pain_points"] = [
      {"pain_point": pp, "count": count}
      for pp, count in comparison["common_pain_points"].most_common(10)
  ]

  return comparison
