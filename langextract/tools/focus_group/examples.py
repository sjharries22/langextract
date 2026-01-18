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

"""Predefined few-shot examples for focus group and interview analysis."""

from __future__ import annotations

from langextract.core.data import ExampleData, Extraction

# =============================================================================
# COMPREHENSIVE ANALYSIS EXAMPLES
# =============================================================================

COMPREHENSIVE_ANALYSIS_EXAMPLES = [
    ExampleData(
        text="""Moderator: What do you think about the current pricing?

P1: Honestly, I think the pricing is way too high compared to competitors.
I've been using the product for two years now, and while I love the features,
I really struggle with the monthly cost. It's becoming hard to justify.

P2: I actually disagree. The value we get is worth the price. The customer
support alone has saved us so many hours. That said, I wish there was a
cheaper tier for smaller teams.

P3: Yeah, I'm with P1 on this one. We almost switched to [Competitor] last
month because of the price difference. The only thing keeping us is the
integration with our existing tools.""",
        extractions=[
            Extraction(
                extraction_class="sentiment",
                extraction_text="the pricing is way too high compared to competitors",
                attributes={
                    "participant": "P1",
                    "sentiment": "negative",
                    "topic": "pricing",
                    "intensity": "strong",
                },
            ),
            Extraction(
                extraction_class="pain_point",
                extraction_text="I really struggle with the monthly cost",
                attributes={
                    "participant": "P1",
                    "category": "cost",
                    "severity": "high",
                },
            ),
            Extraction(
                extraction_class="disagreement",
                extraction_text="I actually disagree",
                attributes={
                    "participant": "P2",
                    "responding_to": "P1",
                    "topic": "pricing",
                },
            ),
            Extraction(
                extraction_class="sentiment",
                extraction_text="The value we get is worth the price",
                attributes={
                    "participant": "P2",
                    "sentiment": "positive",
                    "topic": "value",
                    "intensity": "moderate",
                },
            ),
            Extraction(
                extraction_class="feature_request",
                extraction_text="I wish there was a cheaper tier for smaller teams",
                attributes={
                    "participant": "P2",
                    "category": "pricing",
                    "priority": "medium",
                },
            ),
            Extraction(
                extraction_class="agreement",
                extraction_text="I'm with P1 on this one",
                attributes={
                    "participant": "P3",
                    "agreeing_with": "P1",
                    "topic": "pricing",
                },
            ),
            Extraction(
                extraction_class="experience",
                extraction_text="We almost switched to [Competitor] last month",
                attributes={
                    "participant": "P3",
                    "type": "churn_risk",
                    "competitor_mentioned": "true",
                },
            ),
            Extraction(
                extraction_class="insight",
                extraction_text="The only thing keeping us is the integration with our existing tools",
                attributes={
                    "participant": "P3",
                    "category": "retention_factor",
                    "importance": "high",
                },
            ),
        ],
    ),
    ExampleData(
        text="""Interviewer: Can you describe your typical workflow with our product?

Interviewee: Sure. I usually start my day by checking the dashboard for any
overnight alerts. The notification system is fantastic - it catches issues
before they become problems. But then I spend way too much time generating
reports. The reporting feature is so clunky and outdated. I've been asking
for improvements for months. If you could just add export to PDF, that would
save me at least an hour every day.

Interviewer: That's helpful. Any other pain points?

Interviewee: The mobile app is basically unusable. I've given up trying to
check things from my phone. And don't get me started on the search function -
it never finds what I'm looking for. But overall, I still recommend it to
colleagues because the core functionality is solid.""",
        extractions=[
            Extraction(
                extraction_class="experience",
                extraction_text="I usually start my day by checking the dashboard for any overnight alerts",
                attributes={
                    "participant": "interviewee",
                    "workflow_stage": "morning_routine",
                    "feature": "dashboard",
                },
            ),
            Extraction(
                extraction_class="sentiment",
                extraction_text="The notification system is fantastic",
                attributes={
                    "participant": "interviewee",
                    "sentiment": "very_positive",
                    "topic": "notifications",
                    "intensity": "strong",
                },
            ),
            Extraction(
                extraction_class="pain_point",
                extraction_text="I spend way too much time generating reports",
                attributes={
                    "participant": "interviewee",
                    "category": "efficiency",
                    "feature": "reporting",
                    "severity": "high",
                },
            ),
            Extraction(
                extraction_class="sentiment",
                extraction_text="The reporting feature is so clunky and outdated",
                attributes={
                    "participant": "interviewee",
                    "sentiment": "negative",
                    "topic": "reporting",
                    "intensity": "strong",
                },
            ),
            Extraction(
                extraction_class="feature_request",
                extraction_text="If you could just add export to PDF",
                attributes={
                    "participant": "interviewee",
                    "category": "reporting",
                    "priority": "high",
                    "impact": "save me at least an hour every day",
                },
            ),
            Extraction(
                extraction_class="pain_point",
                extraction_text="The mobile app is basically unusable",
                attributes={
                    "participant": "interviewee",
                    "category": "mobile",
                    "severity": "critical",
                },
            ),
            Extraction(
                extraction_class="pain_point",
                extraction_text="the search function - it never finds what I'm looking for",
                attributes={
                    "participant": "interviewee",
                    "category": "search",
                    "severity": "high",
                },
            ),
            Extraction(
                extraction_class="insight",
                extraction_text="I still recommend it to colleagues because the core functionality is solid",
                attributes={
                    "participant": "interviewee",
                    "category": "loyalty",
                    "sentiment": "positive",
                },
            ),
        ],
    ),
]

