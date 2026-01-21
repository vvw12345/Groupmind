# Groupmind - Social Intelligence Evaluation Dataset Platform

<div align="center">

![Project Architecture](image/Fig2.drawio.png)

**A comprehensive platform for generating, annotating, and evaluating social intelligence datasets**

</div>

---

## 📋 Overview

Groupmind is a complete social intelligence evaluation dataset platform designed to assess large language models' understanding capabilities in complex social scenarios. The platform consists of three core modules: data generation, human annotation verification, and model evaluation, supporting multi-language (Chinese, English) social scenario dialogue dataset construction and assessment.

### Core Objectives

- **Data Generation**: Automatically generate diverse social scenario dialogue datasets
- **Quality Assurance**: Provide human annotation platform to verify AI-generated data quality
- **Model Evaluation**: Systematically evaluate different LLMs' social intelligence capabilities
- **Multi-language Support**: Chinese, English

---

## 🎯 Key Features

### 1. Data Generation Module (`data_generator/`)

![Data Generation Pipeline](image/fig3.drawio.png)

**Highlights:**
- Multi-platform API support (AgentWorld GPT-5.1, SiliconFlow, OpenRouter)
- Multi-language data generation (Chinese, English)
- Three-stage generation pipeline:
  - **Scenario Generation**: Create diverse social scenarios and character settings
  - **Dialogue Simulation**: Generate natural multi-turn dialogues
  - **Label Annotation**: Automatically generate evaluation labels (Atmosphere Recognition, KY Test, Intent Inference)
- Supports scene × atmosphere combination indexing for data diversity
- Real-time saving and progress tracking

**Usage Example:**
```bash
# Generate 200 Chinese samples
python data_generator/pipeline.py --num 200 --language zh --model gpt-5.1

# Generate 100 English samples
python data_generator/pipeline.py --num 100 --language en --model deepseek-v3
```

### 2. Human Annotation Platform (`platform/`)

**Highlights:**
- **Web Interface**: Intuitive annotation interface based on Flask
- **Three Evaluation Tasks**:
  - Atmosphere Recognition
  - KY Test (Social Intelligence Test)
  - Intent Inference
- **Comparison Analysis**: Real-time display of differences between human annotations and AI-generated results
- **Data Saving**: Automatically save annotation results to `annotated_data/` directory

**Start Platform:**
```bash
cd platform
pip install -r requirements.txt
python app.py
```
Visit: http://localhost:5000

### 3. AI Annotation Accuracy Analysis Tool (`platform/`)

**Highlights:**
- Calculate consistency between AI annotations and human annotations
- Generate academic-style analysis reports
- Multi-dimensional accuracy analysis (overall, task-level, theme-level)
- Visualization generation (accuracy tables, task comparison charts, agreement heatmaps)

**Run Analysis:**
```bash
cd platform
python run_analysis.py
```

### 4. Model Evaluation System (`evaluation/`)

**Highlights:**
- **Multi-threaded Evaluation**: Support evaluating multiple models simultaneously
- **Flexible Configuration**: Support different evaluation modes (full omniscient view, limited information, chat mode)
- **Multi-platform Support**: OpenRouter, SiliconFlow, AgentWorld, Yunwu AI
- **Resume Evaluation**: Support continuing from specified sample positions
- **Detailed Reports**: Generate complete evaluation results and statistics

**Run Evaluation:**
```bash
cd evaluation
python run_evaluation.py \
  --data ../data_generator/data/benchmark_zh.json \
  --models deepseek-v3 gpt-4 \
  --platform openrouter \
  --language zh \
  --mode full
```


## 🚀 Quick Start

### Requirements

- Python 3.8+
- Flask (for annotation platform)
- requests (API calls)

### Install Dependencies

```bash
# Install annotation platform dependencies
pip install -r platform/requirements.txt

# Install evaluation system dependencies
pip install requests pandas matplotlib seaborn
```

### Complete Workflow

1. **Generate Dataset**
```bash
cd data_generator
python pipeline.py --num 200 --language zh --model gpt-5.1
```

2. **Human Annotation Verification**
```bash
cd ../platform
python app.py
# Visit http://localhost:5000 in browser for annotation
```

3. **Analyze Annotation Quality**
```bash
python run_analysis.py
```

4. **Evaluate Model Performance**
```bash
cd ../evaluation
python run_evaluation.py \
  --data ../data_generator/data/benchmark_zh_N200_*.json \
  --models deepseek-v3 gpt-4 \
  --platform openrouter
```

---


### Evaluation Tasks

1. **Atmosphere Recognition**: Determine the overall atmosphere and emotional tone of the dialogue
2. **KY Test**: Evaluate the character's emotional intelligence and social sensitivity
3. **Intent Inference**: Analyze the character's true intentions and motivations

---

## 🔧 Configuration

### API Key Configuration

Configure API keys in `data_generator/config.py`:

```python
OPENROUTER_CONFIG = {
    "api_keys": ["your-key-1", "your-key-2"],
    "models": ["deepseek-v3", "gpt-4", ...]
}

SILICONFLOW_CONFIG = {
    "api_keys": ["your-key-1"],
    "models": ["deepseek-v3", ...]
}
```



## 📁 Project Structure

```
Groupmind/
├── data_generator/          # Data generation module
│   ├── api_client.py       # Multi-platform API client
│   ├── pipeline.py         # Data generation pipeline
│   ├── dialogue_simulator.py  # Dialogue simulator
│   ├── label_annotator.py  # Label annotator
│   ├── scenario_generator.py  # Scenario generator
│   ├── data/               # Generated data files
│   └── prompt/             # Prompt templates
├── platform/               # Human annotation platform
│   ├── app.py              # Flask application
│   ├── analysis.py         # Accuracy analysis tool
│   ├── annotation_analysis.py  # Annotation analysis
│   ├── templates/          # Frontend templates
│   ├── static/             # Static resources
│   ├── annotated_data/     # Human annotation results
│   └── requirements.txt    # Python dependencies
├── evaluation/             # Model evaluation system
│   ├── run_evaluation.py   # Evaluation entry point
│   ├── evaluator.py        # Evaluation core
│   └── eval_client_bilingual.py  # Bilingual evaluation client
├── image/                  # Project images
│   ├── Fig2.drawio.png     # Project architecture diagram
│   └── fig3.drawio.png     # Data generation flow diagram
└── README.md               # Project documentation
```
