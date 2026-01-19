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

"""Predefined few-shot examples for population health focus group analysis.

These examples are designed to extract health concerns, barriers to care,
social determinants of health, and community insights from focus group
transcripts for community health needs assessments.
"""

from __future__ import annotations

from langextract.core.data import ExampleData, Extraction

# =============================================================================
# COMPREHENSIVE COMMUNITY HEALTH EXAMPLES
# =============================================================================

COMPREHENSIVE_HEALTH_EXAMPLES = [
    ExampleData(
        text="""Facilitator: What are the biggest health concerns in your community?

P1: Diabetes is a huge problem here. Almost everyone I know has it or is
pre-diabetic. My mother, my aunt, my neighbor - they're all dealing with it.
The doctors just tell us to eat better, but healthy food is expensive and
the nearest grocery store with fresh produce is 20 minutes away.

P2: I agree about diabetes. But for me, mental health is the bigger issue
that nobody talks about. There's so much stress in our community - job
insecurity, bills, violence. And there's nowhere to go for help. The one
mental health clinic closed last year.

P3: The clinic closing was devastating. Now people have to travel an hour
to see a therapist. Most folks just don't go. They deal with depression
and anxiety on their own, or they self-medicate.

P1: That's true. A lot of people turn to alcohol or pills because there's
no other support. We need mental health services back in this neighborhood.""",
        extractions=[
            Extraction(
                extraction_class="health_concern",
                extraction_text="Diabetes is a huge problem here",
                attributes={
                    "participant": "P1",
                    "health_domain": "chronic_disease",
                    "severity": "high",
                    "prevalence": "widespread",
                },
            ),
            Extraction(
                extraction_class="barrier_to_care",
                extraction_text="healthy food is expensive and the nearest grocery store with fresh produce is 20 minutes away",
                attributes={
                    "participant": "P1",
                    "barrier_type": "geographic",
                    "sdoh_category": "neighborhood_environment",
                    "health_domain": "nutrition",
                },
            ),
            Extraction(
                extraction_class="food_access",
                extraction_text="the nearest grocery store with fresh produce is 20 minutes away",
                attributes={
                    "participant": "P1",
                    "sdoh_category": "neighborhood_environment",
                    "issue_type": "food_desert",
                },
            ),
            Extraction(
                extraction_class="health_concern",
                extraction_text="mental health is the bigger issue that nobody talks about",
                attributes={
                    "participant": "P2",
                    "health_domain": "mental_health",
                    "severity": "high",
                    "stigma_mentioned": "true",
                },
            ),
            Extraction(
                extraction_class="sdoh_factor",
                extraction_text="job insecurity, bills, violence",
                attributes={
                    "participant": "P2",
                    "sdoh_category": "economic_stability",
                    "impact": "stress",
                },
            ),
            Extraction(
                extraction_class="resource_gap",
                extraction_text="The one mental health clinic closed last year",
                attributes={
                    "participant": "P2",
                    "service_type": "mental_health",
                    "gap_type": "facility_closure",
                    "sdoh_category": "healthcare_access",
                },
            ),
            Extraction(
                extraction_class="barrier_to_care",
                extraction_text="people have to travel an hour to see a therapist",
                attributes={
                    "participant": "P3",
                    "barrier_type": "geographic",
                    "service_type": "mental_health",
                    "sdoh_category": "healthcare_access",
                },
            ),
            Extraction(
                extraction_class="health_behavior",
                extraction_text="They deal with depression and anxiety on their own, or they self-medicate",
                attributes={
                    "participant": "P3",
                    "health_domain": "mental_health",
                    "behavior_type": "coping_mechanism",
                    "risk_level": "high",
                },
            ),
            Extraction(
                extraction_class="risk_behavior",
                extraction_text="A lot of people turn to alcohol or pills because there's no other support",
                attributes={
                    "participant": "P1",
                    "health_domain": "substance_use",
                    "cause": "lack_of_mental_health_services",
                    "severity": "high",
                },
            ),
            Extraction(
                extraction_class="unmet_need",
                extraction_text="We need mental health services back in this neighborhood",
                attributes={
                    "participant": "P1",
                    "service_type": "mental_health",
                    "priority": "high",
                    "sdoh_category": "healthcare_access",
                },
            ),
        ],
    ),
    ExampleData(
        text="""Facilitator: Tell me about your experiences accessing healthcare.

P4: Getting an appointment is nearly impossible. I called my doctor's office
and they said the next available slot was in three months. Three months!
If I'm sick now, what am I supposed to do?

P5: Same here. I ended up going to the ER for something that should have
been a regular doctor visit because I couldn't wait. Then I got stuck with
a huge bill.

P6: The cost is what stops me. Even with insurance, the copays and deductibles
are so high. I have to choose between paying for my medications or paying
for groceries. Last month I skipped my blood pressure pills to make rent.

P4: I know people who ration their insulin because they can't afford it.
It's dangerous, but what choice do they have?

P5: And if you don't have a car, forget it. The bus doesn't run to the
clinic, and Uber is expensive. My grandmother missed two appointments
because she couldn't get a ride.""",
        extractions=[
            Extraction(
                extraction_class="access_issue",
                extraction_text="the next available slot was in three months",
                attributes={
                    "participant": "P4",
                    "issue_type": "appointment_availability",
                    "wait_time": "3 months",
                    "sdoh_category": "healthcare_access",
                },
            ),
            Extraction(
                extraction_class="healthcare_experience",
                extraction_text="I ended up going to the ER for something that should have been a regular doctor visit",
                attributes={
                    "participant": "P5",
                    "experience_type": "inappropriate_er_use",
                    "cause": "appointment_unavailability",
                },
            ),
            Extraction(
                extraction_class="economic_factor",
                extraction_text="the copays and deductibles are so high",
                attributes={
                    "participant": "P6",
                    "sdoh_category": "economic_stability",
                    "barrier_type": "financial",
                    "severity": "high",
                },
            ),
            Extraction(
                extraction_class="barrier_to_care",
                extraction_text="I have to choose between paying for my medications or paying for groceries",
                attributes={
                    "participant": "P6",
                    "barrier_type": "financial",
                    "impact": "medication_nonadherence",
                    "sdoh_category": "economic_stability",
                },
            ),
            Extraction(
                extraction_class="risk_behavior",
                extraction_text="I skipped my blood pressure pills to make rent",
                attributes={
                    "participant": "P6",
                    "health_domain": "chronic_disease",
                    "behavior_type": "medication_nonadherence",
                    "cause": "cost",
                    "severity": "high",
                },
            ),
            Extraction(
                extraction_class="quote",
                extraction_text="I know people who ration their insulin because they can't afford it",
                attributes={
                    "participant": "P4",
                    "health_domain": "chronic_disease",
                    "issue": "insulin_rationing",
                    "severity": "critical",
                },
            ),
            Extraction(
                extraction_class="transportation_issue",
                extraction_text="The bus doesn't run to the clinic, and Uber is expensive",
                attributes={
                    "participant": "P5",
                    "sdoh_category": "neighborhood_environment",
                    "barrier_type": "transportation",
                    "affected_population": "elderly",
                },
            ),
            Extraction(
                extraction_class="barrier_to_care",
                extraction_text="My grandmother missed two appointments because she couldn't get a ride",
                attributes={
                    "participant": "P5",
                    "barrier_type": "transportation",
                    "affected_population": "elderly",
                    "consequence": "missed_appointments",
                },
            ),
        ],
    ),
]

