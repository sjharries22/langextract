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

"""Main analyzer for population health focus group analysis.

This module provides tools for analyzing community health focus groups and
interviews, extracting health concerns, barriers to care, social determinants
of health, and comparing community voice data with population health indicators.
"""

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
    CommunityHealthSession,
    KeyInformantInterview,
    PopulationHealthData,
)


# Default prompts for different health analysis types
DEFAULT_PROMPTS = {
    "comprehensive": """Extract health insights from community focus group transcripts.
For each insight, identify:
- Health concerns and conditions mentioned
- Barriers to healthcare access (cost, transportation, language, trust, etc.)
- Social determinants of health factors (housing, food access, employment, safety)
- Healthcare experiences (positive and negative)
- Community strengths and assets
- Unmet needs and suggestions for improvement

For each extraction, identify the participant, the health domain (chronic_disease,
mental_health, maternal_child_health, etc.), relevant SDOH category (economic_stability,
healthcare_access, neighborhood_environment, social_community, education_access),
and the severity or priority level.

Preserve exact quotes that capture community voice.""",

    "sdoh": """Extract social determinants of health from community discussions.
Focus on the five SDOH domains from Healthy People 2030:
1. Economic Stability: employment, income, expenses, debt, food security
2. Education Access and Quality: literacy, language, education level, vocational training
3. Healthcare Access and Quality: health coverage, provider availability, care quality
4. Neighborhood and Built Environment: housing, transportation, safety, walkability, parks
5. Social and Community Context: social support, discrimination, community engagement

For each factor mentioned, identify:
- The SDOH category
- How it affects health
- Who is most affected
- Suggested solutions or community assets""",

    "healthcare_access": """Analyze healthcare access and utilization patterns from focus groups.
Extract:
- Barriers to accessing care (cost, availability, location, transportation, language)
- Trust issues with healthcare system or providers
- Experiences with discrimination or dismissive care
- Insurance and coverage challenges
- Provider availability and wait times
- Cultural and linguistic barriers
- Positive healthcare experiences

Note patterns in who experiences these barriers and what populations are most affected.""",

    "maternal_child": """Extract maternal and child health insights from community discussions.
Focus on:
- Prenatal care access and experiences
- Delivery and birthing experiences
- Postpartum support and mental health
- Breastfeeding support
- Childcare and early childhood development
- Pediatric care access
- School health services
- Immunization and well-child visits
- Family planning access

Identify barriers, gaps in services, and community strengths.""",

    "community_strengths": """Identify community assets and strengths from focus group discussions.
Extract:
- Social support networks and community cohesion
- Faith-based organizations providing health services
- Community health workers and promotoras
- Local organizations serving health needs
- Cultural practices that support health
- Successful community programs
- Trusted community leaders and institutions
- Existing resources that could be leveraged

Focus on what's working well and could be expanded.""",

    "chronic_disease": """Extract insights about chronic disease management from community discussions.
Focus on:
- Conditions mentioned (diabetes, heart disease, hypertension, asthma, etc.)
- Disease management challenges
- Medication access and adherence barriers
- Education and knowledge gaps
- Self-management practices
- Provider interactions for chronic care
- Cost of supplies and medications
- Support needs and gaps

Identify what helps and hinders chronic disease management.""",

    "mental_health": """Extract mental health and substance use insights from community discussions.
Focus on:
- Mental health conditions discussed (depression, anxiety, trauma, etc.)
- Substance use issues (alcohol, opioids, other substances)
- Stigma around mental health and seeking help
- Access to mental health services
- Crisis and suicide prevention
- Counseling and therapy availability
- Support groups and peer support
- Impact on families and communities

Note barriers to care and community suggestions for improvement.""",
}


