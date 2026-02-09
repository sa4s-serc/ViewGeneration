# Installation & Setup Guide

This guide provides professional instructions to set up the environment required to replicate the architectural view generation experiments.

## Prerequisites

Before starting, ensure you have the following installed on your system:

- **Python 3.8+**: The core programming language used for the project scripts.
- **PlantUML**: Required for generating diagrams from `.puml` files.
- **Java (JRE/JDK)**: Required to run PlantUML.
- **Graphviz**: Required for certain diagram layouts (like UML class diagrams) within PlantUML.

## Setup Instructions

### 1. Clone the Repository

Begin by cloning the project repository to your local machine:

```bash
cd CodeToDiagram
```

### 2. Virtual Environment Setup

It is highly recommended to use a virtual environment to manage dependencies and avoid conflicts:

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
.\venv\Scripts\activate
```

### 3. Install Python Dependencies

Once the virtual environment is active, install the necessary libraries:

```bash
pip install -r requirements.txt
```

### 4. Configure API Keys

The project utilizes various Large Language Models (LLMs). Follow these steps to configure your API access:

1. Create a `.env` file from the provided template:
   ```bash
   cp .env.example .env
   ```
2. Open the newly created `.env` file in a text editor.
3. Add your respective API keys for the models you intend to use:
   - `OPENAI_API_KEY`
   - `GEMINI_API_KEY`
   - `CLAUDE_API_KEY`
   - `DEEPSEEK_API_KEY`

## Running the Code

When the scripts are executed, they will prompt you for input file paths. 

- **Interactive Inputs**: Most scripts allow you to specify custom paths or press **Enter** to proceed with the default values.
- **Example Usage**:
  ```bash
  python experiments/promptTechniques/zeroShot/GPT-4o/Code/viewGeneration.py
  ```
