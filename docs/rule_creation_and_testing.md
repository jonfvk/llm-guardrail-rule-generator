# LLM Guardrail Rule Generator

## Rule Creation and Testing Process

This document explains how to create custom guardrail rules and test them using the LLM Guardrail Rule Generator offline Python tool.

---

### 1. Understanding Guardrail Rules

Guardrail rules are regex patterns or keywords used to detect sensitive information or prompt injection attempts in LLM inputs and outputs. The tool supports four main categories:

- **PII**: Personally Identifiable Information (e.g., emails, phone numbers, SSNs)
- **PHI**: Protected Health Information (e.g., medical record numbers, ICD codes)
- **PCI**: Payment Card Industry data (e.g., credit card numbers)
- **Prompt Injection**: Keywords indicating attempts to bypass or override instructions

---

### 2. Creating Custom Rules

Custom rules allow you to extend detection beyond the built-in patterns.

#### Rule Components:
- **Name**: Unique identifier for the rule within its category.
- **Category**: One of `pii`, `phi`, `pci`, or `prompt_injection`.
- **Pattern**: A regex pattern string that matches the sensitive data or keywords.

#### Adding Rules Programmatically

Use the `CustomRuleManager` class from `custom_rules.py`:

```python
from llm_guardrail_rule_generator.custom_rules import CustomRuleManager

manager = CustomRuleManager()
manager.add_rule('secret_word', 'pii', r'secret')
```

#### Adding Rules via CLI

You can add rules using the CLI command:

```bash
python -m llm_guardrail_rule_generator.cli add-rule --name secret_word --category pii --pattern 'secret'
```

#### Rule Storage

Rules can be saved to and loaded from JSON files:

- JSON format is a dictionary mapping category to rule names and their regex patterns.

Example JSON:

```json
{
  "pii": {
    "secret_word": "secret"
  }
}
```

Use CLI commands to load and save rules:

```bash
python -m llm_guardrail_rule_generator.cli load-rules --file rules.json
python -m llm_guardrail_rule_generator.cli save-rules --file rules.json
```

---

### 3. Testing Rules

You can test rules against sample texts to verify detection.

#### Single Text Test

Use the CLI to test a single text:

```bash
python -m llm_guardrail_rule_generator.cli test-text --text "This is a secret message."
```

The output will show detected rules and matched strings.

#### Batch Testing

Test multiple texts at once from a file or command line:

```bash
python -m llm_guardrail_rule_generator.cli batch-test --file samples.txt
```

or

```bash
python -m llm_guardrail_rule_generator.cli batch-test --texts "text1" "text2" "text3"
```

#### Programmatic Batch Testing

Use the `batch_test_texts` function:

```python
from llm_guardrail_rule_generator.batch_testing import batch_test_texts

texts = ["sample text 1", "sample text 2"]
results = batch_test_texts(texts)
for result in results:
    print(result)
```

---

### 4. Interpreting Reports

Detection results are formatted into human-readable reports showing:

- Category (PII, PHI, PCI, Prompt Injection)
- Rule names and matched values

Example report snippet:

```
PII detections:
  Rule 'email': ['john.doe@example.com']
  Rule 'ssn': ['123-45-6789']
PHI detections:
  None detected.
PCI detections:
  Rule 'visa': ['4111111111111111']
Prompt Injection detections:
  Keyword: 'ignore previous instructions'
```

---

### 5. Best Practices

- Test new rules on representative sample texts.
- Use precise regex patterns to minimize false positives.
- Regularly update and review rules to adapt to new data formats.

---

### 6. Additional Resources

- Source code and documentation: see the project repository.
- Example patterns are defined in `patterns.py`.
- Unit tests demonstrate usage and expected behavior.

---

### 7. References

- Splunk AI Agent Observability Blog (2023): https://www.splunk.com/en_us/blog/learn/ai-agent-observability.html

---

*Document last updated: 2024-06*