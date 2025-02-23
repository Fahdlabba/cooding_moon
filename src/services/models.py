from langchain_core.prompts import ChatPromptTemplate , MessagesPlaceholder
import requests
from langchain_huggingface import HuggingFaceEndpoint,ChatHuggingFace
import typing as t
from src.config.setting import get_settings

setting=get_settings()

try : 
    client_hg = HuggingFaceEndpoint(
            repo_id="microsoft/Phi-3.5-mini-instruct",
            task="text-generation",
            max_new_tokens=512,
            return_full_text=False,
            temperature=0.5,
            huggingfacehub_api_token=setting.HUGGING_FACE_API_TOKEN
        )

    llm=ChatHuggingFace(llm=client_hg,verbose=False)

except Exception as e:
    print(e)


class LLM : 

    def __init__(self,path:t.Optional[str])->None:

        system_prompt=ChatPromptTemplate.from_messages([
            ("system", self.prompt_loader(path)),
            MessagesPlaceholder("chat_history", optional=True),
            ("human", "{user_input}"),
           
        ])
        self.chat_history=[]
        self.chain=system_prompt | llm

    def prompt_loader(self,path="src/prompts/arabic_subject.txt")->str:
        with open(path, "r") as f:
            return f.read()
        
    def generate_answer(self,query)->str:
        try : 
            response=self.chain.invoke({"user_input":query,"chat_history":self.chat_history})
            self.chat_history.append(response)
            return response.content
        except Exception as e:
            return str(e)
        

class TEXT2SPEECH:

    def __init__(self)->None:
       pass
    
    def generate_audio(self,text:str,id:int)->str:
        try : 
            url = "https://api.elevenlabs.io/v1/text-to-speech/JBFqnCBsd6RMkjVDRZzb?output_format=mp3_44100_128" 
            headers = {
                "Content-Type": "application/json",
                "xi-api-key": setting.ELEVEN_LABS
            }
            data = {
                "text": text,
                "model_id": "eleven_multilingual_v2",
            }
            response = requests.post(url, json=data, headers=headers)
            if response.status_code != 200:
                return response.json()
            with open(f"output_{id}.mp3", "wb") as f:
                f.write(response.content)
        except Exception as e:
            return str(e)
        
        
if __name__=="__main__"   :
    model=LLM(path="src/prompts/story_generator.txt")
    print(model.generate_answer("let's start"))
    # tts=TEXT2SPEECH()
    # tts.generate_audio("ما هو الهدف من الحياة",1)