# =============================================================================
# SENTIMENT-FOCUSED EXAMPLES
# =============================================================================

SENTIMENT_ANALYSIS_EXAMPLES = [
    ExampleData(
        text="""P1: I absolutely love the new interface! It's so much more
intuitive than before. The design team really outdid themselves.

P2: Hmm, I'm not sure I agree. I find the new layout confusing. I keep
getting lost trying to find basic features. It's frustrating.

P3: It's okay, I guess. Not better or worse than before, just different.
I'll probably get used to it eventually.""",
        extractions=[
            Extraction(
                extraction_class="sentiment",
                extraction_text="I absolutely love the new interface",
                attributes={
                    "participant": "P1",
                    "sentiment": "very_positive",
                    "topic": "interface",
                    "intensity": "strong",
                },
            ),
            Extraction(
                extraction_class="sentiment",
                extraction_text="It's so much more intuitive than before",
                attributes={
                    "participant": "P1",
                    "sentiment": "positive",
                    "topic": "usability",
                    "comparison": "improvement",
                },
            ),
            Extraction(
                extraction_class="sentiment",
                extraction_text="I find the new layout confusing",
                attributes={
                    "participant": "P2",
                    "sentiment": "negative",
                    "topic": "layout",
                    "intensity": "moderate",
                },
            ),
            Extraction(
                extraction_class="emotion",
                extraction_text="It's frustrating",
                attributes={
                    "participant": "P2",
                    "emotion": "frustration",
                    "cause": "difficulty finding features",
                },
            ),
            Extraction(
                extraction_class="sentiment",
                extraction_text="It's okay, I guess",
                attributes={
                    "participant": "P3",
                    "sentiment": "neutral",
                    "topic": "interface",
                    "intensity": "weak",
                },
            ),
        ],
    ),
]

# =============================================================================
# THEME-FOCUSED EXAMPLES
# =============================================================================

