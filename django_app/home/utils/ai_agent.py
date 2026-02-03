from groq import Groq
import os
from dotenv import load_dotenv
from .prompts import systemPrompt

load_dotenv()

groq_api_key = os.environ.get("GROQ_API_KEY")

def code_analysis_llm(file_content, file_name):
    prompt = f""" 
        Analyze the followning code for:
        - Code style and formatting issues
        - Potential bugs or error
        - Performace imporvements
        - Best Practices

    File Name : {file_name}
    File Content : {file_content}

    Provide a detailed JSON output wit the structure:
    {{
        "issue" : [
            {{
                "type" : "<style | bugs | performance | best_practice>",
                "line" : <line_number>,
                "description" : "<description>",
                "suggestion" : "<suggestion>"
            }}
        ]
    }}
    ```JSON ONLY
    """


    # Invoking the LLM with the prompt
    client = Groq(api_key=groq_api_key)
    completion = client.chat.completions.create(
        model = "llama-3.1-8b-instant",
        messages = [
            {
                "role" : "system",
                "content" : systemPrompt
            },
            {
                "role" : "user",
                "content" : prompt
            }
        ],
        temperature= 0.8,
        top_p =1
    ) 

    print(completion.choices[0].message.content)



# cont = "PCFET0NUWVBFIGh0bWw+CjxodG1sIGxhbmc9ImVuIj4KPGhlYWQ+CiAgICA8\nbWV0YSBjaGFyc2V0PSJVVEYtOCI+CiAgICA8bWV0YSBuYW1lPSJ2aWV3cG9y\ndCIgY29udGVudD0id2lkdGg9ZGV2aWNlLXdpZHRoLCBpbml0aWFsLXNjYWxl\nPTEuMCI+CiAgICA8dGl0bGU+RG9jdW1lbnQ8L3RpdGxlPgo8L2hlYWQ+Cjxi\nb2R5PgogICAgPGgxPlRoaXMgaXMgbWFueWEgcmF3YXQ8L2gxPgo8L2JvZHk+\nCjwvaHRtbD4=\n"


# code_analysis_llm(cont,filen)