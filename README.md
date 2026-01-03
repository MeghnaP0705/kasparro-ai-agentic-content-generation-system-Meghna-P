# Kasparro AI Agentic Content Generation System

Multi-agent system for automated content generation from product data.

## Quick Start
### ***NOTE*** 
***Before running, delete all files in the output/ folder if you cloned this from GitHub and it already contains JSON outputs, because those files are generated when the system runs and should not be committed.***


1. Run the system:
```
python main.py
```

2. Check output files in `output/` directory:
- `faq.json` - FAQ page with 15+ questions
- `product_page.json` - Complete product page
- `comparison_page.json` - Product comparison

## System Architecture

- **Agents**: Autonomous workers (Data Parser, Question Generator, FAQ Generator, Product Page Generator, Comparison Generator) running in their own loops and communicating via messages rather than direct function calls.
- **Message Layer**: Central message bus and typed messages enabling asynchronous, decoupled agent-to-agent and agent–orchestrator communication.
- **State Machine**: Explicit workflow state machine that drives transitions (parse → questions → FAQ → product page → comparison) based on events, not static control flow.
- **Orchestrator**: Coordinates agents by sending and receiving messages and triggering state transitions, while agents remain independent and reusable.


## Project Structure
```
├── agents/             # Specialized agents
├── content_blocks/     # Reusable content logic
├── messaging/          # Message passing layer
├── orchestrator/       # Workflow orchestration
├── models/             # Data models
├── data/               # Input data
└── output/             # Generated JSON files
```

See `docs/projectdocumentation.md` for detailed system design.
