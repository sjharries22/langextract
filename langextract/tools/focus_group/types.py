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

"""Data types for population health focus group analysis.

This module provides data structures for analyzing community health discussions
and comparing community voice data with population health indicators.
"""

from __future__ import annotations

import dataclasses
import enum
from collections.abc import Sequence
from typing import Any

from langextract.core.data import AnnotatedDocument, Extraction


class ExtractionType(enum.Enum):
  """Extraction types for population health focus group analysis."""

  # Health concerns and conditions
  HEALTH_CONCERN = "health_concern"
  HEALTH_CONDITION = "health_condition"
  SYMPTOM = "symptom"

  # Access and barriers
  BARRIER_TO_CARE = "barrier_to_care"
  ACCESS_ISSUE = "access_issue"
  RESOURCE_GAP = "resource_gap"

  # Social determinants of health (SDOH)
  SDOH_FACTOR = "sdoh_factor"
  HOUSING_ISSUE = "housing_issue"
  FOOD_ACCESS = "food_access"
  TRANSPORTATION_ISSUE = "transportation_issue"
  ECONOMIC_FACTOR = "economic_factor"
  EDUCATION_FACTOR = "education_factor"
  EMPLOYMENT_FACTOR = "employment_factor"
  SAFETY_CONCERN = "safety_concern"
  ENVIRONMENTAL_FACTOR = "environmental_factor"

  # Health behaviors
  HEALTH_BEHAVIOR = "health_behavior"
  PREVENTION_PRACTICE = "prevention_practice"
  RISK_BEHAVIOR = "risk_behavior"

  # Healthcare experiences
  HEALTHCARE_EXPERIENCE = "healthcare_experience"
  PROVIDER_INTERACTION = "provider_interaction"
  CARE_QUALITY = "care_quality"
  TRUST_ISSUE = "trust_issue"

  # Community and social factors
  COMMUNITY_STRENGTH = "community_strength"
  SOCIAL_SUPPORT = "social_support"
  CULTURAL_FACTOR = "cultural_factor"

  # Needs and suggestions
  UNMET_NEED = "unmet_need"
  COMMUNITY_SUGGESTION = "community_suggestion"
  PRIORITY_AREA = "priority_area"

  # General
  QUOTE = "quote"
  INSIGHT = "insight"
  SENTIMENT = "sentiment"
  AGREEMENT = "agreement"
  DISAGREEMENT = "disagreement"


class HealthDomain(enum.Enum):
  """Health domains for categorizing health topics."""

  CHRONIC_DISEASE = "chronic_disease"
  MENTAL_HEALTH = "mental_health"
  MATERNAL_CHILD_HEALTH = "maternal_child_health"
  INFECTIOUS_DISEASE = "infectious_disease"
  SUBSTANCE_USE = "substance_use"
  ORAL_HEALTH = "oral_health"
  NUTRITION = "nutrition"
  PHYSICAL_ACTIVITY = "physical_activity"
  INJURY_PREVENTION = "injury_prevention"
  ENVIRONMENTAL_HEALTH = "environmental_health"
  SEXUAL_HEALTH = "sexual_health"
  AGING = "aging"
  DISABILITY = "disability"
  GENERAL_WELLNESS = "general_wellness"


class SDOHCategory(enum.Enum):
  """Social Determinants of Health categories (Healthy People 2030)."""

  ECONOMIC_STABILITY = "economic_stability"
  EDUCATION_ACCESS = "education_access"
  HEALTHCARE_ACCESS = "healthcare_access"
  NEIGHBORHOOD_ENVIRONMENT = "neighborhood_environment"
  SOCIAL_COMMUNITY = "social_community"


class Sentiment(enum.Enum):
  """Sentiment classification for health-related content."""

  VERY_POSITIVE = "very_positive"
  POSITIVE = "positive"
  NEUTRAL = "neutral"
  NEGATIVE = "negative"
  VERY_NEGATIVE = "very_negative"
  MIXED = "mixed"


class Confidence(enum.Enum):
  """Confidence levels for extracted insights."""

  HIGH = "high"
  MEDIUM = "medium"
  LOW = "low"


class Severity(enum.Enum):
  """Severity levels for health concerns."""

  CRITICAL = "critical"
  HIGH = "high"
  MODERATE = "moderate"
  LOW = "low"


class AlignmentStatus(enum.Enum):
  """Status of alignment between community voice and population data."""

  ALIGNED = "aligned"  # Community concerns match data
  PARTIALLY_ALIGNED = "partially_aligned"  # Some overlap
  DIVERGENT = "divergent"  # Community voice differs from data
  DATA_GAP = "data_gap"  # No population data available
  EMERGING = "emerging"  # Community identifies issue not yet in data


@dataclasses.dataclass
class ParticipantInfo:
  """Information about a focus group participant."""

  participant_id: str
  name: str | None = None
  demographics: dict[str, str] | None = None
  segment: str | None = None  # e.g., "seniors", "parents", "chronic_condition"
  zip_code: str | None = None
  community: str | None = None


