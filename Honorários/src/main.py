import pdfplumber
import json
import os  # Importar o módulo os

# Path to the uploaded file
pdf_file_path = '/media/peixoto/stuff/padroes-direito/Honorários/tabelas/tabela_site_10_2024.pdf'

# Initialize a list to store the extracted data
data = []

# Function to clean and structure extracted text
def process_extracted_text(extracted_text):
    lines = extracted_text.split('\n')
    structured_data = []
    current_section = None
    current_subsection = None
    for line in lines:
        # Skip empty lines or unrelated lines
        if line.strip() == '' or 'ORDEM DOS ADVOGADOS DO BRASIL' in line:
            continue
        # Check if the line is a section header
        if 'TABELA' in line:
            current_section = line.strip()
            continue
        if current_section:
            if 'Obs' in line:
                structured_data.append({"section": current_section, "text": line.strip()})
            else:
                structured_data.append({"section": current_section, "text": line.strip()})
    return structured_data

# Extract text from each page of the PDF and process it
with pdfplumber.open(pdf_file_path) as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        if text:
            page_data = process_extracted_text(text)
            data.extend(page_data)

# Convert the data into a structured JSON format
output_json = json.dumps(data, indent=4, ensure_ascii=False)

# Path to save the JSON output
output_json_path = '/media/peixoto/stuff/padroes-direito/Honorários/extraidos/tabela.json'

# Ensure the output directory exists
os.makedirs(os.path.dirname(output_json_path), exist_ok=True)

# Save the JSON data to a file
with open(output_json_path, 'w', encoding='utf-8') as f:
    f.write(output_json)

output_json_path