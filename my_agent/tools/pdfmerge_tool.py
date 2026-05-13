from PyPDF2 import PdfMerger


def merge_pdfs(pdf_files: list, output_file: str) -> str:
    """
    Merges multiple PDF files into one. Use when the user wants to combine PDFs.

    Args:
        pdf_files: Ordered list of PDF file paths to merge. e.g. ["/a.pdf", "/b.pdf"]
        output_file: File path for the merged output. e.g. "/merged.pdf"

    Returns:
        Success message with output path, or an error message if it failed.
    """

    try:

        merger = PdfMerger()

        for pdf in pdf_files:
            merger.append(pdf)

        merger.write(output_file)

        merger.close()

        return f" تم دمج ملفات PDF في: {output_file}"

    except Exception as e:

        return f"خطأ في دمج ملفات PDF: {str(e)}"