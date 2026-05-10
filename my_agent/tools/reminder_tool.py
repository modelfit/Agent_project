from datetime import datetime, timedelta
from gcsa.google_calendar import GoogleCalendar
from gcsa.event import Event
from gcsa.reminders import EmailReminder
import os


def set_reminder(title: str, date: str, time_str: str, note: str = "", reminder_minutes: int = 30) -> str:
    """
    ينشئ حدثاً في Google Calendar مع تذكير بالبريد الإلكتروني.

    Args:
        title: عنوان التذكير، مثال: 'اجتماع الفريق'
        date: التاريخ بصيغة YYYY-MM-DD، مثال: '2024-12-01'
        time_str: الوقت بصيغة HH:MM، مثال: '09:30'
        note: وصف أو ملاحظة اختيارية
        reminder_minutes: عدد الدقائق قبل الحدث لإرسال التذكير (افتراضي: 30)
    """
    try:
        dt_start = datetime.strptime(f"{date} {time_str}", "%Y-%m-%d %H:%M")

        if dt_start < datetime.now():
            return "خطأ: لا يمكن إنشاء تذكير في وقت مضى."

        dt_end = dt_start + timedelta(hours=1)

        credentials_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "credentials_desktop.json"
        )

        gc = GoogleCalendar(
            credentials_path=credentials_path,
            token_path=os.path.join(
                os.path.dirname(__file__),
                "..",
                "..",
                "token_calendar.pickle"
            )
        )

        event = Event(
            title,
            start=dt_start,
            end=dt_end,
            description=note,
            reminders=[
                EmailReminder(minutes_before_start=reminder_minutes)
            ]
        )

        gc.add_event(event)

        formatted = dt_start.strftime("%Y/%m/%d الساعة %H:%M")
        return (
            f"✅ تم إنشاء التذكير في Google Calendar:\n"
            f"- العنوان: {title}\n"
            f"- الموعد: {formatted}\n"
            f"- سيُرسل تذكير بالبريد الإلكتروني قبل {reminder_minutes} دقيقة"
            + (f"\n- ملاحظة: {note}" if note else "")
        )

    except ValueError:
        return "خطأ: تأكد من صيغة التاريخ (YYYY-MM-DD) والوقت (HH:MM)."
    except Exception as e:
        return f"خطأ في إنشاء التذكير: {str(e)}"


def list_reminders() -> str:
    """
    يعرض التذكيرات القادمة من Google Calendar.
    """
    try:
        credentials_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "credentials_desktop.json"
        )

        gc = GoogleCalendar(
            credentials_path=credentials_path,
            token_path=os.path.join(
                os.path.dirname(__file__),
                "..",
                "..",
                "token_calendar.pickle"
            )
        )

        now = datetime.now()
        events = list(gc.get_events(now, now + timedelta(days=30)))

        if not events:
            return "لا توجد تذكيرات قادمة خلال الـ 30 يوماً القادمة."

        lines = ["📋 التذكيرات القادمة:\n"]
        for i, event in enumerate(events, 1):
            start = event.start
            if isinstance(start, datetime):
                formatted = start.strftime("%Y/%m/%d الساعة %H:%M")
            else:
                formatted = str(start)
            lines.append(f"{i}. {event.summary} — {formatted}")
            if event.description:
                lines.append(f"   ملاحظة: {event.description}")

        return "\n".join(lines)

    except Exception as e:
        return f"خطأ في جلب التذكيرات: {str(e)}"