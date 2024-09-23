"""
ToolMate AI Plugin - ask chatgpt

Ask ChatGPT for conversation only; no function calling

[FUNCTION_CALL]
"""


from toolmate import config
from toolmate.chatgpt import ChatGPT

def ask_chatgpt(function_args):
    config.stopSpinning()
    query = function_args.get("query") # required
    config.currentMessages = config.currentMessages[:-1]
    ChatGPT().run(query, once=True)
    return ""

functionSignature = {
    "examples": [
        "Ask ChatGPT",
    ],
    "name": "ask_chatgpt",
    "description": "Ask ChatGPT to chat or provide information",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The original request in detail, including any supplementary information",
            },
        },
        "required": ["query"],
    },
}

config.addFunctionCall(signature=functionSignature, method=ask_chatgpt)
config.inputSuggestions.append("Ask ChatGPT: ")