# =============================================================================
# SOCIAL DETERMINANTS OF HEALTH EXAMPLES
# =============================================================================

SDOH_EXAMPLES = [
    ExampleData(
        text="""Facilitator: How do living conditions affect health in your area?

P1: Housing is a disaster. The apartments are old, there's mold everywhere,
and the landlords don't fix anything. My kids have asthma, and I'm sure the
mold makes it worse. But I can't afford to move.

P2: We have lead paint in our building. The health department came and tested
and said there's lead, but nothing happened. My son's lead levels were elevated
at his last checkup. I'm terrified about what this is doing to him.

P3: The neighborhood itself is the problem. There's no safe place for kids
to play. The one park is taken over by drug dealers. So kids stay inside,
play video games, and get overweight. Then everyone blames the parents.

P1: And there's violence. I've heard gunshots. You don't walk around at night.
The stress of living like this - it affects your mental health, your sleep,
everything.

P2: What we need is investment in this community. Clean up the buildings,
fix the streets, make it safe. Health starts with where you live.""",
        extractions=[
            Extraction(
                extraction_class="housing_issue",
                extraction_text="The apartments are old, there's mold everywhere, and the landlords don't fix anything",
                attributes={
                    "participant": "P1",
                    "sdoh_category": "neighborhood_environment",
                    "issue_type": "housing_quality",
                    "health_impact": "asthma",
                },
            ),
            Extraction(
                extraction_class="environmental_factor",
                extraction_text="My kids have asthma, and I'm sure the mold makes it worse",
                attributes={
                    "participant": "P1",
                    "health_domain": "environmental_health",
                    "hazard": "mold",
                    "affected_population": "children",
                },
            ),
            Extraction(
                extraction_class="environmental_factor",
                extraction_text="We have lead paint in our building",
                attributes={
                    "participant": "P2",
                    "sdoh_category": "neighborhood_environment",
                    "hazard": "lead",
                    "severity": "critical",
                    "affected_population": "children",
                },
            ),
            Extraction(
                extraction_class="health_concern",
                extraction_text="My son's lead levels were elevated at his last checkup",
                attributes={
                    "participant": "P2",
                    "health_domain": "environmental_health",
                    "condition": "lead_poisoning",
                    "affected_population": "children",
                    "severity": "high",
                },
            ),
            Extraction(
                extraction_class="safety_concern",
                extraction_text="There's no safe place for kids to play. The one park is taken over by drug dealers",
                attributes={
                    "participant": "P3",
                    "sdoh_category": "neighborhood_environment",
                    "issue_type": "lack_of_safe_spaces",
                    "affected_population": "children",
                },
            ),
            Extraction(
                extraction_class="health_behavior",
                extraction_text="kids stay inside, play video games, and get overweight",
                attributes={
                    "participant": "P3",
                    "health_domain": "physical_activity",
                    "behavior_type": "sedentary",
                    "cause": "unsafe_neighborhood",
                    "health_outcome": "obesity",
                },
            ),
            Extraction(
                extraction_class="safety_concern",
                extraction_text="there's violence. I've heard gunshots. You don't walk around at night",
                attributes={
                    "participant": "P1",
                    "sdoh_category": "neighborhood_environment",
                    "issue_type": "violence",
                    "severity": "high",
                },
            ),
            Extraction(
                extraction_class="insight",
                extraction_text="The stress of living like this - it affects your mental health, your sleep, everything",
                attributes={
                    "participant": "P1",
                    "health_domain": "mental_health",
                    "cause": "neighborhood_conditions",
                    "impact": "chronic_stress",
                },
            ),
            Extraction(
                extraction_class="community_suggestion",
                extraction_text="What we need is investment in this community. Clean up the buildings, fix the streets, make it safe",
                attributes={
                    "participant": "P2",
                    "sdoh_category": "neighborhood_environment",
                    "suggestion_type": "infrastructure_investment",
                    "priority": "high",
                },
            ),
            Extraction(
                extraction_class="insight",
                extraction_text="Health starts with where you live",
                attributes={
                    "participant": "P2",
                    "category": "sdoh_awareness",
                    "sdoh_category": "neighborhood_environment",
                },
            ),
        ],
    ),
]

