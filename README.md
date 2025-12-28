# Kasparro AI Agentic Content Generation System

Multi-agent system for automated content generation from product data.

## Quick Start
### ***NOTE*** 
***Before running, delete all the files in the output folder as I have included my output files here as well in the github repository. The files in output folder are obtained after running the code.***
1. Install dependencies (optional - no external deps required):
```
pip install -r requirements.txt
```

2. Run the system:
```
python main.py
```

3. Check output files in `output/` directory:
- `faq.json` - FAQ page with 15+ questions
- `product_page.json` - Complete product page
- `comparison_page.json` - Product comparison

## System Architecture

- **Agents**: Specialized workers (Parser, Question Generator, Content Generator, Comparison)
- **Templates**: Structured page definitions (FAQ, Product, Comparison)
- **Content Blocks**: Reusable logic (Benefits, Usage, Ingredients, Comparison)
- **Orchestrator**: Workflow coordinator with DAG execution

## Project Structure
```
├── agents/             # Specialized agents
├── content_blocks/     # Reusable content logic
├── templates/          # Page templates
├── orchestrator/       # Workflow orchestration
├── models/             # Data models
├── data/               # Input data
└── output/             # Generated JSON files
```

See `docs/projectdocumentation.md` for detailed system design.
