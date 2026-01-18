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

"""Main analyzer for focus group and interview analysis."""

from __future__ import annotations

import dataclasses
from collections.abc import Iterable, Sequence
from typing import Any

from langextract import extraction as lx_extraction
from langextract.core.data import (
    AnnotatedDocument,
    Document,
    ExampleData,
)
from langextract.tools.focus_group import aggregation
from langextract.tools.focus_group import examples as preset_examples
from langextract.tools.focus_group.types import (
    AnalysisResult,
    FocusGroupSession,
    InterviewSession,
)


# Default prompts for different analysis types
DEFAULT_PROMPTS = {
    "comprehensive": """Extract insights from focus group or interview transcripts.
For each insight, identify:
- The type (sentiment, theme, pain_point, feature_request, quote, insight,
  question, agreement, disagreement, suggestion, experience, expectation,
  comparison, emotion)
- The participant who expressed it
- Relevant attributes like sentiment polarity, topic, severity, or priority

Focus on capturing actionable insights that reveal participant attitudes,
needs, and experiences. Preserve the exact wording of important quotes.""",
    "sentiment": """Analyze sentiment in focus group or interview transcripts.
Extract every sentiment expression, identifying:
- The participant expressing the sentiment
- The sentiment polarity (very_positive, positive, neutral, negative, very_negative)
- The topic or feature being discussed
- The intensity of the sentiment (strong, moderate, weak)

Also extract emotions like frustration, excitement, confusion, or satisfaction.""",
    "themes": """Extract themes and topics from focus group or interview transcripts.
Identify:
- Main themes discussed by participants
- Expectations and requirements
- Agreements and shared perspectives among participants
- The importance or priority of each theme

Group related concepts together and note which participants discuss each theme.""",
    "pain_points": """Extract pain points and feature requests from transcripts.
For each pain point, identify:
- The participant experiencing it
- The category (performance, usability, cost, support, etc.)
- The severity (critical, high, medium, low)

For feature requests, capture:
- What is being requested
- The priority and potential impact
- Any context about why it's needed""",
    "user_experience": """Map user journeys and experiences from transcripts.
Extract:
- Journey stages (awareness, consideration, purchase, onboarding, usage)
- Positive and negative experiences at each stage
- Friction points and delighters
- Recommendations and word-of-mouth mentions

Track the emotional arc of the participant's experience.""",
    "competitive": """Extract competitive insights from transcripts.
Identify:
- Competitors mentioned
- Comparative strengths and weaknesses
- Switching triggers and barriers
- Feature comparisons
- Market positioning insights""",
}


@dataclasses.dataclass
class AnalyzerConfig:
  """Configuration for the focus group analyzer.

  Attributes:
    model_id: The language model to use for extraction.
    analysis_type: Type of analysis to perform.
    custom_prompt: Optional custom prompt override.
    custom_examples: Optional custom examples override.
    extraction_passes: Number of extraction passes for thoroughness.
    max_workers: Maximum parallel workers for processing.
    max_char_buffer: Maximum characters per chunk.
    context_window_chars: Context window for coreference resolution.
    use_schema_constraints: Whether to use schema constraints.
    additional_context: Additional context to include in prompts.
  """

  model_id: str = "gemini-2.5-flash"
  analysis_type: str = "comprehensive"
  custom_prompt: str | None = None
  custom_examples: list[ExampleData] | None = None
  extraction_passes: int = 2
  max_workers: int = 10
  max_char_buffer: int = 2000
  context_window_chars: int = 500
  use_schema_constraints: bool = True
  additional_context: str | None = None


