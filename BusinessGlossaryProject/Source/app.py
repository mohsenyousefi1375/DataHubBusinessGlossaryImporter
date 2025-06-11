from fastapi import FastAPI, HTTPException, status, Security
from Model.BusinessGlossaryModel import BusinessGlossaryModel
from Service.DataHubGlossaryImporter import DataHubGlossaryImporter
from core.Security import verify_api_key

my_app = FastAPI()

@my_app.post("/")
async def root(data: BusinessGlossaryModel, status_code: int = status.HTTP_201_CREATED, _=Security(verify_api_key)):
    #dataset = BusinessGlossaryModel(**data)
    try:
        importer  = DataHubGlossaryImporter(data)
        return {"message": "The Business Glossary successfullt created"}
    except HTTPException as e:
        raise HTTPException (detail= e.detail , status_code= status.HTTP_400_BAD_REQUEST)

