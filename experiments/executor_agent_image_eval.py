"""
Example: Executor agent that uses OpenAIAgent as base and evaluates generated images using image similarity metrics
and LLM-as-a-judge structured comparison.

This script demonstrates how to:
- Extend OpenAIAgent to create an ExecutorAgent
- Directly compute similarity metrics (SSIM, PSNR, RMSE, SAM, SRE, UIQ)
- Call an LLM (via OpenAIAgent) to produce a structured comparison JSON and save it
"""

import os
import json
import base64
from moya.agents.openai_agent import OpenAIAgent, OpenAIAgentConfig
import cv2
from image_similarity_measures.quality_metrics import (
    ssim, psnr, rmse, sam, sre, uiq
)

class ExecutorAgent(OpenAIAgent):
    def __init__(self, config):
        super().__init__(config)

    def evaluate_images(self, ground_truth_path, generated_path):
        """
        Compare two images using built-in metrics (no tools).
        """
        imgA = cv2.imread(ground_truth_path)
        imgB = cv2.imread(generated_path)
        if imgA is None or imgB is None:
            return {"error": "Could not load one or both images."}
        imgB_resized = cv2.resize(imgB, (imgA.shape[1], imgA.shape[0]))
        metrics = {
            "SSIM": float(ssim(imgA, imgB_resized)),
            "PSNR": float(psnr(imgA, imgB_resized)),
            "RMSE": float(rmse(imgA, imgB_resized)),
            "SAM": float(sam(imgA, imgB_resized)),
            "SRE": float(sre(imgA, imgB_resized)),
            "UIQ": float(uiq(imgA, imgB_resized)),
        }
        return metrics

    def load_image_as_base64(self, image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode("utf-8")

    def llm_compare_and_save(self, ground_truth_path: str, generated_path: str, output_dir: str = "LLM_as_a_Judge_openai_outputs") -> str:
        os.makedirs(output_dir, exist_ok=True)
        stem = os.path.splitext(os.path.basename(ground_truth_path))[0]
        out_path = os.path.join(output_dir, f"{stem}_comparison.json")

        # Build messages exactly like evaluation/LLM as a judge/evaluation_gpt.py
        system_prompt = "You are a software architecture expert."
        base64_img1 = self.load_image_as_base64(ground_truth_path)
        base64_img2 = self.load_image_as_base64(generated_path)

        prompt = '''
You are analyzing two software architecture diagrams. Extract **all** possible information from BOTH diagrams into structured JSON and COMPARE them.

**Step 1: Extract**
For each diagram, extract:
- Components (with names, descriptions, boundaries, and positions)
- Connectors (with source/target, label, type, etc.)
- Annotations
- Logical groups/layers
- Metadata (filename, title if found)

**Step 2: Compare**
- Identify similar/same components by name or purpose.
- Identify same/similar connectors.
- Highlight differences (components or connections present in one but not the other).
- Analyze the architectural structure, organization (e.g., layers or services), and any observable design patterns.

**Step 3: Explain**
- Provide a natural-language explanation summarizing the similarities and differences between the two diagrams.
- Include points about structure, shared elements, and key distinctions in architecture.

Return a JSON object in this exact structure:
```json
{
 "GroundTruth": {
 "components": [],
 "connectors": [],
 "annotations": [],
 "groups": [],
 "metadata": {}
 },
 "GeneratedImage": {
 "components": [],
 "connectors": [],
 "annotations": [],
 "groups": [],
 "metadata": {}
 },
 "comparison": {
 "common_components": [],
 "unique_to_GroundTruth": [],
 "unique_to_GeneratedImage": [],
 "common_connectors": [],
 "unique_connectors_GroundTruth": [],
 "unique_connectors_GeneratedImage": [],
 "explanation": "A detailed explanation highlighting similarities and differences between the two diagrams and also please rate the generated image on a scale of 1 to 10 based on its accuracy and completeness, similarity compared to the ground truth and explain the reasoning behind the rating.",
 "Rating": 0
 }
}
Only return valid JSON.
'''

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_img1}"}},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_img2}"}},
            ]}
        ]

        # Route through OpenAIAgent to perform the LLM call
        try:
            msg = self.get_response(messages)
            text = msg.get("content", "") if isinstance(msg, dict) else ""
            if not text:
                text = "{}"
        except Exception as e:
            text = f"{{\"error\": \"OpenAI API error: {str(e)}\"}}"

        # Parse JSON; if fails, try to extract a JSON snippet
        data = None
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            import re
            match = re.search(r'\{[\s\S]*\}', text)
            if match:
                snippet = match.group(0)
                try:
                    data = json.loads(snippet)
                except json.JSONDecodeError:
                    pass

        if data is None:
            # Save raw output for debugging
            with open("gpt4o_raw_responses.log", "a", encoding="utf-8") as f:
                f.write(f"--- {os.path.basename(ground_truth_path)} & {os.path.basename(generated_path)} ---\n{text}\n\n")
            return None

        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return out_path

def main():
    # Setup agent config
    config = OpenAIAgentConfig(
        agent_name="executor_agent",
        description="Agent that evaluates generated images using similarity metrics.",
        api_key=os.getenv("OPENAI_API_KEY"),
        model_name="gpt-4o",
        agent_type="ExecutorAgent",
        is_streaming=False,
        system_prompt="You are an agent that evaluates generated images by comparing them to ground truth images using similarity metrics."
    )

    agent = ExecutorAgent(config)

    # Example usage: replace with your actual image paths
    ground_truth_path = input("Enter path to ground truth image: ").strip()
    generated_path = input("Enter path to generated image: ").strip()

    metrics = agent.evaluate_images(ground_truth_path, generated_path)
    print("\nImage Similarity Metrics:")
    if "error" in metrics:
        print(metrics["error"])
    else:
        for k, v in metrics.items():
            print(f"{k}: {v}")

    # LLM-as-a-judge JSON report
    json_path = agent.llm_compare_and_save(ground_truth_path, generated_path)
    if json_path:
        print(f"\nSaved LLM-as-a-judge report to: {json_path}")
    else:
        print("\nLLM-as-a-judge comparison failed; see gpt4o_raw_responses.log for details.")

if __name__ == "__main__":
    main()
