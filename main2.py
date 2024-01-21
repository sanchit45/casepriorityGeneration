from fastapi import FastAPI, HTTPException
import os
from pydantic import BaseModel
from langchain.llms import GooglePalm
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


app = FastAPI()

API_KEY= "AIzaSyA6fYVkYWamANNjKIMwrdEJ9w0fqsmGU98"
os.environ['GOOGLE_API_KEY'] = API_KEY

llm = GooglePalm(temperature = 0.3)


class Casedata(BaseModel):
    case : str

@app.post("/prioritize-cases")
async def prioritize_cases(cases: Casedata):

    title_template = PromptTemplate(
        input_variables=['cases'],
        template="You are a top-tier legal professional who can decide priority of a court case by seeing number of judges involved, number of lawyers involved, age of case, impact on public safety and societal impact. You will rank the cases by analyzing their description and return list of caseID in priority order: {cases}"
    )

    title_chain = LLMChain(llm = llm, prompt = title_template, verbose = True, output_key = 'output')

    response = title_chain({'cases' : cases.case})

    return response["output"]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.2", port=8000)


