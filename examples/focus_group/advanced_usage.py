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

"""Advanced usage example for the Focus Group Analysis tool.

This example demonstrates:
- Using FocusGroupSession and InterviewSession objects
- Custom analyzer configuration
- Comparing multiple sessions
- Custom examples for domain-specific analysis

Before running:
    pip install langextract
    export GEMINI_API_KEY=your_api_key
"""

from langextract.core.data import ExampleData, Extraction
from langextract.tools import focus_group

# Sample transcripts for multiple sessions
SESSION_1_TRANSCRIPT = """
Moderator: Welcome to our discussion on the new checkout experience.

P1: The new checkout is much faster! I love that I don't have to re-enter
my address every time. The saved payment methods are a huge improvement.

P2: I agree it's faster, but I had trouble finding the promo code field.
It took me three tries to figure out where to enter my discount code.

P3: My biggest concern is security. The old checkout showed more security
badges. The new one feels less trustworthy, even if it isn't.

P1: Oh, that's a good point about security. I didn't notice but now that
you mention it, I do miss seeing the lock icon more prominently.

P2: One thing I really want is Apple Pay support. Most other sites have it
and it's so convenient.

P3: Yes! And Google Pay too. Mobile payment options would be great.
"""

SESSION_2_TRANSCRIPT = """
Moderator: Today we're discussing the mobile shopping experience.

P4: I mostly shop on mobile. The app is decent but the search is terrible.
I can never find what I'm looking for. The filters don't work well.

P5: Search is definitely an issue. But for me, the images are the problem.
They take forever to load and sometimes don't load at all on slower networks.

P6: I actually switched to using the website on mobile instead of the app.
The website is more reliable, which is sad because apps should be better.

P4: That's surprising. The app crashes on me sometimes, so maybe I should
try the mobile website too.

P5: What I love is the wishlist feature. Being able to save items and get
notified when they go on sale is fantastic. More apps should do this.

P6: The wishlist notifications are great. Though I wish I could organize
my wishlist into different categories or folders.
"""


def run_session_analysis():
    """Demonstrate analyzing multiple sessions with comparison."""
    print("=" * 60)
    print("Focus Group Analysis Tool - Advanced Usage")
    print("=" * 60)
    print()

    # Create session objects with metadata
    session1 = focus_group.FocusGroupSession(
        session_id="checkout_study_001",
        transcript=SESSION_1_TRANSCRIPT,
        topic="New Checkout Experience",
        date="2024-03-15",
        moderator="Jane Smith",
        participants=[
            focus_group.ParticipantInfo("P1", segment="power_user"),
            focus_group.ParticipantInfo("P2", segment="casual_user"),
            focus_group.ParticipantInfo("P3", segment="security_conscious"),
        ],
        notes="Recruited participants who made at least 3 purchases in past month",
    )

    session2 = focus_group.FocusGroupSession(
        session_id="mobile_study_001",
        transcript=SESSION_2_TRANSCRIPT,
        topic="Mobile Shopping Experience",
        date="2024-03-20",
        moderator="John Doe",
        participants=[
            focus_group.ParticipantInfo("P4", segment="mobile_first"),
            focus_group.ParticipantInfo("P5", segment="casual_mobile"),
            focus_group.ParticipantInfo("P6", segment="cross_platform"),
        ],
        notes="Mobile-first shoppers, ages 25-35",
    )

    # Configure the analyzer
    config = focus_group.AnalyzerConfig(
        model_id="gemini-2.5-flash",
        analysis_type="comprehensive",
        extraction_passes=2,
        max_workers=10,
        use_schema_constraints=True,
    )

    analyzer = focus_group.FocusGroupAnalyzer(config)

    print("Analyzing Session 1: Checkout Experience...")
    result1 = analyzer.analyze_session(session1)
    print(f"  Found {result1.total_extractions} insights")
    print(f"  Overall sentiment: {result1.overall_sentiment.value}")
    print()

    print("Analyzing Session 2: Mobile Experience...")
    result2 = analyzer.analyze_session(session2)
    print(f"  Found {result2.total_extractions} insights")
    print(f"  Overall sentiment: {result2.overall_sentiment.value}")
    print()

    # Compare sessions
    print("Comparing Sessions:")
    print("-" * 40)
    comparison = analyzer.compare_sessions([session1, session2])

    print(f"  Total sessions: {comparison['session_count']}")
    print(f"  Total insights: {comparison['total_extractions']}")
    print()

    print("  Sentiment by session:")
    for s in comparison["sentiment_by_session"]:
        print(f"    Session {s['session']}: {s['sentiment']}")
    print()

    print("  Common themes across sessions:")
    for theme in comparison["common_themes"][:5]:
        print(f"    • {theme['theme']}: {theme['count']} mentions")
    print()

    print("  Common pain points:")
    for pp in comparison["common_pain_points"][:5]:
        print(f"    • {pp['pain_point'][:60]}...")
    print()

    # Save individual dashboards
    focus_group.save_dashboard(result1, "session1_dashboard.html")
    focus_group.save_dashboard(result2, "session2_dashboard.html")
    print("Dashboards saved!")


