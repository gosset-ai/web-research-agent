# Web Research Agent

A Python-based research assistant that uses Claude 3.5 Sonnet to automatically gather and analyze information from the web.

## Features

- Automatic field inference from task descriptions
- Web search capabilities using Google
- Webpage content extraction and parsing
- Iterative information gathering with configurable limits
- Structured JSON output with results and process documentation

## Prerequisites

- Python 3.x
- Anthropic API key

## Installation

1. Clone the repository:

```bash
git clone https://github.com/gosset-ai/web-research-agent.git
cd web-research-agent
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory and add your Anthropic API key:

```bash
ANTHROPIC_API_KEY=<your_anthropic_api_key>
```

## Usage

You can use the agent either by importing it into your Python code or running it directly from the command line.

### Command Line Usage


```bash
python agent.py
```

When prompted, enter your research task. The agent will:
1. Infer relevant fields from your task
2. Search the web for information
3. Extract and process the content
4. Return structured results

### Python Usage

```python
from agent import process_task

task = "Find information about the top 3 AI companies in 2024"
result = process_task(task, max_searches=2, max_results=3)
print(result)
```

### Configuration Parameters

- `max_searches`: Maximum number of search iterations (default: 5)
- `max_results`: Maximum number of results to collect (default: 10)

## Output Format

The agent returns a JSON object containing:

```json
{
    "results": [],        // List of items matching the required fields
    "comments": "",       // Additional information about the results
    "process": "",        // Description of the approach taken
    "preface": "",        // Any additional context
    "next_action": ""     // Next action to take (empty if complete)
}
```

## Available Tools

The agent includes two main tools:

1. `search_web`: Performs Google searches and returns relevant URLs
2. `fetch_page`: Retrieves and parses webpage content

## Error Handling

- The agent includes robust error handling for API calls and web requests
- Default fields are provided if field inference fails
- Failed webpage fetches are gracefully handled

## License

Apache 2.0


