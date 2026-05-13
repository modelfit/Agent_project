def convert_units(value: float, from_unit: str, to_unit: str) -> str:
    """
    Converts a value between units. Use when the user wants to convert measurements.

    Supported conversions: km↔miles, kg↔lb, celsius↔fahrenheit

    Args:
        value: The number to convert. e.g. 100
        from_unit: The source unit. e.g. "km", "kg", "celsius"
        to_unit: The target unit. e.g. "miles", "lb", "fahrenheit"

    Returns:
        Converted result as a string, or an error message if the conversion is unsupported.
    """

    try:

        conversions = {

            ("km", "miles"): value * 0.621371,

            ("miles", "km"): value / 0.621371,

            ("kg", "lb"): value * 2.20462,

            ("lb", "kg"): value / 2.20462,

            ("celsius", "fahrenheit"): (value * 9/5) + 32,

            ("fahrenheit", "celsius"): (value - 32) * 5/9,
        }

        key = (from_unit.lower(), to_unit.lower())

        if key not in conversions:
            return "خطأ: التحويل غير مدعوم."

        result = conversions[key]

        return f"✅ النتيجة: {round(result, 2)}"

    except Exception as e:

        return f"خطأ: {str(e)}"