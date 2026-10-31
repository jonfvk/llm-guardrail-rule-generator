from typing import Dict, List, Union


def format_rule_violations(detections: Dict[str, Union[Dict[str, List[str]], List[str]]]) -> str:
    """Format the detection results into a human-readable report string.

    Args:
        detections (dict): Dictionary with keys 'pii', 'phi', 'pci', 'prompt_injection' mapping to detection results.

    Returns:
        str: Formatted multiline string report of all rule violations.
    """
    lines = []
    for category in ["pii", "phi", "pci", "prompt_injection"]:
        category_results = detections.get(category, None)
        lines.append(f"{category.upper()} detections:")
        if not category_results:
            lines.append("  None detected.")
            continue

        if category == "prompt_injection":
            # prompt_injection is a list of keywords
            if isinstance(category_results, list) and category_results:
                for keyword in category_results:
                    lines.append(f"  Keyword: '{keyword}'")
            else:
                lines.append("  None detected.")
        else:
            # pii, phi, pci are dicts of pattern_name -> matches
            if isinstance(category_results, dict) and category_results:
                for rule_name, matches in category_results.items():
                    unique_matches = sorted(set(matches))
                    lines.append(f"  Rule '{rule_name}': {unique_matches}")
            else:
                lines.append("  None detected.")

    return "\n".join(lines)


if __name__ == "__main__":
    # Example usage
    sample_detections = {
        "pii": {
            "email": ["john.doe@example.com"],
            "ssn": ["123-45-6789"]
        },
        "phi": {},
        "pci": {
            "visa": ["4111111111111111"]
        },
        "prompt_injection": ["ignore previous instructions", "bypass the filter"]
    }
    report = format_rule_violations(sample_detections)
    print(report)
