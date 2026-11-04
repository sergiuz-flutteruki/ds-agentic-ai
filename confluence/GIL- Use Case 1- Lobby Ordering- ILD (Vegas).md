# GIL: Use Case 1: Lobby Ordering: ILD \(Vegas\)

## 📂 Document Summary

| **Initiative** | GIL: Use Case 1: Lobby Ordering |
| --- | --- |
| **Jira GAMX Link** | [GAMDISC-617](https://jira.services.flutteruki.com/browse/GAMDISC-617) |
| **GET Workstream** |  |
| **Desired Delivery Date** | mid-October |
| [**Product Delivery Lifecycle Stage**](https://betfairprod.sharepoint.com/:p:/s/IM-flutterukidelivery/EZVHM28hpApBpdZ6vhEI22ABO2SHVKrbBfUXaB42hywMnQ?e=HK9406) | BUILD |
| **Product Manager** | @Matthew Mosley |
| **Product Owner** | @Diana Pupeza@Bianca Marincas |
| **Delivery Lead** | @Ingrid-Andreea Gavris |
| **Technical Lead** | @Cristian Calacianu@Andrei Berinde@Camelia-Maria Santoma@Seb Goring |

## 📰 Initiative Summary

| **Deliverable Description** |
| --- |
| This is the first use-case of the Gaming Intelligence Layer (GIL) and is a way of automatically ordering zones on the homepage, meaning the order of content is personalised per customer instead of a ‘one size fits all' approachThe model must be built in a way that supports the wider GIL ecosystem, which is defined [here](https://flutteruki.atlassian.net/wiki/spaces/GAM/pages/2635431960/GIL+Front-End+Requirements) |

| **Deliverable Type** |  |
| --- | --- |
| [**UKI OKR Alignment**](https://flutterglobal.interactgo.com/page/flutterukione#h-2024-OBJECTIVES-OUR--3) |  |
| [**Portfolio Category**](https://flutteruki.atlassian.net/wiki/spaces/FU/pages/495225645/Body+Of+Knowledge) |  |
| **Need** | To provide users with a custom homepage zone order |

---

The **Latest Status Report** is a summary for a Deliverable. 

- Think of it as the ‘Executive Summary’, providing an overview of what’s just happened (now) and what’s about to happen (next). It includes the trajectory of the work and action required from stakeholders. 
- If you’ve got more detailed information held somewhere else, link to it and avoid duplication. 
- Make sure to keep this up to date, and it draws the attention of the reader to key information and the action you require of them (or not). 

### ℹ️ Section Owner

|  |  |  |  |
| --- | --- | --- | --- |
| **Who** | Name // Role | **Section Status** | TO DOIN PROGRESSDONE |

## Overview

If a Deliverable is Amber or Red, include a summary of why it is Amber or Red, and the activities enabling its [Path to Green](https://flutteruki.atlassian.net/wiki/spaces/FU/pages/495225645/Body+Of+Knowledge).

| [**Phase**](https://flutteruki.atlassian.net/wiki/spaces/FU/pages/495225645/Body+Of+Knowledge) | [**RAG Status / Trend**](https://flutteruki.atlassian.net/wiki/spaces/FU/pages/495225645/Body+Of+Knowledge) | **Updated by ** | **Last Updated date** |
| --- | --- | --- | --- |
| VALIDATE |  | *Name* | *Date* |

| **Update Summary** |
| --- |
| *A short summary of whats happening with a deliverable right now. This should highlight any key items of interest, imminent deliverables, risks or issues.​* |


## Progress

| **Done this Period** | **Planned For Next Period** |
| --- | --- |
| - *Key items done this period​* | - *Key items planned for the next period* |


## Bigger Picture and Milestones

| **Upcoming Milestones** | **Date** | [**RAG Status**](https://flutteruki.atlassian.net/wiki/spaces/FU/pages/495225645/Body+Of+Knowledge) |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |


## Top 3 Risks

Risk are items that have the potential to impact a deliverable or other related deliverables.

These are the Top 3 Risks impacting this deliverable right now. 

Please refer to the RAID link within the **Delivery tab** for the full list of Risks.

| **Risk ** | **Update** | **Owner** | [**RAG Status**](https://flutteruki.atlassian.net/wiki/spaces/FU/pages/495225645/Body+Of+Knowledge) |
| --- | --- | --- | --- |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |


## Top 3 Issues

Issues are items that are impacting a deliverable or other related deliverables.

These are the Top 3 Issues impacting this deliverable right now. 

Please refer to the RAID link within the **Delivery tab** for the full list of Issues.

| **Issue** | **Update** | **Owner** | [**RAG Status**](https://flutteruki.atlassian.net/wiki/spaces/FU/pages/495225645/Body+Of+Knowledge) |
| --- | --- | --- | --- |
| *Issue description * | *Latest update* | *Name* |  |
| *Issue description * | *Latest update* | *Name* | AMBER |
| *Issue description * | *Latest update* | *Name* | AMBER |


The **Brief **is a summary of the business problem or user need a deliverable is attempting to solve. 

- It should contain the minimum amount of information required to decide if something is worth investing time and energy in. 
- Don’t go into detail about the solution here, just provide enough information for an investment decision to be made. 
- As you learn more, positive or negative, update this page with a summary, you can always return here and update it. 
- Decisions can always be changed when we learn more. 

### ℹ️ Section Owner

|  |  |  |  |
| --- | --- | --- | --- |
| **Who** | Name // Role | **Section Status** | TO DOIN PROGRESSDONE |

## What Problem are we trying to solve? 

Avoid specifying potential solutions or how something needs to work, focus on the Problem.

Our homepages are manually created meaning the order of all content is the same for everyone. This is a problem, as users are not being shown the most engaging and relevant swimlanes early enough in the lobby, leading to missed clicks, reduced game discovery, and suboptimal conversion into gameplay. This can be broken down into the following:

1. **Players aren’t consistently finding content that interests them quickly**
    - Swimlanes are currently ordered manually in a ‘one size fits all’ approach
    - High-interest content can be buried too far down the page
2. **Attention is being wasted on low-performing rows**
    - Users have limited time and scroll depth, so we want to improve their time on site by showing the most relevant content first
    - Lower CTR swimlanes consume valuable above the fold real estate
3. **The lobby isn’t adapting to actual user behaviour**
    - Current ordering doesn’t reflect what users are *actually clicking*
    - Our customer base is interested in a wide variety of games, meaning the ‘one size fits all’ approach isn’t optimal
4. **Commercial performance is being left on the table**
    - If users don’t click into games, they can’t convert to play into revenue
    - Poor ordering leads to fewer game launches which leads to lower monetisation

## How big is the Problem? What is the impact if the Problem is not solved? 

What is scale of the Problem if left unaddressed? Consider the impact on all customers/users, groups of customers/users and internally within Flutter and it’s brands if this Problem is not solved.  

**Most users never see most of our content**

- The average visit to the Sky Vegas homepage will scroll down 35% (reaching the Live Dealer zone)
- 69% of monthly customers will scroll to at least 35% (or more)
- Anything below that is effectively invisible real estate

If our ordering is manual, we’re:

- Wasting premium real estate
- Suppressing high-performing content
- Over-exposing low-performing rows

---

1. **Small CTR changes compound quickly**

The vast majority of clicks on the homepage are on the top 1-2 rows, if we improve clicks into games on the top 1-2 spots by just 1-2%, that translates into:

- Tens of thousands of additional clicks
- Which flow into more game launches
- Which flow into real money (stakes, GGR, etc.)

Because this sits at the top of the funnel, even small gains cascade.

---

1. **It affects *****every***** user, *****every***** session**

This isn’t a niche feature:

- Every logged-in user sees the lobby
- Every session involves some form of browsing or re-entry

So the impact is:

> High frequency × large user base = large total effect

---

1. **Generic ordering creates hidden opportunity cost**

The real risk isn’t just “bad performance”, it’s missed upside:

- High-value users may not discover games they would have staked on
- New or promoted content may underperform due to poor placement
- Personalisation/recommenders get handicapped by weak exposure

This is especially painful as we’re already investing in:

- “Because you played”
- “We think you’ll like”
- “Trending”

If those rows aren’t surfaced well, their value is diluted. We already know these rows increase SPU and have strong Commercial value, so exposing them higher on the homepage should have a positive impact.

---

### What happens if we don’t fix it

Left unaddressed, we’re likely to see:

- Flat or declining engagement, despite adding more content
- Diminishing returns on new game releases
- Over-reliance on a small set of visible games
- Lower lifetime value
- Difficulty proving value of recommendation models (because exposure is flawed)

In short:

> We’re optimising *what* to show, but failing to optimise *where* it’s shown.

## Does this Problem have a Regulatory or Compliance impact? 

Does addressing this Problem have a Regulatory or Compliance Impact? Or does addressing the Problem help to avoid one? 

No to my knowledge.

## Potential Solution

In as few words as possible, define what a potential solution Would Do, and Would Not Do. This helps us to understand a high-level scope early on, without being too prescriptive. 

| #### **What it Does** | #### **What it Doesn’t Do** |
| --- | --- |
| **Lobby Ordering:** - We will build a Data Recommender model that orders the swimlanes by click-through rate, more details on this are in the ‘High level requirements’ section |  |
| **Bigger Picture (GIL):** - This is the first use-case of the Gaming Intelligence Layer (GIL) and is a way of automatically ordering zones on the homepage, meaning the order of content is personalised per customer instead of a ‘one size fits all' approach - The model must be built in a way that supports the wider GIL ecosystem, which are defined [here](https://flutteruki.atlassian.net/wiki/spaces/GAM/pages/2635431960/GIL+Front-End+Requirements) **Spirit statement: **The goal with GIL is to build towards a suite of personalisation models that contribute to, and draw upon, a shared understanding of the customer. Lobby ordering is the first use case — how we build it should facilitate sharing what is learnt by the system with future use cases. | - Built in a way that doesn’t contribute to GIL |
| **Product and Channel:** - For this piece of work, we will be focussing on Sky Vegas mobile-web and desktop only - Native to be considered at a later date but ideally brought into this project to consult and learn early for any specific requirements | - Include any other pages, navigation, game tile creative or game names - Launch on Native - Launch on any other brand |
|  |  |


## Hypothesis, Goals and Success Measures 

If the Problem was solved, what would be the impact, and what metrics could we used to measure this? These could be high-level financial benefits, risk avoidance, changes in customer behaviour, new learnings gained or something else. Consider the insights you are basing this on.

- *How will you measure success?*
    - Success will be measured via experimentation. When launching, we will run an AB test to look at Control (current static lobby) vs Variant 1 (Lobby Ordering)
- *What metrics will you use?*
    - Primary Metric:
        - Page View to Game Launch %

      Guardrail Metric:
        - Time to first Game Launch

      Secondary Metric:
        - Play Engagement Rate (Login to Stake%)
        - Game Launch to Stake %
        - Average stakes per user
        - Average stakes per game launch

      + Full suite of Product metrics to be analysed due to size of project.
- *What is this based on?*
    - Discovery tribe and value stream metrics
- *How soon will you know, and what signals will you receive?*
    - Once experiment is finished
- *What will the signals be to stop?*
    - Decision to rollout or not will be reviewed once experiment is complete





The **Benefits **tab is the place to summarise what addressing a problem or need, or making progress towards delivers. 

- Consider what metrics and measures will move as a result of the project or deliverable. 
- As a deliverable progresses, teams will learn more about problems and needs. 
- It’s ok to return to this to update it, as you know more about the measures and what you can realistically achieve, and what you know about the deliverables to meet these needs.  

### ℹ️ Section Owner

|  |  |  |  |
| --- | --- | --- | --- |
| **Who** | Name // Role | **Section Status** | TO DOIN PROGRESSDONE |

## Benefit Metrics and Measures

What benefits will delivering a solution to address this problem provide? These will be used to assess the success of an Initiative and of it’s final implementation. If you have a benefits tracker, include a link to it (optional).

- 


This is a place to outline any **Designs **to support this work.

- It’s ok to return to this to update this. 
- If you have designs and assets stored elsewhere, link to them to avoid duplication. 

### ℹ️ Section Owner

|  |  |  |  |
| --- | --- | --- | --- |
| **Who** | Name // Role | **Section Status** | TO DOIN PROGRESSDONE |

## Designs

Link to Designs and artefacts to support this deliverable.

| **Designs** | **Links** |
| --- | --- |
| N/A |  |
|  |  |

**Validation **is an opportunity to increase your confidence in the problem or need, your proposed solutions. 

- Validation is lets a deliverable articulate with growing confidence what and who is needed to Validate the investment case, and once completed what is needed to ‘deliver the thing' based on what we know now. 
- It should contain the minimum amount of information required to validate a project or deliverable is the right thing to do based on what we know now. 
- As you learn more, positive or negative update this page with a summary, you can always return here and update it. Decisions can always be changed when we learn more. 
- It’s also a place to record the decision on if it proceeds (or doesn't) and the rationale. 

### ℹ️ Section Owner

|  |  |  |  |
| --- | --- | --- | --- |
| **Who** | Name // Role | **Section Status** | TO DOIN PROGRESSDONE |

## Validation

### Steps to Validate

What are the steps needed to validate the Problem, narrow down solutions and their scope? Think of this as your validation method. This could include which stakeholders to engage with, technologies to investigate or user research to be conducted.

- *Set out the steps of what needs to happen to learn more.*

### People, Resources and Support to Validate

Who and what do you need to validate the Problem and narrow down solutions and their scope?

- *Teams*
- *Roles*
- *Individuals *
- *Skills*

## Move to Solutions

### Current State

What is the current state of our products, technologies, user journeys or customer experiences that create the Problem situation?

- *Define it, draw it, explain it.*

### End State

By overcoming the Problem, how will our products, technologies, user journeys or customer experiences change based on the solutions and their scope?

- *Define it, draw it, explain it.*

### Architecture Engagement

Have you engaged with and sought feedback from Architecture colleagues to understand the potential solutions to resolving the problem described?

- *Who did you talk to?*
- *What was their feedback?*

## What’s Needed to Deliver? 

### Required Teams

Confirm which Teams you think will be needed to deliver this.

| **Tribe** | **X-Tribe Request (Yes/No)** | **Required Team (if known)** | **Latest Status / Approval Details** |
| --- | --- | --- | --- |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |

### Key Deliverables & Sizing

To deliver the solutions, what key deliverables exist and what do we know about this work?

| **What order does the work need delivering? ** | **Who will do the work? ****Team or Tribe name if known** | **How big is the work based on what we know now?****See **[**T-Shirt Sizes**](https://flutteruki.atlassian.net/wiki/spaces/FU/pages/495225645/Body+Of+Knowledge) | **Can this work be done in parallel with other deliverables, does it have dependencies and pre-requisites?** |
| --- | --- | --- | --- |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |

### Delivery Sequencing Diagram

How might delivering this initiative look? What is the ideal sequence of deliverables, and what dependencies exist? 

- *Define it, draw it, explain it.*

### Dependencies on other Deliverables

Will this deliverable be dependant or reliant on another deliverable, which could blocks it or prevents it progressing? If so raise a line item within the GET RAID register and then insert the link to the item(s) within the below table. 

<https://flutteruki.atlassian.net/wiki/spaces/BEGFE/database/854721767>

| **Deliverable Name and Link (if known)** | **Estimated Completion Date (if known)** | **Delivery Lead** | **Reason for Dependency** |
| --- | --- | --- | --- |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |

### Product / Tech / Design / Delivery Debt

As a result of the determined product scope and technical solution, are we cinciously acrewing any debt. If so, raise a line item within the GET Debt Register so that this is visualised and transparent, then link to the item(s) within the below table. 

[Product / Tech / Design / Delivery Debt](https://flutteruki.atlassian.net/wiki/spaces/BEGFE/pages/881459884/Product+Tech+Design+Delivery+Debt)

<https://flutteruki.atlassian.net/wiki/spaces/BEGFE/database/885194959>


| **Item** |
| --- |
|  |
|  |

## Post Validation Recommendations

Based on what we know about the Problem and what we’ve found through Validation, what is the recommendation?

### Decision (Proceed or Not)

- *Should this work go ahead or not?*
- *What is the rational and reasoning?*
- *Are there any other conditions which apply to this decision that might result in it being reviewed? *

### Approval

Please include any additional stakeholders and/or leadership team members that were present that aren't already listed below to approve the above decision.

| **Name** | **Role** | **Date** |
| --- | --- | --- |
| *Name* | (Product role) | *Date* |
| *Name* | (Engineering role) | *Date* |
| *Name* | (Delivery role) | *Date* |

This is a place to outline your **Requirements**. 

- If you have requirements and information stored elsewhere, link to them to avoid duplication. 

### ℹ️ Section Owner

|  |  |  |  |
| --- | --- | --- | --- |
| **Who** | Name // Role | **Section Status** | TO DOIN PROGRESSDONE |

## Requirements

Based on Initiative validation, scope and learnings, what requirements will be delivered?

**High Level Requirements - All ‘Must have’ requirements for MVP LO**

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| #### **ID** | #### **Reference** | #### **Requirement** | **Data Science** | **Data Engineering** | **Gaming Front-end** |
| 1 | Product / Channel | - Sky Vegas - Mobile Web (including Android wrapper app) & Desktop - Native iOS to be considered at a later date but brought into this project to consult and learn early for any specific requirements | - X | - X | - X |
| 2 | Data / User account | - User must have a UKI account - Currently based on GA data (roughly 80% accept rate) - This means a user will have to accept cookies in order to see the personalised lobby ordering - If I opt-out of cookies, the lobby order will be manually ordered as it is today     - Post experiment, this will be updated to use information gained from the experiment to create a custom order based on value tiers or similar - If GIL doesn’t return anything, the page will be manually ordered as it is today - When we switch from GA data, the opt-out journey will be not be required | - X | - X | - X |
| 3 | Zones ranked | - All zones with game tiles, including:     1. Featured     2. The Big Drop Widget     3. We Think You’ll Like     4. Continue Playing     5. Trending     6. Live Dealers     7. Because You Played     8. Slots     9. Jackpot King Widget - Excluded for GIL LO for V1     - Promo Carousel     - Prize Machine widget     - Safer Gambling banner     - Seasonal row | - X | - X | - X |
| 4 | Promo Carousel | - This should be fixed in position 1 for all customers - The position will likely be reviewed as part of the experiment go-live and may be tweaked for future iterations |  |  | - X |
| 5 | Prize Machine Widget | - This should be fixed in position 4 for all customers, and removed once played as per current functionality - The position will likely be reviewed as part of the experiment go-live and may be tweaked for future iterations |  |  | - X |
| 6 | Safer Gambling banner | - This will be displayed in a static position for all users in position 8 (where it is currently) |  |  | - X |
| 6.1 | Confirmed row ordering | Here’s a summary of all homepage zones and whether they’re controlled via GIL or manually fixed: 1. Promo Carousel - fixed 2. GIL LO spot 1 3. GIL LO spot 2 4. PM widget - fixed (disappears once played) 5. GIL LO spot 3 6. Continue Playing - Fixed 7. GIL LO spot 5 8. Safer Gambling module - fixed 9. GIL LO spot 6 10. GIL LO spot 7 11. GIL LO spot 8 12. Seasonal row - fixed 13. JPK Row - Fixed |  |  |  |
| 7 | Seasonal row (static) | - This will be a static row placed on the homepage in a set position (2nd from bottom) and not included in the dynamic LO for V1 - The position can’t be changed - This will be added / removed manually by the Content Ops team |  |  | - X |
| 8 | New flexible row (static) | - The business will have the ability to create a new row on the homepage in any position. It will stay in position until the business decides to take it down - This row will be ignored by the LO ranking model - Other rows that are included in the LO ranking model will be re-ranked around the set position - More than 1 row can be added at a time |  |  | - X |
| 9 | New permanent row (LO) | - A new permanent row will be manually introduced (by Content Ops) in any position on the homepage - This row will stay in a set position until the ranking model has enough traffic to release it into the lobby ordering flow - The front-end will update on a 7 day cycle (which day TBC) - More than 1 row can be added at a time |  |  | - X |
| 9.1 | Change row status | - If a row is being ordered by GIL LO, there should be a toggle to remove it from GIL LO ranking - without needing to remove and re-add the row, to reduce Prismic admin - Once removed, the position of the row can be manually set within Prismic and will apply for all users - **Sept 8th update:** A manually set row can also be toggled to be ordered via GIL LO, at which time the row will automatically be ordered via the latest data set sent from Data Science |  |  | - X |
| 10 | New experimental row (static) | - A new static row will be manually launched in a set position (by Content Ops), chosen by the business, to compare vs control for the period of the experiment     - Control = no new row     - Variant = new row - The position of this row will not change for the duration of the experiment - Rows around the new static row will be ordered by LO ranker - Once the experiment is over, it’s taken down by Content Ops - Once analysis is over, the new row will fall into the ‘New permanent row (LO)' flow - The new row will be ignored by the LO ranker for the duration of the experiment due to it only being seen by a % of customers as defined by the experiment - therefore likely not being ‘ranked’ as it would be if released to 100%. Hence flowing into ‘New permanent row (LO)’ post experiment |  |  | - X |
| 11 | Experiment on existing row - i.e. update to existing recommender (LO) | - We need the ability to test an update to the logic of an existing row - For this type of test, traffic should be split between control (existing row) and variant(s) (updated logic) for analysis - Post analysis, we should be able to update the zone to the winning variant - Once the winning variant is live, the existing row is updated with the new logic - The existing rank of the row will remain ordered by the LO ranker throughout the duration of the experiment - for both control and variant(s) - Both control and variants will be seen as 1 row by the model |  |  | - X |
| 12 | Logged out experience | - Not impacted by this project, the homepage will display in a manual order defined by the Content Ops team |  |  | - X |
| 13 | Ranking model logic | - We will use ‘Zone view to launch’ + additional user metrics to determine the optimal row order, full data model explanation [here](https://flutteruki.atlassian.net/wiki/spaces/UKIDS/pages/2934441179/Lobby+Ordering) | - X |  |  |
| 14 | Model updates | - The model will train every 7 days | - X |  |  |
| 15 | New Customers | - Will see a default manual order on first login - LO will kick-in when the model updates on a 7 day cycle, if they accepted cookies - If they did not accept cookies, the user will see the manual LO | - X | - X |  |
| 16 | Manual override | - Not required | - N/A | - N/A | - N/A |
| 17 | Reporting requirements | - We must have the ability to see all measurement metrics as per the Product Metric Framework for the following:     - Average position of each game row     - CTR of each row     - CTR of each ‘Homepage order’ for top X orders     - Most common row orders     - Row movement frequency | - X | - X |  |
| 18 | Launch plans | - We will launch via experimentation to a percentage or customers that will be determined nearer the time. AB test setup likely to be as follows:     - Control = Manual order     - Variant A = Lobby Ordering - Standard BI metrics should be available to review post experiment - As the model is updated, we will need to be able to compare each update with a previous version and should adopt an approach similar to item 13 - TBC if we use Statsig (separate workstream to be confirmed nearer the time) |  |  | - X |
| 19 | Ongoing experimentation | We must have the ability to experiment on the homepage for the following experiment types: - **Zone experiments**     - Putting new recommenders live (covered by item 10)     - Putting different versions of existing recommenders live (covered by item 13)     - Putting new UI elements live, i.e. sub-headings under a row (covered by item 10)     - Different UI for promo carousel (covered by item 10)     - Different UI for swimlanes (i.e. trending 1-10 with numbers) (covered by item 10)     - Different UIs for widgets i.e. PM / Live dealer widget (covered by item 10)     - Different row names on the FE (covered by item 10) - **Nav experiments**     - Not impacted by this project - **Experiment anywhere other than on the Homepage i.e. category pages**     - Not impacted by this project - **Experiments on Native app**     - Not impacted by this project - **Game experiments**     - Different RTPs of the same game - not impacted by this project     - Different game tiles - not impacted by this project The following experimentation types are not included in V1 of GIL LO as they’re still being worked on part of a wider experimentation project, and will be reviewed later in the project once fixed and proving value to the business: - **Segmentation**     - Game type preference segmentation inc. high value     - U25s live casino repositioning |  |  | - X |
| 20 | De-duplication on recommenders | - For each data recommendation (WTYL, BYPX and Trending) we need to increase the number of recommendations as follows:     - WTYL → from 20 to 30     - BYPX → from 10 to 20     - Trending → staying at 100 - Reason: De-duplication is enabled for these rows. This means that if a game recommended in the row already appears in another row higher up the page, it will be removed from this row. While this approach works well on a static page, it is less suitable for a dynamic page. As the recommender may be positioned further down the page, more rows are likely to appear above it, increasing the probability that recommended games will be de-duplicated and the row itself may be left with little or no content. - This will be reviewed as part of the experiment and potentially tweaked depending on performance coverage. | - X | - X |  |
| 21 | The Big Drop / Jackpot King widget | - To ensure there’s always a game tile visible at the top of the page, and to ensure a strong UI, both The Big Drop and Jackpot King widgets should not appear in position 1. The highest spots they should be on the homepage is position 2. |  |  | - X |
| 22 | User account look-up | - We should have the ability to input the account ID of an individual user so that we can view the homepage in the exact order that customer sees it based on the latest recommendation run. This will be used for de-bugging purposes. - We should also have the ability to see what games are within each row for individual users as part of this requirement. |  | X | X |
| 23 | The Big Drop / Jackpot King widget | - The JPK widget should be ‘pinned’ to the bottom of the homepage for initial launch and released into GIL LO at a later date - Once released and to ensure a clean UI, we need a rule to ensure that TBD widget and the JPK widget aren’t next to one another |  |  | x |
|  |  |  |  |  |  |

**Functional Requirements**

|  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- |
| #### **Reference** | #### **Requirement** | **In/Out of Scope** | **Squad** | **Acceptance Criteria** | **MoSCoW** | **Jira Link(s)** |
|  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |

**Non-functional Requirements**

|  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- |
| #### **Reference** | #### **Requirement** | **In/Out of Scope** | **Squad** | **Acceptance Criteria** | **MoSCoW** | **Jira Link(s)** |
|  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |

**Data Requirements**

|  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | #### **Reference** | #### **Requirement** | **In/Out of Scope** | **Squad** | **Acceptance Criteria** | **MoSCoW** | **Jira Link(s)** |
| 2 |  |  |  |  |  |  |  |
| 3 |  |  |  |  |  |  |  |
| 4 |  |  |  |  |  |  |  |
| 5 |  |  |  |  |  |  |  |
| 6 |  |  |  |  |  |  |  |
| 7 |  |  |  |  |  |  |  |
| 8 |  |  |  |  |  |  |  |
| 9 |  |  |  |  |  |  |  |
| 10 |  |  |  |  |  |  |  |

This is the place to point towards key **Delivery **information. 

### ℹ️ Section Owner

|  |  |  |  |
| --- | --- | --- | --- |
| **Who** | Name // Role | **Section Status** | TO DOIN PROGRESSDONE |

## Delivery Considerations

The following section identifies the basic considerations for a project, programme, initiative, epic or deliverable, and aims to accelerate stakeholder onboarding. 

How each item is achieved is largely at the discretion of each Delivery Lead. 

This list is not intended to be exhaustive and Delivery Leads can add further items based on the needs and evolution of work. 

| **Item** | **Link ** |
| --- | --- |
| [***RAID Log***](https://flutteruki.atlassian.net/wiki/spaces/FU/pages/495225645/Body+Of+Knowledge) | *Link* |
| [***Stakeholder Map***](https://flutteruki.atlassian.net/wiki/spaces/FU/pages/495225645/Body+Of+Knowledge) | *Link* |
| [***Communication Plan***](https://flutteruki.atlassian.net/wiki/spaces/FU/pages/495225645/Body+Of+Knowledge) | *Link* |
| [***Delivery Plan***](https://flutteruki.atlassian.net/wiki/spaces/FU/pages/495225645/Body+Of+Knowledge) | *Link* |
| [***Acceptance Into Service (AIS)***](https://flutteruki.atlassian.net/wiki/spaces/FU/pages/495225645/Body+Of+Knowledge) | *Link* |
| [***Lessons Learnt Log***](https://flutteruki.atlassian.net/wiki/spaces/FU/pages/495225645/Body+Of+Knowledge) | *Link* |
| *Add more items here to support delivery* | *Link* |

## Related Work

| **Initiative / Programme / Workstream / Deliverable Name** | [**Relationship**](https://flutteruki.atlassian.net/wiki/spaces/FU/pages/495225645/Body+Of+Knowledge) | **Link** |
| --- | --- | --- |
|  |  |  |
|  |  |  |

---
