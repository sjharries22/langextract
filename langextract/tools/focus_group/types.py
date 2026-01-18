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

"""Data types for focus group and interview analysis."""

from __future__ import annotations

import dataclasses
import enum
from collections.abc import Sequence
from typing import Any

from langextract.core.data import AnnotatedDocument, Extraction


class ExtractionType(enum.Enum):
  """Standard extraction types for focus group analysis."""

  SENTIMENT = "sentiment"
  THEME = "theme"
  PAIN_POINT = "pain_point"
  FEATURE_REQUEST = "feature_request"
  QUOTE = "quote"
  INSIGHT = "insight"
  QUESTION = "question"
  AGREEMENT = "agreement"
  DISAGREEMENT = "disagreement"
  SUGGESTION = "suggestion"
  EXPERIENCE = "experience"
  EXPECTATION = "expectation"
  COMPARISON = "comparison"
  EMOTION = "emotion"


class Sentiment(enum.Enum):
  """Sentiment classification for extracted content."""

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


@dataclasses.dataclass
class ParticipantInfo:
  """Information about a focus group participant."""

  participant_id: str
  name: str | None = None
  demographics: dict[str, str] | None = None
  segment: str | None = None


@dataclasses.dataclass
class ThemeSummary:
  """Summary of a theme extracted from focus group data."""

  theme_name: str
  frequency: int
  sentiment_distribution: dict[str, int]
  sample_quotes: list[str]
  participants_mentioned: set[str]
  avg_sentiment_score: float | None = None


@dataclasses.dataclass
class ParticipantSummary:
  """Summary of a participant's contributions."""

  participant_id: str
  total_contributions: int
  sentiment_distribution: dict[str, int]
  themes_discussed: list[str]
  key_quotes: list[str]
  avg_sentiment_score: float | None = None


@dataclasses.dataclass
class InsightCluster:
  """A cluster of related insights."""

  cluster_id: str
  theme: str
  insights: list[Extraction]
  sentiment: Sentiment
  confidence: Confidence
  supporting_quotes: list[str]
  participant_count: int


@dataclasses.dataclass
class AnalysisResult:
  """Complete analysis result for focus group data."""

  annotated_documents: Sequence[AnnotatedDocument]
  themes: list[ThemeSummary]
  participant_summaries: list[ParticipantSummary]
  insight_clusters: list[InsightCluster]
  overall_sentiment: Sentiment
  key_findings: list[str]
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
class FocusGroupSession:
  """Represents a focus group session with metadata."""

  session_id: str
  transcript: str
  topic: str | None = None
  date: str | None = None
  moderator: str | None = None
  participants: list[ParticipantInfo] | None = None
  duration_minutes: int | None = None
  location: str | None = None
  notes: str | None = None

  def to_document(self) -> "Document":
    """Convert to a langextract Document."""
    from langextract.core.data import Document

    context_parts = []
    if self.topic:
      context_parts.append(f"Topic: {self.topic}")
    if self.date:
      context_parts.append(f"Date: {self.date}")
    if self.moderator:
      context_parts.append(f"Moderator: {self.moderator}")
    if self.participants:
      context_parts.append(
          f"Participants: {len(self.participants)} participants"
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
class InterviewSession:
  """Represents an interview session with metadata."""

  session_id: str
  transcript: str
  interviewee: ParticipantInfo | None = None
  interviewer: str | None = None
  topic: str | None = None
  date: str | None = None
  duration_minutes: int | None = None
  interview_type: str | None = None  # e.g., "structured", "semi-structured"
  notes: str | None = None

  def to_document(self) -> "Document":
    """Convert to a langextract Document."""
    from langextract.core.data import Document

    context_parts = []
    if self.topic:
      context_parts.append(f"Topic: {self.topic}")
    if self.interviewee:
      context_parts.append(f"Interviewee: {self.interviewee.participant_id}")
    if self.interviewer:
      context_parts.append(f"Interviewer: {self.interviewer}")
    if self.date:
      context_parts.append(f"Date: {self.date}")
    if self.interview_type:
      context_parts.append(f"Type: {self.interview_type}")
    if self.notes:
      context_parts.append(f"Notes: {self.notes}")

    additional_context = "; ".join(context_parts) if context_parts else None

    return Document(
        text=self.transcript,
        document_id=self.session_id,
        additional_context=additional_context,
    )
