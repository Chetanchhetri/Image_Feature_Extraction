import os
import fitz
import ollama
import shutil
from flask import Flask, render_template, request, send_file, jsonify
from fpdf import FPDF
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)

# --- CONFIGURATION ---
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
TEMP_PAGES = os.path.join(BASE_DIR, 'temp_pages')
STATIC_FOLDER = os.path.join(BASE_DIR, 'static')

# Ensure clean directory structure
for folder in [UPLOAD_FOLDER, TEMP_PAGES, STATIC_FOLDER]:
    os.makedirs(folder, exist_ok=True)

class PDFGenerator(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 12)
        if self.page_no() > 1:
            self.cell(0, 10, 'Accesco AI Technical Report', 0, 1, 'C')

def analyze_single_image(img_path):
    prompt = "Extract all technical clearances, dimensions, and reference frames as concise bullet points."
    try:
        response = ollama.chat(
            model="qwen2.5vl:3b",
            messages=[{'role': 'user', 'content': prompt, 'images': [img_path]}]
        )
        return img_path, response['message']['content']
    except Exception as e:
        return img_path, f"Error: {str(e)}"

def run_analysis(image_paths):
    pdf = PDFGenerator()
    report_name = "Analysis_Report.pdf"
    output_path = os.path.join(STATIC_FOLDER, report_name)
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        results = list(executor.map(analyze_single_image, image_paths))

    for i, (path, text) in enumerate(results):
        pdf.add_page()
        pdf.set_font("Helvetica", 'B', 14)
        pdf.cell(0, 10, f"Section {i+1}: Technical Data", 0, 1)
        pdf.image(path, x=10, y=25, w=120)
        pdf.ln(90)
        pdf.set_font("Helvetica", size=10)
        clean_text = text.encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(0, 6, clean_text)

    pdf.output(output_path)
    return report_name

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    files = request.files.getlist("files")
    if not files:
        return jsonify({"error": "No files"}), 400

    image_tasks = []
    for file in files:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        
        if file.filename.lower().endswith('.pdf'):
            doc = fitz.open(file_path)
            for i in range(len(doc)):
                img_name = f"{file.filename}_p{i}.png"
                img_path = os.path.join(TEMP_PAGES, img_name)
                doc[i].get_pixmap(matrix=fitz.Matrix(1.5, 1.5)).save(img_path)
                image_tasks.append(img_path)
        else:
            image_tasks.append(file_path)
    
    report_name = run_analysis(image_tasks)
    
    # Optional: Clean up temp_pages after analysis
    for f in os.listdir(TEMP_PAGES):
        os.remove(os.path.join(TEMP_PAGES, f))
        
    return jsonify({"report_url": f"/download/{report_name}"})

@app.route('/download/<filename>')
def download(filename):
    return send_file(os.path.join(STATIC_FOLDER, filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)