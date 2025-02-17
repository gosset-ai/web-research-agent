import anthropic
from typing import List, Dict
from dotenv import load_dotenv
import os
import json
from tools_selenium import google_search, get_url_content

load_dotenv()
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

def get_anthropic_client():
    """Get or create an Anthropic client instance"""
    return anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

def ask_claude(prompt: str, max_tokens: int = 4096*2, temperature: float = 0) -> str:
    """Send a simple prompt to Claude and return the response"""
    client = get_anthropic_client()
    
    print("\n=== Sending prompt to Claude ===")
    print(f"Prompt: {prompt[:200]}..." if len(prompt) > 200 else f"Prompt: {prompt}")
    
    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-latest",
            max_tokens=max_tokens,
            temperature=temperature,
            system="You are a helpful AI assistant.",
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        response = message.content[0].text
        print(f"Response: {response[:200]}..." if len(response) > 200 else f"Response: {response}")
        return response
    except Exception as e:
        print(f"Error calling Claude: {e}")
        return None

def process_anthropic_response(messages: List[Dict], tools: List[Dict], max_calls: int = 5, max_tokens: int = 4096*2, temperature: float = 0) -> Dict:
    """Recursively process Anthropic responses, handling tool use requests"""
    if max_calls <= 0:
        print("\n⚠️ Max API calls reached. Stopping recursion.")
        return {
            "content": [{
                "type": "text",
                "text": json.dumps({
                    "results": [],
                    "comments": "Max API calls reached. Some results may be incomplete.",
                    "next_action": ""
                })
            }]
        }
    
    print(f"\n=== Sending request to Claude (calls remaining: {max_calls}) ===")
    print("Last message:", messages[-1]['content'][:200], "..." if len(str(messages[-1]['content'])) > 200 else "")
    
    client = get_anthropic_client()
    
    try:
        response = client.messages.create(
            model="claude-3-5-sonnet-latest",
            messages=messages,
            tools=tools,
            max_tokens=max_tokens,
            temperature=temperature,
            system="You are a research assistant helping users find and analyze information from the web."
        )

        # Handle tool use requests
        if response.stop_reason == "tool_use":
            tool_outputs = []
            
            # Process each tool use request
            for content in response.content:
                if content.type == "tool_use":
                    print(f"\n🔧 Using tool: {content.name}")
                    print(f"Tool input: {content.input}")
                    
                    # Execute the tool
                    if content.name == "search_web":
                        results = google_search(content.input["query"])
                        print(f"Search found {len(results)} results")
                        tool_outputs.append({
                            "type": "tool_result",
                            "tool_use_id": content.id,
                            "content": json.dumps(results)
                        })
                    elif content.name == "fetch_page":
                        page_content = get_url_content(content.input["url"])
                        content_preview = page_content[:200] + "..." if page_content and len(page_content) > 200 else page_content
                        print(f"Fetched content: {content_preview}")
                        tool_outputs.append({
                            "type": "tool_result",
                            "tool_use_id": content.id,
                            "content": page_content if page_content else "Failed to fetch page"
                        })

            # Continue conversation with tool results
            if tool_outputs:
                print("\n📤 Sending tool results back to Claude")
                messages.append({
                    "role": "assistant",
                    "content": response.content
                })
                messages.append({
                    "role": "user",
                    "content": tool_outputs
                })
                return process_anthropic_response(messages, tools, max_calls - 1, max_tokens, temperature)

        return response

    except Exception as e:
        print(f"\n❌ Error calling Claude: {e}")
        return {"content": [{"type": "text", "text": f"Error: {str(e)}"}]}