# =============================================================================
# HEALTHCARE ACCESS AND TRUST EXAMPLES
# =============================================================================

HEALTHCARE_ACCESS_EXAMPLES = [
    ExampleData(
        text="""Facilitator: What's your experience with healthcare providers?

P1: I feel like doctors don't listen to me. I tell them my symptoms and they
just rush through the appointment. Last time I was in pain and the doctor
basically said it was in my head. I felt dismissed.

P2: Being treated differently because of how you look or where you're from
is real. My accent - sometimes I feel like providers don't take me seriously.
I have to bring my daughter to translate and advocate for me.

P3: Trust is a big issue. After what happened to my uncle - he went to the
hospital with chest pain and they sent him home, said it was anxiety. He
had a heart attack the next day. Now my family doesn't trust hospitals.

P1: That's why people in our community don't go to the doctor until it's
an emergency. We've learned not to trust the system.

P2: We need doctors who look like us, who understand our culture, who speak
our language. That would make such a difference.""",
        extractions=[
            Extraction(
                extraction_class="healthcare_experience",
                extraction_text="doctors don't listen to me",
                attributes={
                    "participant": "P1",
                    "experience_type": "negative",
                    "issue": "poor_communication",
                },
            ),
            Extraction(
                extraction_class="care_quality",
                extraction_text="the doctor basically said it was in my head. I felt dismissed",
                attributes={
                    "participant": "P1",
                    "quality_issue": "dismissive_care",
                    "impact": "distrust",
                    "sentiment": "negative",
                },
            ),
            Extraction(
                extraction_class="barrier_to_care",
                extraction_text="Being treated differently because of how you look or where you're from",
                attributes={
                    "participant": "P2",
                    "barrier_type": "discrimination",
                    "sdoh_category": "healthcare_access",
                },
            ),
            Extraction(
                extraction_class="cultural_factor",
                extraction_text="I have to bring my daughter to translate and advocate for me",
                attributes={
                    "participant": "P2",
                    "issue_type": "language_barrier",
                    "coping_mechanism": "family_translation",
                    "sdoh_category": "healthcare_access",
                },
            ),
            Extraction(
                extraction_class="trust_issue",
                extraction_text="he went to the hospital with chest pain and they sent him home, said it was anxiety. He had a heart attack the next day",
                attributes={
                    "participant": "P3",
                    "event_type": "misdiagnosis",
                    "outcome": "adverse_event",
                    "severity": "critical",
                },
            ),
            Extraction(
                extraction_class="trust_issue",
                extraction_text="Now my family doesn't trust hospitals",
                attributes={
                    "participant": "P3",
                    "impact": "healthcare_avoidance",
                    "cause": "negative_experience",
                },
            ),
            Extraction(
                extraction_class="insight",
                extraction_text="people in our community don't go to the doctor until it's an emergency",
                attributes={
                    "participant": "P1",
                    "health_behavior": "delayed_care",
                    "cause": "distrust",
                    "impact": "late_presentation",
                },
            ),
            Extraction(
                extraction_class="unmet_need",
                extraction_text="We need doctors who look like us, who understand our culture, who speak our language",
                attributes={
                    "participant": "P2",
                    "need_type": "workforce_diversity",
                    "sdoh_category": "healthcare_access",
                    "priority": "high",
                },
            ),
        ],
    ),
]

