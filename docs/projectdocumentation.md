# Project Documentation

## Problem Statement

Design and implement a modular agentic automation system that takes product data and automatically generates structured, machine-readable content pages in JSON format.

## Solution Overview

A genuine multi-agent system where agents are independent, modular, and coordinated through an orchestration mechanism that supports agent autonomy rather than static control flow:
​- Autonomous Agents – Each agent runs independently with clear input/output contracts and single responsibility
​- Message-Based Communication – Dynamic agent interaction via asynchronous message passing, not direct function calls
- Orchestration Mechanism – State machine-based coordination that reacts to agent responses rather than predetermined sequences
​- Modular Design – Reusable content logic blocks and template-based generation for extensibility
​
## Scopes & Assumptions

- Single product input (GlowBoost Vitamin C Serum)
- No external research or data augmentation
- Pure rule-based logic (no LLM dependency in base implementation)
- JSON output only
- Extensible for additional products and page types

## System Components

- Message Bus: Central broker managing inter-agent communication with per-agent queues
- 5 Autonomous Agents: Data Parser, Question Generator, FAQ Generator, Product Page Generator, Comparison Generator
- State Machine: Manages workflow transitions as a DAG/step pipeline based on agent completion events
​- Content Logic Blocks: Reusable transformation modules (benefits, usage, ingredients, comparison)
​- Template Engine: Custom structured definitions with fields, rules, and formatting
​- Orchestrator: Coordinates agents via message passing without hidden global state

## System Design

**Architecture Pattern**
Orchestrator-Workers Pattern with DAG (Directed Acyclic Graph) execution flow
​
**Agent Boundaries**
Each agent has a single responsibility, defined input/output, and no hidden global state:
​
1. Data Parser Agent
Input: Raw JSON product data dictionary

Output: Validated ProductModel object

Responsibility: Parse and convert data into clean internal model

Autonomy: Runs independently, validates required fields, broadcasts parsed data

2. Question Generator Agent
Input: ProductModel

Output: List of 15+ categorized questions
​
Categories: Informational, Safety, Usage, Purchase, Comparison
​
Responsibility: Automatically generate user questions across all categories

Autonomy: Listens for product data broadcasts, generates questions independently

3. FAQ Generator Agent
Input: ProductModel + Generated questions

Output: FAQ page JSON (minimum 5 Q&As)
​
Responsibility: Apply FAQ template and generate contextual answers

Autonomy: Generates answers based on product data rules

4. Product Page Generator Agent
Input: ProductModel + Content blocks

Output: Product page JSON

Responsibility: Apply content logic blocks (benefits, usage, ingredients) and render via template
​
Autonomy: Assembles complete product page using reusable blocks

5. Comparison Agent
Input: ProductModel (GlowBoost)

Output: Comparison page JSON

Responsibility: Generate fictional Product B and create structured comparison

Autonomy: Creates fictional competitor, performs multi-dimensional comparison

### Workflow DAG
<img width="500" height="500" alt="image" src="https://github.com/user-attachments/assets/ff06e53a-5994-4a2a-8d35-2f591505fa84" />


### Content Blocks (Reusable Logic)
- **BenefitsBlock**: Transforms benefits list into formatted marketing descriptions
- **UsageBlock**: Extracts frequency, timing, and application method from usage text
- **IngredientsBlock**: Formats ingredient lists with primary ingredient identification
- **ComparisonBlock**: Multi-dimensional comparison (price, ingredients, benefits, skin type) with winner determination

### Message Flow (Agent Orchestration)
```
1. Orchestrator → Data Parser: REQUEST(parse_data)
2. Data Parser → Orchestrator: RESPONSE(ProductModel)
3. Data Parser → ALL: INFORM(product_parsed) [Broadcast]

4. Orchestrator → Question Gen: REQUEST(generate_questions)
5. Question Gen → Orchestrator: RESPONSE(15+ questions, 5 categories)

6. Orchestrator → FAQ Gen: REQUEST(generate_faq)
7. FAQ Gen → Orchestrator: RESPONSE(faq.json with 5+ Q&As)

8. Orchestrator → Product Gen: REQUEST(generate_product_page)
9. Product Gen → Orchestrator: RESPONSE(product_page.json)

10. Orchestrator → Comparison Gen: REQUEST(generate_comparison)
11. Comparison Gen → Orchestrator: RESPONSE(comparison_page.json with Product B)
```