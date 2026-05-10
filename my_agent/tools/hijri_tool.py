from hijridate import Gregorian, Hijri


def hijri_to_gregorian(year: int, month: int, day: int) -> str:
    """
    يحوّل التاريخ الهجري إلى ميلادي.

    Args:
        year: السنة الهجرية، مثال: 1445
        month: الشهر الهجري (1-12)، مثال: 9
        day: اليوم الهجري (1-30)، مثال: 1
    """
    try:
        gregorian = Hijri(year, month, day).to_gregorian()
        return f"التاريخ الميلادي: {gregorian.year}-{gregorian.month:02d}-{gregorian.day:02d}"
    except Exception as e:
        return f"خطأ في تحويل التاريخ: {str(e)}"


def gregorian_to_hijri(year: int, month: int, day: int) -> str:
    """
    يحوّل التاريخ الميلادي إلى هجري.

    Args:
        year: السنة الميلادية، مثال: 2024
        month: الشهر الميلادي (1-12)، مثال: 3
        day: اليوم الميلادي (1-31)، مثال: 15
    """
    try:
        hijri = Gregorian(year, month, day).to_hijri()
        return f"التاريخ الهجري: {hijri.year}-{hijri.month:02d}-{hijri.day:02d}"
    except Exception as e:
        return f"خطأ في تحويل التاريخ: {str(e)}"