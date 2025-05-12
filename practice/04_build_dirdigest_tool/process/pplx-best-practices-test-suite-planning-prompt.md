# Best Practices Prompt for Test Suite Planning

The following prompt template incorporates key strategies for directing an LLM to create comprehensive test suite plans for software tools.

## Context Setting Section

**I need to create a comprehensive test suite for [TOOL NAME]. Here's the relevant information about the tool:**

- **Tool Purpose**: [Describe what the tool does and its primary functions]
- **Key Requirements**: [List the main functional and non-functional requirements]
- **Technical Architecture**: [Provide brief architecture overview]
- **Constraints**: [Mention any performance, security, or implementation constraints]
- **Code Structure**: [Share relevant code snippets or describe the structure]

## Test Suite Requirements

**Generate a detailed test suite plan that includes:**

1. **Test Categories**: Break down tests into logical categories (unit, integration, functional, performance)
2. **Priority Levels**: Assign priorities to different test areas based on criticality
3. **Test Case Structure**: For each test area, provide:
   - Test objectives
   - Input requirements
   - Expected outcomes
   - Edge cases to consider
   - Potential failure scenarios

## Guidance for Reasoning

**As you develop this test plan:**
- First analyze the code/requirements to identify critical components requiring thorough testing
- Consider both happy path and edge cases
- Identify potential integration points between components
- Reason through failure scenarios and how tests could detect them
- Consider performance and security implications where relevant

## Output Specifications

**Structure your test suite plan as follows:**
1. Executive summary of testing strategy (2-3 paragraphs)
2. Categorized test scenarios with specific test cases
3. Testing priorities and rationale
4. Implementation recommendations

## Success Criteria Definition

**The test suite should validate that:**
- [List specific success criteria the test suite should verify]
- [Include measurable outcomes where possible]

## Example Format (Optional)

**Include 2-3 example test cases in this format:**
```
Test ID: [unique identifier]
Description: [brief description]
Preconditions: [setup requirements]
Test Steps: [numbered steps]
Expected Result: [specific outcome]
Edge Cases: [variations to consider]
```