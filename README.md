# SEO Multi-Agent

An SEO content generation app built with Streamlit and AutoGen. Enter a topic to run a sequence of AI agents that researches the topic, writes a draft, optimizes it for SEO, and reviews it. The app displays and lets you download the final publish-ready article.

## Agent workflow

The workflow is implemented in `workflow.py` as a directed graph:

1. **SEO Research Agent** — researches the topic, search intent, keywords, trends, and potential article angles. It can call the web search tool.
2. **Content Writer Agent** — writes a structured article based on the research.
3. **SEO Optimizer Agent** — audits and improves the draft, including its structure and keyword use.
4. **Content Review Agent** — performs a final editorial review and returns only the publish-ready article.

The agents are AutoGen `AssistantAgent` instances. `DiGraphBuilder` defines the agent sequence and `GraphFlow` executes it. All agents use an `OpenAIChatCompletionClient` configured for `gpt-4.1-mini`. The client is created and closed for each workflow run.

Web search is provided by the project's `web_search` function in `web_tools.py`, which uses DDGS.

## Requirements

- Python
- An OpenAI API key
- Internet access for model calls and web search

## Setup

From the project directory, create and activate a virtual environment, then install the dependencies:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create a `.env` file in the project directory and add your API key:

```text
OPENAI_API_KEY=your-api-key
```

Keep the API key private. Do not commit the `.env` file.

## Run the app

```powershell
streamlit run app.py
```

Enter a topic and select **Generate SEO Content**. The final article appears in the app and can be downloaded as a Markdown file. Use **Refresh** in the sidebar to clear the current result.

## Project files

- `app.py` — Streamlit user interface.
- `agents.py` — agent prompts and AutoGen agent/client construction.
- `workflow.py` — graph construction, execution, and result extraction.
- `web_tools.py` — web search tool used by the research agent.
- `config.py` — loads `OPENAI_API_KEY` from `.env` and configures the model.
- `test_research.py` — standalone sequential run of the four agents.
- `requirements.txt` — project dependencies.
