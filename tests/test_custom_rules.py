import unittest
from src.llm_guardrail_rule_generator.custom_rules import CustomRuleManager

class TestCustomRuleManager(unittest.TestCase):
    def setUp(self):
        self.manager = CustomRuleManager()

    def test_add_and_detect_rule(self):
        # Add a simple rule to detect the word 'secret'
        self.manager.add_rule('secret_word', 'pii', r'secret')
        text = 'This is a secret message containing secret info.'
        detections = self.manager.detect_with_custom_rules(text)
        self.assertIn('pii', detections)
        self.assertIn('secret_word', detections['pii'])
        self.assertEqual(detections['pii']['secret_word'], ['secret', 'secret'])

    def test_add_duplicate_rule_raises(self):
        self.manager.add_rule('rule1', 'phi', r'pattern1')
        with self.assertRaises(ValueError):
            self.manager.add_rule('rule1', 'phi', r'pattern2')

    def test_remove_rule(self):
        self.manager.add_rule('rule_to_remove', 'pci', r'pattern')
        self.manager.remove_rule('rule_to_remove', 'pci')
        self.assertNotIn('pci', self.manager.rules)

    def test_remove_nonexistent_rule_raises(self):
        with self.assertRaises(KeyError):
            self.manager.remove_rule('nonexistent', 'pii')

    def test_list_rules(self):
        self.manager.add_rule('rule1', 'pii', r'pattern1')
        self.manager.add_rule('rule2', 'phi', r'pattern2')
        all_rules = self.manager.list_rules()
        self.assertIn('pii', all_rules)
        self.assertIn('phi', all_rules)
        self.assertIn('rule1', all_rules['pii'])
        self.assertIn('rule2', all_rules['phi'])

        pii_rules = self.manager.list_rules('pii')
        self.assertEqual(list(pii_rules.keys()), ['pii'])
        self.assertIn('rule1', pii_rules['pii'])

    def test_detect_with_no_rules(self):
        detections = self.manager.detect_with_custom_rules('some random text')
        self.assertEqual(detections, {})

if __name__ == '__main__':
    unittest.main()
