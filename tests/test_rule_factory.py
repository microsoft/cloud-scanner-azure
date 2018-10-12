import os

from cloud_scanner.contracts import RuleFactory
from .unittest_base import TestCase


class TestRuleFactory(TestCase):
    def setUp(self):
        os.environ["TAG_UPDATES_QUEUE_NAME"] = "resource-tag-updates"
        os.environ["QUEUE_TYPE"] = "simulator"

    def test_get_all_rules(self):
        rules = RuleFactory.get_rules()

        self.assertEqual(4, len(rules))
