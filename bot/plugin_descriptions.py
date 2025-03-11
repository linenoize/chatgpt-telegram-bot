# Plugin descriptions for the router to better understand which plugin to use for different queries

PLUGIN_DESCRIPTIONS = {
    "WolframAlpha": {
        "description": "Used for mathematical calculations, scientific data, unit conversions, complex equations, data analysis, and answering factual questions about math, science, geography, etc.",
        "examples": [
            "Calculate the derivative of x^2*sin(x)",
            "What is the capital of France?",
            "Convert 100 miles to kilometers",
            "How far is the moon from Earth?",
            "Solve the equation 3x^2 + 2x - 5 = 0"
        ]
    },
    "Weather": {
        "description": "Provides current weather conditions and forecasts for locations worldwide. Can tell temperature, precipitation, and other weather metrics.",
        "examples": [
            "What's the weather like in Tokyo?",
            "Will it rain tomorrow in New York?",
            "Temperature in Paris this weekend",
            "What's the forecast for London next week?",
            "How hot is it in Dubai right now?"
        ]
    },
    "Crypto": {
        "description": "Retrieves current cryptocurrency rates and information from CoinCap.",
        "examples": [
            "What's the price of Bitcoin?",
            "Show me Ethereum's current rate",
            "Get the value of Dogecoin",
            "What's the crypto price for Solana?",
            "How much is 1 BTC worth right now?"
        ]
    },
    "DuckDuckGo": {
        "description": "Performs web searches using DuckDuckGo search engine. Use this for general information, news, and web lookups.",
        "examples": [
            "Search for best pizza recipes",
            "Find information about climate change",
            "Look up latest news about SpaceX",
            "Search for Python tutorial websites",
            "Find reviews of iPhone 15"
        ]
    },
    "DuckDuckGo Images": {
        "description": "Searches for images and GIFs using DuckDuckGo. Use this when the user wants to see pictures or images of something.",
        "examples": [
            "Show me pictures of the Eiffel Tower",
            "Find images of golden retrievers",
            "Search for GIFs of dancing cats",
            "Show image of Mount Everest",
            "Find pictures of classic cars"
        ]
    },
    "Spotify": {
        "description": "Interacts with Spotify to find music, get user's listening history, look up songs, artists and albums.",
        "examples": [
            "What song am I currently playing on Spotify?",
            "Show my top artists on Spotify",
            "Find Taylor Swift's latest album",
            "What are my most played tracks?",
            "Search for the song 'Bohemian Rhapsody'"
        ]
    },
    "WorldTimeAPI": {
        "description": "Gets the current time in different locations and timezones around the world.",
        "examples": [
            "What time is it in Tokyo?",
            "Current time in New York",
            "What's the time difference between London and Sydney?",
            "Tell me the time in California",
            "Current time in UTC"
        ]
    },
    "YouTube Audio Extractor": {
        "description": "Extracts audio from YouTube videos. Useful when someone wants to listen to just the audio part of a video.",
        "examples": [
            "Extract audio from this YouTube link: https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "Get audio from YouTube video https://youtu.be/abc123",
            "Download the sound from this YouTube video link",
            "Convert this YouTube link to MP3",
            "Extract the audio track from this YouTube URL"
        ]
    },
    "Dice": {
        "description": "Simulates rolling dice or other random chance games. Use when someone wants to play a game or make a random choice.",
        "examples": [
            "Roll a dice",
            "Throw a dice for me",
            "Roll a 6-sided die",
            "I need a random number between 1 and 6",
            "Let's roll a dice to decide"
        ]
    },
    "DeepL Translate": {
        "description": "Translates text between different languages using DeepL's translation service.",
        "examples": [
            "Translate 'Hello, how are you?' to Spanish",
            "What is 'I love you' in French?",
            "Translate this to German: 'The weather is nice today'",
            "How do you say 'Where is the bathroom?' in Italian?",
            "Convert this text to Japanese: 'Thank you for your help'"
        ]
    },
    "gTTS": {
        "description": "Converts text to speech using Google's Text-to-Speech service. Creates audio files from written text.",
        "examples": [
            "Convert this text to speech: 'Welcome to our presentation'",
            "Make an audio file saying 'Hello World'",
            "Read this text aloud: 'The quick brown fox jumps over the lazy dog'",
            "Create voice recording of this message",
            "Turn this sentence into spoken audio"
        ]
    },
    "TTS": {
        "description": "Converts text to speech using OpenAI's Text-to-Speech service. Creates high-quality audio files from written text.",
        "examples": [
            "Use TTS for 'Welcome to our presentation'",
            "Create speech from 'The meeting will begin in 5 minutes'",
            "Generate spoken audio for this announcement",
            "Create a voice recording saying 'Attention all passengers'",
            "Convert this paragraph to spoken words"
        ]
    },
    "Whois": {
        "description": "Looks up domain registration information, showing who owns a website, when it was registered, and when it expires.",
        "examples": [
            "Who owns google.com?",
            "Get whois information for microsoft.com",
            "When was amazon.com registered?",
            "Show domain details for openai.com",
            "Check the registration info for wikipedia.org"
        ]
    },
    "WebShot": {
        "description": "Takes screenshots of websites. Use only when someone specifically wants to see the visual appearance of a website without visiting it.",
        "examples": [
            "Take a screenshot of google.com",
            "Show me what cnn.com looks like",
            "Capture a screenshot of twitter.com",
            "Get a visual of how reddit.com appears",
            "Show me a visual preview of nytimes.com"
        ]
    }, 
    "IP.FM": {
        "description": "Provides geolocation and network information for IP addresses.",
        "examples": [
            "Where is IP address 8.8.8.8 located?",
            "Get information about IP 104.16.132.229",
            "Locate this IP: 172.217.168.174",
            "What country is IP 13.107.42.14 from?",
            "Find the location of IP address 157.240.22.35"
        ]
    },
    "PatternPlugin": {
        "description": "A collection of specialized AI patterns for different tasks like summarizing content, analyzing data, creating visualizations, extracting insights, and more.",
        "examples": [
            "List all available patterns",
            "Find a pattern for summarizing text",
            "Use the 'summarize' pattern on this article",
            "I need a pattern to analyze this data",
            "What pattern would help me extract insights from this text?",
            "Execute the 'extract_wisdom' pattern on this podcast transcript",
            "Create a visualization of these concepts",
            "What's a good pattern for writing an essay?",
            "Help me format this content as a professional email",
            "Generate a creative story from my notes using a pattern"
        ]
    },
    "URL Summarizer": {
        "description": "Fetches and analyzes the content of a webpage, providing a concise summary of the main points and key information.",
        "examples": [
            "Summarize this webpage: https://example.com",
            "Can you give me a summary of what's on nytimes.com/technology",
            "Read and summarize the content from this URL",
            "What are the main points on this website?",
            "Extract the key information from this blog post URL"
        ]
    },
}

# Pattern-specific descriptions
# These will be dynamically added based on the available patterns
PATTERN_DESCRIPTIONS = {
    "list_patterns": {
        "description": "Lists all available AI patterns that can be used for different tasks like summarizing, analyzing, or visualizing information.",
        "examples": [
            "What patterns do you have available?",
            "Show me all AI patterns",
            "List the available patterns for content analysis",
            "What patterns can I use for writing?",
            "Show patterns related to data visualization"
        ]
    },
    "execute_pattern": {
        "description": "Executes a specific AI pattern on the provided input to process information in a specialized way.",
        "examples": [
            "Run the summarize pattern on this article",
            "Use the extract_wisdom pattern for this text",
            "Execute analyze_paper pattern on this research paper",
            "Process this content with the create_visualization pattern",
            "Apply the translate pattern to this paragraph"
        ]
    },
    "find_pattern": {
        "description": "Helps identify the most appropriate AI pattern for a specific task or problem.",
        "examples": [
            "What pattern should I use to summarize a research paper?",
            "Find me a pattern for creating a mindmap",
            "Which pattern is best for extracting key points from a lecture?",
            "What pattern would help me analyze this debate?",
            "Suggest a pattern for improving my academic writing"
        ]
    }
}