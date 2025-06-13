import os
import google.generativeai as genai
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables from .env file for local development
load_dotenv()

# Configure the Gemini API key
try:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment variables.")
    genai.configure(api_key=api_key)
except Exception as e:
    # This will help in debugging configuration issues
    print(f"Error configuring GenerativeAI: {e}")

# Initialize FastAPI app
app = FastAPI()

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Pydantic model for incoming chat requests
class ChatRequest(BaseModel):
    message: str
    simplify: bool = False

# --- Gemini Model Configuration ---
# Create the generative model instance
generation_config = {
    "temperature": 0.7,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    safety_settings=safety_settings
)

# --- API Routes ---

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """
    Serves the main HTML page.
    """
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/chat", response_class=JSONResponse)
async def chat_handler(chat_request: ChatRequest):
    """
    Handles the chat logic by calling the Gemini API.
    """
    try:
        user_message = chat_request.message
        simplify_mode = chat_request.simplify

        if simplify_mode:
            # If simplify mode is on, the prompt is straightforward
            prompt = f"Please provide a simple, clear, and concise answer to the following user message: '{user_message}'"
        else:
            # The main prompt engineering for the Tharoor style
            prompt = f"""
            You are TharoorGPT. Your persona is that of Shashi Tharoor, known for his erudition and eloquent, verbose English.
            Your task is to rephrase the user's input in this distinct style.

            Follow these instructions precisely:
            1.  Analyze the user's message: '{user_message}'.
            2.  Craft a response that is eloquent, sophisticated, and uses a rich vocabulary, as Shashi Tharoor would.
            3.  From your response, identify 3-5 of the most complex or esoteric words.
            4.  Your FINAL output MUST BE a valid JSON object. Do not add any text before or after the JSON object.
            5.  The JSON object must have two keys:
                - "tharoor_response": A string containing your full, eloquent reply.
                - "vocabulary": An array of JSON objects. Each object in this array must have two keys: "word" (the complex word from your response) and "definition" (its clear and concise meaning).

            Example user message: "Let's make things better."
            Example JSON output:
            {{
                "tharoor_response": "Indeed, let us endeavor to ameliorate the prevailing circumstances, fostering a veritable renaissance of progress and shared prosperity.",
                "vocabulary": [
                    {{"word": "endeavor", "definition": "To try hard to do or achieve something."}},
                    {{"word": "ameliorate", "definition": "To make something bad or unsatisfactory better."}},
                    {{"word": "veritable", "definition": "Used as an intensifier, often to qualify a metaphor."}},
                    {{"word": "renaissance", "definition": "A revival of or renewed interest in something."}}
                ]
            }}

            Now, process the user's message.
            """

        # Call the Gemini API
        convo = model.start_chat(history=[])
        convo.send_message(prompt)
        
        # The response from Gemini should be a stringified JSON
        response_text = convo.last.text
        
        # If in simplify mode, we need to format it into the standard JSON structure ourselves
        if simplify_mode:
            return JSONResponse(content={
                "tharoor_response": response_text,
                "vocabulary": []
            })
        else:
            # Parse the JSON string from the model's response
            # A simple .replace() can fix common model errors like newlines inside the string
            import json
            cleaned_response = response_text.strip().replace('\n', '')
            # Find the start and end of the JSON object
            start_index = cleaned_response.find('{')
            end_index = cleaned_response.rfind('}') + 1
            json_string = cleaned_response[start_index:end_index]
            
            response_json = json.loads(json_string)
            return JSONResponse(content=response_json)

    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Alas, a most regrettable digital malady has occurred. Please attempt your query anon.")