@dataclasses.dataclass
class HealthIndicator:
  """A population health indicator with value and metadata."""

  indicator_id: str
  name: str
  value: float
  unit: str  # e.g., "percent", "per_100k", "rate"
  year: int | str
  source: str  # e.g., "CDC", "County Health Rankings", "BRFSS"
  geography: str  # e.g., "County", "State", "ZIP code"
  geography_name: str  # e.g., "Cook County", "Illinois"
  comparison_value: float | None = None  # State/national benchmark
  comparison_geography: str | None = None
  trend: str | None = None  # "improving", "worsening", "stable"
  confidence_interval: tuple[float, float] | None = None
  health_domain: HealthDomain | None = None
  sdoh_category: SDOHCategory | None = None
  notes: str | None = None


@dataclasses.dataclass
class PopulationHealthData:
  """Collection of population health indicators for a community."""

  geography: str
  geography_name: str
  indicators: list[HealthIndicator]
  data_year: str | None = None
  sources: list[str] | None = None

  def get_indicator(self, indicator_id: str) -> HealthIndicator | None:
    """Get indicator by ID."""
    for ind in self.indicators:
      if ind.indicator_id == indicator_id:
        return ind
    return None

  def get_indicators_by_domain(
      self, domain: HealthDomain
  ) -> list[HealthIndicator]:
    """Get all indicators for a health domain."""
    return [ind for ind in self.indicators if ind.health_domain == domain]

  def get_indicators_by_sdoh(
      self, category: SDOHCategory
  ) -> list[HealthIndicator]:
    """Get all indicators for an SDOH category."""
    return [ind for ind in self.indicators if ind.sdoh_category == category]


@dataclasses.dataclass
class ThemeSummary:
  """Summary of a health theme from focus group data."""

  theme_name: str
  frequency: int
  sentiment_distribution: dict[str, int]
  sample_quotes: list[str]
  participants_mentioned: set[str]
  health_domain: HealthDomain | None = None
  sdoh_category: SDOHCategory | None = None
  avg_sentiment_score: float | None = None
  related_indicators: list[str] | None = None  # Indicator IDs


@dataclasses.dataclass
class ParticipantSummary:
  """Summary of a participant's contributions."""

  participant_id: str
  total_contributions: int
  sentiment_distribution: dict[str, int]
  themes_discussed: list[str]
  key_quotes: list[str]
  health_concerns_raised: list[str] | None = None
  barriers_mentioned: list[str] | None = None
  avg_sentiment_score: float | None = None


@dataclasses.dataclass
class HealthConcernSummary:
  """Summary of a health concern raised in focus groups."""

  concern: str
  frequency: int
  severity: Severity
  affected_groups: list[str]  # Participant segments affected
  sample_quotes: list[str]
  health_domain: HealthDomain | None = None
  related_indicators: list[str] | None = None
  community_priority_score: float | None = None


@dataclasses.dataclass
class BarrierSummary:
  """Summary of a barrier to care or health."""

  barrier: str
  frequency: int
  barrier_type: str  # e.g., "financial", "geographic", "cultural", "systemic"
  affected_groups: list[str]
  sample_quotes: list[str]
  sdoh_category: SDOHCategory | None = None
  related_indicators: list[str] | None = None


@dataclasses.dataclass
class InsightCluster:
  """A cluster of related health insights."""

  cluster_id: str
  theme: str
  insights: list[Extraction]
  sentiment: Sentiment
  confidence: Confidence
  supporting_quotes: list[str]
  participant_count: int
  health_domain: HealthDomain | None = None
  sdoh_category: SDOHCategory | None = None


@dataclasses.dataclass
class DataComparison:
  """Comparison between community voice and population health data."""

  topic: str
  community_frequency: int
  community_sentiment: Sentiment
  community_quotes: list[str]
  population_indicator: HealthIndicator | None
  alignment_status: AlignmentStatus
  interpretation: str | None = None
  action_implications: list[str] | None = None


@dataclasses.dataclass
class CommunityHealthGap:
  """A gap between community needs and available resources/data."""

  gap_description: str
  evidence_from_community: list[str]  # Quotes
  frequency_mentioned: int
  affected_populations: list[str]
  severity: Severity
  gap_type: str  # "service_gap", "data_gap", "awareness_gap", "resource_gap"
  potential_actions: list[str] | None = None