# =============================================================================
# MATERNAL AND CHILD HEALTH EXAMPLES
# =============================================================================

MATERNAL_CHILD_HEALTH_EXAMPLES = [
    ExampleData(
        text="""Facilitator: Let's talk about health needs of mothers and children.

P1: When I was pregnant, I couldn't find an OB who was taking new patients.
I was four months along before I got my first prenatal visit. That's scary
when you're high-risk.

P2: The hospital where I delivered was 45 minutes away. When I went into
labor early, I was terrified we wouldn't make it. We need a birthing center
closer to home.

P3: After the baby came, I struggled with postpartum depression. Nobody
checked on me. All the focus was on the baby. I felt invisible and alone.
I wish someone had asked how I was really doing.

P1: Childcare is another issue. I want to take my kids to well-child visits,
but I can't take time off work and there's no evening or weekend appointments.
So they miss their shots.

P2: Our school doesn't have a nurse. If a kid gets sick or hurt, they just
call us to pick them up. What if it's something serious?""",
        extractions=[
            Extraction(
                extraction_class="access_issue",
                extraction_text="I couldn't find an OB who was taking new patients",
                attributes={
                    "participant": "P1",
                    "health_domain": "maternal_child_health",
                    "issue_type": "provider_shortage",
                    "specialty": "obstetrics",
                },
            ),
            Extraction(
                extraction_class="barrier_to_care",
                extraction_text="I was four months along before I got my first prenatal visit",
                attributes={
                    "participant": "P1",
                    "health_domain": "maternal_child_health",
                    "barrier_type": "appointment_availability",
                    "consequence": "delayed_prenatal_care",
                    "severity": "high",
                },
            ),
            Extraction(
                extraction_class="resource_gap",
                extraction_text="The hospital where I delivered was 45 minutes away",
                attributes={
                    "participant": "P2",
                    "health_domain": "maternal_child_health",
                    "gap_type": "facility_distance",
                    "service_type": "labor_delivery",
                },
            ),
            Extraction(
                extraction_class="unmet_need",
                extraction_text="We need a birthing center closer to home",
                attributes={
                    "participant": "P2",
                    "health_domain": "maternal_child_health",
                    "need_type": "facility",
                    "priority": "high",
                },
            ),
            Extraction(
                extraction_class="health_concern",
                extraction_text="I struggled with postpartum depression",
                attributes={
                    "participant": "P3",
                    "health_domain": "maternal_child_health",
                    "condition": "postpartum_depression",
                    "severity": "high",
                },
            ),
            Extraction(
                extraction_class="care_quality",
                extraction_text="Nobody checked on me. All the focus was on the baby",
                attributes={
                    "participant": "P3",
                    "quality_issue": "inadequate_postpartum_support",
                    "health_domain": "maternal_child_health",
                },
            ),
            Extraction(
                extraction_class="barrier_to_care",
                extraction_text="I can't take time off work and there's no evening or weekend appointments",
                attributes={
                    "participant": "P1",
                    "barrier_type": "scheduling",
                    "consequence": "missed_well_child_visits",
                    "sdoh_category": "healthcare_access",
                },
            ),
            Extraction(
                extraction_class="resource_gap",
                extraction_text="Our school doesn't have a nurse",
                attributes={
                    "participant": "P2",
                    "gap_type": "school_health_services",
                    "affected_population": "children",
                    "setting": "school",
                },
            ),
        ],
    ),
]

