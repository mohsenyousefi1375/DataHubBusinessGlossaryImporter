from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class BusinessGlossaryModel (BaseModel):
    name: str = Field( min_length=2, description="The official business term name. This should be a clear and concise identifier of the concept or entity.")
    physical_address: str= Field( min_length=2, description="The location or node where the term is stored or organized, often resembling a folder path in the business glossary system.")
    technical_name: str = Field( min_length=2, description= "The SSAS measure name. [SSAS].[instance name].[measure name]")
    description: str = Field( min_length=10, description= "A detailed explanation of the business term that provides clarity on its meaning, context, and usage.")    
    synonyms: Optional[str] = Field(description="Alternative names or terms that are used interchangeably with the primary business term.")
    algorithms_supporting_definitions: Optional[str]   = Field(description="Information about any algorithms, models, or computational processes that utilize or support the term's definition.")  
    created_date: date = Field(  description="The date when the glossary entry was initially created.")
    updated_date: date = Field(  description="The date when the glossary entry was last updated or modified.")
    business_owner_group_name:str= Field( min_length=3, description="the name of the business group in the datahub who define the term and  responsible for the term’s governance and accuracy.")
    business_owner_person_Email:str= Field( min_length=3, description="Contact email of the business owner responsible for the term.")
    technical_owner: str= Field( min_length=3, description="The team responsible for the technical implementation or maintenance related to this term. BITeam")
    domain: str= Field( min_length=3, description="	The business domain or area to which the term belongs (e.g., Finance, Marketing, IT).")
    policies: Optional[str] = Field(  description="Any applicable data policies, compliance requirements, or governance rules relevant to the term.")
    Common_misunderstandings: Optional[str] = Field(  description="	Typical misconceptions or common mistakes related to the term to help clarify and avoid confusion.")
    isDeprecated: bool = Field(  description="	Flag indicating whether the term is deprecated or obsolete and should no longer be used.")
    Contained_by: Optional[str] = Field(  description="Indicates if the term is contained within another term or category, representing hierarchy or grouping.")
    Inherited_by: Optional[str] = Field(  description="	Specifies if the term's definition or attributes are inherited by other terms or subcategories.")
    tags: Optional[str] = Field(  description="	Keywords or tags associated with the term to enhance searchability and classification.")

        
    
    def validate_decription(self):
        pass

    def validate_term_duplication(self):
        pass
    