from fastapi.routing import APIRouter
from src.services.models import LLM , TEXT2SPEECH
from fastapi import HTTPException




router=APIRouter()



@router.get("/subject")
def get_subject(data:str)->str:
    try : 
        model=LLM()
        return {"answer":model.generate_answer(data)}
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    
@router.get("/Quiz")
def get_quiz(data:str)->str:
    try : 
        model=LLM(path="src/prompts/quiz_generator.txt")
        return model.generate_answer(data)
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))


@router.get("/story_teller")
def get_story(data:str)->str:
    try : 
        model=LLM(path="src/prompts/story_generator.txt")
        return model.generate_answer(data)
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    

    