# =============================================================================
# COMMUNITY STRENGTHS AND ASSETS EXAMPLES
# =============================================================================

COMMUNITY_STRENGTHS_EXAMPLES = [
    ExampleData(
        text="""Facilitator: What strengths does your community have?

P1: We look out for each other. When my neighbor was sick, we brought her
food and checked on her every day. That's how we were raised - to take
care of each other.

P2: The church is the heart of this community. They do health fairs, food
drives, exercise classes. It's where people go for support when they're
struggling.

P3: We have some great community health workers - promotoras - who go
door to door helping people understand their health conditions and how
to manage them. They speak our language and they get it.

P1: The senior center is wonderful too. My mother goes there for lunch
and to socialize. They check her blood pressure and remind her about her
medications. It's keeping her healthy and connected.

P2: If we could build on these strengths - get more funding for the
community programs that work - we'd see real improvements in health.""",
        extractions=[
            Extraction(
                extraction_class="community_strength",
                extraction_text="We look out for each other",
                attributes={
                    "participant": "P1",
                    "strength_type": "social_cohesion",
                    "sdoh_category": "social_community",
                },
            ),
            Extraction(
                extraction_class="social_support",
                extraction_text="When my neighbor was sick, we brought her food and checked on her every day",
                attributes={
                    "participant": "P1",
                    "support_type": "informal_caregiving",
                    "sdoh_category": "social_community",
                },
            ),
            Extraction(
                extraction_class="community_strength",
                extraction_text="The church is the heart of this community. They do health fairs, food drives, exercise classes",
                attributes={
                    "participant": "P2",
                    "strength_type": "faith_based_support",
                    "services": "health_education,food_assistance,physical_activity",
                    "sdoh_category": "social_community",
                },
            ),
            Extraction(
                extraction_class="community_strength",
                extraction_text="community health workers - promotoras - who go door to door helping people understand their health conditions",
                attributes={
                    "participant": "P3",
                    "strength_type": "community_health_workers",
                    "service": "health_education",
                    "cultural_competency": "high",
                },
            ),
            Extraction(
                extraction_class="community_strength",
                extraction_text="The senior center is wonderful",
                attributes={
                    "participant": "P1",
                    "strength_type": "senior_services",
                    "services": "meals,social,health_monitoring",
                    "affected_population": "elderly",
                },
            ),
            Extraction(
                extraction_class="community_suggestion",
                extraction_text="If we could build on these strengths - get more funding for the community programs that work",
                attributes={
                    "participant": "P2",
                    "suggestion_type": "program_expansion",
                    "approach": "asset_based",
                    "priority": "high",
                },
            ),
        ],
    ),
]

