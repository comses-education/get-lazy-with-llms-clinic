I have split the Landlab repository into three parts, and for each part, I've created a digest containing relevant file contents. Your goal is to process one of these digests and generate a section of a comprehensive technical document. This document will serve as a practical guide for scientists and developers (and ultimately, a coding LLM) on how to use the Landlab framework to create models and simulations, leveraging ALL of its features and components covered in the provided digest.

The three parts are:

1.  **landlab-docs-digest**
    *   Focus: Primarily user-facing documentation, tutorials, examples, and conceptual explanations.
    *   Digest includes: Only the `docs/` folder from the Landlab repository. (Excludes `src/*`)

2.  **landlab-src-without-components-digest**
    *   Focus: The core Landlab framework, grid functionalities, utilities, I/O, and base classes (excluding process components).
    *   Digest includes: The `src/` folder, **excluding** `src/landlab/components/*`. (Excludes: `docs/*`, `src/landlab/components/*`)

3.  **landlab-components-digest**
    *   Focus: The individual process components available in Landlab.
    *   Digest includes: Only `src/landlab/components/*`. (Excludes everything else)

---

**Your Task**:
Based on the provided `<PART-DIGEST>`, generate a detailed and actionable section for a technical document. This section must provide clear guidance, **including practical code examples**, on how to use the Landlab features and components found within this specific part of the repository.

**Guidelines for the Technical Document Section**:

*   **Instructional Focus**: Your output should *teach* the user how to use Landlab elements. Don't just list what's there; explain *how to use it*.
*   **Target Audience**: Scientists and developers who want to build Landlab models. Assume they have Python proficiency but may be new to Landlab. The output should also be structured clearly for a coding LLM to understand and use for code generation.
*   **Structure and Clarity**:
    *   Use Markdown for formatting (headings, subheadings, code blocks, lists).
    *   Organize content logically, likely mirroring the structure of the Landlab modules/sub-packages within the digest.
    *   Start with a brief overview of what this section (based on the digest part) covers.
*   **Content Requirements**:
    *   **Key Modules/Classes/Functions**: For each significant element:
        *   Clearly state its **purpose** and primary use case.
        *   Explain its **key parameters** (for instantiation or function calls) and common **attributes/methods**.
        *   Provide **minimal, illustrative Python code examples** demonstrating its typical instantiation and usage. Examples should be self-contained where possible or clearly state dependencies.
        *   Highlight **common usage patterns** and best practices.
    *   **Core Abstractions & Concepts**: If the digest reveals core Landlab abstractions (e.g., grids, fields, component API), explain these concepts and show how to work with them using code.
    *   **Data Flow and Interactions**: Where relevant, explain how different parts (within this digest) interact, and how data (e.g., model grid fields) is typically passed or accessed.
    *   **Setup and Initialization**: If applicable, explain any necessary setup or initialization steps for using the features in this part.
    *   **Connecting to Other Parts (Conceptual)**: While focusing on the current digest, briefly mention if and how elements within this part typically connect to or are used by elements from other conceptual parts of Landlab (e.g., how core grid functionalities are used by components).
*   **Code Examples**:
    *   Must be **functional** (or clearly marked as conceptual snippets).
    *   Should be **concise** and focus on the specific feature being explained.
    *   Use clear variable names and include necessary imports (e.g., `from landlab import RasterModelGrid`).
    *   Add comments within the code to explain crucial steps.
*   **Avoid**:
    *   Exhaustive lists of every single private method or internal detail. Focus on the public API and user-facing functionality.
    *   Simply re-stating comments from the source code. Synthesize and explain.
    *   Overly complex examples. Start simple.

---

**Context for the LLM**: You are essentially writing a chapter or a major section of "The Landlab User Manual & Developer Guide". The final combined document (from all three parts) should comprehensively cover how to use *all* of Landlab. Ensure your contribution for this part is detailed, accurate, and highly practical.

Please generate the technical document section for: **<PART>**
Here is the digest:

<PART-DIGEST>