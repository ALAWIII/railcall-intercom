class InputValidator:
    """
    Validates raw inputs based on presence rules.

    Example:
        InputValidator(
            inputs,
            at_least=[{"fields": ["email", "external_id", "role"], "count": 1}],
            exactly=[{"fields": ["phone", "email"], "count": 1}],
            at_most=[{"fields": ["phone", "email", "external_id"], "count": 2}],
        ).validate()
    """

    def __init__(
        self,
        inputs: dict,
        *,
        exactly: list[dict] | None = None,
        at_least: list[dict] | None = None,
        at_most: list[dict] | None = None,
    ):
        """Initializes the validator with raw inputs and validation rules."""

        self.inputs = inputs or {}
        self.exactly = self._normalize(exactly, default_count=1)
        self.at_least = self._normalize(at_least, default_count=1)
        self.at_most = self._normalize(at_most, default_count=1)

    def validate(self) -> None:
        """Executes all configured validation rules and raises RuntimeError on failure."""
        self._exactly()
        self._at_least()
        self._at_most()

    def _exactly(self) -> None:
        """Validates that an exact number of specified fields are present, its much like xor for n valuse."""
        for rule in self.exactly:
            fields = rule["fields"]
            count = rule["count"]
            present = self._present_fields(fields)

            if len(present) != count:
                raise RuntimeError(self._exactly_error(fields, count, present))

    def _at_least(self) -> None:
        """Validates that a minimum number of specified fields are present."""

        for rule in self.at_least:
            fields = rule["fields"]
            count = rule["count"]
            present = self._present_fields(fields)

            if len(present) < count:
                raise RuntimeError(self._at_least_error(fields, count, present))

    def _at_most(self) -> None:
        """Validates that no more than a maximum number of specified fields are present."""

        for rule in self.at_most:
            fields = rule["fields"]
            count = rule["count"]
            present = self._present_fields(fields)

            if len(present) > count:
                raise RuntimeError(self._at_most_error(fields, count, present))

    def _present_fields(self, fields: list) -> list:
        """Returns a list of fields from the given list that have non-empty values in inputs."""

        return [field for field in fields if self._is_present(self.inputs.get(field))]

    def _exactly_error(self, fields: list, count: int, present: list) -> str:
        """Generates a descriptive error message for 'exactly' rule violations."""
        provided = self._format(present)

        if len(present) < count:
            missing = [field for field in fields if field not in present]
            needed = count - len(present)

            return (
                f"Exactly {count} of {self._format(fields)} must be provided. "
                f"Provided: {provided}. "
                f"Add {needed} of: {self._format(missing)}."
            )

        extra = len(present) - count

        return (
            f"Exactly {count} of {self._format(fields)} must be provided. "
            f"Provided: {provided}. "
            f"Remove {extra} of: {self._format(present)}."
        )

    def _at_least_error(self, fields: list, count: int, present: list) -> str:
        """Generates a descriptive error message for 'at_least' rule violations."""

        provided = self._format(present)
        missing = [field for field in fields if field not in present]
        needed = count - len(present)

        return (
            f"At least {count} of {self._format(fields)} must be provided. "
            f"Provided: {provided}. "
            f"Add at least {needed} of: {self._format(missing)}."
        )

    def _at_most_error(self, fields: list, count: int, present: list) -> str:
        """Generates a descriptive error message for 'at_most' rule violations."""

        provided = self._format(present)
        extra = len(present) - count

        return (
            f"At most {count} of {self._format(fields)} may be provided. "
            f"Provided: {provided}. "
            f"Remove {extra} of: {self._format(present)}."
        )

    @staticmethod
    def _is_present(value) -> bool:
        """Checks if a value is considered present (not None or empty string/list/dict)."""

        if value is None:
            return False
        return not (isinstance(value, (str, list, dict)) and len(value) == 0)

    @staticmethod
    def _format(fields: list) -> str:
        """Formats a list of strings into a comma-separated string, or 'none' if empty."""

        return ", ".join(fields) if fields else "none"

    @staticmethod
    def _normalize(rules: list | None, default_count: int) -> list:
        """Standardizes rule inputs into a consistent dictionary format."""

        if not rules:
            return []

        if isinstance(rules, dict):
            rules = [rules]

        if all(isinstance(field, str) for field in rules):
            return [{"fields": rules, "count": default_count}]

        normalized = []

        for rule in rules:
            if isinstance(rule, dict):
                fields = rule.get("fields", [])
                count = rule.get("count", default_count)
                normalized.append({"fields": fields, "count": count})
            else:
                normalized.append({"fields": list(rule), "count": default_count})

        return normalized
