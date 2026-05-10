from .calculator_tool import calculator
from .hijri_tool import hijri_to_gregorian, gregorian_to_hijri
from .email_tool import send_email
from .reminder_tool import set_reminder, list_reminders
# from .rag_tool import search_documents

all_tools = [
    calculator,
    hijri_to_gregorian,
    gregorian_to_hijri,
    send_email,
    set_reminder,
    list_reminders,
    # search_documents,
]