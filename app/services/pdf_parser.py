import fitz


def extract_text_from_pdf(file_path: str) -> str:
    """Extract plain text from every page of the PDF."""
    text = ""
    try:
        doc = fitz.open(file_path)
        for page in doc:
            text += page.get_text()
        doc.close()
    except Exception as e:
        print(f"Error reading PDF text: {e}")
    return text


def extract_links_from_pdf(file_path: str) -> list:
    """
    Extract all hyperlink URLs embedded in the PDF as clickable annotations.
    These are invisible to get_text() but visible via page.get_links().
    Returns a flat list of URL strings.
    """
    urls = []
    try:
        doc = fitz.open(file_path)
        for page in doc:
            for link in page.get_links():
                # link["uri"] holds the actual href for external/web links
                uri = link.get("uri", "")
                if uri:
                    urls.append(uri)
        doc.close()
    except Exception as e:
        print(f"Error reading PDF links: {e}")
    return urls