import re
from typing import Dict, Pattern, List, Union

class CustomRule:
    """Represents a custom guardrail rule with a name, category, and pattern."""

    def __init__(self, name: str, category: str, pattern: Union[str, Pattern]):
        self.name = name
        self.category = category
        if isinstance(pattern, str):
            self.pattern = re.compile(pattern)
        else:
            self.pattern = pattern

    def find_matches(self, text: str) -> List[str]:
        return self.pattern.findall(text)


class CustomRuleManager:
    """Manages a collection of custom guardrail rules."""

    def __init__(self):
        # Store rules by category, each category maps rule name to CustomRule
        self.rules: Dict[str, Dict[str, CustomRule]] = {}

    def add_rule(self, name: str, category: str, pattern: Union[str, Pattern]) -> None:
        """Add a new custom rule.

        Args:
            name (str): Unique name for the rule.
            category (str): Category of the rule (e.g., 'pii', 'phi', 'pci', 'prompt_injection').
            pattern (str or re.Pattern): Regex pattern string or compiled pattern.

        Raises:
            ValueError: If the rule name already exists in the category.
        """
        if category not in self.rules:
            self.rules[category] = {}
        if name in self.rules[category]:
            raise ValueError(f"Rule '{name}' already exists in category '{category}'.")
        self.rules[category][name] = CustomRule(name, category, pattern)

    def remove_rule(self, name: str, category: str) -> None:
        """Remove a custom rule by name and category.

        Args:
            name (str): Name of the rule to remove.
            category (str): Category of the rule.

        Raises:
            KeyError: If the rule or category does not exist.
        """
        if category not in self.rules or name not in self.rules[category]:
            raise KeyError(f"Rule '{name}' not found in category '{category}'.")
        del self.rules[category][name]
        if not self.rules[category]:
            del self.rules[category]

    def list_rules(self, category: str = None) -> Dict[str, List[str]]:
        """List all rules or rules in a specific category.

        Args:
            category (str, optional): Category to list rules from. If None, list all.

        Returns:
            Dict[str, List[str]]: Mapping of category to list of rule names.
        """
        if category:
            if category in self.rules:
                return {category: list(self.rules[category].keys())}
            else:
                return {category: []}
        else:
            return {cat: list(rules.keys()) for cat, rules in self.rules.items()}

    def detect_with_custom_rules(self, text: str) -> Dict[str, Dict[str, List[str]]]:
        """Detect matches in text using all custom rules.

        Args:
            text (str): Text to scan.

        Returns:
            Dict[str, Dict[str, List[str]]]: Mapping category -> rule name -> matches.
        """
        results = {}
        for category, rules in self.rules.items():
            category_results = {}
            for name, rule in rules.items():
                matches = rule.find_matches(text)
                if matches:
                    category_results[name] = matches
            if category_results:
                results[category] = category_results
        return results


if __name__ == "__main__":
    manager = CustomRuleManager()
    # Add a custom rule to detect a fake pattern
    manager.add_rule("test_email", "pii", r"test\d+@example\.com")
    sample_text = "Please contact test123@example.com for info."
    detections = manager.detect_with_custom_rules(sample_text)
    print("Custom rule detections:")
    for category, rules in detections.items():
        print(f"Category: {category}")
        for name, matches in rules.items():
            print(f"  Rule: {name}, Matches: {matches}")
