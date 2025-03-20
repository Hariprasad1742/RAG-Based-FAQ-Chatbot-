import fitz  # PyMuPDF
import pandas as pd

# Load PDF
pdf_path = r"E:\dvserse\Chatbot\FAQ_Dataset.pdf"
doc = fitz.open(pdf_path)

doc = fitz.open(pdf_path)

faq_list = []
current_category = ""

# Extract text from PDF
for page in doc:
    text = page.get_text("text")
    lines = text.split("\n")
    
    for line in lines:
        if line.startswith("Category:"):
            current_category = line.replace("Category: ", "").strip()
        elif line.startswith("Q: "):
            question = line.replace("Q: ", "").strip()
        elif line.startswith("A: "):
            answer = line.replace("A: ", "").strip()
            faq_list.append((current_category, question, answer))

# Convert to DataFrame and save as CSV
faq_df = pd.DataFrame(faq_list, columns=["Category", "Question", "Answer"])
faq_df.to_csv("faq_dataset.csv", index=False)

print("✅ FAQ data extracted and saved as faq_dataset.csv")
