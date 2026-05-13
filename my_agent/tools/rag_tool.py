from ..rag.retriever import retrieve


def search_documents(query: str) -> str:
    """
    يبحث في المستندات المرفوعة للإجابة على سؤال المستخدم.
    استخدم هذه الأداة عندما يسأل المستخدم عن محتوى ملف
    أو يريد معلومة من المستندات التي تم رفعها مسبقاً.

    كيف تعمل:
        1. يحول السؤال إلى متجه (embedding) بنفس النموذج
           المستخدم عند رفع الملفات (IBM Granite)
        2. يبحث في Supabase عن أقرب أجزاء المستندات
        3. يعيد النص الأكثر صلة بالسؤال

    الفرق بين search_documents و recall_memory:
        - search_documents → يبحث في الملفات المرفوعة
        - recall_memory    → يبحث في تاريخ المحادثات

    Args:
        query: سؤال المستخدم أو الموضوع المراد البحث عنه
    """
    try:
        results = retrieve(query)

        if not results:
            return "لم يتم العثور على معلومات ذات صلة في المستندات المرفوعة."

        combined = "\n\n---\n\n".join(results)
        return f"المعلومات ذات الصلة من المستندات:\n\n{combined}"

    except Exception as e:
        return f"خطأ أثناء البحث في المستندات: {str(e)}"