from models.product_model import ProductModel
from typing import List, Dict

class QuestionGeneratorAgent:
    """Agent responsible for generating categorized user questions."""

    def __init__(self):
        self.agent_name = "QuestionGeneratorAgent"
        self.categories = ["Informational", "Safety", "Usage", "Purchase", "Comparison"]
        self.min_questions = 15

    def execute(self, product: ProductModel) -> List[Dict]:
        """Generate categorized questions about the product."""
        print(f"[{self.agent_name}] Generating questions for {product.name}...")

        questions = []
        questions.extend(self._generate_informational_questions(product))
        questions.extend(self._generate_safety_questions(product))
        questions.extend(self._generate_usage_questions(product))
        questions.extend(self._generate_purchase_questions(product))
        questions.extend(self._generate_comparison_questions(product))

        print(f"[{self.agent_name}] Generated {len(questions)} questions")
        return questions

    def _generate_informational_questions(self, product: ProductModel) -> List[Dict]:
        """Generate informational category questions."""
        return [
            {"question": f"What is {product.name}?", "category": "Informational"},
            {"question": f"What are the key ingredients in {product.name}?", "category": "Informational"},
            {"question": f"What is the concentration of active ingredients?", "category": "Informational"},
            {"question": f"What skin types is {product.name} suitable for?", "category": "Informational"},
        ]

    def _generate_safety_questions(self, product: ProductModel) -> List[Dict]:
        """Generate safety category questions."""
        return [
            {"question": f"Are there any side effects of using {product.name}?", "category": "Safety"},
            {"question": f"Is {product.name} safe for sensitive skin?", "category": "Safety"},
            {"question": f"Can I use {product.name} with other products?", "category": "Safety"},
        ]

    def _generate_usage_questions(self, product: ProductModel) -> List[Dict]:
        """Generate usage category questions."""
        return [
            {"question": f"How do I use {product.name}?", "category": "Usage"},
            {"question": f"When should I apply {product.name}?", "category": "Usage"},
            {"question": f"How many drops of {product.name} should I use?", "category": "Usage"},
            {"question": f"Can I use {product.name} daily?", "category": "Usage"},
        ]

    def _generate_purchase_questions(self, product: ProductModel) -> List[Dict]:
        """Generate purchase category questions."""
        return [
            {"question": f"What is the price of {product.name}?", "category": "Purchase"},
            {"question": f"Where can I buy {product.name}?", "category": "Purchase"},
            {"question": f"Is {product.name} worth the price?", "category": "Purchase"},
        ]

    def _generate_comparison_questions(self, product: ProductModel) -> List[Dict]:
        """Generate comparison category questions."""
        return [
            {"question": f"How does {product.name} compare to other Vitamin C serums?", "category": "Comparison"},
            {"question": f"What makes {product.name} different?", "category": "Comparison"},
        ]
