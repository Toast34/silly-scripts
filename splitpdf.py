import re
import time
import os
import sys
import pdfplumber
from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import Destination

INPUT_PDF = ""
OUTPUT_ROOT = ""
FOOTER_REGEX = r"\b1\s+of\s+\d+"
FOOTER_RATIO = 0.90
TITLE = ""


def compute_has_children(toc):
    numbers_list = [".".join(e["numbers"]) for e in toc]
    has_children = {}

    for n in numbers_list:
        prefix = n + "."
        has_children[n] = any(
            other != n and other.startswith(prefix)
            for other in numbers_list
        )

    return has_children


# parse table of contents
def parse_toc(pdf, toc_pages):
    """
    Extract TOC entries: numeric hierarchy, title, page number.
    Repairs missing root-level entries (e.g., when TOC starts at 1.1).
    """
    toc = []

    for page in pdf.pages[:toc_pages]:
        text = page.extract_text() or ""
        for line in text.splitlines():
            m = re.match(
                r"^(\d+(?:\.\d+)*)\s+(.+?)\.+\s*(\d+)$",
                line.strip()
            )
            if m:
                numbering = m.group(1)
                title = m.group(2).strip()
                page_no = int(m.group(3)) - 1

                toc.append({
                    "numbers": numbering.split("."),
                    "title": title.split(" .")[0],
                    "page": page_no
                })

    if not toc:
        return []

    toc.sort(key=lambda x: x["page"])

    first = toc[0]

    if len(first["numbers"]) > 1:
        root_num = first["numbers"][0]

        # Check if root already exists
        if not any(e["numbers"] == [root_num] for e in toc):
            toc.insert(0, {
                "numbers": [root_num],
                "title": f"{TITLE}",
                "page": first["page"]
            })

    return toc

# footer detection
def is_footer_page(page):
    footer = page.crop(
        (0, page.height * FOOTER_RATIO, page.width, page.height)
    )
    text = footer.extract_text() or ""
    return re.search(FOOTER_REGEX, text, re.IGNORECASE)

# directory creation
def ensure_folder(numbers, titles_by_number, has_children):
    """
    Creates folders only for non-leaf nodes.
    Leaf nodes return their parent folder.
    """
    path = OUTPUT_ROOT
    os.makedirs(path, exist_ok=True)

    full_label = ".".join(numbers)

    # If this is a leaf, stop at parent
    if not has_children.get(full_label, False):
        numbers = numbers[:-1]

    for i in range(len(numbers)):
        label = ".".join(numbers[:i+1])
        title = titles_by_number[label]
        folder_name = f"{label} {title}"
        path = os.path.join(path, folder_name)
        os.makedirs(path, exist_ok=True)

    return path



# splits pdf into multiple sections based on TOC and footer pages
def split_pdf():
    reader = PdfReader(INPUT_PDF)
    plumber = pdfplumber.open(INPUT_PDF)
    
    toc_pages = 0
    for i, (pl_page, pdf_page) in enumerate(zip(plumber.pages, reader.pages)):
        if is_footer_page(pl_page):
            toc_pages = i
            break
    toc = parse_toc(plumber, toc_pages)

    # Map page → toc entry
    toc_index = 0
    current_toc = toc[0]

    titles_by_number = {
        ".".join(e["numbers"]): e["title"] for e in toc
    }

    writer = PdfWriter()
    start_page = 0
    
    has_children = compute_has_children(toc)

    def save_section(start_page_idx):
        nonlocal writer
        print(current_toc)
        label = ".".join(current_toc["numbers"])
        
        folder = ensure_folder(
            current_toc["numbers"],
            titles_by_number,
            has_children
        )
        
        filename = f"{label} {current_toc['title']}.pdf"
        filename = re.sub(r"[^\w\d .-]", "", filename)
        print(folder)
        print(filename)
        for attempt in range(5):
            try:
                output_path = os.path.join(folder, filename)
                with open(output_path, "wb") as f:
                    writer.write(f)
                break
            except PermissionError:
                if attempt == 4:
                    raise
                time.sleep(0.1)

        print(f"Created: {output_path}")
        writer = PdfWriter()

    for i, (pl_page, pdf_page) in enumerate(zip(plumber.pages, reader.pages)):
        # Advance TOC entry based on page index
        if toc_index + 1 < len(toc) and i >= toc[toc_index + 1]["page"]:
            save_section(start_page)
            toc_index += 1
            current_toc = toc[toc_index]
            start_page = i

        if is_footer_page(pl_page):
            save_section(start_page)
            start_page = i

        writer.add_page(pdf_page)

    save_section(start_page)
    plumber.close()


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python splitpdf.py [Title] [path-to-input-pdf] [path-to-output-folder]")
        exit()
    TITLE = sys.argv[1]
    INPUT_PDF = sys.argv[2]
    OUTPUT_ROOT = sys.argv[3]
    split_pdf()