from duckduckgo_search import DDGS


def web_search(query: str, max_results: int = 20) -> str:
    """
    يبحث في الإنترنت عن معلومات حديثة باستخدام DuckDuckGo.
    استخدم هذه الأداة عندما يسأل المستخدم عن أخبار حديثة أو معلومات
    غير موجودة في المستندات المرفوعة.

    Args:
        query: نص البحث
        max_results: عدد النتائج المطلوبة (افتراضي: 20)
    """
    try:
        results = []

        with DDGS() as ddgs:
            search_results = ddgs.text(
                query,
                max_results=max_results,
            )

            for r in search_results:
                results.append(
                    f"### {r['title']}\n"
                    f"{r['body']}\n"
                    f"{r['href']}\n"
                )

        if not results:
            return "لم يتم العثور على نتائج لهذا البحث."

        header = f"نتائج البحث عن: {query}\n\n"
        return header + "\n---\n".join(results)

    except Exception as e:
        return f"خطأ في البحث: {str(e)}"