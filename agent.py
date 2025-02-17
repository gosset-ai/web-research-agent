from typing import List, Dict
import json
from utils import (
    ask_claude, 
    process_anthropic_response
)

def infer_fields_from_task(task: str) -> List[str]:
    """Infer output fields from the task description using Claude"""
    prompt = f"""Given this task: "{task}"
    What fields should I extract? Return only a JSON array of field names in snake_case format.
    For example: ["company_name", "revenue", "employee_count"]
    Keep the fields simple and focused on the core information requested.
    """
    
    try:
        response_text = ask_claude(prompt)
        if not response_text:
            raise ValueError("No response from Claude")
            
        fields = json.loads(response_text)
        
        # Validate that we got a list of strings
        if not isinstance(fields, list) or not all(isinstance(f, str) for f in fields):
            raise ValueError("Invalid fields format from LLM")
            
        return fields
        
    except Exception as e:
        print(f"Error inferring fields: {e}")
        # Return default fields if something goes wrong
        return ["name", "description"]

def process_single_action(message: str, tools: List[Dict]) -> Dict:
    """Process a single action based on the given message"""
    print("\n=== Processing action ===")    
    
    initial_messages = [{
        "role": "user",
        "content": message
    }]
    
    response = process_anthropic_response(initial_messages, tools)
    
    # Handle different response types
    try:
        if isinstance(response.content, list):
            for content in response.content:
                if content.type == "text":
                    result = json.loads(content.text)
                    print("\n✅ Action processed successfully")
                    return result
        print("\n⚠️ No valid response content found")
        return {}
    except Exception as e:
        print(f"\n❌ Error processing response: {e}")
        return {}

def process_task(task: str, max_searches: int = 5, max_results: int = 10) -> Dict:
    """Process a task and return results in specified format
    
    Args:
        task: The task description
        max_searches: Maximum number of search iterations to perform
        max_results: Maximum number of results to collect
    """
    print("\n=== Starting new task ===")
    print(f"Task: {task}")
    print(f"Limits: max {max_searches} searches, max {max_results} results")
    
    # Infer fields from task
    fields = infer_fields_from_task(task)
    print(f"\n📋 Inferred fields: {', '.join(fields)}")
    
    # Define available tools
    tools = [
        {
            "name": "search_web",
            "description": "Search the web using Google",
            "input_schema": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query string",
                    }
                },
                "required": ["query"],
            }
        },
        {
            "name": "fetch_page",
            "description": "Fetch and parse webpage content. May return None if the page is not accessible.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "URL to fetch",
                    }
                },
                "required": ["url"],
            }
        }
    ]

    TASK_TEMPLATE = f"""Your initial task is:

{task}

{{NEXT_TASK}}

Previous actions taken:
{{ACTION_HISTORY}}

Required fields for each result: {', '.join(fields)}
Maximum results to collect: {max_results}

If your task is to find information online, you can use search_web to search Google and fetch_page to get webpage content.

Return a JSON with:
- results: list of items matching the required fields (limit to {max_results} total results)
- comments: any additional information about the results
- process: description of your approach
- preface: any additional text that you would have added before the json. Include it here, don't include it anywhere else. Output json must be valid.
- next_action: what should be searched or analyzed next (empty string if done)

MAKE SURE THAT YOU OUTPUT A VALID JSON OBJECT. DO NOT INCLUDE ANY OTHER TEXT.
If you cannot find information, return empty lists/strings as appropriate."""

    # Initial task message with empty action history
    initial_task = TASK_TEMPLATE.format(NEXT_TASK="", ACTION_HISTORY="None")
    
    all_results = []
    action_history = []

    # Process actions iteratively until no next_action is provided or limits reached
    current_message = initial_task
    search_count = 0
    
    while True:
        if search_count >= max_searches:
            print(f"\n🛑 Reached maximum number of searches ({max_searches})")
            break
            
        result = process_single_action(current_message, tools)
        search_count += 1
        
        if "results" in result:
            new_results = result.get("results", [])
            remaining_capacity = max_results - len(all_results)
            
            if remaining_capacity <= 0:
                print(f"\n🛑 Reached maximum number of results ({max_results})")
                break
                
            # Add only up to the remaining capacity
            all_results.extend(new_results[:remaining_capacity])
        
        # Check if we should continue
        next_action = result.get("next_action", "")
        if not next_action:
            break
        
        # Add the next_action to history before executing it
        action_history.append(next_action)
        
        # Update message for next iteration with action history
        action_history_text = "\n".join([f"- {action}" for action in action_history])
        current_message = TASK_TEMPLATE.format(
            NEXT_TASK=next_action,
            ACTION_HISTORY=action_history_text
        )

    return {
        "results": all_results,
        "comments": result.get("comments", "") + (
            f"\nSearch limit reached: {search_count >= max_searches}" if search_count >= max_searches else ""
        ),
        "process": result.get("process", ""),
        "preface": result.get("preface", ""),
        "next_action": ""
    }

if __name__ == "__main__":
    # Get task from input
    print("Enter the task instructions:")
    task = input().strip()
    
    # Process task with default limits
    result = process_task(task, max_searches=2, max_results=3)
    
    # Print result as JSON
    print(json.dumps(result, indent=2))
