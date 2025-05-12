# Generate Landlab Overland Flow Model 🤝
Perplexity generates a simple working landlab overflow model in one go with following prompt chain:
```
    what would be the most relevant context documents. urls, etc to solve this task:
    "Generate a Python script that creates a simple overland flow simulation using Landlab's OverlandFlow component."
```
```
    use the context documents above to actually come up with a PLAN for 
    "Generating a Python script that creates a simple overland flow simulation using Landlab's OverlandFlow component."
```

```
    use the PLAN and CONTEXT DOCS to implement the script
```
```
    create a README how to use this script with uv
```
- Here is the entire chain conversation with `perplexity`: https://www.perplexity.ai/search/what-would-be-the-most-relevan-Q0gqNooZQ2agdE6wsyb1Bg that generated:
    - [main.py](./result/pplx-one-shot/landlab-simulation/main.py)
    - [README.md](./result/pplx-one-shot/landlab-simulation/README.md)

- Here is one-shot (with one self correction) solution without any context from `gemini 2.5 pro`: 
    - [overland_flow_simulation.py](./result/gemini-one-shot/overland-flow-simulation/overland_flow_simulation.py)
    - [README.md](./result/gemini-one-shot/overland-flow-simulation/README.md)

**But the purpose of this example task is to learn how to digest different document types: PDF, URL, large Github repository into a Markdown file to be used as context for LLMs.**

We will use `perplexity` for researching relevant context documents and `gemini 2.5 pro` for coding and large context.
Furthermore, we will use following tools:

- go to `https://r.jina.ai/reader/<YOUR_URL>` to convert online resources at `YOUR_URL` into markdown (might not always work due to captchas, or other blockers). For example: 
    - https://r.jina.ai/https://csdms.colorado.edu/csdms_wiki/images/OverlandFlow_Users_Manual.pdf
    - https://r.jina.ai/https://landlab.readthedocs.io/en/v2.9.2/user_guide/overland_flow_user_guide.html

- https://cloud.llamaindex.ai/ to convert pdf into markdown
- https://github.com/cyclotruc/gitingest to digest the landlab repository into markdown (for the sake of showing how to digest a big repository). For example:
    - https://gitingest.com/cyclotruc/gitingest
    - https://gitingest.com/landlab/landlab (this might take a long time due to the size of the landlab repository and also might be not what you want)
- https://gitdiagram.com/ to draw a component diagram of any github repo. For example:
    - https://gitdiagram.com/landlab/landlab

Visit [Recommended Tools](./../../theory/Recommended%20Tools.md)  for a larger list of useful tools.

## 1. **Define Task**
    
    Generate a Python script that creates a simple overland flow simulation using Landlab's OverlandFlow component.
    
    - Follow PEP 8 style guide.
    - Ensure the script is runnable and includes import statements, model setup, time loop, and output.
    - Use clear comments to explain each part of the script.
    

## 2. Find Relevant Context (ask pplx):
```
    What would be the most relevant context documents. urls, etc to solve this task:
    "Generate a Python script that creates a simple overland flow simulation using Landlab's OverlandFlow component."
```
Here is the full answer: [Most Relevant Resources for Creating an Overland Flow Simulation with Landlab](./process/context/pplx-relevant-context-docs-response.md)

After reviewing the list, let's narrow it down to:

- https://csdms.colorado.edu/csdms_wiki/images/OverlandFlow_Users_Manual.pdf
- https://landlab.readthedocs.io/en/v2.9.2/user_guide/overland_flow_user_guide.html
- https://github.com/gantian127/overlandflow_usecase
- https://github.com/landlab/tutorials/blob/next/overland_flow/notebook_demo.ipynb
- https://github.com/landlab/landlab

### 2.1 Download the Context Documents

1. Go to https://r.jina.ai/https://csdms.colorado.edu/csdms_wiki/images/OverlandFlow_Users_Manual.pdf
2. Go to https://r.jina.ai/https://landlab.readthedocs.io/en/v2.9.2/user_guide/overland_flow_user_guide.html
3. Go to https://gitingest.com/gantian127/overlandflow_usecase
4. Download https://github.com/landlab/tutorials/blob/next/overland_flow/notebook_demo.ipynb

### 2.2 Digest the landlab repo