@dataclasses.dataclass
class AnalyzerConfig:
  """Configuration for the population health focus group analyzer.

  Attributes:
    model_id: The language model to use for extraction.
    analysis_type: Type of health analysis to perform.
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


class CommunityHealthAnalyzer:
  """Analyzer for community health focus groups and interviews.

  This class provides a high-level interface for extracting health insights
  from community focus group transcripts and key informant interviews,
  with the ability to compare findings with population health data.

  Example usage:
    ```python
    from langextract.tools.focus_group import CommunityHealthAnalyzer

    analyzer = CommunityHealthAnalyzer()
    result = analyzer.analyze("path/to/transcript.txt")

    # Access health insights
    for concern in result.health_concerns:
        print(f"{concern.concern}: {concern.frequency} mentions")

    for barrier in result.barriers:
        print(f"{barrier.barrier}: {barrier.barrier_type}")

    # Compare with population data
    result_with_comparison = analyzer.analyze_with_data(
        transcript,
        population_data=county_health_data
    )
    for comparison in result_with_comparison.data_comparisons:
        print(f"{comparison.topic}: {comparison.alignment_status}")
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
      AnalysisResult containing extracted health insights and summaries.
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

    # Create analysis result with health-specific aggregations
    return aggregation.create_health_analysis_result(
        annotated_documents=annotated_docs,
        metadata=metadata,
    )

  def analyze_with_data(
      self,
      transcript: str | Document | Sequence[Document],
      population_data: PopulationHealthData,
      metadata: dict[str, Any] | None = None,
  ) -> AnalysisResult:
    """Analyze transcript and compare with population health data.

    Args:
      transcript: A transcript string, Document, or sequence of Documents.
      population_data: Population health indicators for comparison.
      metadata: Optional metadata to include in the result.

    Returns:
      AnalysisResult with data comparisons showing alignment between
      community voice and population health data.
    """
    # First do standard analysis
    result = self.analyze(transcript, metadata)

    # Then compare with population data
    result = aggregation.compare_with_population_data(result, population_data)

    return result

  def analyze_session(
      self,
      session: CommunityHealthSession | KeyInformantInterview,
  ) -> AnalysisResult:
    """Analyze a community health session.

    Args:
      session: A CommunityHealthSession or KeyInformantInterview object.

    Returns:
      AnalysisResult containing extracted health insights.
    """
    document = session.to_document()

    # Build metadata from session
    metadata: dict[str, Any] = {"session_id": session.session_id}
    if isinstance(session, CommunityHealthSession):
      metadata["type"] = "community_focus_group"
      if session.community:
        metadata["community"] = session.community
      if session.topic:
        metadata["topic"] = session.topic
      if session.target_population:
        metadata["target_population"] = session.target_population
      if session.participants:
        metadata["participant_count"] = len(session.participants)
    else:
      metadata["type"] = "key_informant_interview"
      if session.community:
        metadata["community"] = session.community
      if session.interviewee_role:
        metadata["interviewee_role"] = session.interviewee_role
      if session.organization:
        metadata["organization"] = session.organization

    return self.analyze(document, metadata=metadata)

  def analyze_sessions(
      self,
      sessions: Iterable[CommunityHealthSession | KeyInformantInterview],
  ) -> list[AnalysisResult]:
    """Analyze multiple sessions.

    Args:
      sessions: Iterable of session objects.

    Returns:
      List of AnalysisResult objects, one per session.
    """
    return [self.analyze_session(session) for session in sessions]

  def analyze_multiple_groups(
      self,
      sessions: Iterable[CommunityHealthSession | KeyInformantInterview],
      population_data: PopulationHealthData | None = None,
  ) -> dict[str, Any]:
    """Analyze and compare multiple focus groups.

    This is useful for comparing what different community groups say
    and identifying common themes across groups.

    Args:
      sessions: Iterable of session objects to analyze.
      population_data: Optional population health data for comparison.

    Returns:
      Dictionary containing:
        - individual_results: Results for each session
        - combined_themes: Themes across all sessions
        - common_concerns: Health concerns mentioned in multiple groups
        - common_barriers: Barriers mentioned in multiple groups
        - data_comparisons: Comparison with population data (if provided)
    """
    results = self.analyze_sessions(sessions)

    comparison = aggregation.compare_multiple_sessions(results)

    if population_data:
      # Create combined result for comparison
      combined = aggregation.combine_session_results(results)
      combined = aggregation.compare_with_population_data(
          combined, population_data
      )
      comparison["data_comparisons"] = combined.data_comparisons
      comparison["community_health_gaps"] = combined.community_health_gaps

    return comparison

  def analyze_batch(
      self,
      transcripts: Iterable[str],
      document_ids: Iterable[str] | None = None,
      communities: Iterable[str] | None = None,
  ) -> AnalysisResult:
    """Analyze multiple transcripts as a batch.

    All transcripts are analyzed together, producing a single combined result.

    Args:
      transcripts: Iterable of transcript strings.
      document_ids: Optional document IDs for each transcript.
      communities: Optional community names for each transcript.

    Returns:
      Combined AnalysisResult for all transcripts.
    """
    transcripts_list = list(transcripts)
    ids_list = list(document_ids) if document_ids else [
        f"session_{i}" for i in range(len(transcripts_list))
    ]
    communities_list = list(communities) if communities else [None] * len(
        transcripts_list
    )

    documents = [
        Document(
            text=text,
            document_id=doc_id,
            additional_context=(
                f"Community: {community}; {self.config.additional_context or ''}"
                if community
                else self.config.additional_context
            ),
        )
        for text, doc_id, community in zip(
            transcripts_list, ids_list, communities_list
        )
    ]

    return self.analyze(documents)


# Backwards compatibility alias
FocusGroupAnalyzer = CommunityHealthAnalyzer


def analyze(
    transcript: str | Document | Sequence[Document],
    analysis_type: str = "comprehensive",
    model_id: str = "gemini-2.5-flash",
    **kwargs: Any,
) -> AnalysisResult:
  """Convenience function for quick community health analysis.

  Args:
    transcript: Transcript text, Document, or sequence of Documents.
    analysis_type: Type of analysis (comprehensive, sdoh, healthcare_access,
      maternal_child, community_strengths, chronic_disease, mental_health).
    model_id: Language model to use.
    **kwargs: Additional configuration options.

  Returns:
    AnalysisResult containing extracted health insights.

  Example:
    ```python
    from langextract.tools.focus_group import analyze

    result = analyze(
        transcript_text,
        analysis_type="comprehensive"
    )
    print(result.overall_sentiment)
    for concern in result.health_concerns:
        print(f"{concern.concern}: {concern.severity}")
    ```
  """
  config = AnalyzerConfig(
      model_id=model_id,
      analysis_type=analysis_type,
      **kwargs,
  )
  analyzer = CommunityHealthAnalyzer(config)
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
    AnalysisResult containing extracted health insights.
  """
  with open(file_path, "r", encoding=encoding) as f:
    transcript = f.read()

  return analyze(
      transcript,
      analysis_type=analysis_type,
      model_id=model_id,
      **kwargs,
  )


def analyze_with_population_data(
    transcript: str | Document | Sequence[Document],
    population_data: PopulationHealthData,
    analysis_type: str = "comprehensive",
    model_id: str = "gemini-2.5-flash",
    **kwargs: Any,
) -> AnalysisResult:
  """Analyze transcript and compare with population health data.

  This function analyzes focus group transcripts and compares the community
  voice data with population health indicators to identify:
  - Where community concerns align with population data
  - Where community concerns diverge from data (potential emerging issues)
  - Data gaps where community voices reveal issues not captured in data

  Args:
    transcript: Transcript text, Document, or sequence of Documents.
    population_data: Population health indicators for the community.
    analysis_type: Type of analysis to perform.
    model_id: Language model to use.
    **kwargs: Additional configuration options.

  Returns:
    AnalysisResult with data_comparisons showing alignment analysis.
  """
  config = AnalyzerConfig(
      model_id=model_id,
      analysis_type=analysis_type,
      **kwargs,
  )
  analyzer = CommunityHealthAnalyzer(config)
  return analyzer.analyze_with_data(transcript, population_data)
