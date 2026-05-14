from .calculator_tool import calculator
from .hijri_tool import hijri_to_gregorian, gregorian_to_hijri
from .reminder_tool import set_reminder, list_reminders
from .email_tool import send_email
from .rag_tool import search_documents
from .memory_tool import recall_memory, show_chat_history, forget_everything
from .prayer_tool import get_prayer_times
from .websearch_tool import web_search
from .poem_tool import search_poems
# from .pdfmerge_tool import merge_pdfs
from .unit_converter import convert_units

all_tools = [
    calculator,
    hijri_to_gregorian,
    gregorian_to_hijri,
    set_reminder,
    list_reminders,
    send_email,
    search_documents,
    recall_memory,
    show_chat_history,
    forget_everything,
    get_prayer_times,
    web_search,
    search_poems,
    # merge_pdfs,
    convert_units

]