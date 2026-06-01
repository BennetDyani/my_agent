# Agentic AI Practice

A practical exploration of LLM-powered agents using **LangChain** and **Google Generative AI**. This repository demonstrates how to build intelligent agents that interact with external data and services.

## 📋 Project Overview

This project showcases two main use cases:

1. **Health Analyzer** - An intelligent blood health analysis system
2. **LLM Calling** - Examples of calling and configuring LLMs with different parameters

The project is primarily built with **Jupyter Notebooks** (70%) for exploration and learning, with supporting **Python** utilities (30%).

## 📁 Project Structure

```
my_agent/
├── health_analyzer/              # Blood health analysis module
│   ├── blood_health_analysis.ipynb   # Main analysis notebook
│   ├── blood_analysis.txt            # Sample blood report data
│   └── streamlit_app/
│       └── app.py                    # Interactive Streamlit web app
├── llm_calling/                  # LLM integration examples
│   └── simple_llm_calling.ipynb   # Basic LLM calling patterns
├── main.py                       # Entry point
├── pyproject.toml               # Project configuration & dependencies
└── README.md                    # This file
```

## 🔍 What's Inside

### Health Analyzer (`health_analyzer/`)

An intelligent system for analyzing blood test reports and providing health insights.

**Features:**
- **Automated Data Extraction** - Parses blood test reports and extracts numerical values
- **Status Classification** - Classifies each test result as HIGH, LOW, or NORMAL based on reference ranges
- **LLM-Powered Analysis** - Uses Google Gemini AI to generate:
  - Personalized health summaries
  - Diet recommendations (Africa-focused, specifically South African cuisine)
  - Health insights based on the blood work

**Files:**
- `blood_health_analysis.ipynb` - Main notebook demonstrating the full workflow
- `app.py` - Streamlit web interface for interactive analysis
- `blood_analysis.txt` - Sample blood test report for demonstration

**How it works:**
1. Loads a blood analysis report (text format)
2. Parses medical values and extracts test names, numeric values, and reference ranges
3. Classifies each result (Normal/High/Low) based on clinical reference ranges
4. Sends parsed data + patient context to Google Gemini
5. Receives AI-generated health summaries and personalized diet plans

### LLM Calling (`llm_calling/`)

Educational examples of LLM integration patterns.

**Files:**
- `simple_llm_calling.ipynb` - Demonstrates:
  - Basic LLM invocation using LangChain
  - Using system messages to control output
  - Temperature settings for creativity vs. consistency
  - Different LLM models (Google Gemini, Groq)

## 🚀 How It Works

### Architecture

```
Blood Report (text)
        ↓
   Parse & Extract
        ↓
  Classify Results
        ↓
  [LangChain → Google Gemini AI]
        ↓
   AI Analysis + Insights
```

### Key Technologies

| Component | Purpose |
|-----------|---------|
| **LangChain** | LLM framework for chaining operations |
| **Google Generative AI** | Gemini models for analysis and generation |
| **Streamlit** | Interactive web interface |
| **Pandas** | Data parsing and manipulation |
| **Jupyter** | Interactive development & exploration |

## 📦 Dependencies

```toml
langchain>=0.3.0
langchain-core>=1.0.0
langchain-google-genai>=4.2.2
langchain-groq>=0.3.0
python-dotenv>=1.2.2
streamlit>=1.57.0
notebook>=7.5.6
```

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.14+
- Google Generative AI API key (for Gemini models)
- Optional: OpenAI API key (for GPT models)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/BennetDyani/my_agent.git
   cd my_agent
   ```

2. **Install dependencies using `uv` (recommended):**
   ```bash
   uv pip install -e .
   ```

   Or using pip:
   ```bash
   pip install -e .
   ```

3. **Set up environment variables:**
   Create a `.env` file in the project root:
   ```env
   GOOGLE_API_KEY=your_google_api_key_here
   OPENAI_API_KEY=your_openai_api_key_here  # Optional
   ```

## 🎯 Usage

### 1. Run the Streamlit App (Recommended)

```bash
streamlit run health_analyzer/streamlit_app/app.py
```

Then open your browser to `http://localhost:8501`

**Features:**
- Upload your own blood analysis text file
- View parsed test values in a table
- Visualize values as a chart
- Ask the AI custom questions about the report
- Pre-built prompts: Summary, Extract Values, Diet Plan
- Download results as CSV

### 2. Run Jupyter Notebooks

#### Blood Health Analysis:
```bash
jupyter notebook health_analyzer/blood_health_analysis.ipynb
```

Explores:
- Parsing blood reports
- LLM-powered extraction and classification
- Generating health summaries and diet plans

#### LLM Calling Examples:
```bash
jupyter notebook llm_calling/simple_llm_calling.ipynb
```

Covers:
- Basic LLM invocation
- System message control
- Temperature and creativity parameters
- Different model comparisons

### 3. Run Main Script

```bash
python main.py
```

## 📊 Example Workflow

1. **Input:** Blood test report in text format (like `blood_analysis.txt`)
2. **Processing:**
   - Parse test names and values
   - Extract numeric values
   - Compare against reference ranges
3. **Analysis:** Send to Google Gemini
4. **Output:** AI-generated health insights, diet recommendations, risk assessments

## 🔧 Configuration

### Models Used

- **Gemini 2.5 Flash** - Fast, balanced performance (default)
- **Gemini 4 31B** - More detailed responses
- **Groq** - Alternative provider (faster inference)

Change models in notebooks by modifying:
```python
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
```

### Environment Variables

```env
# Google Generative AI
GOOGLE_API_KEY=sk-xxx

# OpenAI (optional)
OPENAI_API_KEY=sk-xxx
```

## 🎓 Learning Resources

This project demonstrates:
- **LLM Integration** - How to call and configure LLMs
- **Prompt Engineering** - System messages, temperature, role-based prompts
- **Data Extraction** - Parsing unstructured medical text
- **Interactive Apps** - Building UIs with Streamlit
- **Agent Patterns** - Multi-step workflows with LLMs

## 🧪 Testing

Run the notebooks to explore different scenarios:
- Different blood report formats
- Varied LLM models and configurations
- Different prompt strategies
- Temperature variations for creativity

## 📝 Example Report Format

The system expects blood reports in this format:

```
Patient: [Name], Age [X], [Gender]
Date: [Date]

COMPLETE BLOOD COUNT (CBC)
--------------------------
Hemoglobin: [value] [units] (Normal: [range])
...

LIPID PANEL
-----------
Total Cholesterol: [value] [units] (Normal: [range])
...
```

See `health_analyzer/blood_analysis.txt` for a complete example.

## 🚧 Future Enhancements

- [ ] Multi-language support for reports
- [ ] PDF report parsing
- [ ] Historical trend analysis
- [ ] Integration with health databases
- [ ] Export reports as PDF
- [ ] Mobile app version

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Submit issues for bugs or suggestions
- Create pull requests with improvements
- Suggest new use cases or LLM integrations

## 📧 Contact

For questions or feedback, please reach out via GitHub issues.

---

**Built with ❤️ for exploring AI agents and LLM capabilities**
