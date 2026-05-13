from ..memory import search_memory, format_memories, load_recent, clear_memory


def recall_memory(query: str, session_id: str = "default_session") -> str:
    """
    يبحث في ذاكرة المحادثات السابقة عن معلومات ذات صلة.
    استخدم هذه الأداة عندما يسأل المستخدم عن شيء قيل سابقاً
    أو يريد استرجاع معلومة من محادثة قديمة.

    كيف تعمل:
        1. يحول السؤال إلى متجه (embedding)
        2. يبحث في Supabase عن أقرب المحادثات السابقة
        3. يعيد النتائج الأكثر صلة بالسياق الحالي

    Args:
        query: ما يريد المستخدم تذكره أو البحث عنه
        session_id: معرف الجلسة (افتراضي: default_session)
    """
    memories = search_memory(session_id, query)
    if not memories:
        return "لم يتم العثور على ذكريات ذات صلة بهذا الموضوع."
    return format_memories(memories)


def show_chat_history(session_id: str = "default_session") -> str:
    """
    يعرض آخر 20 رسالة من سجل المحادثة بالترتيب الزمني.
    يفيد عند الحاجة لرؤية ما تم التحدث عنه مؤخراً.

    Args:
        session_id: معرف الجلسة (افتراضي: default_session)
    """
    messages = load_recent(session_id)
    if not messages:
        return "لا يوجد سجل محادثة محفوظ."

    lines = ["📜 سجل المحادثة الأخير:\n"]
    for msg in messages:
        role_label = "أنت" if msg["role"] == "user" else "المساعد"
        lines.append(f"{role_label}: {msg['content']}")
    return "\n".join(lines)


def forget_everything(session_id: str = "default_session") -> str:
    """
    يمسح كامل ذاكرة المحادثة لهذه الجلسة من Supabase.
    لا يمكن التراجع عن هذا الإجراء.

    Args:
        session_id: معرف الجلسة (افتراضي: default_session)
    """
    return clear_memory(session_id)