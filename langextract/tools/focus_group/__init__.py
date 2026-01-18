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

"""Focus Group and Interview Analysis Tool.

This module provides tools for extracting, analyzing, and visualizing insights
from focus group transcripts and interview recordings.

Example usage:

    ```python
    from langextract.tools import focus_group

    # Quick analysis
    result = focus_group.analyze(
        "P1: I love the new feature! P2: Me too, it's great.",
        analysis_type="sentiment"
    )
    print(result.overall_sentiment)  # Sentiment.POSITIVE

    # Using the analyzer class for more control
    analyzer = focus_group.FocusGroupAnalyzer(
        focus_group.AnalyzerConfig(
            analysis_type="comprehensive",
            extraction_passes=2,
        )
    )
    result = analyzer.analyze("path/to/transcript.txt")

    # Create visualization
    focus_group.save_dashboard(result, "analysis.html")

    # Access insights
    for theme in result.themes:
        print(f"{theme.theme_name}: {theme.frequency} mentions")

    for finding in result.key_findings:
        print(f"- {finding}")
    ```

Available analysis types:
    - comprehensive: Full analysis of sentiments, themes, pain points, etc.
    - sentiment: Focus on sentiment and emotion extraction
    - themes: Focus on theme and topic extraction
    - pain_points: Focus on pain points and feature requests
    - user_experience: Focus on user journey and experience mapping
    - competitive: Focus on competitive analysis and comparisons
"""

from langextract.tools.focus_group.aggregation import (
    aggregate_by_attribute,
    calculate_overall_sentiment,
    calculate_sentiment_over_time,
    cluster_insights,
    compare_sessions,
    create_analysis_result,
    extract_participant_summaries,
    extract_themes,
    generate_key_findings,
)
from langextract.tools.focus_group.analyzer import (
    AnalyzerConfig,
    FocusGroupAnalyzer,
    analyze,
    analyze_file,
)
from langextract.tools.focus_group.examples import (
    COMPREHENSIVE_ANALYSIS_EXAMPLES,
    COMPETITIVE_EXAMPLES,
    EXAMPLE_PRESETS,
    PAIN_POINTS_EXAMPLES,
    SENTIMENT_ANALYSIS_EXAMPLES,
    THEME_EXTRACTION_EXAMPLES,
    USER_EXPERIENCE_EXAMPLES,
    combine_examples,
    get_examples,
)
from langextract.tools.focus_group.types import (
    AnalysisResult,
    Confidence,
    ExtractionType,
    FocusGroupSession,
    InsightCluster,
    InterviewSession,
    ParticipantInfo,
    ParticipantSummary,
    Sentiment,
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
    "FocusGroupAnalyzer",
    "AnalyzerConfig",
    # Types
    "AnalysisResult",
    "Confidence",
    "ExtractionType",
    "FocusGroupSession",
    "InsightCluster",
    "InterviewSession",
    "ParticipantInfo",
    "ParticipantSummary",
    "Sentiment",
    "ThemeSummary",
    # Examples
    "get_examples",
    "combine_examples",
    "EXAMPLE_PRESETS",
    "COMPREHENSIVE_ANALYSIS_EXAMPLES",
    "SENTIMENT_ANALYSIS_EXAMPLES",
    "THEME_EXTRACTION_EXAMPLES",
    "PAIN_POINTS_EXAMPLES",
    "USER_EXPERIENCE_EXAMPLES",
    "COMPETITIVE_EXAMPLES",
    # Aggregation
    "aggregate_by_attribute",
    "calculate_overall_sentiment",
    "calculate_sentiment_over_time",
    "cluster_insights",
    "compare_sessions",
    "create_analysis_result",
    "extract_participant_summaries",
    "extract_themes",
    "generate_key_findings",
    # Visualization
    "create_dashboard",
    "create_highlighted_transcript",
    "export_to_json",
    "save_dashboard",
    "save_json_report",
]
