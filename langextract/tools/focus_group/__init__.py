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

"""Population Health Focus Group Analysis Tool.

This module provides tools for extracting, analyzing, and visualizing health
insights from community focus group transcripts and key informant interviews.
It enables comparison of community voice data with population health indicators
to identify alignment, gaps, and emerging health concerns.

Example usage:

    ```python
    from langextract.tools import focus_group

    # Quick analysis of a transcript
    result = focus_group.analyze(
        transcript_text,
        analysis_type="comprehensive"
    )

    # Access health insights
    for concern in result.health_concerns:
        print(f"{concern.concern}: {concern.severity}")

    for barrier in result.barriers:
        print(f"{barrier.barrier}: {barrier.barrier_type}")

    # Compare with population health data
    population_data = focus_group.PopulationHealthData(
        geography="County",
        geography_name="Example County",
        indicators=[
            focus_group.HealthIndicator(
                indicator_id="diabetes_prevalence",
                name="Diabetes Prevalence",
                value=12.5,
                unit="%",
                year=2023,
                source="CDC",
                geography="County",
                geography_name="Example County",
                comparison_value=10.0,
                health_domain=focus_group.HealthDomain.CHRONIC_DISEASE,
            ),
        ]
    )

    result = focus_group.analyze_with_population_data(
        transcript_text,
        population_data=population_data
    )

    for comparison in result.data_comparisons:
        print(f"{comparison.topic}: {comparison.alignment_status}")

    # Generate visualization
    focus_group.save_dashboard(result, "community_health_analysis.html")
    ```

Available analysis types:
    - comprehensive: Full health assessment analysis
    - sdoh: Social determinants of health focus
    - healthcare_access: Healthcare access and trust issues
    - maternal_child: Maternal and child health focus
    - community_strengths: Community assets and strengths
    - chronic_disease: Chronic disease management
    - mental_health: Mental health and substance use
"""

from langextract.tools.focus_group.aggregation import (
    calculate_overall_sentiment,
    cluster_insights,
    combine_session_results,
    compare_multiple_sessions,
    compare_sessions,
    compare_with_population_data,
    create_analysis_result,
    create_health_analysis_result,
    extract_barriers,
    extract_community_strengths,
    extract_health_concerns,
    extract_participant_summaries,
    extract_priority_areas,
    extract_themes,
    generate_key_findings,
)
from langextract.tools.focus_group.analyzer import (
    AnalyzerConfig,
    CommunityHealthAnalyzer,
    FocusGroupAnalyzer,
    analyze,
    analyze_file,
    analyze_with_population_data,
)
from langextract.tools.focus_group.examples import (
    CHRONIC_DISEASE_EXAMPLES,
    COMMUNITY_STRENGTHS_EXAMPLES,
    COMPREHENSIVE_HEALTH_EXAMPLES,
    EXAMPLE_PRESETS,
    HEALTHCARE_ACCESS_EXAMPLES,
    MATERNAL_CHILD_HEALTH_EXAMPLES,
    MENTAL_HEALTH_EXAMPLES,
    SDOH_EXAMPLES,
    combine_examples,
    get_examples,
)
from langextract.tools.focus_group.types import (
    AlignmentStatus,
    AnalysisResult,
    BarrierSummary,
    CommunityHealthGap,
    CommunityHealthSession,
    Confidence,
    DataComparison,
    ExtractionType,
    FocusGroupSession,
    HealthConcernSummary,
    HealthDomain,
    HealthIndicator,
    InsightCluster,
    InterviewSession,
    KeyInformantInterview,
    ParticipantInfo,
    ParticipantSummary,
    PopulationHealthData,
    SDOHCategory,
    Sentiment,
    Severity,
    ThemeSummary,
)
from langextract.tools.focus_group.visualization import (
    create_dashboard,
    create_highlighted_transcript,
    export_to_json,
    save_dashboard,
    save_json_report,
)

__all__ = [
    # Analyzer
    "analyze",
    "analyze_file",
    "analyze_with_population_data",
    "CommunityHealthAnalyzer",
    "FocusGroupAnalyzer",
    "AnalyzerConfig",
    # Types - Core
    "AnalysisResult",
    "Confidence",
    "ExtractionType",
    "Sentiment",
    "Severity",
    # Types - Health
    "HealthDomain",
    "SDOHCategory",
    "AlignmentStatus",
    "HealthIndicator",
    "PopulationHealthData",
    "HealthConcernSummary",
    "BarrierSummary",
    "DataComparison",
    "CommunityHealthGap",
    # Types - Sessions
    "CommunityHealthSession",
    "KeyInformantInterview",
    "FocusGroupSession",
    "InterviewSession",
    "ParticipantInfo",
    # Types - Summaries
    "ThemeSummary",
    "ParticipantSummary",
    "InsightCluster",
    # Examples
    "get_examples",
    "combine_examples",
    "EXAMPLE_PRESETS",
    "COMPREHENSIVE_HEALTH_EXAMPLES",
    "SDOH_EXAMPLES",
    "HEALTHCARE_ACCESS_EXAMPLES",
    "MATERNAL_CHILD_HEALTH_EXAMPLES",
    "COMMUNITY_STRENGTHS_EXAMPLES",
    "CHRONIC_DISEASE_EXAMPLES",
    "MENTAL_HEALTH_EXAMPLES",
    # Aggregation
    "calculate_overall_sentiment",
    "cluster_insights",
    "combine_session_results",
    "compare_multiple_sessions",
    "compare_sessions",
    "compare_with_population_data",
    "create_analysis_result",
    "create_health_analysis_result",
    "extract_barriers",
    "extract_community_strengths",
    "extract_health_concerns",
    "extract_participant_summaries",
    "extract_priority_areas",
    "extract_themes",
    "generate_key_findings",
    # Visualization
    "create_dashboard",
    "create_highlighted_transcript",
    "export_to_json",
    "save_dashboard",
    "save_json_report",
]
