# Architectural View Generation Experiment Repository

## Description
This repository contains the complete experimental data and source code for the study on **LLM-based Automated Architecture View Generation: Where Are We Now?**. The project explores automated knowledge mining from software repositories and the subsequent generation of structured architectural diagrams (Mermaid, PlantUML) using Large Language Models (LLMs).

The study evaluates multiple prompting strategies and AI agents against a grounded truth dataset of hundreds of open-source projects for generating the Architectural Views.

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
│   │   ├── ArchView/                       # Architectural-notation-aware 
│   │   └── Agent/                          # Agentic using claude code
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


## Installation & Setup
To replicate the experiments, please follow the detailed instructions in **[install.md](install.md)**.

### Prerequisites Summary
- Python 3.8+
- [PlantUML](https://plantuml.com/) (requires Java & Graphviz)
- API Keys for the respective LLMs (configured via `.env`)

## Replication Guide (Step-by-Step)

To reproduce the results (tables, figures, and metrics) presented in the paper, follow these steps:

### 1. Architectural View Generation
First, generate the diagrams for a specific experimental setting:
- Navigate to the `experiments/promptTechniques/` directory.
- Choose a configuration (e.g., `zeroShot/GPT-4o/`).
- Run the `viewGeneration.py` script located in the `Code/` folder of your chosen setting.
  ```bash
  python experiments/promptTechniques/zeroShot/GPT-4o/Code/viewGeneration.py
  ```
- This will generate architectural code (Mermaid/PlantUML) and corresponding images in the `Results/` directory of that experiment.

### 2. Output Evaluation
Once views are generated, evaluate them using automated metrics:

#### A. Image Similarity (SSIM/Cosine)
- Navigate to `evaluation/Image_Similarity_Metrics/`.
- Run `check_image_similarity.py`. When prompted, provide the path to your generated images folder and the ground truth folder (`dataset/ground_truth_views/`).
  ```bash
  python evaluation/Image_Similarity_Metrics/check_image_similarity.py
  ```

#### B. LLM as a Judge (Quality Scoring)
- Navigate to `evaluation/LLM as a judge/`.
- Run `evaluation_3cs.py` to get automated scores for Accuracy, Detail, and Clarity.
  ```bash
  python evaluation/LLM as a judge/evaluation_3cs.py
  ```

### 3. Result Aggregation and Table Generation
After evaluation, move the resulting `.csv` files to the `Results/` folder of the corresponding experiment. Then:
- Use `calculate.py` to aggregate statistics and generate summary metrics.
- Use `llm_analysis.py` to process judge scores and produce formatting for the tables presented in the paper.
- These scripts are available in each `Results/` subdirectory (e.g., `experiments/promptTechniques/zeroShot/GPT-4o/Results/`).

### 4. Human Evaluation
For details on manual assessment, refer to the `evaluation/human_evaluation/` directory.
- Review the `evaluation_rubric.md` for scoring criteria.
- Consistency and consensus results can be analyzed using `consensus_rating.py`.
- To check the samples used in the human evaluation, please check [human evaluation website](https://elegant-lily-a7bdfd.netlify.app)

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
- To check the human evaluation website, please check the website [human evaluation](https://elegant-lily-a7bdfd.netlify.app)