THEME_EXTRACTION_EXAMPLES = [
    ExampleData(
        text="""Moderator: What features are most important to your team?

P1: For us, it's all about collaboration. We need everyone on the team to
be able to work on the same project simultaneously. Real-time editing is
essential.

P2: Security is our top priority. We handle sensitive data, so we need
robust encryption and access controls. Compliance features are non-negotiable.

P3: I'd say automation. We want to eliminate manual tasks wherever possible.
The more we can automate, the more time we have for strategic work.

P4: Echoing P1, collaboration is huge. But I'd add that integration with
other tools is critical. We use dozens of apps and they all need to talk
to each other.""",
        extractions=[
            Extraction(
                extraction_class="theme",
                extraction_text="it's all about collaboration",
                attributes={
                    "participant": "P1",
                    "theme": "collaboration",
                    "importance": "high",
                },
            ),
            Extraction(
                extraction_class="expectation",
                extraction_text="We need everyone on the team to be able to work on the same project simultaneously",
                attributes={
                    "participant": "P1",
                    "category": "collaboration",
                    "specificity": "high",
                },
            ),
            Extraction(
                extraction_class="theme",
                extraction_text="Security is our top priority",
                attributes={
                    "participant": "P2",
                    "theme": "security",
                    "importance": "critical",
                },
            ),
            Extraction(
                extraction_class="expectation",
                extraction_text="we need robust encryption and access controls",
                attributes={
                    "participant": "P2",
                    "category": "security",
                    "specificity": "high",
                },
            ),
            Extraction(
                extraction_class="theme",
                extraction_text="automation",
                attributes={
                    "participant": "P3",
                    "theme": "automation",
                    "importance": "high",
                },
            ),
            Extraction(
                extraction_class="insight",
                extraction_text="The more we can automate, the more time we have for strategic work",
                attributes={
                    "participant": "P3",
                    "category": "productivity",
                    "value_proposition": "time_savings",
                },
            ),
            Extraction(
                extraction_class="agreement",
                extraction_text="Echoing P1, collaboration is huge",
                attributes={
                    "participant": "P4",
                    "agreeing_with": "P1",
                    "theme": "collaboration",
                },
            ),
            Extraction(
                extraction_class="theme",
                extraction_text="integration with other tools is critical",
                attributes={
                    "participant": "P4",
                    "theme": "integration",
                    "importance": "critical",
                },
            ),
        ],
    ),
]

# =============================================================================
# PAIN POINTS AND FEATURE REQUESTS EXAMPLES
# =============================================================================

PAIN_POINTS_EXAMPLES = [
    ExampleData(
        text="""P1: The biggest issue for me is the loading time. Every time
I open the app, I'm waiting at least 30 seconds. In 2024, that's unacceptable.

P2: Agreed on performance. But my main complaint is the lack of offline mode.
When I'm traveling and have spotty internet, I can't do anything. I need to
be able to work offline and sync later.

P3: Has anyone else noticed the frequent crashes? I lose work at least once
a week because the app just closes without warning. There's no auto-save.

P1: Oh yes, the crashes! And when you contact support, they just tell you
to clear your cache. That's not a real solution.""",
        extractions=[
            Extraction(
                extraction_class="pain_point",
                extraction_text="The biggest issue for me is the loading time",
                attributes={
                    "participant": "P1",
                    "category": "performance",
                    "severity": "high",
                },
            ),
            Extraction(
                extraction_class="quote",
                extraction_text="Every time I open the app, I'm waiting at least 30 seconds",
                attributes={
                    "participant": "P1",
                    "context": "performance complaint",
                    "metric": "30 seconds load time",
                },
            ),
            Extraction(
                extraction_class="pain_point",
                extraction_text="the lack of offline mode",
                attributes={
                    "participant": "P2",
                    "category": "functionality",
                    "severity": "high",
                },
            ),
            Extraction(
                extraction_class="feature_request",
                extraction_text="I need to be able to work offline and sync later",
                attributes={
                    "participant": "P2",
                    "category": "offline_mode",
                    "priority": "high",
                    "use_case": "traveling",
                },
            ),
            Extraction(
                extraction_class="pain_point",
                extraction_text="the frequent crashes",
                attributes={
                    "participant": "P3",
                    "category": "stability",
                    "severity": "critical",
                    "frequency": "at least once a week",
                },
            ),
            Extraction(
                extraction_class="pain_point",
                extraction_text="I lose work at least once a week because the app just closes without warning",
                attributes={
                    "participant": "P3",
                    "category": "data_loss",
                    "severity": "critical",
                },
            ),
            Extraction(
                extraction_class="feature_request",
                extraction_text="There's no auto-save",
                attributes={
                    "participant": "P3",
                    "category": "reliability",
                    "priority": "critical",
                    "implied_request": "add auto-save",
                },
            ),
            Extraction(
                extraction_class="pain_point",
                extraction_text="when you contact support, they just tell you to clear your cache",
                attributes={
                    "participant": "P1",
                    "category": "support",
                    "severity": "medium",
                    "frustration": "unhelpful responses",
                },
            ),
        ],
    ),
]

