# Architectural View Generation Experiment Repository

## Description
This repository contains the complete experimental data and source code for the study on **LLM-based Automated Architecture View Generation: Where Are We Now?**. The project explores automated knowledge mining from software repositories and the subsequent generation of structured architectural diagrams (Mermaid, PlantUML) using Large Language Models (LLMs).

The study evaluates multiple prompting strategies and AI agents against a grounded truth dataset of hundreds of open-source projects.

## Repository Structure

```text
CodeToDiagram/
├── dataset/                                # Ground truth data and mining scripts
│   ├── filtering/                          # Repo filtering & UML detection logic
│   ├── ground_truth_views/                 # 340+ original diagrams (.png, .jpg)
│   ├── statistics/                         # Quantitative analysis of the dataset
│   ├── download_views.py                   # Script to fetch images from GitHub
│   ├── filtered_dataset.csv                # Detailed metadata for experiments
│   └── random_samples_generator.py         # Utilities for sample selection
├── evaluation/                             # Multi-dimensional evaluation models
│   ├── human_evaluation/                   # Manual rating data and rubrics
│   │   ├── analysis_results/               # IRR and consensus statistical reports
│   │   ├── justifications/                 # Qualitative feedback from human raters
│   │   └── evaluation_rubric.md            # Criteria for Accuracy, Detail, Clarity
│   ├── Image_Similarity_Metrics/           # CV-based automated comparison
│   │   └── check_image_similarity.py       # SSIM/Cosine similarity scripts
│   └── LLM as a judge/                     # Automated LLM-based quality scoring
├── experiments/                            # Core research experimentation logic
│   ├── promptTechniques/                   # Standardized prompting approaches
│   │   ├── zeroShot/                       # [Claude/GPT/DeepSeek] Zero-Shot logic
│   │   ├── 1shot/                          # [Claude/GPT/DeepSeek] One-Shot logic
│   │   ├── fewshot/                        # [Claude/GPT/DeepSeek] Few-Shot logic
│   │   ├── ArchView/                       # Architectural-notation-aware prompts
│   │   └── Agent/                          # Agentic/Iterative generation logic
│   └── Repo_Summary_Extraction/            # Repository context condensation
│       └── Summary_extraction.py           # Logic for creating repo summaries
├── pilot study/                            # Early investigations and baselines
│   ├── scripts/                            # Initial analysis and token counting
│   ├── Code/                               # Early ChatGPT/Gemini view generation
│   ├── Link/                               # Experiments with external documentation links
│   ├── Folder structure/                   # Investigations on repo layout context
│   └── Prompt Engineering/                 # Exploratory prompt template versions

├── figures/                                # Result visualizations (heatmaps, plots)
├── mermaidtrials/                          # Mermaid.js specific experiments
├── src/                                    # Shared project source code
├── requirements.txt                        # Python dependencies
├── install.md                              # Comprehensive setup guide
└── .env.example                            # API configuration template
```

### Directory Details

#### 1. Dataset (`dataset/`)
Contains the curated data used for experiments and evaluation.
- `ground_truth_views/`: 340+ original architectural diagrams from open-source projects.
- `filtered_dataset.csv`: Metadata for the selected repositories, including architectural styles, notations, and granularity.
- `filtering/`: Scripts for data extraction, repository filtering, and statistics generation.
- `statistics/`: Quantitative analysis of the dataset characteristics.

#### 2. Experiments (`experiments/`)
The core of the project, containing various generation approaches.
- `Architectural_knowledge_extraction/`: Scripts for extracting repo-level summaries using LLMs (e.g., `Summary_extraction.py`).
- `promptTechniques/`: Implementation of different prompting strategies across multiple models:
  - `zeroShot/`: Basic generation without examples.
  - `fewshot/`: Generation with context-relevant examples.
  - `Agent/`: Agentic workflows for iterative refinement.
  - `ArchView/`: Specialized templates for architectural notation.
  - Models included: `GPT-4o`, `Claude_3.5_Sonnet`, `Deepseek_V2.5`.

#### 3. Evaluation (`evaluation/`)
Tools and results for assessing the quality of generated views.
- `human_evaluation/`: Manual assessment data using a predefined [evaluation rubric](evaluation/human_evaluation/evaluation_rubric.md).
- `Image_Similarity_Metrics/`: Automated comparison using pixel-based and structural similarity (SSIM, Cosine).
- `LLM as a judge/`: Automated quality evaluation via a "judge" LLM.
- `indepth/`: Comparative data analysis and cross-model performance csv files.

#### 4. Pilot Study (`pilot study/`)
Early-stage investigations and baseline implementations.
- `Code/`: Initial scripts for ChatGPT and Gemini experiments.
- `Prompt Engineering/`: Early iterations of prompt templates.

## Experimental Conditions
The experiment evaluates several generation conditions:

- **Zero-Shot**: Pure generation from repository summaries.
- **One-Shot / Few-Shot**: Providing one or more positive examples of code-to-diagram mappings.
- **Agentic**: Multi-turn interaction to refine the generated diagrams.
- **Approach-based**: Testing templates tailored to specific architectural notations (e.g., boxes and arrows vs. UML).

## AI Agents
The following Large Language Models were evaluated in this study:
- **GPT-4o** (OpenAI)
- **Claude 3.5 Sonnet** (Anthropic)
- **DeepSeek V2.5**
- **Gemini 1.5 Pro/Flash** (used in pilot study and summarization)

## Installation & Setup
To replicate the experiments, please follow the detailed instructions in **[install.md](install.md)**.

### Prerequisites Summary
- Python 3.8+
- [PlantUML](https://plantuml.com/) (requires Java & Graphviz)
- API Keys for the respective LLMs (configured via `.env`)

## Running the Code
Most generation and evaluation scripts are interactive.
```bash
python experiments/promptTechniques/zeroShot/GPT-4o/Code/viewGeneration.py
```
*The script will ask for the input JSONL summary path and use the default if simply Enter is pressed.*

## Configuration
API keys must be stored in a `.env` file at the root directory:
```env
OPENAI_API_KEY=your_key
GEMINI_API_KEY=your_key
CLAUDE_API_KEY=your_key
DEEPSEEK_API_KEY=your_key
```
See **[.env.example](.env.example)** for the template.

## Notes
- All generated outputs are stored within corresponding `results/` or `output_images/` folders within the experiment directories.
- The repository-level summaries used for generation are typically stored in `.jsonl` formats.
- For questions regarding specific evaluation rubrics, refer to `evaluation/human_evaluation/evaluation_rubric.md`.
