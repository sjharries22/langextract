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

"""Basic usage example for the Population Health Focus Group Analysis tool.

This example demonstrates how to analyze community health focus group transcripts
and extract health concerns, barriers to care, and community insights.

Before running:
    pip install langextract
    export GEMINI_API_KEY=your_api_key
"""

from langextract.tools import focus_group

# Sample community health focus group transcript
SAMPLE_TRANSCRIPT = """
Facilitator: Thank you all for joining today's community health discussion.
Let's start by talking about the biggest health concerns in your neighborhood.

P1: Diabetes is everywhere in our community. My mother has it, my sister has it,
half my neighbors are dealing with it. The doctors tell us to eat healthy, but
have you seen the prices at the grocery store? And the closest one with fresh
produce is a 30-minute bus ride away.

P2: I agree about diabetes, but mental health is what really worries me. Nobody
talks about it, but everyone's struggling. The stress of making ends meet, the
violence in our neighborhood - it takes a toll. And there's nowhere to go for
help. The mental health clinic on Main Street closed two years ago.

P3: The clinic closing was devastating. Now if you need to see a therapist,
you're looking at a 45-minute drive to the city. Most people just don't go.
They deal with anxiety and depression on their own, or they self-medicate.

Facilitator: What barriers do you face when trying to get healthcare?

P1: Getting an appointment is nearly impossible. I called my doctor last month
and they said the next available slot was in three months. Three months! If
I'm sick now, what am I supposed to do? I ended up going to the ER.

P2: The cost is what stops me. Even with insurance, the copays are so high.
Last month I had to choose between my blood pressure medication and groceries.
I skipped the pills. It's dangerous, but what choice do I have?

P3: Transportation is my biggest challenge. I don't have a car, and the bus
doesn't go to the clinic. My daughter has asthma and missed her last two
checkups because I couldn't get there.

Facilitator: What strengths does your community have?

P1: We look out for each other. When my neighbor was sick, we all pitched in
to bring her meals and check on her. That's how we were raised.

P2: The church does a lot of good work. They run health fairs, food pantries,
exercise classes. It's where people go when they need support.

P3: We have some amazing community health workers - promotoras - who go door
to door helping people understand their health conditions. They speak our
language and understand our culture. We need more of them.

Facilitator: What would improve health in your community?

P1: Bring back the mental health clinic. That's the number one thing.

P2: More affordable healthy food options. Maybe a community garden or a
farmers market that accepts food stamps.

P3: Doctors who look like us and speak our language. Someone who understands
where we're coming from. Trust is everything.
"""


def main():
    """Run the community health analysis example."""
    print("=" * 60)
    print("Community Health Focus Group Analysis - Basic Example")
    print("=" * 60)
    print()

    # Analyze the transcript
    print("Analyzing community health focus group transcript...")
    print()

    result = focus_group.analyze(
        SAMPLE_TRANSCRIPT,
        analysis_type="comprehensive",
        model_id="gemini-2.5-flash",
        extraction_passes=2,
    )

    # Display overall sentiment
    print(f"Overall Community Sentiment: {result.overall_sentiment.value}")
    print(f"Total Insights Extracted: {result.total_extractions}")
    print()

    # Display key findings
    print("Key Findings:")
    print("-" * 40)
    for finding in result.key_findings:
        print(f"  - {finding}")
    print()

    # Display health concerns
    if result.health_concerns:
        print("Health Concerns Identified:")
        print("-" * 40)
        for concern in result.health_concerns[:5]:
            print(f"  - [{concern.severity.value.upper()}] {concern.concern}")
            if concern.sample_quotes:
                print(f"    Quote: \"{concern.sample_quotes[0][:80]}...\"")
        print()

    # Display barriers to care
    if result.barriers:
        print("Barriers to Healthcare Access:")
        print("-" * 40)
        for barrier in result.barriers[:5]:
            print(f"  - [{barrier.barrier_type}] {barrier.barrier[:60]}...")
        print()

    # Display community strengths
    if result.community_strengths:
        print("Community Strengths:")
        print("-" * 40)
        for strength in result.community_strengths[:5]:
            print(f"  - {strength[:80]}...")
        print()

    # Display priority areas
    if result.priority_areas:
        print("Community-Identified Priorities:")
        print("-" * 40)
        for priority in result.priority_areas[:5]:
            print(f"  - {priority[:80]}...")
        print()

    # Display top themes
    print("Top Health Themes:")
    print("-" * 40)
    for theme in result.themes[:5]:
        domain = f" ({theme.health_domain.value})" if theme.health_domain else ""
        print(f"  - {theme.theme_name}{domain}: {theme.frequency} mentions")
    print()

    # Save visualizations
    print("Saving visualizations...")

    focus_group.save_dashboard(result, "community_health_dashboard.html")
    print("  - Dashboard: community_health_dashboard.html")

    focus_group.save_json_report(result, "community_health_report.json")
    print("  - JSON Report: community_health_report.json")

    print()
    print("Analysis complete!")


if __name__ == "__main__":
    main()
