import json
from orchestrator.workflow_orchestrator import WorkflowOrchestrator

def load_product_data():
    """Load product data from JSON file."""
    with open("data/product_data.json", "r") as f:
        return json.load(f)

def main():
    """Main entry point for autonomous multi-agent system."""
    print("\n" + "="*70)
    print("Kasparro AI - Multi-Agent Content Generation System")
    print("True Autonomous Agent Architecture with Message Passing")
    print("="*70 + "\n")

    try:
        # Load input data
        product_data = load_product_data()
        print(f"Loaded product: {product_data['name']}\n")

        # Initialize orchestrator (automatically starts all agents)
        orchestrator = WorkflowOrchestrator()

        # Run the autonomous pipeline
        orchestrator.run_pipeline(product_data)

        print("\n✅ Content generation completed successfully!")
        print("\nGenerated files in output/ directory:")
        print("  - faq.json (FAQ page with 15+ questions)")
        print("  - product_page.json (Complete product page)")
        print("  - comparison_page.json (Product comparison)\n")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
