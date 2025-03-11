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
        self.patterns_dir = os.path.join(os.path.dirname(__file__), 'patterns')
        # Create patterns directory if it doesn't exist
        os.makedirs(self.patterns_dir, exist_ok=True)
        # Load pattern descriptions if available
        self.pattern_descriptions = self._load_pattern_descriptions()
        
    def _load_pattern_descriptions(self) -> Dict:
        """Load pattern descriptions from the pattern_descriptions.json file if available"""
        try:
            descriptions_path = os.path.join(os.path.dirname(__file__), 'pattern_descriptions.json')
            if os.path.exists(descriptions_path):
                with open(descriptions_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {"patterns": []}
        except Exception as e:
            logging.warning(f"Failed to load pattern descriptions: {str(e)}")
            return {"patterns": []}
    
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
        for pattern in self.pattern_descriptions.get("patterns", []):
            if pattern.get("patternName") == pattern_name:
                return pattern.get("description", "No description available")
        return "No description available"
    
    def get_pattern_tags(self, pattern_name: str) -> List[str]:
        """Get the tags for a pattern"""
        for pattern in self.pattern_descriptions.get("patterns", []):
            if pattern.get("patternName") == pattern_name:
                return pattern.get("tags", [])
        return []
    
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
            "name": "find_pattern",
            "description": "Find the most appropriate pattern for a specific task or problem",
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
            
            # Filter by category if provided
            if category:
                patterns = [p for p in patterns if any(tag.upper() == category for tag in self.get_pattern_tags(p))]
            
            # Format the results
            result = "Available Patterns:\n\n"
            for pattern in patterns:
                description = self.get_pattern_description(pattern)
                tags = self.get_pattern_tags(pattern)
                result += f"- **{pattern}**: {description}\n"
                if tags:
                    result += f"  Tags: {', '.join(tags)}\n"
            
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
            response, _ = await helper.get_chat_response(chat_id=chat_id, query=formatted_prompt)
            
            # Return the result
            return {"result": f"**Pattern '{pattern_name}' Result:**\n\n{response}"}
        
        elif function_name == "find_pattern":
            task_description = kwargs.get("task_description")
            if not task_description:
                return {"result": "Task description is required"}
            
            # Get all patterns and their descriptions
            patterns = self.get_available_patterns()
            pattern_info = []
            for pattern in patterns:
                description = self.get_pattern_description(pattern)
                tags = self.get_pattern_tags(pattern)
                pattern_info.append({
                    "name": pattern,
                    "description": description,
                    "tags": tags
                })
            
            # Create a prompt to find the best pattern
            prompt = f"""
            I'm looking for the most appropriate pattern to solve this task:
            
            {task_description}
            
            Here are the available patterns and their descriptions:
            
            {json.dumps(pattern_info, indent=2)}
            
            Please suggest the best pattern for this task, explain why it's appropriate, and how to use it.
            """
            
            # Get a response from the OpenAI API
            response, _ = await helper.get_chat_response(chat_id=chat_id, query=prompt)
            
            # Return the suggestion
            return {"result": response}
        
        else:
            return {"result": f"Unknown function: {function_name}"}