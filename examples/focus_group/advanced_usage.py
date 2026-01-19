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

"""Advanced usage example for the Population Health Focus Group Analysis tool.

This example demonstrates:
- Analyzing multiple community groups
- Comparing community voice data with population health indicators
- Using CommunityHealthSession objects with metadata
- Comparing findings across four different focus groups

Before running:
    pip install langextract
    export GEMINI_API_KEY=your_api_key
"""

from langextract.tools import focus_group

# Four different community focus group transcripts
SENIORS_TRANSCRIPT = """
Facilitator: What health challenges are most pressing for older adults here?

P1: Getting our medications is a constant struggle. The pharmacy is across
town and I can't drive anymore. My daughter helps when she can, but she works.

P2: The cost of prescriptions is outrageous. I'm on fixed income and some
months I have to choose which medications to take. You can't take all of them.

P3: Isolation is killing us. Since COVID, many of us are afraid to go out.
I haven't seen my grandchildren in months. The loneliness affects everything.

P1: Falls are what I worry about most. I fell last year and was on the floor
for hours before anyone found me. We need those medical alert systems but
they're expensive.

P2: The senior center used to be our lifeline but it's only open three days
a week now due to budget cuts. We need more programs for older folks.
"""

PARENTS_TRANSCRIPT = """
Facilitator: What are the biggest health concerns for families with children?

P1: Affordable childcare that's also healthy. My kids are in daycare and
they're constantly getting sick. But I can't afford to take time off work.

P2: The school doesn't have a nurse anymore. If my child has an asthma attack,
they just call me to come get her. What if it's an emergency?

P3: Mental health for teenagers is a crisis. My son's friends are dealing
with anxiety, depression, some talk about self-harm. There's a 6-month wait
to see a child psychiatrist.

P1: Lead paint in these old apartments terrifies me. My building was built
in the 1960s and the landlord won't do anything about it. My son's lead
levels were elevated at his last checkup.

P2: We need more after-school programs. Kids have nowhere safe to go, so
they stay inside on screens. No wonder obesity is such a problem.
"""

SPANISH_SPEAKING_TRANSCRIPT = """
Facilitador: ¿Cuáles son los mayores desafíos de salud en su comunidad?

P1: La barrera del idioma es enorme. Cuando voy al doctor, no hay intérpretes.
Mi hija tiene que faltar a la escuela para traducir. Eso no está bien.

P2: Tenemos miedo de ir al hospital. Preguntan sobre documentos. Mucha gente
evita el cuidado médico por miedo a la deportación.

P3: La diabetes es una epidemia en nuestra comunidad. Pero la comida saludable
es muy cara. Compramos lo que podemos pagar - arroz, frijoles, tortillas.

P1: Necesitamos más promotoras de salud. Ellas entienden nuestra cultura y
hablan nuestro idioma. Confío más en ellas que en los doctores.

P2: El estrés de trabajar dos empleos y no tener seguro médico - afecta todo.
No dormimos bien, no comemos bien. Es un ciclo vicioso.
"""

RURAL_TRANSCRIPT = """
Facilitator: What are the health challenges specific to rural communities?

P1: Distance is everything. The nearest hospital is 45 miles away. If you
have a heart attack out here, you better hope the ambulance gets there fast.

P2: We don't have specialists. If you need to see a cardiologist or
dermatologist, you're driving to the city. That's a whole day gone.

P3: The opioid crisis hit us hard. I've lost two neighbors to overdoses.
There's no addiction treatment anywhere near here.

P1: Our one doctor retired last year and nobody wants to replace her.
We're down to a nurse practitioner two days a week.

P2: Internet is so bad that telehealth doesn't work. They keep saying
we can do video visits, but our connection drops every five minutes.

P3: Farming is hard on the body. Back problems, chemical exposure, injuries.
But we can't afford to take time off. The cows still need milking.
"""


def create_population_health_data():
    """Create sample population health data for comparison."""
    return focus_group.PopulationHealthData(
        geography="County",
        geography_name="Example County",
        data_year="2023",
        sources=["CDC", "County Health Rankings", "BRFSS"],
        indicators=[
            focus_group.HealthIndicator(
                indicator_id="diabetes_prevalence",
                name="Adult Diabetes Prevalence",
                value=14.2,
                unit="%",
                year=2023,
                source="CDC",
                geography="County",
                geography_name="Example County",
                comparison_value=10.5,  # State average
                comparison_geography="State",
                trend="worsening",
                health_domain=focus_group.HealthDomain.CHRONIC_DISEASE,
            ),
            focus_group.HealthIndicator(
                indicator_id="mental_health_providers",
                name="Mental Health Providers per 100k",
                value=45,
                unit=" per 100k",
                year=2023,
                source="County Health Rankings",
                geography="County",
                geography_name="Example County",
                comparison_value=120,  # State average
                comparison_geography="State",
                trend="worsening",
                health_domain=focus_group.HealthDomain.MENTAL_HEALTH,
                sdoh_category=focus_group.SDOHCategory.HEALTHCARE_ACCESS,
            ),
            focus_group.HealthIndicator(
                indicator_id="uninsured_rate",
                name="Uninsured Rate",
                value=12.5,
                unit="%",
                year=2023,
                source="Census ACS",
                geography="County",
                geography_name="Example County",
                comparison_value=8.0,
                comparison_geography="State",
                sdoh_category=focus_group.SDOHCategory.HEALTHCARE_ACCESS,
            ),
            focus_group.HealthIndicator(
                indicator_id="food_insecurity",
                name="Food Insecurity Rate",
                value=15.3,
                unit="%",
                year=2023,
                source="Feeding America",
                geography="County",
                geography_name="Example County",
                comparison_value=10.2,
                comparison_geography="State",
                health_domain=focus_group.HealthDomain.NUTRITION,
                sdoh_category=focus_group.SDOHCategory.ECONOMIC_STABILITY,
            ),
            focus_group.HealthIndicator(
                indicator_id="drug_overdose_deaths",
                name="Drug Overdose Death Rate",
                value=32.5,
                unit=" per 100k",
                year=2023,
                source="CDC Wonder",
                geography="County",
                geography_name="Example County",
                comparison_value=22.0,
                comparison_geography="State",
                trend="worsening",
                health_domain=focus_group.HealthDomain.SUBSTANCE_USE,
            ),
        ],
    )


