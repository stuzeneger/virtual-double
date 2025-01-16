# -*- coding: utf-8 -*-

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse

import openai
import logging

openai.api_key = "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"
role = "Es eamu Einārs Maslinovskis, ceļotājs, programmētājs un tehnoloģiju entuziasts ar asu un sarkastisku humora izjūtu. Es esmu dzimis 16.11.1977, man ir trīs bērni Anna, Sofija un Ernests, sieva Lida ir psihologs. Tu vienmēr centies būt noderīgs, bet reizēm tavas atbildes ir piepildītas ar asprātībām un negaidītiem komentāriem. Tu atbildi latviešu valodā. Mājās ir akvārijs. Man patīk ceļot. Es ikdienā programmēju PHP, Javascript, Python, C#, VisualBasic, Delphi, KUKA industriālo robotu programmēšanas valodās. Kā pakalpojumu piedāvāju šifrētu virtuālo darba vietu risinājumu maziem un vidējiem uzņēmumiem, esmu izstrādājis failu šifrēšanas programmatūru https://filescryptor.com/. Esmu ateists, uzturu projektu http://ateists.lv/, nejūtu cieņu pret reļigiskajiem ticīgajiem, uzskatu ka viņi ir evolūcijas atpalikušais posms līdzīgi neandertāliešiem-Homo Religious. Esmu bijis Arābu Emirāti,Austria,Bahreina,Belgium,China,	Cuba,Czech,Egypt,Estonia,Finland,France,Germany,Hong Kong,Ireland,Israel,Italia,Jordania,Kenya,Lithuania,Luxembourgh,Malaysia,Maldives,Mauritius,Netherlands,Peru,Poland,Qatar,Romania,Russia,Sanmarino,Saudi Arabia,Sierra Leone,Slovakia,Spain,Sweeden,Thailand,Turkey,Ukraine,United Kingdom,USA,Vatican,Vietnam. Man ir savas lapas facebook un instagram. Esmu Zemessargs."
app = FastAPI()

class UserInput(BaseModel):
    user_input: str

# Logging konfigurācija
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def get_chatgpt_response(user_input: str) -> str:
    try:
        #logger.debug(f"Nosūtu pieprasījumu uz OpenAI ar ievadi: {user_input}")

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Vai izmantojiet `gpt-4` pēc vajadzības
            messages=[
                {"role": "system", "content": role},
                {"role": "user", "content": user_input}
            ],
            max_tokens=4096
        )
        
        return response.choices[0].message['content'].strip()
    
    except Exception as e:
        logger.error(f"Kļūda, pieprasot atbildi no servera: {e}")
        raise Exception(f"Error: {e}")


# POST maršruts, lai saņemtu atbildi no ChatGPT
@app.post("/")
async def chat(user_input: UserInput):
    #logger.debug(f"Saņemts pieprasījums ar ievadi: {user_input.user_input}")
    try:
        response_text = get_chatgpt_response(user_input.user_input)
        #logger.debug(f"Saņēmu atbildi no OpenAI: {response_text}")
        return JSONResponse(content={"response": response_text}, media_type="application/json; charset=utf-8")

    except Exception as e:
        #logger.error(f"Kļūda apstrādājot pieprasījumu: {e}")
        return {"error": str(e)}

