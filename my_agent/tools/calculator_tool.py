def calculator(expression: str) -> str:
    """
    يحسب العمليات الحسابية الرياضية.
    استخدم هذه الأداة لأي عملية حسابية مثل الجمع والطرح والضرب والقسمة.

    Args:
        expression: العملية الحسابية كنص، مثال: '15 * 3 + 10'
    """
    try:
        allowed = set("0123456789+-*/(). ")
        if not all(c in allowed for c in expression):
            return "خطأ: العملية الحسابية تحتوي على رموز غير مسموح بها."

        result = eval(expression)
        return f"نتيجة العملية '{expression}' = {result}"

    except ZeroDivisionError:
        return "خطأ: لا يمكن القسمة على صفر."

    except Exception as e:
        return f"خطأ في العملية الحسابية: {str(e)}"