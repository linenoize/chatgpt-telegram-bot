# Improved PatternPlugin that reads pattern_explanations.md

import os
import logging
import json
from typing import Dict, List

from .plugin import Plugin


class PatternPlugin(Plugin):
    """
    A plugin to execute Fabric patterns stored in the bot/patterns directory.
    """
    def __init__(self):
        self.patterns_dir = os.path.join(os.path.dirname(__file__), '..', 'patterns')
        # Create patterns directory if it doesn't exist
        os.makedirs(self.patterns_dir, exist_ok=True)
        # Load pattern explanations file
        self.pattern_explanations = self._load_pattern_explanations()
        
    def _load_pattern_explanations(self) -> Dict:
        """
        Load pattern explanations from pattern_explanations.md
        """
        try:
            explanations_path = os.path.join(self.patterns_dir, 'pattern_explanations.md')
            if os.path.exists(explanations_path):
                with open(explanations_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Parse the content
                pattern_dict = {}
                
                # Skip the first few lines (header)
                lines = content.strip().split('\n')
                
                # Find the key pattern line and store it specially
                key_pattern_line = next((line for line in lines if "Key pattern to use" in line), None)
                if key_pattern_line:
                    pattern_dict["key_pattern"] = key_pattern_line.strip()
                
                # Parse the numbered pattern descriptions
                current_pattern = None
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                        
                    # Match lines like "1. **pattern_name**: Description text"
                    import re
                    pattern_match = re.match(r'^\d+\.\s+\*\*([^*]+)\*\*:\s+(.+)$', line)
                    if pattern_match:
                        pattern_name = pattern_match.group(1)
                        description = pattern_match.group(2)
                        pattern_dict[pattern_name] = {
                            "description": description
                        }
                
                return pattern_dict
            else:
                logging.warning(f"Pattern explanations file not found at {explanations_path}")
                return {}
        except Exception as e:
            logging.warning(f"Failed to load pattern explanations: {str(e)}")
            return {}
    
    def get_available_patterns(self) -> List[str]:
        """Get a list of available pattern names"""
        try:
            return [d for d in os.listdir(self.patterns_dir) 
                   if os.path.isdir(os.path.join(self.patterns_dir, d)) 
                   and os.path.exists(os.path.join(self.patterns_dir, d, 'system.md'))]
        except Exception as e:
            logging.error(f"Failed to list patterns: {str(e)}")
            return []
    
    def get_pattern_description(self, pattern_name: str) -> str:
        """Get the description for a pattern"""
        if pattern_name in self.pattern_explanations:
            return self.pattern_explanations[pattern_name].get("description", "No description available")
        return "No description available"
    
    def get_pattern_content(self, pattern_name: str) -> str:
        """Read the content of a pattern's system.md file"""
        try:
            pattern_path = os.path.join(self.patterns_dir, pattern_name, 'system.md')
            if os.path.exists(pattern_path):
                with open(pattern_path, 'r', encoding='utf-8') as f:
                    return f.read()
            return f"Pattern {pattern_name} not found"
        except Exception as e:
            logging.error(f"Failed to read pattern {pattern_name}: {str(e)}")
            return f"Error loading pattern {pattern_name}: {str(e)}"
    
    def get_source_name(self) -> str:
        return "PatternPlugin"

    def get_spec(self) -> [Dict]:
        """
        Define the function specs for the pattern plugin.
        """
        patterns = self.get_available_patterns()
        
        specs = [{
            "name": "list_patterns",
            "description": "List all available patterns that can be used to solve various problems",
            "parameters": {
                "type": "object",
                "properties": {
                    "category": {"type": "string", "description": "Optional category to filter patterns by (e.g., ANALYSIS, WRITING, DEVELOPMENT)"}
                }
            }
        }]
        
        # Add a function for executing any pattern
        specs.append({
            "name": "execute_pattern",
            "description": "Execute a specific pattern by name to solve a problem or format information",
            "parameters": {
                "type": "object",
                "properties": {
                    "pattern_name": {
                        "type": "string", 
                        "description": "The name of the pattern to execute", 
                        "enum": patterns
                    },
                    "input_text": {"type": "string", "description": "The text input to process with the pattern"}
                },
                "required": ["pattern_name", "input_text"]
            }
        })
        
        # Add a function for finding the right pattern
        specs.append({
            "name": "suggest_pattern",
            "description": "Suggests appropriate fabric patterns or commands based on user input, providing clear explanations and options for users.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_description": {"type": "string", "description": "Description of the task or problem to solve"}
                },
                "required": ["task_description"]
            }
        })
        
        return specs

    async def execute(self, function_name, helper, **kwargs) -> Dict:
        """
        Execute the requested function
        """
        if function_name == "list_patterns":
            category = kwargs.get("category", "").upper()
            patterns = self.get_available_patterns()
            
            # Format the results
            result = "Available Patterns:\n\n"
            for pattern in patterns:
                description = self.get_pattern_description(pattern)
                result += f"- **{pattern}**: {description}\n"
            
            return {"result": result}
        
        elif function_name == "execute_pattern":
            pattern_name = kwargs.get("pattern_name")
            input_text = kwargs.get("input_text")
            
            if not pattern_name or not input_text:
                return {"result": "Both pattern_name and input_text are required"}
            
            # Get the pattern content
            pattern_content = self.get_pattern_content(pattern_name)
            if pattern_content.startswith("Pattern") or pattern_content.startswith("Error"):
                return {"result": pattern_content}
            
            # Format the content to be used as a prompt
            formatted_prompt = f"{pattern_content}\n\n# INPUT:\n\nINPUT: {input_text}"
            
            # Get a response from the OpenAI API
            response, _ = await helper.get_chat_response(chat_id=kwargs.get('chat_id', 0), query=formatted_prompt)
            
            # Return the result
            return {"result": f"**Pattern '{pattern_name}' Result:**\n\n{response}"}
        
        elif function_name == "suggest_pattern":
            task_description = kwargs.get("task_description")
            if not task_description:
                return {"result": "Task description is required"}
            
            # Get all patterns and their descriptions
            patterns = self.get_available_patterns()
            pattern_info = []
            for pattern in patterns:
                description = self.get_pattern_description(pattern)
                pattern_info.append({
                    "name": pattern,
                    "description": description
                })
            
            # Add the key pattern message from the explanations file
            key_pattern_msg = ""
            if "key_pattern" in self.pattern_explanations:
                key_pattern_msg = f"\n\n{self.pattern_explanations['key_pattern']}"
            
            # Create a prompt to find the best pattern
            prompt = f"""
            I'm looking for the most appropriate pattern to solve this task:
            
            {task_description}
            
            Here are the available patterns and their descriptions:
            
            {json.dumps(pattern_info, indent=2)}
            {key_pattern_msg}
            
            Please suggest the best pattern for this task, explain why it's appropriate, and ask for my confirmation before proceeding. Also explain what the pattern does so I can understand its purpose.
            """
            
            # Get a response from the OpenAI API
            response, _ = await helper.get_chat_response(chat_id=kwargs.get('chat_id', 0), query=prompt)
            
            # Return the suggestion
            return {"result": response}
        
        else:
            return {"result": f"Unknown function: {function_name}"}