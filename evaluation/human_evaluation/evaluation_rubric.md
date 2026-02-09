# Architecture Diagram Evaluation Rubric

## Objective
Evaluate the quality of the generated architecture diagram by comparing it with the ground truth diagram.

## Instructions
1. Compare the **Ground Truth** image with the **Generated** image.
2. Evaluate the generated diagram according to the criteria below.
3. For each criterion, select one rating:
   - **Meets Expectations**: No significant issues.
   - **Partially Meets Expectations**: Minor issues or small improvements needed.
   - **Does Not Meet Expectations**: Major issues or incorrect/missing elements.
4. Provide a brief justification for each rating, focusing on specific observations from the diagrams.

## Evaluation Criteria

### 1. Clarity
The generated diagram should be understandable to both technical and non-technical stakeholders.
- **Visual Elements**: Assess whether the symbols, icons, labels, and information are clear and unambiguous.
- **Naming**: Ensure each component and connector has a clear and descriptive name that reflects its purpose or function.
- **Layout**: Verify that components are arranged in a logical and readable layout.

### 2. Consistency
Check whether symbols, icons, styles, notations, connectors, and components are used uniformly throughout the diagram.
- **Alignment**: Assess whether the generated diagram is structurally and semantically aligned with the ground truth diagram.

### 3. Completeness
Evaluate whether the diagram includes all the necessary information from the ground truth.
- **Elements & Connections**: Identify any missing, extra, or incorrect elements (components) or connections (relationships).

### 4. Accuracy
Check how accurately the diagram reflects the system architecture as shown in the ground truth.
- **Discrepancies**: Identify specific discrepancies in components or connectors between the two diagrams.
- **Correctness**: Ensure the relationships and flow matches the ground truth.

### 5. Level of Detail
Evaluate whether the level of detail is appropriate as specified in the metadata and matches the ground truth.
- **Granularity**: Determine if the diagram is appropriately detailed or too vague for the intended audience.
- **Concerns Alignment**: Check if the concerns observed in the generated view match the metadata information.
