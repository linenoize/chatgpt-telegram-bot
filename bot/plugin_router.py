import json
import logging
import re
from typing import Dict, List, Tuple, Optional

from openai_helper import OpenAIHelper
from plugin_manager import PluginManager

# Import the detailed plugin descriptions
try:
    from plugin_descriptions import PLUGIN_DESCRIPTIONS
except ImportError:
    # If the file doesn't exist, use an empty dict
    PLUGIN_DESCRIPTIONS = {}


class PluginRouter:
    """
    A class to route natural language queries to the appropriate plugin
    """

    def __init__(self, openai_helper: OpenAIHelper, plugin_manager: PluginManager):
        self.openai = openai_helper
        self.plugin_manager = plugin_manager
        self.plugin_info = self._generate_plugin_descriptions()
        self.last_function_name = None

    def _generate_plugin_descriptions(self) -> Dict[str, Dict]:
        """
        Generates detailed descriptions of all available plugins and their functions
        """
        descriptions = {}
        
        for function_spec in self.plugin_manager.get_functions_specs():
            function_name = function_spec.get("name")
            plugin = self.plugin_manager.get_plugin_by_function_name(function_name)
            plugin_source = plugin.get_source_name() if plugin else "Unknown"
            
            if plugin_source not in descriptions:
                descriptions[plugin_source] = {
                    "plugin_class": plugin.__class__.__name__ if plugin else "Unknown",
                    "detailed_description": self._get_detailed_description(plugin.__class__.__name__ if plugin else ""),
                    "functions": []
                }
                
            descriptions[plugin_source]["functions"].append({
                "name": function_name,
                "description": function_spec.get("description", ""),
                "parameters": function_spec.get("parameters", {})
            })
            
        return descriptions
    
    def _get_detailed_description(self, plugin_class_name: str) -> Dict:
        """
        Get the detailed description for a plugin from the PLUGIN_DESCRIPTIONS constant
        or get the description from the plugin class docstring as fallback
        """
        # Try to find the plugin in our predefined descriptions
        for key, desc in PLUGIN_DESCRIPTIONS.items():
            if key in plugin_class_name or plugin_class_name in key:
                return desc
        
        # If not found, return a basic description
        return {
            "description": f"Plugin for {plugin_class_name} functionality.",
            "examples": []
        }

    async def determine_plugin_and_params(self, chat_id: int, query: str) -> Tuple[Optional[str], Dict]:
        """
        Uses natural language to determine which plugin to use and what parameters to pass
        
        Returns:
        - function_name: The name of the function to call (or None if no suitable function found)
        - parameters: Parameters to pass to the function
        """
        enhanced_descriptions = {}
        
        # Create an enhanced description object with more context and examples
        for plugin_name, plugin_data in self.plugin_info.items():
            plugin_class = plugin_data.get("plugin_class", "")
            detailed_desc = plugin_data.get("detailed_description", {})
            
            enhanced_descriptions[plugin_name] = {
                "description": detailed_desc.get("description", ""),
                "examples": detailed_desc.get("examples", []),
                "functions": plugin_data["functions"]
            }
        
        plugins_json = json.dumps(enhanced_descriptions, indent=2)
        
        system_prompt = (
            "You are a routing assistant that helps determine which plugin function to call based on a user query. "
            "Your task is to analyze the user's natural language request and match it to the most appropriate plugin function. "
            "\n\n"
            "For each plugin, I've provided a description, example queries, and the functions it offers. "
            "Use this information to determine which plugin and specific function best matches the user's request. "
            "\n\n"
            "Your response must be in JSON format with exactly these fields:\n"
            "- \"function_name\": The name of the function to call\n"
            "- \"parameters\": An object containing the parameter values needed for the function\n"
            "- \"reasoning\": A brief explanation of why you chose this function\n"
            "\n"
            "If you cannot determine an appropriate function, respond with: "
            "{\"function_name\": \"none\", \"parameters\": {}, \"reasoning\": \"explanation why no function matches\"}"
            "\n\n"
            f"Available plugins:\n{plugins_json}"
        )
        
        try:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ]
            
            response = await self.openai.client.chat.completions.create(
                model=self.openai.config['model'],
                messages=messages,
                temperature=0.1,  # Lower temperature for more deterministic results
                max_tokens=800
            )
            
            content = response.choices[0].message.content
            
            # Use regex to extract the JSON part from the response
            json_match = re.search(r'({.*})', content, re.DOTALL)
            if json_match:
                try:
                    result = json.loads(json_match.group(1))
                    function_name = result.get("function_name")
                    parameters = result.get("parameters", {})
                    reasoning = result.get("reasoning", "No reasoning provided")
                    
                    if function_name == "none":
                        logging.info(f"No matching function found. Reasoning: {reasoning}")
                        return None, {}
                    
                    # Verify that the function exists
                    if not any(func["name"] == function_name for plugin in self.plugin_info.values() 
                              for func in plugin["functions"]):
                        logging.warning(f"Function {function_name} does not exist in available plugins")
                        return None, {}
                    
                    # Store the last function name for reference
                    self.last_function_name = function_name
                    
                    logging.info(f"Selected plugin function: {function_name}")
                    logging.info(f"Reasoning: {reasoning}")
                    
                    return function_name, parameters
                    
                except json.JSONDecodeError:
                    logging.warning(f"Invalid JSON in response: {content}")
                    return None, {}
            else:
                logging.warning(f"Couldn't extract JSON from response: {content}")
                return None, {}
                
        except Exception as e:
            logging.exception(f"Error determining plugin: {str(e)}")
            return None, {}

    async def route_and_execute(self, chat_id: int, query: str) -> Dict:
        """
        Routes the query to the appropriate plugin and executes it
        
        Returns the result from the plugin execution
        """
        function_name, parameters = await self.determine_plugin_and_params(chat_id, query)
        
        if not function_name:
            return {"result": "I couldn't determine which tool to use for your request. Could you please be more specific?"}
        
        logging.info(f"Routing query to function {function_name} with parameters {parameters}")
        try:
            result = await self.plugin_manager.call_function(
                function_name, 
                self.openai, 
                json.dumps(parameters)
            )
            return json.loads(result)
        except Exception as e:
            logging.exception(f"Error executing plugin {function_name}: {str(e)}")
            return {"result": f"Error using {function_name}: {str(e)}"}