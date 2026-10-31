import argparse
import json
from typing import List
from .custom_rules import CustomRuleManager
from .batch_testing import batch_test_texts
from .reporting import format_rule_violations


rule_manager = CustomRuleManager()


def load_rules_from_file(filepath: str) -> None:
    """Load custom rules from a JSON file.

    The JSON file should be a dict of category to dict of rule_name to pattern string.

    Args:
        filepath (str): Path to the JSON file.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    for category, rules in data.items():
        for name, pattern in rules.items():
            try:
                rule_manager.add_rule(name, category, pattern)
            except ValueError as e:
                print(f"Warning: {e}")


def save_rules_to_file(filepath: str) -> None:
    """Save current custom rules to a JSON file.

    Args:
        filepath (str): Path to save the JSON file.
    """
    export_data = {}
    for category, rules in rule_manager.rules.items():
        export_data[category] = {name: rule.pattern.pattern for name, rule in rules.items()}
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(export_data, f, indent=2)


def cmd_add_rule(args):
    try:
        rule_manager.add_rule(args.name, args.category, args.pattern)
        print(f"Rule '{args.name}' added to category '{args.category}'.")
    except ValueError as e:
        print(f"Error: {e}")


def cmd_remove_rule(args):
    try:
        rule_manager.remove_rule(args.name, args.category)
        print(f"Rule '{args.name}' removed from category '{args.category}'.")
    except KeyError as e:
        print(f"Error: {e}")


def cmd_list_rules(args):
    rules = rule_manager.list_rules(args.category)
    if args.category:
        print(f"Rules in category '{args.category}':")
    else:
        print("All rules by category:")
    for category, names in rules.items():
        print(f"- {category}:")
        if names:
            for name in names:
                print(f"  - {name}")
        else:
            print("  (none)")


def cmd_test_text(args):
    detections = rule_manager.detect_with_custom_rules(args.text)
    report = format_rule_violations(detections)
    print(report)


def cmd_batch_test(args):
    texts = []
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            texts = [line.strip() for line in f if line.strip()]
    elif args.texts:
        texts = args.texts
    else:
        print("No input texts provided for batch testing.")
        return

    results = []
    for text in texts:
        detection = rule_manager.detect_with_custom_rules(text)
        results.append(detection)

    for i, detection in enumerate(results):
        print(f"--- Text {i+1} detections ---")
        print(format_rule_violations(detection))
        print()


def main():
    parser = argparse.ArgumentParser(description="Manage and test LLM guardrail rules.")
    subparsers = parser.add_subparsers(title="commands", dest="command")

    # Add rule
    parser_add = subparsers.add_parser("add", help="Add a custom rule")
    parser_add.add_argument("name", help="Unique name for the rule")
    parser_add.add_argument("category", help="Category of the rule (pii, phi, pci, prompt_injection)")
    parser_add.add_argument("pattern", help="Regex pattern string for the rule")
    parser_add.set_defaults(func=cmd_add_rule)

    # Remove rule
    parser_remove = subparsers.add_parser("remove", help="Remove a custom rule")
    parser_remove.add_argument("name", help="Name of the rule to remove")
    parser_remove.add_argument("category", help="Category of the rule")
    parser_remove.set_defaults(func=cmd_remove_rule)

    # List rules
    parser_list = subparsers.add_parser("list", help="List custom rules")
    parser_list.add_argument("-c", "--category", help="Category to list rules from")
    parser_list.set_defaults(func=cmd_list_rules)

    # Test single text
    parser_test = subparsers.add_parser("test", help="Test a single text against custom rules")
    parser_test.add_argument("text", help="Text to test")
    parser_test.set_defaults(func=cmd_test_text)

    # Batch test
    parser_batch = subparsers.add_parser("batch", help="Batch test multiple texts")
    parser_batch.add_argument("-f", "--file", help="File containing texts, one per line")
    parser_batch.add_argument("-t", "--texts", nargs="*", help="List of texts to test")
    parser_batch.set_defaults(func=cmd_batch_test)

    # Load rules from file
    parser_load = subparsers.add_parser("load", help="Load custom rules from JSON file")
    parser_load.add_argument("filepath", help="Path to JSON file")
    parser_load.set_defaults(func=lambda args: load_rules_from_file(args.filepath))

    # Save rules to file
    parser_save = subparsers.add_parser("save", help="Save custom rules to JSON file")
    parser_save.add_argument("filepath", help="Path to save JSON file")
    parser_save.set_defaults(func=lambda args: save_rules_to_file(args.filepath))

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return

    # Execute the chosen command
    args.func(args)


if __name__ == "__main__":
    main()
