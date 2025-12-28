# Project Documentation

## Problem Statement

Design and implement a modular agentic automation system that takes product data and automatically generates structured, machine-readable content pages in JSON format.

## Solution Overview

A multi-agent system with clear separation of concerns:
- **Data Parser Agent**: Validates and transforms raw input
- **Question Generator Agent**: Creates categorized user questions
- **Content Generation Agent**: Produces structured pages using templates and blocks
- **Comparison Agent**: Generates product comparisons

## Scopes & Assumptions

- Single product input (GlowBoost Vitamin C Serum)
- No external research or data augmentation
- Pure rule-based logic (no LLM dependency in base implementation)
- JSON output only
- Extensible for additional products and page types

## System Design

### Architecture Pattern
**Orchestrator-Workers Pattern** with DAG execution flow

### Agent Boundaries
1. **DataParserAgent**
   - Input: Raw JSON dict
   - Output: ProductModel object
   - Responsibility: Data validation and transformation

2. **QuestionGeneratorAgent**
   - Input: ProductModel
   - Output: List of categorized questions (15+)
   - Responsibility: Generate user questions across 5 categories

3. **ContentGenerationAgent**
   - Input: ProductModel + content blocks + template
   - Output: Rendered JSON page
   - Responsibility: Apply content blocks and render templates

4. **ComparisonAgent**
   - Input: Two ProductModel objects
   - Output: Comparison data dict
   - Responsibility: Product comparison and fictional product generation

### Workflow DAG
<img width="1664" height="2496" alt="image" src="https://github.com/user-attachments/assets/ff06e53a-5994-4a2a-8d35-2f591505fa84" />


### Content Blocks (Reusable Logic)
- **BenefitsBlock**: Formats benefits into marketing copy
- **UsageBlock**: Extracts frequency, timing, application method
- **IngredientsBlock**: Formats ingredient lists
- **ComparisonBlock**: Multi-dimensional product comparison

### Templates
- **FAQTemplate**: Structures Q&A with categories
- **ProductPageTemplate**: Complete product page with sections
- **ComparisonTemplate**: Side-by-side product comparison

### Extensibility
- Add new agents by implementing single-responsibility classes
- Create new templates by extending BaseTemplate
- Add content blocks as independent modules
- Orchestrator supports additional workflow steps via state management
