# LLM Guardrail Rule Generator

Offline Python tool to create and test runtime guardrail rules for detecting PII, PHI, PCI leakage, and prompt injection in LLM inputs/outputs.

## Overview

Guardrails prevent sensitive data leaks and misuse but need easy offline rule creation and testing. This tool uses regex and keyword matching to define guardrail rules and test them against sample texts offline.

## Features

- Detect common PII (emails, phone numbers, SSNs), PHI (medical record numbers, ICD codes), PCI (credit card numbers), and prompt injection attempts.
- Add custom regex-based rules programmatically or via CLI.
- Test single or batch texts for rule violations.
- Generate human-readable reports of detected sensitive data.
- Manage rules with load/save JSON files.
- Fully offline and standalone Python utility.

## Installation

Clone the repository and install dependencies (only Python standard library required):

```bash
git clone <repo-url>
cd llm-guardrail-rule-generator
# No external dependencies, just run with Python 3.7+
```

## Usage

### CLI

Run the CLI module:

```bash
python -m llm_guardrail_rule_generator.cli --help
```

Commands include:

- `add-rule` to add a custom rule
- `remove-rule` to remove a rule
- `list-rules` to list rules
- `load-rules` and `save-rules` to manage rule files
- `test-text` to test a single text
- `batch-test` to test multiple texts

### Programmatic API

Import and use the `CustomRuleManager` and detection functions:

```python
from llm_guardrail_rule_generator.custom_rules import CustomRuleManager
from llm_guardrail_rule_generator.batch_testing import batch_test_texts

manager = CustomRuleManager()
manager.add_rule('secret_word', 'pii', r'secret')

texts = ["This is a secret message.", "No sensitive data here."]
results = batch_test_texts(texts)
for result in results:
    print(result)
```

## Documentation

See `docs/rule_creation_and_testing.md` for detailed instructions on creating and testing rules.

## Testing

Run unit tests with:

```bash
python -m unittest discover tests
```

## Source

- https://www.splunk.com/en_us/blog/learn/ai-agent-observability.html (accessed 2024-06)

## License

MIT License