# =============================================================================
# CHRONIC DISEASE MANAGEMENT EXAMPLES
# =============================================================================

CHRONIC_DISEASE_EXAMPLES = [
    ExampleData(
        text="""Facilitator: How do people manage chronic conditions like diabetes?

P1: Managing diabetes is a full-time job. Testing blood sugar, counting carbs,
taking medications, going to appointments. It's exhausting and expensive.
The test strips alone cost me $100 a month.

P2: My husband has diabetes and heart disease. He's supposed to eat healthy
and exercise, but after working two jobs he's too tired. And the healthy food
costs twice as much as the junk food.

P3: Education is the problem. When my father was diagnosed, nobody explained
what diabetes actually means or what he should do. He just got a prescription
and was sent home. He didn't change anything because he didn't understand.

P1: We need more diabetes education in the community - in Spanish, at times
when working people can attend. The classes at the hospital are during
work hours.

P2: And support groups. My husband feels alone with this. If he could talk
to other men managing diabetes, it would help.""",
        extractions=[
            Extraction(
                extraction_class="health_condition",
                extraction_text="Managing diabetes is a full-time job",
                attributes={
                    "participant": "P1",
                    "health_domain": "chronic_disease",
                    "condition": "diabetes",
                    "burden": "high",
                },
            ),
            Extraction(
                extraction_class="economic_factor",
                extraction_text="The test strips alone cost me $100 a month",
                attributes={
                    "participant": "P1",
                    "barrier_type": "cost_of_supplies",
                    "health_domain": "chronic_disease",
                    "sdoh_category": "economic_stability",
                },
            ),
            Extraction(
                extraction_class="barrier_to_care",
                extraction_text="after working two jobs he's too tired",
                attributes={
                    "participant": "P2",
                    "barrier_type": "time_constraints",
                    "cause": "employment_demands",
                    "impact": "unable_to_exercise",
                },
            ),
            Extraction(
                extraction_class="food_access",
                extraction_text="the healthy food costs twice as much as the junk food",
                attributes={
                    "participant": "P2",
                    "sdoh_category": "economic_stability",
                    "barrier_type": "cost",
                    "health_domain": "nutrition",
                },
            ),
            Extraction(
                extraction_class="care_quality",
                extraction_text="nobody explained what diabetes actually means or what he should do. He just got a prescription and was sent home",
                attributes={
                    "participant": "P3",
                    "quality_issue": "inadequate_education",
                    "health_domain": "chronic_disease",
                    "consequence": "poor_disease_management",
                },
            ),
            Extraction(
                extraction_class="unmet_need",
                extraction_text="We need more diabetes education in the community - in Spanish, at times when working people can attend",
                attributes={
                    "participant": "P1",
                    "need_type": "health_education",
                    "health_domain": "chronic_disease",
                    "requirements": "language_accessible,convenient_scheduling",
                    "priority": "high",
                },
            ),
            Extraction(
                extraction_class="unmet_need",
                extraction_text="support groups. My husband feels alone with this",
                attributes={
                    "participant": "P2",
                    "need_type": "peer_support",
                    "health_domain": "chronic_disease",
                    "affected_population": "men_with_diabetes",
                },
            ),
        ],
    ),
]

# =============================================================================
# MENTAL HEALTH AND SUBSTANCE USE EXAMPLES
# =============================================================================

