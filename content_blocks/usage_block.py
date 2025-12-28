from models.product_model import ProductModel
import re

class UsageBlock:
    """Generates usage-related content."""

    def generate(self, product: ProductModel) -> dict:
        """Transform usage information into structured content."""
        return {
            "instructions": product.usage,
            "frequency": self._extract_frequency(product.usage),
            "timing": self._extract_timing(product.usage),
            "application_method": self._extract_application_method(product.usage)
        }

    def _extract_frequency(self, usage: str) -> str:
        """Extract frequency from usage text."""
        usage_lower = usage.lower()
        if "morning" in usage_lower and "evening" not in usage_lower:
            return "Once daily (morning)"
        elif "evening" in usage_lower or "night" in usage_lower:
            return "Once daily (evening)"
        elif "twice" in usage_lower:
            return "Twice daily"
        return "As directed"

    def _extract_timing(self, usage: str) -> str:
        """Extract timing from usage text."""
        usage_lower = usage.lower()
        if "morning" in usage_lower:
            return "Morning"
        elif "evening" in usage_lower or "night" in usage_lower:
            return "Evening"
        return "Anytime"

    def _extract_application_method(self, usage: str) -> str:
        """Extract application method from usage text."""
        usage_lower = usage.lower()
        if "apply" in usage_lower:
            match = re.search(r'apply\s+(\d+-?\d*\s+\w+)', usage_lower)
            if match:
                return match.group(1).strip()
        return "As directed"
