from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class BusinessGlossaryModel (BaseModel):
    name: str = Field( min_length=2, description="Business term name")
    physical_address: str= Field( min_length=2, description="Business term node (folder)")
    technical_name: str = Field( min_length=2)
    description: str = Field( min_length=10)    
    synonyms: Optional[str]
    algorithms_supporting_definitions: Optional[str]     
    created_date: date
    updated_date: date
    business_owner_group_name:str= Field( min_length=3, description="business datahub group name")
    business_owner_person_Email:str= Field( min_length=3, description="business datahub Email")
    technical_owner: str
    domain: str
    policies: Optional[str]
    Common_misunderstandings: Optional[str]
    isDeprecated: bool
    Contained_by: Optional[str]
    Inherited_by: Optional[str]
    tags: Optional[str]

        
    
    def validate_decription(self):
        pass

    def validate_term_duplication(self):
        pass
    