MENTAL_HEALTH_EXAMPLES = [
    ExampleData(
        text="""Facilitator: Can we talk about mental health in your community?

P1: Mental health is the silent epidemic. Everyone is struggling but nobody
admits it. There's so much shame around depression and anxiety in our culture.
You're supposed to be strong, not ask for help.

P2: The opioid crisis hit us hard. I've lost two cousins to overdoses.
It started with prescriptions for pain after injuries, then spiraled.
Now people are using fentanyl and dying.

P3: For young people, it's anxiety and depression. My daughter's friends
talk about cutting and suicide. The school counselor has 500 students -
there's no way she can help everyone who needs it.

P1: We need more counselors, more programs, and we need to talk about this
openly. The stigma is killing people - literally.

P2: And treatment for addiction that's affordable and available. The one
rehab center has a six-month waiting list. By then it's too late for
many people.""",
        extractions=[
            Extraction(
                extraction_class="health_concern",
                extraction_text="Mental health is the silent epidemic",
                attributes={
                    "participant": "P1",
                    "health_domain": "mental_health",
                    "severity": "high",
                    "prevalence": "widespread",
                },
            ),
            Extraction(
                extraction_class="cultural_factor",
                extraction_text="There's so much shame around depression and anxiety in our culture. You're supposed to be strong, not ask for help",
                attributes={
                    "participant": "P1",
                    "health_domain": "mental_health",
                    "barrier_type": "stigma",
                    "cultural_factor": "mental_health_stigma",
                },
            ),
            Extraction(
                extraction_class="health_concern",
                extraction_text="The opioid crisis hit us hard. I've lost two cousins to overdoses",
                attributes={
                    "participant": "P2",
                    "health_domain": "substance_use",
                    "issue": "opioid_epidemic",
                    "severity": "critical",
                    "impact": "mortality",
                },
            ),
            Extraction(
                extraction_class="insight",
                extraction_text="It started with prescriptions for pain after injuries, then spiraled",
                attributes={
                    "participant": "P2",
                    "health_domain": "substance_use",
                    "pathway": "prescription_to_addiction",
                },
            ),
            Extraction(
                extraction_class="health_concern",
                extraction_text="For young people, it's anxiety and depression",
                attributes={
                    "participant": "P3",
                    "health_domain": "mental_health",
                    "affected_population": "youth",
                    "conditions": "anxiety,depression",
                },
            ),
            Extraction(
                extraction_class="health_concern",
                extraction_text="My daughter's friends talk about cutting and suicide",
                attributes={
                    "participant": "P3",
                    "health_domain": "mental_health",
                    "affected_population": "youth",
                    "issues": "self_harm,suicidal_ideation",
                    "severity": "critical",
                },
            ),
            Extraction(
                extraction_class="resource_gap",
                extraction_text="The school counselor has 500 students - there's no way she can help everyone who needs it",
                attributes={
                    "participant": "P3",
                    "gap_type": "workforce_shortage",
                    "setting": "school",
                    "service_type": "mental_health",
                },
            ),
            Extraction(
                extraction_class="barrier_to_care",
                extraction_text="The one rehab center has a six-month waiting list",
                attributes={
                    "participant": "P2",
                    "health_domain": "substance_use",
                    "barrier_type": "wait_time",
                    "service_type": "addiction_treatment",
                    "wait_time": "6 months",
                },
            ),
        ],
    ),
]

# =============================================================================
# EXAMPLE PRESETS MAPPING
# =============================================================================

EXAMPLE_PRESETS = {
    "comprehensive": COMPREHENSIVE_HEALTH_EXAMPLES,
    "sdoh": SDOH_EXAMPLES,
    "healthcare_access": HEALTHCARE_ACCESS_EXAMPLES,
    "maternal_child": MATERNAL_CHILD_HEALTH_EXAMPLES,
    "community_strengths": COMMUNITY_STRENGTHS_EXAMPLES,
    "chronic_disease": CHRONIC_DISEASE_EXAMPLES,
    "mental_health": MENTAL_HEALTH_EXAMPLES,
}


def get_examples(preset: str = "comprehensive") -> list[ExampleData]:
  """Get predefined examples for a specific analysis type.

  Args:
    preset: The type of analysis. Options are:
      - "comprehensive": Full health assessment analysis
      - "sdoh": Social determinants of health focus
      - "healthcare_access": Healthcare access and trust issues
      - "maternal_child": Maternal and child health focus
      - "community_strengths": Community assets and strengths
      - "chronic_disease": Chronic disease management
      - "mental_health": Mental health and substance use

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
