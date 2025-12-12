"""
Embedding-based metrics: BERTScore
"""

import evaluate
from typing import List, Dict
import numpy as np


def compute_bertscore(predictions: List[str], references: List[str], 
                     model_type: str = "microsoft/deberta-xlarge-mnli") -> Dict[str, float]:
    """
    Compute BERTScore.
    
    Args:
        predictions: List of generated summaries
        references: List of reference summaries
        model_type: Model to use for BERTScore
        
    Returns:
        Dictionary with BERTScore (precision, recall, F1)
    """
    print(f"Computing BERTScore (using {model_type})...")
    
    bertscore = evaluate.load("bertscore")
    
    results = bertscore.compute(
        predictions=predictions,
        references=references,
        model_type=model_type,
        lang="en"
    )
    
    return {
        "bertscore_precision": np.mean(results["precision"]),
        "bertscore_recall": np.mean(results["recall"]),
        "bertscore_f1": np.mean(results["f1"])
    }