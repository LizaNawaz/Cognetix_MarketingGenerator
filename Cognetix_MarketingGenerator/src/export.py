from fpdf import FPDF


def make_text_export(drafts, metadata=None):
    metadata = metadata or {}

    lines = [
        "Cognetix AI Marketing Content Generator",
        f"Product: {metadata.get('product', '')}",
        f"Platform: {metadata.get('platform', '')}",
        f"Tone: {metadata.get('tone', '')}",
        f"Length: {metadata.get('length', '')}",
        f"Language: {metadata.get('language', '')}",
        ""
    ]

    for index, draft in enumerate(drafts, start=1):
        lines.extend([
            f"VARIATION {index}",
            f"Headline / Subject: {draft.get('headline', '')}",
            "",
            draft.get("content", ""),
            "",
            "Hashtags: " + " ".join(
                draft.get("hashtags", [])
            ),
            "",
            "-" * 45,
            ""
        ])

    return "\n".join(lines)


def _safe_text(value):
    """
    Built-in Helvetica has limited Unicode support.
    Replace unsupported characters to prevent PDF errors.
    """
    value = str(value)

    replacements = {
        "\u2019": "'",
        "\u2018": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2013": "-",
        "\u2014": "-",
        "\u2026": "..."
    }

    for old, new in replacements.items():
        value = value.replace(old, new)

    return value.encode(
        "latin-1",
        errors="replace"
    ).decode("latin-1")


def make_pdf_export(drafts, metadata=None):
    metadata = metadata or {}

    pdf = FPDF()
    pdf.set_auto_page_break(
        auto=True,
        margin=15
    )

    pdf.add_page()

    pdf.set_font("Helvetica", "B", 16)
    pdf.multi_cell(
        0,
        10,
        "Cognetix AI Marketing Content Generator"
    )

    pdf.ln(3)
    pdf.set_font("Helvetica", size=10)

    details = (
        f"Product: {metadata.get('product', '')}\n"
        f"Platform: {metadata.get('platform', '')}\n"
        f"Tone: {metadata.get('tone', '')}\n"
        f"Length: {metadata.get('length', '')}\n"
        f"Language: {metadata.get('language', '')}"
    )

    pdf.multi_cell(
        0,
        6,
        _safe_text(details)
    )

    for index, draft in enumerate(drafts, start=1):
        pdf.ln(5)

        pdf.set_font("Helvetica", "B", 13)

        heading = (
            f"Variation {index}: "
            f"{draft.get('headline', '')}"
        )

        pdf.multi_cell(
            0,
            7,
            _safe_text(heading)
        )

        pdf.ln(2)
        pdf.set_font("Helvetica", size=11)

        pdf.multi_cell(
            0,
            6,
            _safe_text(draft.get("content", ""))
        )

        hashtags = " ".join(
            draft.get("hashtags", [])
        )

        if hashtags:
            pdf.ln(2)
            pdf.multi_cell(
                0,
                6,
                _safe_text(f"Hashtags: {hashtags}")
            )

    output = pdf.output()

    if isinstance(output, bytearray):
        return bytes(output)

    return output