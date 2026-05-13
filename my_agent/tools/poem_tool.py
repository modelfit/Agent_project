from ..memory import get_supabase, embed_text


def search_poems(
    query: str,
    theme: str = "",
    poet_era: str = "",
    top_k: int = 3,
) -> str:
    """
    يبحث في قاعدة بيانات الأشعار العربية ويعيد أبيات ذات صلة بالموضوع.
    استخدم هذه الأداة عندما يكتب المستخدم قصيدة أو يطلب شعراً.
    تعيد الأداة أبياتاً مشابهة مع معلومات الشاعر كمرجع للرد الشعري.

    Args:
        query: موضوع القصيدة أو أبيات المستخدم للبحث عن أشعار مشابهة
        theme: تصفية حسب الموضوع مثل 'قصيدة رومانسية' (اختياري)
        poet_era: تصفية حسب العصر مثل 'العصر العباسي' (اختياري)
        top_k: عدد القصائد المطلوبة (افتراضي: 3)
    """
    try:
        query_embedding = embed_text(query)

        result = get_supabase().rpc(
            "match_poems",
            {
                "query_embedding": query_embedding,
                "match_count": top_k * 3,
            }
        ).execute()

        poems = result.data

        if theme:
            poems = [p for p in poems if theme.lower() in (p.get("theme") or "").lower()]

        if poet_era:
            poems = [p for p in poems if poet_era.lower() in (p.get("poet_era") or "").lower()]

        poems = poems[:top_k]

        if not poems:
            return "لم يتم العثور على أشعار مشابهة."

        lines = ["أشعار مشابهة من قاعدة البيانات:\n"]

        for p in poems:
            lines.append(f"### {p.get('title', 'بلا عنوان')}")
            lines.append(
                f"**الشاعر:** {p.get('poet_name', 'مجهول')} | "
                f"**العصر:** {p.get('poet_era', 'غير محدد')} | "
                f"**البحر:** {p.get('meter', 'غير محدد')} | "
                f"**الموضوع:** {p.get('theme', 'غير محدد')}"
            )
            lines.append("")
            verses = p.get("verses", "").split("\n")[:6]
            lines.append("\n".join(verses))
            lines.append("")

        return "\n".join(lines)

    except Exception as e:
        return f"خطأ في البحث عن الأشعار: {str(e)}"