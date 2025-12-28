import json
import sys
from orchestrator.workflow_orchestrator import WorkflowOrchestrator

def load_product_data():
    """Load product data from JSON file."""
    with open("data/product_data.json", "r") as f:
        return json.load(f)

def main():
    """Main entry point for the application."""
    print("\n" + "="*60)
    print("Multi-Agent Content Generation System")
    print("Kasparro AI Engineer Challenge")
    print("="*60 + "\n")
    
    try:
        # Load input data
        product_data = load_product_data()
        print(f"Loaded product: {product_data['name']}\n")
        
        # Initialize orchestrator
        orchestrator = WorkflowOrchestrator()
        
        # Run the complete pipeline
        orchestrator.run_pipeline(product_data)
        
        print("\n✅ Content generation completed successfully!")
        print("\nCheck the output/ directory for generated JSON files.")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
