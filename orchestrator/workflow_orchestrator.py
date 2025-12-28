import json
import os
from agents.data_parser_agent import DataParserAgent
from agents.question_generator_agent import QuestionGeneratorAgent
from agents.content_generation_agent import ContentGenerationAgent
from agents.comparison_agent import ComparisonAgent
from content_blocks.benefits_block import BenefitsBlock
from content_blocks.usage_block import UsageBlock
from content_blocks.ingredients_block import IngredientsBlock
from templates.faq_template import FAQTemplate
from templates.product_page_template import ProductPageTemplate
from templates.comparison_template import ComparisonTemplate

class WorkflowOrchestrator:
    """Orchestrates the multi-agent workflow for content generation."""

    def __init__(self):
        self.orchestrator_name = "WorkflowOrchestrator"
        self.state = {}
        self.agents = self._initialize_agents()
        print(f"[{self.orchestrator_name}] Initialized with {len(self.agents)} agents")

    def _initialize_agents(self):
        """Initialize all agents."""
        return {
            "parser": DataParserAgent(),
            "question_gen": QuestionGeneratorAgent(),
            "faq_gen": ContentGenerationAgent([], FAQTemplate()),
            "product_gen": ContentGenerationAgent(
                [BenefitsBlock(), UsageBlock(), IngredientsBlock()],
                ProductPageTemplate()
            ),
            "comparison_gen": ComparisonAgent()
        }

    def run_pipeline(self, raw_data: dict):
        """Execute the complete agentic workflow."""
        print(f"\n{'='*60}")
        print(f"[{self.orchestrator_name}] Starting content generation pipeline")
        print(f"{'='*60}\n")

        # Step 1: Parse product data
        print("Step 1: Parsing product data")
        self.state["product"] = self.agents["parser"].execute(raw_data)

        # Step 2: Generate questions
        print("\nStep 2: Generating user questions")
        self.state["questions"] = self.agents["question_gen"].execute(self.state["product"])

        # Step 3: Generate FAQ page
        print("\nStep 3: Generating FAQ page")
        faq_output = self.agents["faq_gen"].execute(
            self.state["product"], 
            self.state["questions"]
        )
        self._save_json(faq_output, "output/faq.json")

        # Step 4: Generate product page
        print("\nStep 4: Generating product page")
        product_output = self.agents["product_gen"].execute(self.state["product"])
        self._save_json(product_output, "output/product_page.json")

        # Step 5: Generate comparison page
        print("\nStep 5: Generating comparison page")
        product_b = self.agents["comparison_gen"].create_fictional_product(self.state["product"])
        comparison_data = self.agents["comparison_gen"].execute(self.state["product"], product_b)

        comparison_template = ComparisonTemplate()
        comparison_output = comparison_template.render(
            self.state["product"], 
            product_b, 
            comparison_data
        )
        self._save_json(comparison_output, "output/comparison_page.json")

        print(f"\n{'='*60}")
        print(f"[{self.orchestrator_name}] Pipeline complete!")
        print(f"{'='*60}")
        print("\nGenerated files:")
        print("  - output/faq.json")
        print("  - output/product_page.json")
        print("  - output/comparison_page.json")

    def _save_json(self, data: dict, filepath: str):
        """Save data as JSON file."""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"  ✓ Saved: {filepath}")
