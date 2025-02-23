# Taalem API Documentation

This document provides an in-depth explanation of the Taalem API project. It covers project structure, configuration, API endpoints, and detailed explanations of each module.

---

## Table of Contents

1. [Overview](#overview)
2. [Project Structure](#project-structure)
3. [Configuration](#configuration)
4. [Modules Description](#modules-description)
   - [Settings and Environment](#settings-and-environment)
   - [Language Model Services](#language-model-services)
   - [FastAPI Routes](#fastapi-routes)
   - [Main Application](#main-application)
5. [API Endpoints](#api-endpoints)
6. [Running the Application](#running-the-application)
7. [Usage Examples](#usage-examples)
8. [Additional Information](#additional-information)

---

## Overview

Taalem API is a FastAPI-based application that uses a language model service to generate content for Arabic prompts. The application supports:
- Generating imaginative stories for children.
- Producing quizzes in JSON format.
- Handling requests using pre-defined prompts ensuring child-friendly content.

It employs the HuggingFace API for text generation and integrates text-to-speech functionality.

---

## Project Structure
├── .env                         # Environment variables for API tokens
├── readme.md                    # Documentation (currently empty, now supplemented by this file)
├── app.py                       # Main FastAPI application startup file
└── src
    ├── config
    │   └── setting.py           # Settings and environment configuration using Pydantic
    ├── prompts
    │   ├── arabic_subject.txt   # System prompt for Arabic learning interactions
    │   ├── quiz_generator.txt   # Prompt for generating quizzes in Arabic
    │   └── story_generator.txt  # Prompt for generating Arabic stories
    ├── router
    │   └── subject.py           # API routing for endpoints related to generation
    └── services
        └── models.py            # Service layer defining the LLM class, text-to-speech integration, and generation logic


---

## Configuration

### Environment Variables

The application uses `.env` for essential configuration:
- `HUGGING_FACE_API_TOKEN`: The API token required to authenticate with HuggingFace services.

**.env Example:**
    `HUGGING_FACE_API_TOKEN="hf_*********************"`

Additional environment-specific files (e.g., `.env.dev`, `.env.prod`) can be used by setting the `ENVIRONMENT` variable.

### Settings Module

- **File:** `src/config/setting.py`
- **Purpose:** Uses Pydantic's BaseSettings to load environment variables and cache the settings.  
- **Function:** `get_settings()` returns a cached Settings instance, reading from the appropriate `.env` file based on the `ENVIRONMENT` variable.

---

## Modules Description

### Settings and Environment

- **Module:** `src/config/setting.py`
  - Loads the `HUGGING_FACE_API_TOKEN` from the environment.
  - Supports different environments (local, dev, prod) via dynamic `_env_file` parameter.

### Language Model Services

- **Module:** `src/services/models.py`
  - **LLM Class:**  
    - Initializes using a system prompt file.  
    - Loads prompts from a file (e.g., `arabic_subject.txt`, `quiz_generator.txt`, or `story_generator.txt`).
    - Connects the prompt with the language model chain (`llm`) to generate answers.
  - **TEXT2SPEECH Class:**  
    - Integrates with the ElevenLabs API to generate audio from text.
    - Saves audio output as an MP3 file.
  - **Chain Execution:**  
    - The prompt is combined with the conversation history and then passed to the language agent.
    - Generated responses are appended to the conversation history.

### FastAPI Routes

- **Module:** `src/router/subject.py`
  - Contains API endpoints:
    - `/subject`: Generates content based on the Arabic subject prompt.
    - `/Quiz`: Generates quiz content using the `quiz_generator.txt` prompt.
    - `/story_teller`: Generates a story using the `story_generator.txt` prompt.
  - Uses FastAPI's dependency injection and exception handling to provide response feedback.

### Main Application

- **Module:** `app.py`
  - Sets up the main FastAPI app.
  - Configures CORS to allow all origins.
  - Includes the router from `subject.py`.
  - Provides a simple ASCII art response at the root endpoint.
  - Runs the API using Uvicorn on port 8002.

---

## API Endpoints

### Root Endpoint

- **URL:** `/`
- **Method:** `GET`
- **Description:** Returns a simple ASCII art to indicate the API is running.

### Generate Arabic Subject Content

- **URL:** `/subject`
- **Method:** `GET`
- **Parameters:**
  - `data` (str): Input data for generation.
- **Response:**  
  Returns a JSON object such as:
  ```json
  {
    "answer": "Generated content in Arabic..."
  }


Generate Quiz
* URL: /Quiz
* Method: GET
* Parameters:
    * data (str): Input data for generating quiz content.
* Response:
    Returns the generated quiz content as text in JSON format.
Generate Story
* URL: /story_teller
* Method: GET
* Parameters:
    data (str): Input data for story generation.
* Response:
    Returns the generated story content as text.


# Running the Application

##### Prerequisites
* Python 3.7+
* Required libraries (install using pip install -r requirements.txt)
* Uvicorn for running the FastAPI server

##### Running Locally
1. Install dependencies:

    `pip install -r requirements.txt`


2. Ensure that your .env file is configured with the correct API token.
3. Start the server:

    `uvicorn app:app --host 0.0.0.0 --port 8002`

4. Navigate to http://localhost:8002 to see the ASCII art welcome message.


## Usage Examples
#### Testing the /subject Endpoint

Use cURL or your web browser to test:

    `curl "http://localhost:8002/subject?data=مرحبا"`

##### Response:
    {
    "answer": "النص المولد من نموذج اللغة..."
    }


##### Testing the /Quiz Endpoint
    `curl "http://localhost:8002/Quiz?data=ابدأ"`
##### Response (example):
    `{
    "quiz": [
        {
        "question": "ما هو الحرف الأول في كلمة 'بيت'؟",
        "options": { "أ": "ب", "ب": "ت", "ج": "ي" },
        "correct_answer": "أ",
        "feedback": "أحسنت!"
        }
        // more questions...
    ]
    }`

#### Testing the /story_teller Endpoint

    `curl "http://localhost:8002/story_teller?data=ابدأ"`

##### Response:

    {
    "answer": "القصة المولدة..."
    }