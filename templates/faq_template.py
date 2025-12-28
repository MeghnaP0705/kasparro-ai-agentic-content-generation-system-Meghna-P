from templates.base_template import BaseTemplate
from models.product_model import ProductModel
from typing import List, Dict

class FAQTemplate(BaseTemplate):
    """Template for FAQ page generation."""

    def define_structure(self):
        """Define FAQ template structure."""
        self.fields = ["questions", "answers", "categories"]
        self.rules = {
            "min_questions": 5,
            "categories": ["Informational", "Safety", "Usage", "Purchase", "Comparison"]
        }

    def render(self, questions: List[Dict], product: ProductModel) -> dict:
        """Render FAQ page with questions and product data."""
        faqs = self._structure_faqs(questions, product)

        return {
            "page_type": "FAQ",
            "product_name": product.name,
            "total_questions": len(faqs),
            "faqs": faqs,
            "categories": list(set([faq["category"] for faq in faqs]))
        }

    def _structure_faqs(self, questions: List[Dict], product: ProductModel) -> List[Dict]:
        """Structure questions into FAQ format with answers."""
        structured_faqs = []

        for q in questions:
            faq_item = {
                "question": q["question"],
                "answer": self._generate_answer(q, product),
                "category": q["category"]
            }
            structured_faqs.append(faq_item)

        return structured_faqs

    def _generate_answer(self, question: Dict, product: ProductModel) -> str:
        """Generate answer based on question category and product data."""
        category = question["category"]
        q_text = question["question"].lower()

        if "price" in q_text or "cost" in q_text:
            return f"{product.name} is priced at ₹{product.price}."

        if "ingredients" in q_text:
            ingredients = ", ".join(product.key_ingredients)
            return f"The key ingredients in {product.name} are {ingredients}."

        if "benefits" in q_text or "does it do" in q_text:
            benefits = " and ".join([b.lower() for b in product.benefits])
            return f"{product.name} helps with {benefits}."

        if "use" in q_text or "apply" in q_text:
            return f"{product.usage}"

        if "skin type" in q_text:
            skin_types = " and ".join(product.skin_type)
            return f"{product.name} is suitable for {skin_types} skin."

        if "side effect" in q_text:
            return f"{product.side_effects}"

        if "concentration" in q_text or "%" in q_text:
            return f"{product.name} contains {product.concentration}."

        return f"Please refer to the product details for more information about {product.name}."