@dataclasses.dataclass
class AnalysisResult:
  """Complete analysis result for population health focus group data."""

  annotated_documents: Sequence[AnnotatedDocument]
  themes: list[ThemeSummary]
  participant_summaries: list[ParticipantSummary]
  insight_clusters: list[InsightCluster]
  overall_sentiment: Sentiment
  key_findings: list[str]

  # Population health specific
  health_concerns: list[HealthConcernSummary] | None = None
  barriers: list[BarrierSummary] | None = None
  community_strengths: list[str] | None = None
  priority_areas: list[str] | None = None

  # Comparison with population data
  data_comparisons: list[DataComparison] | None = None
  community_health_gaps: list[CommunityHealthGap] | None = None

  metadata: dict[str, Any] | None = None

  @property
  def total_extractions(self) -> int:
    """Total number of extractions across all documents."""
    return sum(
        len(doc.extractions or []) for doc in self.annotated_documents
    )

  @property
  def extraction_type_counts(self) -> dict[str, int]:
    """Count of extractions by type."""
    counts: dict[str, int] = {}
    for doc in self.annotated_documents:
      for extraction in doc.extractions or []:
        counts[extraction.extraction_class] = (
            counts.get(extraction.extraction_class, 0) + 1
        )
    return counts

  def get_extractions_by_type(
      self, extraction_type: str | ExtractionType
  ) -> list[Extraction]:
    """Get all extractions of a specific type."""
    if isinstance(extraction_type, ExtractionType):
      extraction_type = extraction_type.value
    extractions = []
    for doc in self.annotated_documents:
      for extraction in doc.extractions or []:
        if extraction.extraction_class == extraction_type:
          extractions.append(extraction)
    return extractions

  def get_extractions_by_health_domain(
      self, domain: HealthDomain
  ) -> list[Extraction]:
    """Get all extractions related to a health domain."""
    extractions = []
    for doc in self.annotated_documents:
      for extraction in doc.extractions or []:
        if extraction.attributes:
          if extraction.attributes.get("health_domain") == domain.value:
            extractions.append(extraction)
    return extractions

  def get_extractions_by_sdoh(
      self, category: SDOHCategory
  ) -> list[Extraction]:
    """Get all extractions related to an SDOH category."""
    extractions = []
    for doc in self.annotated_documents:
      for extraction in doc.extractions or []:
        if extraction.attributes:
          if extraction.attributes.get("sdoh_category") == category.value:
            extractions.append(extraction)
    return extractions

  def get_extractions_by_participant(
      self, participant_id: str
  ) -> list[Extraction]:
    """Get all extractions from a specific participant."""
    extractions = []
    for doc in self.annotated_documents:
      for extraction in doc.extractions or []:
        if extraction.attributes:
          if extraction.attributes.get("participant") == participant_id:
            extractions.append(extraction)
    return extractions


@dataclasses.dataclass
class CommunityHealthSession:
  """Represents a community health focus group session."""

  session_id: str
  transcript: str
  community: str  # Community/neighborhood name
  topic: str | None = None  # Health topic focus
  date: str | None = None
  facilitator: str | None = None
  participants: list[ParticipantInfo] | None = None
  duration_minutes: int | None = None
  location: str | None = None
  geography: str | None = None  # County, ZIP, etc.
  target_population: str | None = None  # e.g., "seniors", "parents"
  notes: str | None = None

  def to_document(self) -> "Document":
    """Convert to a langextract Document."""
    from langextract.core.data import Document

    context_parts = []
    if self.community:
      context_parts.append(f"Community: {self.community}")
    if self.topic:
      context_parts.append(f"Health Topic: {self.topic}")
    if self.target_population:
      context_parts.append(f"Population: {self.target_population}")
    if self.geography:
      context_parts.append(f"Geography: {self.geography}")
    if self.date:
      context_parts.append(f"Date: {self.date}")
    if self.participants:
      context_parts.append(
          f"Participants: {len(self.participants)} community members"
      )
    if self.notes:
      context_parts.append(f"Notes: {self.notes}")

    additional_context = "; ".join(context_parts) if context_parts else None

    return Document(
        text=self.transcript,
        document_id=self.session_id,
        additional_context=additional_context,
    )


@dataclasses.dataclass
class KeyInformantInterview:
  """Represents a key informant interview for community health assessment."""

  session_id: str
  transcript: str
  interviewee: ParticipantInfo | None = None
  interviewee_role: str | None = None  # e.g., "clinic director", "community leader"
  organization: str | None = None
  interviewer: str | None = None
  topic: str | None = None
  community: str | None = None
  date: str | None = None
  duration_minutes: int | None = None
  notes: str | None = None

  def to_document(self) -> "Document":
    """Convert to a langextract Document."""
    from langextract.core.data import Document

    context_parts = []
    if self.community:
      context_parts.append(f"Community: {self.community}")
    if self.topic:
      context_parts.append(f"Topic: {self.topic}")
    if self.interviewee_role:
      context_parts.append(f"Interviewee Role: {self.interviewee_role}")
    if self.organization:
      context_parts.append(f"Organization: {self.organization}")
    if self.date:
      context_parts.append(f"Date: {self.date}")
    if self.notes:
      context_parts.append(f"Notes: {self.notes}")

    additional_context = "; ".join(context_parts) if context_parts else None

    return Document(
        text=self.transcript,
        document_id=self.session_id,
        additional_context=additional_context,
    )


# Backwards compatibility aliases
FocusGroupSession = CommunityHealthSession
InterviewSession = KeyInformantInterview
