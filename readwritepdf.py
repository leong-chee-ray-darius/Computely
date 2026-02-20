#Read pdf
from pypdf import PdfReader
import json
pdf_path="/content/gdrive/My Drive/Computing/G3 Computing Textbook V4 (Online) (2025-06).pdf"
output_json_path = "/content/gdrive/My Drive/Computing/textbook_data.json"
reader = PdfReader(pdf_path)
pdf_data = []
print("Extracting text...")
for i, page in enumerate(reader.pages):
    page_text = page.extract_text()
    pdf_data.append({
        "page_number": i + 1,
        "content": page_text.strip()
    })
with open(output_json_path, 'w', encoding='utf-8') as f:
    json.dump(pdf_data, f, ensure_ascii=False, indent=4)
print(f"File successfully saved to: {output_json_path}")
