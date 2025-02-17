# Web Research Agent

A Python-based research assistant that uses Claude 3.5 Sonnet to automatically gather and analyze information from the web.

## Features

- **Dynamic Field Inference**: Automatically determines relevant data fields based on your task description
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

When prompted, enter your research task. For example:
```
Enter the task instructions:
Find the top 3 biotech companies developing treatments for schizophrenia
```

The agent will:
1. Analyze your task to determine relevant fields (e.g., company_name, focus_area, development_stage)
2. Search the web for information
3. Extract and structure the content
4. Return comprehensive results

### Python Usage

```python
from agent import process_task

task = "Find the top 3 biotech companies developing treatments for schizophrenia"
result = process_task(task, max_searches=2, max_results=3)
print(result)
```

Example output:
```json
{
    "results": [
        {
            "company_name": "Karuna Therapeutics",
            "focus_area": "CNS disorders, primarily schizophrenia",
            "development_stage": "Late-stage clinical",
            "key_products": "KarXT (xanomeline-trospium) for schizophrenia",
            "market_cap": "6.5B USD",
            "headquarters": "Boston, Massachusetts"
        },
        // ... additional results
    ],
    "comments": "Analysis of current market leaders...",
}
```

### Configuration Parameters

- `max_searches`: Maximum number of search iterations (default: 5)
- `max_results`: Maximum number of results to collect (default: 10)

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

## About Gosset

[Gosset](https://www.gosset.ai/) provides comprehensive biotech intelligence data powered by AI agents. Key features include:

- **Comprehensive Trial Data**: Access safety and efficacy data from every time point of every trial for every drug
- **Structured Information**: Trial design and eligibility criteria organized for easy filtering
- **Multiple Data Sources**: Results aggregated from research papers, conference posters, investor decks, and press releases
- **Flexible Access**: Data available via dashboard, spreadsheet, or API

### Use Cases

- **Investors**: Comprehensive head-to-head drug comparison data and competitive landscape analyses
- **Corporate Development**: Rich scientific portfolio information and competitive intelligence
- **Biotech Consultants**: Quick analysis of trial design parameters and drug efficacy results

Learn more at [https://www.gosset.ai/](https://www.gosset.ai/)