def main():
    """Run the advanced community health analysis example."""
    print("=" * 60)
    print("Population Health Focus Group Analysis - Advanced Example")
    print("Comparing Four Community Groups with Population Data")
    print("=" * 60)
    print()

    # Create session objects for each group
    sessions = [
        focus_group.CommunityHealthSession(
            session_id="seniors_group_001",
            transcript=SENIORS_TRANSCRIPT,
            community="Riverside Senior Center",
            topic="Health Needs of Older Adults",
            target_population="Seniors 65+",
            date="2024-03-01",
        ),
        focus_group.CommunityHealthSession(
            session_id="parents_group_001",
            transcript=PARENTS_TRANSCRIPT,
            community="Eastside Community Center",
            topic="Family and Child Health",
            target_population="Parents with children",
            date="2024-03-08",
        ),
        focus_group.CommunityHealthSession(
            session_id="spanish_group_001",
            transcript=SPANISH_SPEAKING_TRANSCRIPT,
            community="Centro Comunitario Latino",
            topic="Necesidades de Salud Comunitaria",
            target_population="Spanish-speaking residents",
            date="2024-03-15",
        ),
        focus_group.CommunityHealthSession(
            session_id="rural_group_001",
            transcript=RURAL_TRANSCRIPT,
            community="Valley Township Hall",
            topic="Rural Health Challenges",
            target_population="Rural residents",
            date="2024-03-22",
        ),
    ]

    # Create population health data
    population_data = create_population_health_data()

    # Configure analyzer
    config = focus_group.AnalyzerConfig(
        model_id="gemini-2.5-flash",
        analysis_type="comprehensive",
        extraction_passes=2,
    )
    analyzer = focus_group.CommunityHealthAnalyzer(config)

    # Analyze and compare all groups with population data
    print("Analyzing four community focus groups...")
    print()

    comparison = analyzer.analyze_multiple_groups(
        sessions,
        population_data=population_data
    )

    # Display comparison results
    print(f"Sessions analyzed: {comparison['session_count']}")
    print(f"Total insights extracted: {comparison['total_extractions']}")
    print()

    # Sentiment by group
    print("Sentiment by Community Group:")
    print("-" * 40)
    for s in comparison["sentiment_by_session"]:
        session_id = s.get("session_id", f"Session {s['session']}")
        print(f"  {session_id}: {s['sentiment']}")
    print()

    # Common themes across all groups
    print("Common Themes Across All Groups:")
    print("-" * 40)
    for theme in comparison["combined_themes"][:10]:
        print(f"  - {theme['theme']}: mentioned {theme['count']} times")
    print()

    # Common health concerns
    print("Common Health Concerns:")
    print("-" * 40)
    for concern in comparison["common_concerns"][:8]:
        print(f"  - {concern['concern'][:50]}...: {concern['count']} mentions")
    print()

    # Common barriers
    print("Common Barriers to Care:")
    print("-" * 40)
    for barrier in comparison["common_barriers"][:8]:
        print(f"  - {barrier['barrier'][:50]}...: {barrier['count']} mentions")
    print()

    # Data comparisons - Community Voice vs Population Data
    if "data_comparisons" in comparison and comparison["data_comparisons"]:
        print("Community Voice vs Population Health Data:")
        print("-" * 40)
        for dc in comparison["data_comparisons"][:10]:
            status_emoji = {
                "aligned": "[ALIGNED]",
                "divergent": "[EMERGING]",
                "data_gap": "[NO DATA]",
                "partially_aligned": "[PARTIAL]",
            }.get(dc.alignment_status.value, "[?]")

            print(f"  {status_emoji} {dc.topic}")
            print(f"    Community mentions: {dc.community_frequency}")
            if dc.population_indicator:
                ind = dc.population_indicator
                print(f"    Data: {ind.name} = {ind.value}{ind.unit}")
                if ind.comparison_value:
                    print(f"    Benchmark: {ind.comparison_value}{ind.unit}")
            if dc.interpretation:
                print(f"    {dc.interpretation[:80]}...")
            print()

    # Data gaps - Issues raised by community not in data
    if "community_health_gaps" in comparison and comparison["community_health_gaps"]:
        print("Community Health Gaps (Not Reflected in Data):")
        print("-" * 40)
        for gap in comparison["community_health_gaps"][:5]:
            print(f"  - {gap.gap_description}")
            print(f"    Mentioned {gap.frequency_mentioned} times")
            print(f"    Severity: {gap.severity.value}")
        print()

    # Save individual group dashboards
    print("Saving dashboards for each community group...")
    for i, result in enumerate(comparison["individual_results"]):
        session = sessions[i]
        filename = f"{session.session_id}_dashboard.html"
        focus_group.save_dashboard(result, filename)
        print(f"  - {filename}")

    print()
    print("Analysis complete!")
    print()
    print("Key Insight: By comparing community voice data from four different")
    print("groups with population health indicators, we can identify where")
    print("community concerns are validated by data (aligned) and where")
    print("communities are identifying emerging issues not yet captured")
    print("in traditional health metrics (divergent/data gaps).")


if __name__ == "__main__":
    main()