#### 2.2.1 Learn how to use `gitingest` tool
1. Install the [gitingest tool](https://github.com/cyclotruc/gitingest) `pip install gitingest`
2. Learn how to use gitingest: 
    1. Visit https://gitingest.com/cyclotruc/gitingest and download the digest of the gitingest repo or use the already [downloded file](./process/context/tmp/gitingest-digest.md)
    2. Ask `gemini 2.5 pro`: `Give me command examples of how to use the flags of the gitingest tool` and attach the gitingest digest to the prompt.
3. Get comfortable running this tool with various flags. It will save you time in the future.

#### 2.2.2 Use gitingest to digest the landlab repo

1. Clone the landlab repo `git clone https://github.com/landlab/landlab` and inspect it with [`tree` command](https://en.wikipedia.org/wiki/Tree_(command)). If you have troubles installing or using `tree`, [here](./process/context/tmp/landlab-tree-output.md) is the output of the command for the `landlab` repo.
2. Use `gitingest` to create a digest of the landlab repo. Be careful: this repository is large and you need to figure out what files to include and what files to exclude, but since we want *to get lazy with LLMs* we will just ask `gemini 2.5 pro`:
```
Here is the digest of the gitingest repo:
<INSERT GITINGEST DIGEST HERE>

Here is the tree of the landlab repo, i want to use the gitingest tool on:
<INSERT THE OUTPUT OF THE TREE COMMAND IN THE LANDLAB REPO HERE>

Give me a reasonable gitingest command that would include all code and documentation files, 
but would exclude data files, and any other files that wouldn't contribute much to the
understanding of the architecture and functionality of the repository.
```
Here is what `gemini 2.5 pro` came up with:
```
gitingest . \
    -o landlab_core_digest.txt \
    -i "*.py" \
    -i "*.pyx" \
    -i "*.pxd" \
    -i "*.hpp" \
    -i "*.md" \
    -i "*.rst" \
    -i "*.ipynb" \
    -i "MANIFEST.in" \
    -i "pyproject.toml" \
    -i "setup.py" \
    -i "setup.cfg" \
    -i "noxfile.py" \
    -i "Makefile" \
    -i "make.bat" \
    -i "*requirements*.txt" \
    -i "*requirements.in" \
    -i "environment*.yml" \
    -i "CITATION.cff" \
    -i "docs/source/conf.py" \
    -i "docs/source/_templates/*" \
    -i "*.jinja" \
    -e "docs/source/_static/*" \
    -e "docs/source/tutorials/**/data/*" \
    -e "docs/source/tutorials/**/assets/*" \
    -e "docs/source/tutorials/**/*.asc" \
    -e "docs/source/teaching/**/*.asc" \
    -e "docs/source/teaching/**/*.jpg" \
    -e "docs/source/tutorials/**/*.png" \
    -e "docs/source/teaching/**/*.png" \
    -e "docs/source/tutorials/**/*.mp4" \
    -e "src/landlab/data/**/*" \
    -e "generated/*" \
    -e "news/*" \
    -e "joss/*" \
    -e "*digest.md" \
    -e "cython-files.txt" \
    -e "USEDBY.md" \
    -e "CHANGES.md" \
    -e "AUTHORS.md" \
    -e "FUNDING.md"
```
which is **too restrictive for our purposes**. We want to have source code and information about available components too.

ask `gemini 2.5 pro`:
```
    the command is too restrictive and doesn't include the src directory. Verify how to use gitingest and adjust the the command above: include the src directory recursively except for data files(only code and txt, md)
```

This time the generated command is:
```
gitingest . \
    -o landlab_src_focused_digest.txt \
    -e "docs/source/_static/*" \
    -e "docs/source/tutorials/**/data/*" \
    -e "docs/source/tutorials/**/assets/*" \
    -e "docs/source/tutorials/**/*.asc" \
    -e "docs/source/teaching/**/*.asc" \
    -e "docs/source/teaching/**/*.jpg" \
    -e "docs/source/tutorials/**/*.png" \
    -e "docs/source/teaching/**/*.png" \
    -e "docs/source/tutorials/**/*.mp4" \
    -e "src/landlab/data/**/*" \
    -e "generated/*" \
    -e "news/*" \
    -e "joss/*" \
    -e "*digest.md" \
    -e "cython-files.txt" \
    -e "USEDBY.md" \
    -e "CHANGES.md" \
    -e "AUTHORS.md" \
    -e "FUNDING.md" \
    -e "tests/*"
```
which is better. However, there is still when executing this command, **the generated landlab_core_digest.txt is 18MB large! Which is huge.** We need to narrow it down. Asking `gemini 2.5 pro` if we can limit the size of processed files gives us:
```
Gitingest has a `-s` flag which is supposed to limit the processed files by size in bytes.
```

Let's add `-s 102400` to the command and rerun it. It didn't seem to work. The resulting digest file was still 18MB large. 
Ask `gemini 2.5 pro`:`
```
    check the gitingest digest again, because the -s flag doesn't seem to work
```
This, quite interestingly, reveals:
```
    Upon re-examining the gitingest code you provided, specifically src/gitingest/ingestion.py in the _process_file function, I can confirm there is currently no logic implemented to actually use the max_file_size value passed from the CLI or the IngestionQuery object to skip individual files based on their size.
```
Chasing bugs in `gitingest` goes beyond our scope this time, so let's reuse the exclusion list provided above: 

```
    docs/source/tutorials/**/data/*,docs/source/tutorials/**/assets/*,docs/source/tutorials/**/*.asc,docs/source/teaching/**/*.asc,docs/source/teaching/**/*.jpg,docs/source/tutorials/**/*.png,docs/source/teaching/**/*.png,docs/source/tutorials/**/*.mp4,src/landlab/data/**/*,generated/*,news/*,joss/*,*digest.md,cython-files.txt,USEDBY.md,CHANGES.md,AUTHORS.md,FUNDING.md,tests/*,.github/*,scripts/*,.*.*
```
You can copy paste it into https://gitingest.com/landlab/landlab/ and set the `Include files under` slider to `500kb`.
The resulting file is 6.5MB (~2.6M tokens) which is still too large to be ingested by `gemini 2.5 pro`.

After inspecting the sizes of directories in landlab folder, I came to the conclusion to split the repo in 3 parts and generate digests for each part:

1. **docs-digest** (add to exclusion list: `src/*`)
```
    gitingest . \
        -o landlab-docs-digest.txt \
        -e "docs/source/_static/*" \
        -e "docs/source/tutorials/**/data/*" \
        -e "docs/source/tutorials/**/assets/*" \
        -e "docs/source/tutorials/**/*.asc" \
        -e "docs/source/teaching/**/*.asc" \
        -e "docs/source/teaching/**/*.jpg" \
        -e "docs/source/tutorials/**/*.png" \
        -e "docs/source/teaching/**/*.png" \
        -e "docs/source/tutorials/**/*.mp4" \
        -e "src/landlab/data/**/*" \
        -e "docs/source/tutorials/species_evolution/model_grid_steady_state_elevation.txt" \
        -e "docs/source/tutorials/terrain_analysis/flow__distance_utility/nocella_resampled.txt" \
        -e "docs/source/tutorials/grids/global_elevation_etopo_ico_level5.txt" \
        -e "generated/*" \
        -e "news/*" \
        -e "joss/*" \
        -e "*digest*.md" \
        -e ".mailmap" \
        -e "cython-files.txt" \
        -e "USEDBY.md" \
        -e "CHANGES.md" \
        -e "AUTHORS.md" \
        -e "FUNDING.md" \
        -e "tests/*" \
        -e ".github/*" \
        -e "scripts/*" \
        -e ".*.*" \
        -e "src/*"
```
2. **src-without-components-digest** (add `docs/*,src/landlab/components/*` to exclusion list)
```
    gitingest . \
        -o landlab-src-without-components-digest.txt \
        -e "src/landlab/data/**/*" \
        -e "generated/*" \
        -e "news/*" \
        -e "joss/*" \
        -e "*digest.md" \
        -e ".mailmap" \
        -e "cython-files.txt" \
        -e "USEDBY.md" \
        -e "CHANGES.md" \
        -e "AUTHORS.md" \
        -e "FUNDING.md" \
        -e "tests/*" \
        -e ".github/*" \
        -e "scripts/*" \
        -e ".*.*" \
        -e "docs/*" \
        -e "src/landlab/components/*"
```
3. **components-digest** (only ingest the src/landlab/components/* files). Execute inside `src/landlab/components/`:
```
    gitingest . -o components-digest.txt
```

Here are the 3 digests:
- [landlab-docs-digest](./process/context/landlab-digests/landlab-docs-digest.txt) (size: 1752KB ~ 531,966 tokens)
- [landlab-src-without-components-digest](./process/context/landlab-digests/landlab-src-without-components-digest.txt) (size: 1824KB ~ 578,261 tokens)
- [landlab-components-digest](./process/context/landlab-digests/landlab-components-digest.txt) (size: 2164KB ~ 659,931 tokens)

These digests will individually fit into the context window of `gemini 2.5 pro`, but not together. So, let's compact them.

#### 2.2.3. Compact huge digests

Let's create the Digest Compaction Prompt. Ask `gemini 2.5 pro`:
```
Improve the following prompt: 

The summary should actually be a technical document that provides clear guidance (with code examples!) on how to use Landlab framework to create modesl and simulations using ALL of it's features and components.

```I have split the Landlab repository into three parts for summarization:

1. **landlab-docs-digest**
   Includes only the `docs/` folder from the Landlab repository.
   (Exclude everything under `src/*`)

2. **landlab-src-without-components-digest**
   Includes the `src/` folder, **excluding** `src/landlab/components/*`.
   (Exclude: `docs/*`, `src/landlab/components/*`)

3. **landlab-components-digest**
   Includes only `src/landlab/components/*`.
   (Exclude everything else)

---

**Your task**:
Generate a high-quality, structured summary of the contents in `<PART>`. This summary will help a coding LLM understand and use Landlab and its components to create scientific simulations.

**Guidelines**:

* Use best practices for summarizing large repositories:

  * Capture key functionality, modules, and their purposes.
  * Identify core abstractions, data flow, and dependencies.
  * Highlight important files, classes, and functions with brief explanations.
  * Note usage patterns, if evident.
  * 
* Write clearly and concisely for an audience of scientists and developers.
* Do not include unnecessary implementation details or exhaustive lists.

Please generate the summary for: **<PART>**
Here is the digest:

<PART-DIGEST>

```
Here are 2 versions of the improved Digest Compaction Prompt:
- [Digest Compaction Prompt v1](./process/context/landlab-techdocs-for-llms/digest-compaction-prompt-v1.md)
- [Digest Compaction Prompt v2](./process/context/landlab-techdocs-for-llms/digest-compaction-prompt-v2.md)

We'll use [Digest Compaction Prompt v1](./process/context/landlab-techdocs-for-llms/digest-compaction-prompt-v1.md) to ask `gemini 2.5 pro` to generate Technical Docs for all 3 parts:

- [landlab-docs-digest-techdoc](./process/context/landlab-techdocs-for-llms/landlab-docs-digest-techdoc.md)
- [landlab-components-digest-techdoc](./process/context/landlab-techdocs-for-llms/landlab-components-digest-techdoc.md)
- [landlab-docs-digest-techdoc](./process/context/landlab-techdocs-for-llms/landlab-docs-digest-techdoc.md)


Now, let's just merge the 3 Technical Docs into 1.

**Finally, we have can use the [Complete Landlab Technical Document for LLMs](./process/context/landlab-techdocs-for-llms/landlab-techdoc-for-llms.md) as context for our needs!**


## 3. Given the Context, Solve the Task in One Shot

Prepare the context docs:

1. Convert jupyter notebooks to python:
    - `jupyter nbconvert --to python overland_flow.ipynb`
    - `jupyter nbconvert --to python notebook_demo.ipynb`
2. Copy paste them into the Meta Prompt below.
3. Attach the following files:
    - [Overland Flow Component User Manual.md](./process/context/relevant-context/Overland%20Flow%20Component%20User%20Manual.md)
    - [The Landlab OverlandFlow Component Users Manual.md](./process/context/relevant-context/The%20Landlab%20OverlandFlow%20Component%20Users%20Manual.md)

```
    Generate a Python script that creates a simple overland flow simulation using Landlab's OverlandFlow component.
    Create a detailed README how to use this script with uv.
    CONTEXT: <INSERT ALL CONTEXT DOCS HERE>
```

## Result
[Overland Flow Simulation](./result/gemini-one-shot-with-context/landlab-overland-flow-demo/README.md)
