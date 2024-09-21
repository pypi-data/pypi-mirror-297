def validate_disabled_introspection_types(value):
    # check type of DISABLED_INTROSPECTION_TYPES
    if not isinstance(value, list):
        raise ValueError("DISABLED_INTROSPECTION_TYPES must be a list")

    # check if every element in DISABLED_INTROSPECTION_TYPES starts with "__"
    if not all([t.startswith("__") for t in value]):
        raise ValueError(
            "Every element in DISABLED_INTROSPECTION_TYPES must start with '__'"
        )