class FocusGroupAnalyzer:
  """Analyzer for focus groups and interviews.

  This class provides a high-level interface for extracting insights from
  focus group transcripts and interview recordings.

  Example usage:
    ```python
    from langextract.tools.focus_group import FocusGroupAnalyzer

    analyzer = FocusGroupAnalyzer()
    result = analyzer.analyze("path/to/transcript.txt")

    # Or analyze multiple sessions
    results = analyzer.analyze_sessions([session1, session2])

    # Access insights
    for theme in result.themes:
        print(f"{theme.theme_name}: {theme.frequency} mentions")
    ```
  """

  def __init__(self, config: AnalyzerConfig | None = None):
    """Initialize the analyzer.

    Args:
      config: Optional configuration. Uses defaults if not provided.
    """
    self.config = config or AnalyzerConfig()
    self._prompt = self._get_prompt()
    self._examples = self._get_examples()

  def _get_prompt(self) -> str:
    """Get the prompt for analysis."""
    if self.config.custom_prompt:
      return self.config.custom_prompt
    return DEFAULT_PROMPTS.get(
        self.config.analysis_type, DEFAULT_PROMPTS["comprehensive"]
    )

  def _get_examples(self) -> list[ExampleData]:
    """Get the examples for analysis."""
    if self.config.custom_examples:
      return self.config.custom_examples
    return preset_examples.get_examples(self.config.analysis_type)

  def analyze(
      self,
      transcript: str | Document | Sequence[Document],
      metadata: dict[str, Any] | None = None,
  ) -> AnalysisResult:
    """Analyze a transcript or set of documents.

    Args:
      transcript: A transcript string, Document, or sequence of Documents.
      metadata: Optional metadata to include in the result.

    Returns:
      AnalysisResult containing extracted insights and summaries.
    """
    # Convert string to Document if needed
    if isinstance(transcript, str):
      documents = [
          Document(
              text=transcript,
              additional_context=self.config.additional_context,
          )
      ]
    elif isinstance(transcript, Document):
      documents = [transcript]
    else:
      documents = list(transcript)

    # Run extraction
    annotated_docs = lx_extraction.extract(
        text_or_documents=documents,
        prompt_description=self._prompt,
        examples=self._examples,
        model_id=self.config.model_id,
        extraction_passes=self.config.extraction_passes,
        max_workers=self.config.max_workers,
        max_char_buffer=self.config.max_char_buffer,
        context_window_chars=self.config.context_window_chars,
        use_schema_constraints=self.config.use_schema_constraints,
    )

    # Ensure we have a list
    if isinstance(annotated_docs, AnnotatedDocument):
      annotated_docs = [annotated_docs]
    else:
      annotated_docs = list(annotated_docs)

    # Create analysis result with aggregations
    return aggregation.create_analysis_result(
        annotated_documents=annotated_docs,
        metadata=metadata,
    )

  def analyze_session(
      self,
      session: FocusGroupSession | InterviewSession,
  ) -> AnalysisResult:
    """Analyze a focus group or interview session.

    Args:
      session: A FocusGroupSession or InterviewSession object.

    Returns:
      AnalysisResult containing extracted insights and summaries.
    """
    document = session.to_document()

    # Build metadata from session
    metadata: dict[str, Any] = {"session_id": session.session_id}
    if isinstance(session, FocusGroupSession):
      metadata["type"] = "focus_group"
      if session.topic:
        metadata["topic"] = session.topic
      if session.date:
        metadata["date"] = session.date
      if session.participants:
        metadata["participant_count"] = len(session.participants)
    else:
      metadata["type"] = "interview"
      if session.topic:
        metadata["topic"] = session.topic
      if session.interviewee:
        metadata["interviewee"] = session.interviewee.participant_id

    return self.analyze(document, metadata=metadata)

  def analyze_sessions(
      self,
      sessions: Iterable[FocusGroupSession | InterviewSession],
  ) -> list[AnalysisResult]:
    """Analyze multiple sessions.

    Args:
      sessions: Iterable of session objects.

    Returns:
      List of AnalysisResult objects, one per session.
    """
    return [self.analyze_session(session) for session in sessions]

  def analyze_batch(
      self,
      transcripts: Iterable[str],
      document_ids: Iterable[str] | None = None,
  ) -> AnalysisResult:
    """Analyze multiple transcripts as a batch.

    All transcripts are analyzed together, producing a single combined result.

    Args:
      transcripts: Iterable of transcript strings.
      document_ids: Optional document IDs for each transcript.

    Returns:
      Combined AnalysisResult for all transcripts.
    """
    transcripts_list = list(transcripts)
    ids_list = list(document_ids) if document_ids else [
        f"doc_{i}" for i in range(len(transcripts_list))
    ]

    documents = [
        Document(
            text=text,
            document_id=doc_id,
            additional_context=self.config.additional_context,
        )
        for text, doc_id in zip(transcripts_list, ids_list)
    ]

    return self.analyze(documents)

  def compare_sessions(
      self,
      sessions: Iterable[FocusGroupSession | InterviewSession],
  ) -> dict[str, Any]:
    """Analyze and compare multiple sessions.

    Args:
      sessions: Iterable of session objects to compare.

    Returns:
      Dictionary containing comparison metrics and insights.
    """
    results = self.analyze_sessions(sessions)
    return aggregation.compare_sessions(results)


def analyze(
    transcript: str | Document | Sequence[Document],
    analysis_type: str = "comprehensive",
    model_id: str = "gemini-2.5-flash",
    **kwargs: Any,
) -> AnalysisResult:
  """Convenience function for quick analysis.

  Args:
    transcript: Transcript text, Document, or sequence of Documents.
    analysis_type: Type of analysis (comprehensive, sentiment, themes,
      pain_points, user_experience, competitive).
    model_id: Language model to use.
    **kwargs: Additional configuration options.

  Returns:
    AnalysisResult containing extracted insights.

  Example:
    ```python
    from langextract.tools.focus_group import analyze

    result = analyze(
        "P1: I love the new feature! P2: Me too, it's amazing.",
        analysis_type="sentiment"
    )
    print(result.overall_sentiment)
    ```
  """
  config = AnalyzerConfig(
      model_id=model_id,
      analysis_type=analysis_type,
      **kwargs,
  )
  analyzer = FocusGroupAnalyzer(config)
  return analyzer.analyze(transcript)


def analyze_file(
    file_path: str,
    analysis_type: str = "comprehensive",
    model_id: str = "gemini-2.5-flash",
    encoding: str = "utf-8",
    **kwargs: Any,
) -> AnalysisResult:
  """Analyze a transcript from a file.

  Args:
    file_path: Path to the transcript file.
    analysis_type: Type of analysis to perform.
    model_id: Language model to use.
    encoding: File encoding.
    **kwargs: Additional configuration options.

  Returns:
    AnalysisResult containing extracted insights.
  """
  with open(file_path, "r", encoding=encoding) as f:
    transcript = f.read()

  return analyze(
      transcript,
      analysis_type=analysis_type,
      model_id=model_id,
      **kwargs,
  )
