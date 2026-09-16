import unittest

from main import case_matches


class CaseMatchesTests(unittest.TestCase):
    def test_exact_match(self):
        for test_id in (
            "SystemPowerModeSet",
            "AppLaunchNegativeTest",
            "InputLongKeyPressKeyDown",
            "SystemSettingsSetOutputResolution",
        ):
            with self.subTest(test_id=test_id):
                self.assertTrue(case_matches(test_id, test_id))

    def test_prefix_wildcard(self):
        cases = [
            ("SystemPowerModeSet", "SystemPower*", True),
            ("AppLaunchNegativeTest", "App*", True),
            ("InputLongKeyPressKeyDown", "Input*", True),
            ("SystemSettingsSetOutputResolution", "App*", False),
        ]
        for test_id, pattern, expected in cases:
            with self.subTest(test_id=test_id, pattern=pattern):
                self.assertEqual(case_matches(test_id, pattern), expected)

    def test_suffix_and_infix_wildcard(self):
        cases = [
            ("AppLaunchNegativeTest", "*NegativeTest", True),
            ("InputLongKeyPressKeyDown", "Input*KeyDown", True),
            ("InputLongKeyPressKeyUp", "Input*KeyDown", False),
            ("SystemSettingsSetOutputResolution", "*Set*Resolution", True),
        ]
        for test_id, pattern, expected in cases:
            with self.subTest(test_id=test_id, pattern=pattern):
                self.assertEqual(case_matches(test_id, pattern), expected)

    def test_single_character_wildcard(self):
        self.assertTrue(case_matches("SystemPowerModeSet", "SystemPower????Set"))
        self.assertFalse(case_matches("SystemPowerModeSet", "SystemPower???Set"))

    def test_character_class(self):
        self.assertTrue(case_matches("AppLaunchNegativeTest", "[AI]pp*"))
        self.assertFalse(case_matches("AppLaunchNegativeTest", "[IS]pp*"))

    def test_matching_is_case_sensitive(self):
        self.assertFalse(case_matches("SystemPowerModeSet", "systempower*"))
        self.assertFalse(case_matches("SystemPowerModeSet", "systempowermodeset"))

    def test_no_wildcard_does_not_match_substring(self):
        self.assertFalse(case_matches("SystemPowerModeSet", "SystemPower"))
        self.assertFalse(case_matches("SystemPowerModeSet", "ModeSet"))

    def test_comma_separated_patterns_select_multiple_suites(self):
        requested_cases = [c.strip() for c in "App*, Input*KeyDown".split(",")]
        listed_ids = [
            "AppLaunchNegativeTest",
            "InputLongKeyPressKeyDown",
            "InputLongKeyPressKeyUp",
            "SystemPowerModeSet",
        ]
        matched = [
            test_id
            for test_id in listed_ids
            if any(case_matches(test_id, pattern) for pattern in requested_cases)
        ]
        self.assertEqual(matched, ["AppLaunchNegativeTest", "InputLongKeyPressKeyDown"])


if __name__ == "__main__":
    unittest.main()
