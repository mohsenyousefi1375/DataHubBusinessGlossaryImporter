from fastapi import FastAPI, APIRouter, status 
from Model.BusinessGlossaryModel import BusinessGlossaryModel
from Service.DataHubGlossaryImporter import DataHubGlossaryImporter


my_app = FastAPI()

@my_app.post("/")
async def root(data: BusinessGlossaryModel, status_code: int = status.HTTP_201_CREATED):
    #dataset = BusinessGlossaryModel(**data)
    importer  = DataHubGlossaryImporter(data)