# =============================================================================
# USER JOURNEY AND EXPERIENCE EXAMPLES
# =============================================================================

USER_EXPERIENCE_EXAMPLES = [
    ExampleData(
        text="""Interviewer: Walk me through how you discovered and started
using our product.

P1: I first heard about it from a colleague at a conference. He was raving
about how it transformed their workflow. I signed up for the free trial that
same day. The onboarding was smooth - I was up and running in about an hour.
But then I hit a wall trying to import our existing data. That took three
days and multiple support tickets to resolve. Once that was done though,
adoption across my team was quick. Within a month, everyone was using it
daily.""",
        extractions=[
            Extraction(
                extraction_class="experience",
                extraction_text="I first heard about it from a colleague at a conference",
                attributes={
                    "participant": "P1",
                    "journey_stage": "awareness",
                    "channel": "word_of_mouth",
                    "context": "conference",
                },
            ),
            Extraction(
                extraction_class="quote",
                extraction_text="He was raving about how it transformed their workflow",
                attributes={
                    "participant": "P1",
                    "context": "referral",
                    "sentiment": "very_positive",
                },
            ),
            Extraction(
                extraction_class="experience",
                extraction_text="I signed up for the free trial that same day",
                attributes={
                    "participant": "P1",
                    "journey_stage": "acquisition",
                    "trigger": "recommendation",
                    "immediacy": "high",
                },
            ),
            Extraction(
                extraction_class="sentiment",
                extraction_text="The onboarding was smooth",
                attributes={
                    "participant": "P1",
                    "sentiment": "positive",
                    "topic": "onboarding",
                    "journey_stage": "activation",
                },
            ),
            Extraction(
                extraction_class="pain_point",
                extraction_text="I hit a wall trying to import our existing data",
                attributes={
                    "participant": "P1",
                    "category": "data_migration",
                    "severity": "high",
                    "journey_stage": "activation",
                },
            ),
            Extraction(
                extraction_class="experience",
                extraction_text="That took three days and multiple support tickets to resolve",
                attributes={
                    "participant": "P1",
                    "journey_stage": "activation",
                    "friction": "high",
                    "time_to_resolve": "3 days",
                },
            ),
            Extraction(
                extraction_class="insight",
                extraction_text="Within a month, everyone was using it daily",
                attributes={
                    "participant": "P1",
                    "category": "adoption",
                    "journey_stage": "retention",
                    "success_metric": "team-wide daily usage",
                },
            ),
        ],
    ),
]

# =============================================================================
# COMPETITIVE ANALYSIS EXAMPLES
# =============================================================================

