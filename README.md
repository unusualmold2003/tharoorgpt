# TharoorGPT

![TharoorGPT Logo](https://github.com/unusualmold2003/tharoorgpt/blob/main/pixel_art.jpeg)

TharoorGPT is a web application that leverages the power of Google's Gemini API to rephrase user input in the distinctive, eloquent, and often verbose style of renowned Indian politician and author, Shashi Tharoor. It's designed to be an engaging and educational tool, offering not just sophisticated responses but also providing definitions for complex vocabulary used. For those seeking brevity, a "Simplify Response" toggle is also available.

## ✨ Features

* **Tharoor-esque Responses:** Transforms ordinary text into highly erudite and eloquent prose, characteristic of Shashi Tharoor's speaking and writing style.
* **Vocabulary Definitions:** Automatically identifies and provides concise definitions for 3-5 complex words used in the generated response.
* **Interactive Learning:** Hover over highlighted words in the response to reveal their definitions, enhancing vocabulary.
* **Simplify Mode:** A toggle to get a straightforward, concise answer if the user prefers simplicity over verbosity.
* **User-Friendly Interface:** A clean, responsive chat interface built with Tailwind CSS and Jinja2 templates.
* **FastAPI Backend:** A robust and efficient Python backend for handling API requests and interacting with the Gemini model.
* **Message Limit:** Implements a session-based message limit (7 messages) to manage API usage.

## 🚀 Technologies Used

* **Backend:**
    * Python 3.9+
    * FastAPI
    * Google Generative AI SDK (`google-generativeai`)
    * `python-dotenv` (for local environment variable management)
* **Frontend:**
    * HTML5
    * CSS (Tailwind CSS)
    * JavaScript
    * Jinja2 (Templating engine)

## ⚙️ Setup and Installation

Follow these steps to get TharoorGPT up and running on your local machine.

### 1. Clone the Repository

```bash
git clone [https://github.com/your-username/TharoorGPT.git](https://github.com/your-username/TharoorGPT.git)
cd TharoorGPT
```

#### 2. Create a Virtual Environment (Recommended)
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```
#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Obtain a Google API Key
Go to the Google AI Studio and obtain your API Key.
Create a .env file in the root directory of your project.
Add your API key to the .env file:
```bash
GOOGLE_API_KEY="YOUR_API_KEY_HERE"
```
#### 5. Create templates and static directories
Ensure you have the following directory structure:
```
TharoorGPT/
├── .env
├── main.py
├── requirements.txt
├── templates/
│   └── index.html
└── static/
    └── pixel_art.jpeg  (This is the pixelated image you want to use)
```
Important: Place the provided index.html content into templates/index.html and place your desired pixelated image as pixel_art.jpeg in the static directory.

#### 6. Run the app!
Visit [TharoorGPT](https://tharoorgpt.vercel.app/) to see it in live action!
