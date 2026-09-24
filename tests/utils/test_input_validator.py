import pytest

from handlers.utils.input_validator import InputValidator


class TestIsPresent:
    def test_none_is_not_present(self):
        assert InputValidator._is_present(None) is False

    def test_empty_string_is_not_present(self):
        assert InputValidator._is_present("") is False

    def test_empty_list_is_not_present(self):
        assert InputValidator._is_present([]) is False

    def test_empty_dict_is_not_present(self):
        assert InputValidator._is_present({}) is False

    def test_false_is_present(self):
        # False is a valid boolean value, not "empty"
        assert InputValidator._is_present(False) is True

    def test_zero_is_present(self):
        # 0 is a valid number, not "empty"
        assert InputValidator._is_present(0) is True

    def test_string_is_present(self):
        assert InputValidator._is_present("test") is True

    def test_number_is_present(self):
        assert InputValidator._is_present(42) is True


class TestNormalize:
    def test_none_returns_empty(self):
        assert InputValidator._normalize(None, 1) == []

    def test_single_dict(self):
        rule = [{"fields": ["a", "b"], "count": 2}]
        assert InputValidator._normalize(rule, 1) == rule

    def test_list_of_dicts(self):
        rules = [{"fields": ["a"], "count": 1}, {"fields": ["b", "c"], "count": 2}]
        assert InputValidator._normalize(rules, 1) == rules

    def test_list_of_strings_uses_default_count(self):
        rules = ["a", "b"]
        assert InputValidator._normalize(rules, 3) == [
            {"fields": ["a", "b"], "count": 3}
        ]


class TestAtLeast:
    def test_passes_when_enough_fields_present(self):
        inputs = {"email": "test@test.com", "role": "user"}
        validator = InputValidator(
            inputs, at_least=[{"fields": ["email", "phone"], "count": 1}]
        )
        validator.validate()  # Should not raise

    def test_fails_when_no_fields_present(self):
        inputs = {"name": "John"}
        validator = InputValidator(
            inputs, at_least=[{"fields": ["email", "phone"], "count": 1}]
        )
        with pytest.raises(
            RuntimeError, match="At least 1 of email, phone must be provided"
        ):
            validator.validate()

    def test_passes_with_multiple_fields_when_count_is_1(self):
        # anyOf behavior: providing more than the minimum is fine
        inputs = {"email": "test@test.com", "phone": "123"}
        validator = InputValidator(
            inputs, at_least=[{"fields": ["email", "phone"], "count": 1}]
        )
        validator.validate()


class TestExactly:
    def test_passes_when_exact_count_met(self):
        inputs = {"email": "test@test.com"}
        validator = InputValidator(
            inputs, exactly=[{"fields": ["email", "phone"], "count": 1}]
        )
        validator.validate()

    def test_fails_when_too_few(self):
        inputs = {"name": "John"}
        validator = InputValidator(
            inputs, exactly=[{"fields": ["email", "phone"], "count": 1}]
        )
        with pytest.raises(
            RuntimeError, match="Exactly 1 of email, phone must be provided"
        ):
            validator.validate()

    def test_fails_when_too_many(self):
        # XOR behavior: providing both when only 1 is allowed
        inputs = {"email": "test@test.com", "phone": "123"}
        validator = InputValidator(
            inputs, exactly=[{"fields": ["email", "phone"], "count": 1}]
        )
        with pytest.raises(RuntimeError, match="Remove 1"):
            validator.validate()


class TestAtMost:
    def test_passes_when_under_limit(self):
        inputs = {"email": "test@test.com"}
        validator = InputValidator(
            inputs, at_most=[{"fields": ["email", "phone", "role"], "count": 2}]
        )
        validator.validate()

    def test_passes_when_at_limit(self):
        inputs = {"email": "test@test.com", "phone": "123"}
        validator = InputValidator(
            inputs, at_most=[{"fields": ["email", "phone", "role"], "count": 2}]
        )
        validator.validate()

    def test_fails_when_over_limit(self):
        inputs = {"email": "test@test.com", "phone": "123", "role": "user"}
        validator = InputValidator(
            inputs, at_most=[{"fields": ["email", "phone", "role"], "count": 2}]
        )
        with pytest.raises(
            RuntimeError, match="At most 2 of email, phone, role may be provided"
        ):
            validator.validate()


class TestCombinedRules:
    def test_intercom_create_contact_scenario_fails(self):
        # Missing at least one of email, external_id, role
        inputs = {"name": "John Doe", "phone": "123456"}
        validator = InputValidator(
            inputs, at_least=[{"fields": ["email", "external_id", "role"], "count": 1}]
        )
        with pytest.raises(
            RuntimeError, match="At least 1 of email, external_id, role"
        ):
            validator.validate()

    def test_intercom_create_contact_scenario_passes(self):
        inputs = {"name": "John Doe", "email": "john@test.com"}
        validator = InputValidator(
            inputs, at_least=[{"fields": ["email", "external_id", "role"], "count": 1}]
        )
        validator.validate()

    def test_multiple_rules_all_pass(self):
        inputs = {"email": "test@test.com", "role": "user"}
        validator = InputValidator(
            inputs,
            at_least=[{"fields": ["email", "phone"], "count": 1}],
            exactly=[{"fields": ["role", "admin_id"], "count": 1}],
        )
        validator.validate()

    def test_multiple_rules_one_fails(self):
        # Fails the 'exactly' rule because both role and admin_id are provided
        inputs = {"email": "test@test.com", "role": "user", "admin_id": "123"}
        validator = InputValidator(
            inputs,
            at_least=[{"fields": ["email", "phone"], "count": 1}],
            exactly=[{"fields": ["role", "admin_id"], "count": 1}],
        )
        with pytest.raises(RuntimeError, match="Exactly 1 of role, admin_id"):
            validator.validate()
