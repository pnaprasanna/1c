import sys
import re
from pathlib import Path

BM_FILE = Path("bm.md")
COLUMNS = ["Info", "URL", "Explanation", "Tags"]

def main():
    if len(sys.argv) != 5:
        print("Usage: python add_record.py <Info> <URL> <Explanation> <Tags>")
        sys.exit(1)

    info, url, explanation, tags = sys.argv[1:]

    if not all([info, url, explanation, tags]):
        raise ValueError("All fields are required")

    if not re.match(r"^https?://", url):
        raise ValueError("Invalid URL")

    lines = BM_FILE.read_text(encoding="utf-8").splitlines()
    rows = [l for l in lines if l.strip().startswith("|")][2:]

    if any(url in r for r in rows):
        raise ValueError("Duplicate URL")

    new_row = f"| {info} | {url} | {explanation} | {tags} |"
    insert_at = max(i for i, l in enumerate(lines) if l.strip().startswith("|")) + 1
    lines.insert(insert_at, new_row)
    BM_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("✅ Record added")

if __name__ == "__main__":
    main()
``
