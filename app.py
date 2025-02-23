from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse 
from src.router import subject
from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn
import os
import ast
load_dotenv()



app = FastAPI(
    title="Taalem API",
    summary="Taalem API",
)



app.include_router(subject.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

art_ascii = rf"""

 / _ \|  \/  |   /\\ \   / /  __ \     /\    
 | (_) | \  / |  /  \\ \_/ /| |__) |   /  \   
  \__, | |\/| | / /\ \\   / |  _  /   / /\ \  
    / /| |  | |/ ____ \| |  | | \ \  / ____ \ 
   /_/ |_|  |_/_/    \_\_|  |_|  \_\/_/    \_\
                                                                                                                 
"""


@app.get("/",response_class=PlainTextResponse)
async def root():
    return art_ascii



if __name__ == "__main__":
    try : 
        uvicorn.run(
            app,
            port=8002,
            host="0.0.0.0"

        )
    except KeyboardInterrupt as ki : 
        print("Shutting down the app")
    except Exception as e : 
        print(f"Error occured in app : {e}")
        
    