COMPETITIVE_EXAMPLES = [
    ExampleData(
        text="""Moderator: How does our product compare to alternatives you've tried?

P1: I used [Competitor A] for two years before switching. Their pricing was
better, but the features were limited. You have more depth.

P2: We evaluated [Competitor B] recently. They have a better mobile experience,
hands down. But their desktop app is a mess. You're stronger on desktop.

P3: Coming from [Competitor C], the learning curve here was steeper. They
have better documentation and tutorials. But once you learn your system,
it's more powerful.

P1: That's a good point about the learning curve. Maybe you need a better
onboarding program.""",
        extractions=[
            Extraction(
                extraction_class="comparison",
                extraction_text="I used [Competitor A] for two years before switching",
                attributes={
                    "participant": "P1",
                    "competitor": "Competitor A",
                    "relationship": "former_user",
                    "duration": "2 years",
                },
            ),
            Extraction(
                extraction_class="comparison",
                extraction_text="Their pricing was better, but the features were limited",
                attributes={
                    "participant": "P1",
                    "competitor": "Competitor A",
                    "competitor_strength": "pricing",
                    "competitor_weakness": "features",
                },
            ),
            Extraction(
                extraction_class="insight",
                extraction_text="You have more depth",
                attributes={
                    "participant": "P1",
                    "category": "competitive_advantage",
                    "strength": "feature_depth",
                },
            ),
            Extraction(
                extraction_class="comparison",
                extraction_text="They have a better mobile experience, hands down",
                attributes={
                    "participant": "P2",
                    "competitor": "Competitor B",
                    "competitor_strength": "mobile",
                    "confidence": "high",
                },
            ),
            Extraction(
                extraction_class="insight",
                extraction_text="You're stronger on desktop",
                attributes={
                    "participant": "P2",
                    "category": "competitive_advantage",
                    "strength": "desktop_experience",
                },
            ),
            Extraction(
                extraction_class="comparison",
                extraction_text="the learning curve here was steeper",
                attributes={
                    "participant": "P3",
                    "competitor": "Competitor C",
                    "our_weakness": "learning_curve",
                },
            ),
            Extraction(
                extraction_class="comparison",
                extraction_text="They have better documentation and tutorials",
                attributes={
                    "participant": "P3",
                    "competitor": "Competitor C",
                    "competitor_strength": "documentation",
                },
            ),
            Extraction(
                extraction_class="insight",
                extraction_text="once you learn your system, it's more powerful",
                attributes={
                    "participant": "P3",
                    "category": "competitive_advantage",
                    "strength": "power",
                    "caveat": "learning_curve",
                },
            ),
            Extraction(
                extraction_class="suggestion",
                extraction_text="Maybe you need a better onboarding program",
                attributes={
                    "participant": "P1",
                    "category": "improvement",
                    "area": "onboarding",
                    "priority": "medium",
                },
            ),
        ],
    ),
]

# =============================================================================
# EXAMPLE PRESETS MAPPING
# =============================================================================

EXAMPLE_PRESETS = {
    "comprehensive": COMPREHENSIVE_ANALYSIS_EXAMPLES,
    "sentiment": SENTIMENT_ANALYSIS_EXAMPLES,
    "themes": THEME_EXTRACTION_EXAMPLES,
    "pain_points": PAIN_POINTS_EXAMPLES,
    "user_experience": USER_EXPERIENCE_EXAMPLES,
    "competitive": COMPETITIVE_EXAMPLES,
}


def get_examples(preset: str = "comprehensive") -> list[ExampleData]:
  """Get predefined examples for a specific analysis type.

  Args:
    preset: The type of analysis. Options are:
      - "comprehensive": Full analysis including sentiments, themes, pain
        points
      - "sentiment": Focus on sentiment and emotion extraction
      - "themes": Focus on theme and topic extraction
      - "pain_points": Focus on pain points and feature requests
      - "user_experience": Focus on user journey and experience mapping
      - "competitive": Focus on competitive analysis and comparisons

  Returns:
    List of ExampleData for the specified preset.

  Raises:
    ValueError: If preset is not recognized.
  """
  if preset not in EXAMPLE_PRESETS:
    available = ", ".join(sorted(EXAMPLE_PRESETS.keys()))
    raise ValueError(
        f"Unknown preset '{preset}'. Available presets: {available}"
    )
  return EXAMPLE_PRESETS[preset]


def combine_examples(*presets: str) -> list[ExampleData]:
  """Combine examples from multiple presets.

  Args:
    *presets: Preset names to combine.

  Returns:
    Combined list of ExampleData from all specified presets.
  """
  combined = []
  seen_texts = set()
  for preset in presets:
    for example in get_examples(preset):
      if example.text not in seen_texts:
        combined.append(example)
        seen_texts.add(example.text)
  return combined
