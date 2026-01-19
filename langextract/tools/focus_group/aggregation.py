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

"""Aggregation and summary utilities for population health focus group analysis.

This module provides functions for aggregating and summarizing health insights
from focus group extractions, and comparing community voice data with
population health indicators.
"""

from __future__ import annotations

import collections
import dataclasses
from collections.abc import Sequence
from typing import Any

from langextract.core.data import AnnotatedDocument, Extraction
from langextract.tools.focus_group.types import (
    AlignmentStatus,
    AnalysisResult,
    BarrierSummary,
    CommunityHealthGap,
    Confidence,
    DataComparison,
    ExtractionType,
    HealthConcernSummary,
    HealthDomain,
    HealthIndicator,
    InsightCluster,
    ParticipantSummary,
    PopulationHealthData,
    SDOHCategory,
    Sentiment,
    Severity,
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

# Mapping of health topics to indicator keywords for comparison
TOPIC_INDICATOR_MAPPING = {
    "diabetes": ["diabetes", "a1c", "blood_sugar", "glucose"],
    "obesity": ["obesity", "bmi", "overweight"],
    "mental_health": ["mental", "depression", "anxiety", "suicide"],
    "substance_use": ["opioid", "drug", "alcohol", "substance", "overdose"],
    "heart_disease": ["heart", "cardiovascular", "hypertension", "blood_pressure"],
    "asthma": ["asthma", "respiratory"],
    "food_access": ["food", "nutrition", "hunger", "snap"],
    "housing": ["housing", "homeless", "lead"],
    "transportation": ["transportation", "transit"],
    "insurance": ["uninsured", "insurance", "coverage"],
    "prenatal": ["prenatal", "pregnancy", "birth", "maternal"],
    "infant": ["infant", "mortality", "low_birth_weight"],
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


def _get_severity(severity_str: str | None) -> Severity:
  """Convert severity string to Severity enum."""
  if not severity_str:
    return Severity.MODERATE
  severity_str = severity_str.lower()
  if severity_str == "critical":
    return Severity.CRITICAL
  elif severity_str == "high":
    return Severity.HIGH
  elif severity_str == "low":
    return Severity.LOW
  return Severity.MODERATE


def extract_themes(
    documents: Sequence[AnnotatedDocument],
) -> list[ThemeSummary]:
  """Extract and summarize health themes from annotated documents."""
  theme_data: dict[str, dict[str, Any]] = collections.defaultdict(
      lambda: {
          "count": 0,
          "sentiments": collections.Counter(),
          "quotes": [],
          "participants": set(),
          "health_domains": collections.Counter(),
          "sdoh_categories": collections.Counter(),
      }
  )

  for doc in documents:
    for extraction in doc.extractions or []:
      theme = None

      # Get theme from extraction
      if extraction.attributes:
        theme = (
            extraction.attributes.get("topic")
            or extraction.attributes.get("theme")
            or extraction.attributes.get("health_domain")
            or extraction.attributes.get("category")
        )

      if theme:
        theme = theme.lower().strip()
        theme_data[theme]["count"] += 1

        if extraction.attributes:
          # Track sentiment
          sentiment = extraction.attributes.get("sentiment", "neutral")
          theme_data[theme]["sentiments"][sentiment] += 1

          # Track participant
          participant = extraction.attributes.get("participant")
          if participant:
            theme_data[theme]["participants"].add(participant)

          # Track health domain
          health_domain = extraction.attributes.get("health_domain")
          if health_domain:
            theme_data[theme]["health_domains"][health_domain] += 1

          # Track SDOH category
          sdoh = extraction.attributes.get("sdoh_category")
          if sdoh:
            theme_data[theme]["sdoh_categories"][sdoh] += 1

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

    # Get most common health domain
    health_domain = None
    if data["health_domains"]:
      most_common = data["health_domains"].most_common(1)[0][0]
      try:
        health_domain = HealthDomain(most_common)
      except ValueError:
        pass

    # Get most common SDOH category
    sdoh_category = None
    if data["sdoh_categories"]:
      most_common = data["sdoh_categories"].most_common(1)[0][0]
      try:
        sdoh_category = SDOHCategory(most_common)
      except ValueError:
        pass

    summaries.append(
        ThemeSummary(
            theme_name=theme_name,
            frequency=data["count"],
            sentiment_distribution=sentiment_dist,
            sample_quotes=data["quotes"],
            participants_mentioned=data["participants"],
            health_domain=health_domain,
            sdoh_category=sdoh_category,
            avg_sentiment_score=avg_score,
        )
    )

  summaries.sort(key=lambda x: x.frequency, reverse=True)
  return summaries


def extract_health_concerns(
    documents: Sequence[AnnotatedDocument],
) -> list[HealthConcernSummary]:
  """Extract health concerns from annotated documents."""
  concern_data: dict[str, dict[str, Any]] = collections.defaultdict(
      lambda: {
          "count": 0,
          "severities": [],
          "affected_groups": set(),
          "quotes": [],
          "health_domains": collections.Counter(),
      }
  )

  concern_types = {
      ExtractionType.HEALTH_CONCERN.value,
      ExtractionType.HEALTH_CONDITION.value,
      ExtractionType.SYMPTOM.value,
  }

  for doc in documents:
    for extraction in doc.extractions or []:
      if extraction.extraction_class in concern_types:
        # Use the text or condition attribute as the concern key
        concern = extraction.extraction_text[:100].lower()
        if extraction.attributes:
          condition = extraction.attributes.get("condition")
          if condition:
            concern = condition.lower()

        concern_data[concern]["count"] += 1
        concern_data[concern]["quotes"].append(extraction.extraction_text)

        if extraction.attributes:
          severity = extraction.attributes.get("severity")
          if severity:
            concern_data[concern]["severities"].append(severity)

          affected = extraction.attributes.get("affected_population")
          if affected:
            concern_data[concern]["affected_groups"].add(affected)

          participant = extraction.attributes.get("participant")
          if participant:
            concern_data[concern]["affected_groups"].add(f"participant_{participant}")

          health_domain = extraction.attributes.get("health_domain")
          if health_domain:
            concern_data[concern]["health_domains"][health_domain] += 1

  # Convert to HealthConcernSummary
  summaries = []
  for concern, data in concern_data.items():
    # Determine overall severity
    if data["severities"]:
      severity_counts = collections.Counter(data["severities"])
      most_common = severity_counts.most_common(1)[0][0]
      severity = _get_severity(most_common)
    else:
      severity = Severity.MODERATE

    # Get most common health domain
    health_domain = None
    if data["health_domains"]:
      most_common = data["health_domains"].most_common(1)[0][0]
      try:
        health_domain = HealthDomain(most_common)
      except ValueError:
        pass

    summaries.append(
        HealthConcernSummary(
            concern=concern,
            frequency=data["count"],
            severity=severity,
            affected_groups=list(data["affected_groups"]),
            sample_quotes=data["quotes"][:5],
            health_domain=health_domain,
        )
    )

  summaries.sort(key=lambda x: x.frequency, reverse=True)
  return summaries


def extract_barriers(
    documents: Sequence[AnnotatedDocument],
) -> list[BarrierSummary]:
  """Extract barriers to care from annotated documents."""
  barrier_data: dict[str, dict[str, Any]] = collections.defaultdict(
      lambda: {
          "count": 0,
          "barrier_types": collections.Counter(),
          "affected_groups": set(),
          "quotes": [],
          "sdoh_categories": collections.Counter(),
      }
  )

  barrier_types = {
      ExtractionType.BARRIER_TO_CARE.value,
      ExtractionType.ACCESS_ISSUE.value,
      ExtractionType.RESOURCE_GAP.value,
      ExtractionType.TRANSPORTATION_ISSUE.value,
      ExtractionType.FOOD_ACCESS.value,
      ExtractionType.HOUSING_ISSUE.value,
      ExtractionType.ECONOMIC_FACTOR.value,
  }

  for doc in documents:
    for extraction in doc.extractions or []:
      if extraction.extraction_class in barrier_types:
        barrier = extraction.extraction_text[:100].lower()

        barrier_data[barrier]["count"] += 1
        barrier_data[barrier]["quotes"].append(extraction.extraction_text)

        if extraction.attributes:
          barrier_type = extraction.attributes.get("barrier_type")
          if barrier_type:
            barrier_data[barrier]["barrier_types"][barrier_type] += 1

          affected = extraction.attributes.get("affected_population")
          if affected:
            barrier_data[barrier]["affected_groups"].add(affected)

          sdoh = extraction.attributes.get("sdoh_category")
          if sdoh:
            barrier_data[barrier]["sdoh_categories"][sdoh] += 1

  # Convert to BarrierSummary
  summaries = []
  for barrier, data in barrier_data.items():
    # Determine barrier type
    if data["barrier_types"]:
      barrier_type = data["barrier_types"].most_common(1)[0][0]
    else:
      barrier_type = "unknown"

    # Get most common SDOH category
    sdoh_category = None
    if data["sdoh_categories"]:
      most_common = data["sdoh_categories"].most_common(1)[0][0]
      try:
        sdoh_category = SDOHCategory(most_common)
      except ValueError:
        pass

    summaries.append(
        BarrierSummary(
            barrier=barrier,
            frequency=data["count"],
            barrier_type=barrier_type,
            affected_groups=list(data["affected_groups"]),
            sample_quotes=data["quotes"][:5],
            sdoh_category=sdoh_category,
        )
    )

  summaries.sort(key=lambda x: x.frequency, reverse=True)
  return summaries


def extract_community_strengths(
    documents: Sequence[AnnotatedDocument],
) -> list[str]:
  """Extract community strengths and assets."""
  strengths = []

  strength_types = {
      ExtractionType.COMMUNITY_STRENGTH.value,
      ExtractionType.SOCIAL_SUPPORT.value,
  }

  for doc in documents:
    for extraction in doc.extractions or []:
      if extraction.extraction_class in strength_types:
        strengths.append(extraction.extraction_text)

  return strengths


def extract_priority_areas(
    documents: Sequence[AnnotatedDocument],
) -> list[str]:
  """Extract community-identified priority areas."""
  priorities = []

  priority_types = {
      ExtractionType.PRIORITY_AREA.value,
      ExtractionType.UNMET_NEED.value,
      ExtractionType.COMMUNITY_SUGGESTION.value,
  }

  for doc in documents:
    for extraction in doc.extractions or []:
      if extraction.extraction_class in priority_types:
        priorities.append(extraction.extraction_text)

  return priorities


def extract_participant_summaries(
    documents: Sequence[AnnotatedDocument],
) -> list[ParticipantSummary]:
  """Extract summaries for each participant."""
  participant_data: dict[str, dict[str, Any]] = collections.defaultdict(
      lambda: {
          "count": 0,
          "sentiments": collections.Counter(),
          "themes": set(),
          "quotes": [],
          "health_concerns": set(),
          "barriers": set(),
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
      topic = (
          extraction.attributes.get("topic")
          or extraction.attributes.get("theme")
          or extraction.attributes.get("health_domain")
      )
      if topic:
        participant_data[participant]["themes"].add(topic.lower())

      # Track health concerns
      if extraction.extraction_class in {
          ExtractionType.HEALTH_CONCERN.value,
          ExtractionType.HEALTH_CONDITION.value,
      }:
        participant_data[participant]["health_concerns"].add(
            extraction.extraction_text[:50]
        )

      # Track barriers
      if extraction.extraction_class in {
          ExtractionType.BARRIER_TO_CARE.value,
          ExtractionType.ACCESS_ISSUE.value,
      }:
        participant_data[participant]["barriers"].add(
            extraction.extraction_text[:50]
        )

      # Collect quotes
      if len(participant_data[participant]["quotes"]) < 5:
        participant_data[participant]["quotes"].append(
            extraction.extraction_text
        )

  # Convert to ParticipantSummary
  summaries = []
  for participant_id, data in participant_data.items():
    sentiment_dist = dict(data["sentiments"])
    sentiment_scores = [
        _get_sentiment_score(s) * count
        for s, count in sentiment_dist.items()
    ]
    total = sum(sentiment_dist.values())
    avg_score = sum(sentiment_scores) / total if total > 0 else None

    summaries.append(
        ParticipantSummary(
            participant_id=participant_id,
            total_contributions=data["count"],
            sentiment_distribution=sentiment_dist,
            themes_discussed=sorted(data["themes"]),
            key_quotes=data["quotes"],
            health_concerns_raised=list(data["health_concerns"]),
            barriers_mentioned=list(data["barriers"]),
            avg_sentiment_score=avg_score,
        )
    )

  summaries.sort(key=lambda x: x.total_contributions, reverse=True)
  return summaries


def cluster_insights(
    documents: Sequence[AnnotatedDocument],
    min_cluster_size: int = 2,
) -> list[InsightCluster]:
  """Cluster related health insights together."""
  theme_extractions: dict[str, list[Extraction]] = collections.defaultdict(list)

  for doc in documents:
    for extraction in doc.extractions or []:
      if not extraction.attributes:
        continue

      theme = (
          extraction.attributes.get("topic")
          or extraction.attributes.get("theme")
          or extraction.attributes.get("health_domain")
          or extraction.attributes.get("category")
      )

      if theme:
        theme_extractions[theme.lower()].append(extraction)

  clusters = []
  cluster_id = 0

  for theme, extractions in theme_extractions.items():
    if len(extractions) < min_cluster_size:
      continue

    cluster_id += 1

    sentiments = []
    participants = set()
    quotes = []
    health_domains = collections.Counter()
    sdoh_categories = collections.Counter()

    for extraction in extractions:
      if extraction.attributes:
        sentiment = extraction.attributes.get("sentiment")
        if sentiment:
          sentiments.append(sentiment)

        participant = extraction.attributes.get("participant")
        if participant:
          participants.add(participant)

        hd = extraction.attributes.get("health_domain")
        if hd:
          health_domains[hd] += 1

        sdoh = extraction.attributes.get("sdoh_category")
        if sdoh:
          sdoh_categories[sdoh] += 1

      quotes.append(extraction.extraction_text)

    # Determine sentiment
    sentiment_counts = collections.Counter(sentiments)
    if sentiment_counts:
      most_common = sentiment_counts.most_common(1)[0][0]
      try:
        cluster_sentiment = Sentiment(most_common)
      except ValueError:
        cluster_sentiment = Sentiment.NEUTRAL
    else:
      cluster_sentiment = Sentiment.NEUTRAL

    # Determine confidence
    if len(extractions) >= 5:
      confidence = Confidence.HIGH
    elif len(extractions) >= 3:
      confidence = Confidence.MEDIUM
    else:
      confidence = Confidence.LOW

    # Get health domain
    health_domain = None
    if health_domains:
      most_common = health_domains.most_common(1)[0][0]
      try:
        health_domain = HealthDomain(most_common)
      except ValueError:
        pass

    # Get SDOH category
    sdoh_category = None
    if sdoh_categories:
      most_common = sdoh_categories.most_common(1)[0][0]
      try:
        sdoh_category = SDOHCategory(most_common)
      except ValueError:
        pass

    clusters.append(
        InsightCluster(
            cluster_id=f"cluster_{cluster_id}",
            theme=theme,
            insights=extractions,
            sentiment=cluster_sentiment,
            confidence=confidence,
            supporting_quotes=quotes[:5],
            participant_count=len(participants),
            health_domain=health_domain,
            sdoh_category=sdoh_category,
        )
    )

  clusters.sort(key=lambda x: x.participant_count, reverse=True)
  return clusters


def calculate_overall_sentiment(
    documents: Sequence[AnnotatedDocument],
) -> Sentiment:
  """Calculate overall sentiment across all documents."""
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
  """Generate key findings from the analysis."""
  findings = []

  type_counts: dict[str, int] = collections.Counter()
  health_concerns = []
  barriers = []
  strengths = []

  for doc in documents:
    for extraction in doc.extractions or []:
      type_counts[extraction.extraction_class] += 1

      if extraction.extraction_class == ExtractionType.HEALTH_CONCERN.value:
        health_concerns.append(extraction.extraction_text)
      elif extraction.extraction_class == ExtractionType.BARRIER_TO_CARE.value:
        barriers.append(extraction.extraction_text)
      elif extraction.extraction_class == ExtractionType.COMMUNITY_STRENGTH.value:
        strengths.append(extraction.extraction_text)

  total = sum(type_counts.values())
  if total > 0:
    findings.append(
        f"Extracted {total} insights from community discussions"
    )

  if health_concerns:
    findings.append(
        f"Identified {len(health_concerns)} health concerns raised by community"
    )

  if barriers:
    findings.append(
        f"Found {len(barriers)} barriers to healthcare access"
    )

  if strengths:
    findings.append(
        f"Recognized {len(strengths)} community strengths and assets"
    )

  # Theme analysis
  themes = extract_themes(documents)
  if themes:
    top_themes = [t.theme_name for t in themes[:3]]
    findings.append(f"Top health themes: {', '.join(top_themes)}")

  # Participant analysis
  participants = extract_participant_summaries(documents)
  if participants:
    findings.append(
        f"Analyzed input from {len(participants)} participants"
    )

  return findings[:max_findings]


def create_health_analysis_result(
    annotated_documents: Sequence[AnnotatedDocument],
    metadata: dict[str, Any] | None = None,
) -> AnalysisResult:
  """Create a complete health-focused AnalysisResult."""
  return AnalysisResult(
      annotated_documents=annotated_documents,
      themes=extract_themes(annotated_documents),
      participant_summaries=extract_participant_summaries(annotated_documents),
      insight_clusters=cluster_insights(annotated_documents),
      overall_sentiment=calculate_overall_sentiment(annotated_documents),
      key_findings=generate_key_findings(annotated_documents),
      health_concerns=extract_health_concerns(annotated_documents),
      barriers=extract_barriers(annotated_documents),
      community_strengths=extract_community_strengths(annotated_documents),
      priority_areas=extract_priority_areas(annotated_documents),
      metadata=metadata,
  )


# Keep original function name for backwards compatibility
def create_analysis_result(
    annotated_documents: Sequence[AnnotatedDocument],
    metadata: dict[str, Any] | None = None,
) -> AnalysisResult:
  """Create a complete AnalysisResult from annotated documents."""
  return create_health_analysis_result(annotated_documents, metadata)


def _find_matching_indicator(
    topic: str,
    indicators: list[HealthIndicator],
) -> HealthIndicator | None:
  """Find a population health indicator matching a community topic."""
  topic_lower = topic.lower()

  # Check direct mapping
  for mapped_topic, keywords in TOPIC_INDICATOR_MAPPING.items():
    if any(kw in topic_lower for kw in keywords):
      for indicator in indicators:
        indicator_name = indicator.name.lower()
        if any(kw in indicator_name for kw in keywords):
          return indicator

  # Try direct name match
  for indicator in indicators:
    if topic_lower in indicator.name.lower():
      return indicator
    if indicator.indicator_id.lower() in topic_lower:
      return indicator

  return None


def compare_with_population_data(
    result: AnalysisResult,
    population_data: PopulationHealthData,
) -> AnalysisResult:
  """Compare analysis results with population health data.

  This function creates DataComparison objects showing how community voice
  data aligns (or doesn't) with population health indicators.

  Args:
    result: Analysis result from focus group analysis.
    population_data: Population health indicators for comparison.

  Returns:
    Updated AnalysisResult with data_comparisons populated.
  """
  comparisons = []
  gaps = []

  # Get all topics mentioned in community discussions
  community_topics: dict[str, dict[str, Any]] = collections.defaultdict(
      lambda: {"count": 0, "sentiment": [], "quotes": []}
  )

  for doc in result.annotated_documents:
    for extraction in doc.extractions or []:
      if extraction.attributes:
        topic = (
            extraction.attributes.get("topic")
            or extraction.attributes.get("health_domain")
            or extraction.attributes.get("condition")
        )
        if topic:
          topic = topic.lower()
          community_topics[topic]["count"] += 1
          sent = extraction.attributes.get("sentiment")
          if sent:
            community_topics[topic]["sentiment"].append(sent)
          community_topics[topic]["quotes"].append(extraction.extraction_text)

  # Compare each community topic with population data
  for topic, data in community_topics.items():
    indicator = _find_matching_indicator(topic, population_data.indicators)

    # Determine community sentiment
    if data["sentiment"]:
      sent_counts = collections.Counter(data["sentiment"])
      most_common = sent_counts.most_common(1)[0][0]
      try:
        community_sentiment = Sentiment(most_common)
      except ValueError:
        community_sentiment = Sentiment.NEUTRAL
    else:
      community_sentiment = Sentiment.NEUTRAL

    if indicator:
      # Determine alignment status
      if indicator.comparison_value:
        if indicator.value > indicator.comparison_value * 1.1:
          alignment = AlignmentStatus.ALIGNED  # Data confirms community concern
        elif indicator.value < indicator.comparison_value * 0.9:
          alignment = AlignmentStatus.DIVERGENT  # Data doesn't match concern
        else:
          alignment = AlignmentStatus.PARTIALLY_ALIGNED
      else:
        alignment = AlignmentStatus.PARTIALLY_ALIGNED

      comparison = DataComparison(
          topic=topic,
          community_frequency=data["count"],
          community_sentiment=community_sentiment,
          community_quotes=data["quotes"][:3],
          population_indicator=indicator,
          alignment_status=alignment,
          interpretation=_generate_interpretation(
              topic, data["count"], indicator, alignment
          ),
      )
      comparisons.append(comparison)
    else:
      # No matching indicator - this is a potential data gap
      comparison = DataComparison(
          topic=topic,
          community_frequency=data["count"],
          community_sentiment=community_sentiment,
          community_quotes=data["quotes"][:3],
          population_indicator=None,
          alignment_status=AlignmentStatus.DATA_GAP,
          interpretation=f"Community raised '{topic}' {data['count']} times, but no matching population data was found.",
      )
      comparisons.append(comparison)

      # Create gap entry if frequently mentioned
      if data["count"] >= 2:
        gap = CommunityHealthGap(
            gap_description=f"Community concern about {topic} not reflected in available data",
            evidence_from_community=data["quotes"][:3],
            frequency_mentioned=data["count"],
            affected_populations=[],  # Could be extracted from data
            severity=Severity.MODERATE if data["count"] < 5 else Severity.HIGH,
            gap_type="data_gap",
        )
        gaps.append(gap)

  # Sort comparisons by community frequency
  comparisons.sort(key=lambda x: x.community_frequency, reverse=True)

  # Update result with comparisons
  return dataclasses.replace(
      result,
      data_comparisons=comparisons,
      community_health_gaps=gaps,
  )


def _generate_interpretation(
    topic: str,
    frequency: int,
    indicator: HealthIndicator,
    alignment: AlignmentStatus,
) -> str:
  """Generate interpretation text for a data comparison."""
  if alignment == AlignmentStatus.ALIGNED:
    return (
        f"Community concerns about {topic} are supported by data: "
        f"{indicator.name} is {indicator.value}{indicator.unit} "
        f"(vs benchmark of {indicator.comparison_value})."
    )
  elif alignment == AlignmentStatus.DIVERGENT:
    return (
        f"Community raised {topic} {frequency} times, but data shows "
        f"{indicator.name} ({indicator.value}{indicator.unit}) is better "
        f"than benchmark. May indicate emerging concern or specific subpopulation issue."
    )
  else:
    return (
        f"Community mentioned {topic} {frequency} times. Related indicator: "
        f"{indicator.name} = {indicator.value}{indicator.unit}."
    )


def compare_multiple_sessions(
    results: Sequence[AnalysisResult],
) -> dict[str, Any]:
  """Compare findings across multiple focus group sessions."""
  comparison = {
      "session_count": len(results),
      "total_extractions": sum(r.total_extractions for r in results),
      "individual_results": results,
      "combined_themes": collections.Counter(),
      "common_concerns": collections.Counter(),
      "common_barriers": collections.Counter(),
      "sentiment_by_session": [],
  }

  for i, result in enumerate(results):
    # Track sentiment
    comparison["sentiment_by_session"].append({
        "session": i + 1,
        "sentiment": result.overall_sentiment.value,
        "session_id": result.metadata.get("session_id") if result.metadata else None,
    })

    # Track themes
    for theme in result.themes:
      comparison["combined_themes"][theme.theme_name] += theme.frequency

    # Track health concerns
    if result.health_concerns:
      for concern in result.health_concerns:
        comparison["common_concerns"][concern.concern] += concern.frequency

    # Track barriers
    if result.barriers:
      for barrier in result.barriers:
        comparison["common_barriers"][barrier.barrier] += barrier.frequency

  # Convert to sorted lists
  comparison["combined_themes"] = [
      {"theme": t, "count": c}
      for t, c in comparison["combined_themes"].most_common(15)
  ]
  comparison["common_concerns"] = [
      {"concern": c, "count": n}
      for c, n in comparison["common_concerns"].most_common(10)
  ]
  comparison["common_barriers"] = [
      {"barrier": b, "count": n}
      for b, n in comparison["common_barriers"].most_common(10)
  ]

  return comparison


def combine_session_results(
    results: Sequence[AnalysisResult],
) -> AnalysisResult:
  """Combine multiple session results into one."""
  all_docs = []
  for result in results:
    all_docs.extend(result.annotated_documents)

  return create_health_analysis_result(all_docs)


# Backwards compatibility aliases
compare_sessions = compare_multiple_sessions