def run_custom_examples():
    """Demonstrate using custom examples for domain-specific analysis."""
    print()
    print("=" * 60)
    print("Custom Examples for E-commerce Analysis")
    print("=" * 60)
    print()

    # Define custom examples for e-commerce-specific extraction
    custom_examples = [
        ExampleData(
            text="""P1: The checkout process is frustrating. I had items in my cart
and they disappeared when I went to pay. Lost a $50 order because of this bug.

P2: Same happened to me! The cart timeout is way too short. I was just
comparing prices and when I came back, everything was gone.""",
            extractions=[
                Extraction(
                    extraction_class="bug_report",
                    extraction_text="items in my cart and they disappeared when I went to pay",
                    attributes={
                        "participant": "P1",
                        "severity": "critical",
                        "feature": "cart",
                        "impact": "lost_sale",
                        "value": "$50",
                    },
                ),
                Extraction(
                    extraction_class="pain_point",
                    extraction_text="The cart timeout is way too short",
                    attributes={
                        "participant": "P2",
                        "category": "cart",
                        "severity": "high",
                    },
                ),
                Extraction(
                    extraction_class="agreement",
                    extraction_text="Same happened to me!",
                    attributes={
                        "participant": "P2",
                        "agreeing_with": "P1",
                        "topic": "cart_issues",
                    },
                ),
            ],
        ),
    ]

    # Create analyzer with custom examples
    config = focus_group.AnalyzerConfig(
        model_id="gemini-2.5-flash",
        analysis_type="comprehensive",
        custom_examples=custom_examples,
        custom_prompt="""Extract e-commerce specific insights from focus group transcripts.
Look for:
- Bug reports with severity and business impact
- Cart and checkout issues
- Payment problems
- Pricing concerns
- Feature requests with priority

For each issue, identify the affected feature area and potential revenue impact.""",
    )

    analyzer = focus_group.FocusGroupAnalyzer(config)

    sample_transcript = """
P1: I tried to use a gift card but it kept saying invalid. Turns out the
system doesn't accept gift cards with spaces in the code. That's a bug!

P2: The mobile app doesn't show shipping costs until the very end. I feel
tricked when I see the final total is $15 more than expected.

P3: What really annoys me is that saved payment methods disappear randomly.
I've had to re-enter my card three times this month. It's a security concern
too - are my details being stored properly?
"""

    print("Analyzing with custom e-commerce examples...")
    result = analyzer.analyze(sample_transcript)

    print(f"Found {result.total_extractions} insights")
    print()

    # Show extractions by type
    print("Extractions by type:")
    for ext_type, count in result.extraction_type_counts.items():
        print(f"  • {ext_type}: {count}")
    print()

    # Show all extractions
    print("Detailed extractions:")
    for doc in result.annotated_documents:
        for ext in doc.extractions or []:
            print(f"  [{ext.extraction_class}] {ext.extraction_text[:60]}...")
            if ext.attributes:
                for k, v in ext.attributes.items():
                    print(f"      {k}: {v}")
            print()


def run_interview_analysis():
    """Demonstrate analyzing individual interviews."""
    print()
    print("=" * 60)
    print("Interview Analysis")
    print("=" * 60)
    print()

    interview_transcript = """
Interviewer: Can you walk me through your typical workflow?

Interviewee: Sure. I start each morning checking my dashboard for overnight
alerts. The system is great at catching issues early. Then I spend about
an hour on reports - that's the tedious part. The report builder is clunky
and I often have to export to Excel to get the formatting right.

Interviewer: What would make reporting easier?

Interviewee: Honestly, just better templates. I create the same report every
week and have to set up the same filters each time. A "save as template"
feature would save me hours. Also, scheduling reports to auto-generate
would be amazing.

Interviewer: How satisfied are you overall?

Interviewee: I'd say 7 out of 10. The core analytics are powerful and
accurate - that's what matters most. But the UX needs work. My team
complains about the learning curve. It took our new hire three weeks
to get comfortable. Compare that to CompetitorX where people are
productive in days.
"""

    # Create interview session
    interview = focus_group.InterviewSession(
        session_id="user_interview_042",
        transcript=interview_transcript,
        interviewee=focus_group.ParticipantInfo(
            participant_id="USER_042",
            name="Anonymous",
            demographics={"role": "Data Analyst", "tenure": "2 years"},
            segment="power_user",
        ),
        interviewer="Research Team",
        topic="Product Feedback",
        date="2024-03-22",
        interview_type="semi-structured",
        duration_minutes=30,
    )

    # Analyze
    config = focus_group.AnalyzerConfig(
        analysis_type="user_experience",  # Focus on journey and experience
    )
    analyzer = focus_group.FocusGroupAnalyzer(config)

    print("Analyzing interview...")
    result = analyzer.analyze_session(interview)

    print(f"Insights found: {result.total_extractions}")
    print(f"Overall sentiment: {result.overall_sentiment.value}")
    print()

    print("Key findings:")
    for finding in result.key_findings:
        print(f"  • {finding}")
    print()

    # Create highlighted transcript view
    highlighted = focus_group.create_highlighted_transcript(result)
    with open("interview_highlighted.html", "w") as f:
        f.write(f"""
<!DOCTYPE html>
<html>
<head><title>Interview Analysis</title>
<style>
body {{ font-family: sans-serif; padding: 20px; max-width: 800px; margin: 0 auto; }}
h1 {{ color: #333; }}
.transcript-view {{ line-height: 1.8; }}
.highlight {{ padding: 2px 4px; border-radius: 3px; }}
.tooltip {{ position: absolute; background: #333; color: white; padding: 8px 12px;
            border-radius: 6px; font-size: 0.85rem; max-width: 300px; display: none; }}
</style>
</head>
<body>
<h1>Interview Analysis: {interview.session_id}</h1>
<p><strong>Topic:</strong> {interview.topic}</p>
<p><strong>Interviewee:</strong> {interview.interviewee.segment}</p>
<h2>Highlighted Transcript</h2>
{highlighted}
</body>
</html>
""")
    print("Highlighted transcript saved to: interview_highlighted.html")


if __name__ == "__main__":
    run_session_analysis()
    run_custom_examples()
    run_interview_analysis()
