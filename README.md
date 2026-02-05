VisionExtract: Multimodal Feature Intelligence
VisionExtract is a high-performance image feature extraction engine designed to bridge the "Semantic Gap" in RAG pipelines. Powered by the Qwen2.5-VL-3B Vision-Language Model, it transforms complex visual data—like nested tables, technical diagrams, and flowcharts—into structured, LLM-ready context.

🚀 Key Features
Hierarchical Table Extraction: Preserves the structural integrity of complex tables (Markdown/JSON) that standard OCR often flattens.

Diagram-to-Logic Mapping: Converts technical schematics and flowcharts into logical text chains for better RAG retrieval.

Spatial Awareness: Utilizes the vision-language core to identify object coordinates and anchor points.

Edge-Ready Performance: Optimized using the 3B parameter version of Qwen2.5-VL for rapid, local inference.

🛠️ Installation
1. Prerequisites
Python 3.10+

CUDA-compatible GPU (Recommended for 3B model inference)

Ollama (If running via Ollama) or Hugging Face Transformers

2. Clone the Repository
Bash
git clone https://github.com/yourusername/VisionExtract.git
cd VisionExtract
3. Set Up Environment
Bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
4. Pull the Model
If you are using Ollama:

Bash
ollama pull qwen2.5-vl:3b
💻 Usage
Running the Web UI
The project includes a clean, white "Vision-Extract" UI for easy batch processing.

Bash
python app.py
Then navigate to http://localhost:5000 in your browser.

API Example (Python)
You can also use the extraction engine programmatically:

Python
from vision_extract import ExtractCore

# Initialize the engine
extractor = ExtractCore(model="qwen2.5-vl:3b")

# Extract structured data from a technical diagram
result = extractor.analyze("path/to/diagram.png", prompt="Extract all components and their connections as a JSON graph.")

print(result)
📂 Project Structure
/app.py - FastAPI/Flask backend server.

/templates - Frontend UI 

/core - Model inference logic and prompt engineering.

/test_assets - Sample images for benchmarking (Blueprints, Tables, MRI scans).

🤝 Contributing
Contributions are welcome! Please open an issue or submit a pull request for any feature enhancements.

📄 License
MIT License - See LICENSE for details.
