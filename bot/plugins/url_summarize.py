import logging
import requests
from typing import Dict
from bs4 import BeautifulSoup
from urllib.parse import urlparse

from .plugin import Plugin


class URLSummarizePlugin(Plugin):
    """
    A plugin to fetch and summarize the content of a webpage
    """
    def get_source_name(self) -> str:
        return "URL Summarizer"

    def get_spec(self) -> [Dict]:
        return [{
            "name": "summarize_webpage",
            "description": "Fetch and summarize the content of a webpage from a given URL",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "The website URL to summarize"}
                },
                "required": ["url"],
            },
        }]

    async def execute(self, function_name, helper, **kwargs) -> Dict:
        try:
            url = kwargs['url']
            
            # Add https:// if not present
            if not urlparse(url).scheme:
                url = f"https://{url}"
            
            # Fetch the webpage content
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()  # Raise exception for 4XX/5XX responses
            
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.extract()
            
            # Get the page title
            title = soup.title.string if soup.title else "No title found"
            
            # Extract text content
            paragraphs = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'article'])
            text_content = '\n'.join([para.get_text().strip() for para in paragraphs])
            
            # Clean the text (remove extra whitespace)
            text_content = ' '.join(text_content.split())
            
            # Truncate if too long (to avoid token limits)
            if len(text_content) > 15000:
                text_content = text_content[:15000] + "..."
            
            # Use the OpenAI GPT model to summarize the content
            prompt = f"Please provide a summary of this webpage content from {url}. Include key points and main ideas only.\n\nContent:\n{text_content}"
            
            summary, tokens = await helper.get_chat_response(chat_id=0, query=prompt)
            
            return {
                "result": {
                    "title": title,
                    "url": url,
                    "summary": summary
                }
            }
            
        except requests.exceptions.RequestException as e:
            logging.warning(f"Error fetching URL {kwargs.get('url', 'unknown')}: {str(e)}")
            return {"result": f"Failed to access the website: {str(e)}"}
        except Exception as e:
            logging.exception(e)
            return {"result": f"Failed to summarize the website: {str(e)}"}