import sys, os
sys.path.append(os.path.abspath("..")) 
from Model.BusinessGlossaryModel import BusinessGlossaryModel  
import Service.Utils as utils

class DataHubGlossaryImporter:

    def __init__(self, data:BusinessGlossaryModel):
        self.business_term = data
        self.create_business_glossary_nodes()
        self.add_business_glossry()
        self.add_owners_to_business_glossary_term()
        self.add_business_glossary_assets()
        # create tags



    def add_business_glossry(self):
        
        definition = self.generate_business_term_descrition()
        properties = self.generate_business_term_properties()


        business_term_urn = utils.create_business_glossary_term(term_name= self.business_term.name, 
                                                                physical_address= self.
                                                                business_term.physical_address,
                                                                definition= definition,
                                                                customProperties= properties                                                                
                                                                )
        
    
    def create_business_glossary_nodes(self):
        
        root = self.business_term.physical_address
        nodes = root.split('.')
        for i in range(0, len(nodes)):
            if (i == 0):
                utils.create_business_glossary_node(node_name= nodes[i] )
            else :
                utils.create_business_glossary_node(node_name=nodes[i], parent_node_name=nodes[i-1] )


    def generate_business_term_descrition(self):
        return (f'**Description**:\n{self.business_term.description}\n\n\n ' +
                f'**Synonyms**:\n{self.business_term.synonyms}\n\n\n '+
                f'**Algorithm supporting definitions**:\n{self.business_term.algorithms_supporting_definitions}\n\n\n '+
                f'**Common misunderstandings**:\n{self.business_term.Common_misunderstandings}\n\n\n '                               
                )
    
    def generate_business_term_properties(self):

        return {
                        "Is deprecated":str( self.business_term.isDeprecated),
                        "Created date": str(self.business_term.created_date),
                        "Updated date": str(self.business_term.updated_date)                       
                }
    
    def add_owners_to_business_glossary_term(self):

        #create business group in the datahub if it is not exists
        utils.create_datahub_group(display_name=self.business_term.business_owner_group_name,
                                   list_of_members=[self.business_term.business_owner_person_Email]
                                   )
        #create technical group in the datahub if it is not exists
        utils.create_datahub_group(display_name=self.business_term.technical_owner,
                                   list_of_members=["datahub"]
                                   )

        # add technical owner
        utils.add_owner_to_business_glossary(datahub_user_name= None, 
                                             datahub_group_name= self.business_term.technical_owner, 
                                             business_term_name= self.business_term.name,
                                             ownership_type="TECHNICAL_OWNER"
                                             )
        # add business owner
        utils.add_owner_to_business_glossary(datahub_user_name= None, 
                                             datahub_group_name= self.business_term.business_owner_group_name, 
                                             business_term_name= self.business_term.name,
                                             ownership_type="BUSINESS_OWNER"
                                             )

    def add_business_glossary_assets(self):
        technical_dataset= self.business_term.technical_name.split('].[')
        technical_dataset = [item.replace(']', '').replace('[', '')  for item in technical_dataset]
        platform = technical_dataset[0]
        instance = technical_dataset[1]
        dataset_name = technical_dataset[2]
        column_name ="" #technical_dataset[3]


        utils.add_link_to_dataset( 
                                   platform=platform,
                                   instance=instance,
                                   dataset_name= dataset_name,
                                   COLUMN_NAME=column_name,
                                   GLOSSARY_TERM= self.business_term.name                                   
                                  )
 

