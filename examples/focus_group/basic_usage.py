#!/usr/bin/env python3
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

"""Basic usage example for the Focus Group Analysis tool.

This example demonstrates how to analyze a focus group transcript
and extract insights using the langextract focus group tool.

Before running:
    pip install langextract
    export GEMINI_API_KEY=your_api_key
"""

from langextract.tools import focus_group

# Sample focus group transcript
SAMPLE_TRANSCRIPT = """
Moderator: Thank you all for joining today's discussion about our mobile app.
Let's start with your overall impressions. Sarah, would you like to begin?

Sarah (P1): Sure! Overall, I really enjoy using the app. The interface is
clean and intuitive. But I have to say, the loading times are frustrating.
Sometimes I'm waiting 10-15 seconds just to see my dashboard. That's way
too long in 2024.

Mike (P2): I agree with Sarah on the loading times. It's definitely an issue.
But what bothers me more is the lack of offline functionality. When I'm
commuting on the subway, I lose connection and can't do anything. I wish I
could at least view my recent data offline.

Jennifer (P3): For me, the biggest pain point is the notification system.
I get way too many notifications, and there's no easy way to customize them.
I end up just turning them all off, which means I miss important alerts.

Moderator: Those are great points. How about features you'd like to see added?

Sarah (P1): I'd love to have a dark mode option. I often use the app at night
and the bright white screen is hard on my eyes.

Mike (P2): Export to PDF would be amazing. Right now I have to take screenshots
to share reports with my team. It's really inefficient.

Jennifer (P3): I second the PDF export! Also, it would be great to have
integration with Google Calendar. I manually copy my schedule right now.

Moderator: How does our app compare to competitors you've used?

Mike (P2): I used CompetitorX before switching. Their mobile experience was
actually better - faster, smoother. But your desktop app is superior, which
is why I made the switch. The analytics features here are unmatched.

Sarah (P1): I tried CompetitorY briefly. Their notification system is much
more flexible - you can set up custom rules for different types of alerts.
That's something I'd love to see here.

Jennifer (P3): Honestly, your customer support is what sets you apart. When
I had issues, the team was incredibly responsive. That's rare these days.
The product itself has room for improvement, but the support gives me
confidence that things will get better.

Moderator: Any final thoughts before we wrap up?

Sarah (P1): Just that despite the issues, I'm still a fan. The core
functionality is solid. I just hope the performance improves.

Mike (P2): Same here. Fix the mobile performance and add offline mode,
and I'll be completely satisfied.

Jennifer (P3): I appreciate being heard. Looking forward to seeing these
improvements!
"""


def main():
    """Run the focus group analysis example."""
    print("=" * 60)
    print("Focus Group Analysis Tool - Basic Usage Example")
    print("=" * 60)
    print()

    # Method 1: Quick analysis with the convenience function
    print("Analyzing transcript with comprehensive analysis...")
    print()

    result = focus_group.analyze(
        SAMPLE_TRANSCRIPT,
        analysis_type="comprehensive",
        model_id="gemini-2.5-flash",
        extraction_passes=2,  # Multiple passes for thoroughness
    )

    # Display overall sentiment
    print(f"Overall Sentiment: {result.overall_sentiment.value}")
    print(f"Total Insights Extracted: {result.total_extractions}")
    print()

    # Display key findings
    print("Key Findings:")
    print("-" * 40)
    for finding in result.key_findings:
        print(f"  • {finding}")
    print()

    # Display top themes
    print("Top Themes:")
    print("-" * 40)
    for theme in result.themes[:5]:
        print(f"  • {theme.theme_name}: {theme.frequency} mentions")
        if theme.sample_quotes:
            print(f"    Sample: \"{theme.sample_quotes[0][:60]}...\"")
    print()

    # Display pain points
    print("Pain Points:")
    print("-" * 40)
    pain_points = result.get_extractions_by_type(focus_group.ExtractionType.PAIN_POINT)
    for pp in pain_points[:5]:
        severity = pp.attributes.get("severity", "unknown") if pp.attributes else "unknown"
        print(f"  • [{severity.upper()}] {pp.extraction_text[:80]}")
    print()

    # Display feature requests
    print("Feature Requests:")
    print("-" * 40)
    feature_requests = result.get_extractions_by_type(focus_group.ExtractionType.FEATURE_REQUEST)
    for fr in feature_requests[:5]:
        print(f"  • {fr.extraction_text[:80]}")
    print()

    # Display participant summary
    print("Participant Summary:")
    print("-" * 40)
    for ps in result.participant_summaries:
        print(f"  {ps.participant_id}:")
        print(f"    Contributions: {ps.total_contributions}")
        print(f"    Topics: {', '.join(ps.themes_discussed[:3])}")
    print()

    # Save visualizations
    print("Saving visualizations...")

    # Save interactive dashboard
    focus_group.save_dashboard(result, "focus_group_dashboard.html")
    print("  • Dashboard saved to: focus_group_dashboard.html")

    # Save JSON report
    focus_group.save_json_report(result, "focus_group_report.json")
    print("  • JSON report saved to: focus_group_report.json")

    print()
    print("Analysis complete!")


if __name__ == "__main__":
    main()
