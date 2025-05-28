import logging
import time
from datahub.emitter.mcp import MetadataChangeProposalWrapper
from datahub.emitter.rest_emitter import DatahubRestEmitter
from core.config import gms_server
from datahub.metadata.urns import CorpUserUrn
from datahub.emitter.mce_builder import make_user_urn, make_group_urn,make_dataset_urn,make_dataset_urn_with_platform_instance
from datahub.ingestion.graph.client import DatahubClientConfig, DataHubGraph, DataHubGraphConfig
from typing import Optional

from datahub.metadata.schema_classes import (
    GlossaryNodeInfoClass,
    GlossaryTermInfoClass,
    GlossaryTermAssociationClass,
    GlossaryTermsClass,
    MetadataChangeProposalClass,
    OwnershipClass,
    OwnerClass,
    OwnershipTypeClass,
    )

from datahub.api.entities.corpgroup.corpgroup import (
    CorpGroup,
    CorpGroupGenerationConfig,
)

 
from datahub.metadata.com.linkedin.pegasus2avro.common import AuditStamp


def create_business_glossary_node(node_name:str, parent_node_name:str = None, node_definition:str = "" ):
    # Setup logging and emitter
    log = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)
    rest_emitter = DatahubRestEmitter(gms_server=gms_server)

    
    
    if parent_node_name !=None:
        #node_urn = f"urn:li:glossaryNode:{parent_node_name}.{node_name}"
        #parent_node_urn = f"urn:li:glossaryNode:{parent_node_name}"
        node_urn = generate_business_glossary_node_urn(f"{parent_node_name}.{node_name}")
        parent_node_urn = generate_business_glossary_node_urn(parent_node_name)


    else:
        parent_node_urn = None
        #node_urn = f"urn:li:glossaryNode:{node_name}"
        node_urn = generate_business_glossary_node_urn(node_name)


    node_info = GlossaryNodeInfoClass(
        name=node_name,
        parentNode=parent_node_urn,
        definition= node_definition
    )

    node_mcp = MetadataChangeProposalWrapper(
        entityUrn=node_urn,
        aspect=node_info,
    )
    rest_emitter.emit(node_mcp)
    log.info(f"Created node: {node_urn}")
    

def generate_business_glossary_node_urn( name : str):
    return f"urn:li:glossaryNode:{name}"

def generate_business_glossary_term_urn( name : str):
    return f"urn:li:glossaryTerm:{name}"




def create_business_glossary_term(term_name:str, physical_address:str, definition:str, customProperties:dict ):
    
    # Setup logging and emitter
    log = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)
    rest_emitter = DatahubRestEmitter(gms_server=gms_server)

    term_urn = generate_business_glossary_term_urn(term_name)
    node_urn = generate_business_glossary_node_urn(physical_address)

    term_info = GlossaryTermInfoClass(
        definition=definition,
        name=term_name,
        termSource="manual",
        parentNode=node_urn,
        customProperties= customProperties
    )

    term_mcp = MetadataChangeProposalWrapper(
        entityUrn=term_urn,
        aspect=term_info,
    )
    rest_emitter.emit(term_mcp)
    log.info(f"Created term: {term_urn}")
    return term_urn

    
def create_datahub_group( display_name:str ,list_of_members:list = [],group_email:str = None, description:str = None, slack = None ):
   
    log = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)

    members=[]

    for i in list_of_members:
        members.append(str(CorpUserUrn(i)))

    group = CorpGroup(
        id = display_name,
        owners = [str(CorpUserUrn("datahub"))],
        members = members,
        display_name=display_name,
        email=group_email,
        description = description,
        slack=slack,
    )
    # Create graph client
    datahub_graph = DataHubGraph(DataHubGraphConfig(server=gms_server))

    for event in group.generate_mcp(
        generation_config=CorpGroupGenerationConfig(
            override_editable=False, datahub_graph=datahub_graph
        )
    ):
        datahub_graph.emit(event)
    log.info(f"Upserted group {group.urn}")



def add_owner_to_business_glossary(datahub_user_name:str, datahub_group_name:str, business_term_name:str, ownership_type):
    log = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)


    # Inputs -> owner, ownership_type, dataset
    if datahub_user_name:
        owner_to_add = make_user_urn(datahub_user_name)

    elif datahub_group_name:
        owner_to_add = make_group_urn (datahub_group_name)


    ownership_type =ownership_type #OwnershipTypeClass.TECHNICAL_OWNER


    # Some objects to help with conditional pathways later
    owner_class_to_add = OwnerClass(owner=owner_to_add, type=ownership_type)
    ownership_to_add = OwnershipClass(owners=[owner_class_to_add])


    graph = DataHubGraph(DatahubClientConfig(server=gms_server))

    glossary_urn = generate_business_glossary_term_urn(business_term_name)


    current_owners: Optional[OwnershipClass] = graph.get_aspect(
        entity_urn=glossary_urn, aspect_type=OwnershipClass
    )


    need_write = False
    if current_owners:
        if (owner_to_add, ownership_type) not in [
            (x.owner, x.type) for x in current_owners.owners
        ]:
            # owners exist, but this owner is not present in the current owners
            current_owners.owners.append(owner_class_to_add)
            need_write = True
    else:
        # create a brand new ownership aspect
        current_owners = ownership_to_add
        need_write = True

    if need_write:
        event: MetadataChangeProposalWrapper = MetadataChangeProposalWrapper(
            entityUrn=glossary_urn,
            aspect=current_owners,
            entityType="glossaryTerm"
        )
        graph.emit(event)
        log.info(
            f"Owner {owner_to_add}, type {ownership_type} added to dataset {glossary_urn}"
        )

    else:
        log.info(f"Owner {owner_to_add} already exists, omitting write")   


def add_link_to_dataset (dataset_name:str,platform:str ,COLUMN_NAME:str ,GLOSSARY_TERM:str, instance:str):
    ENV = "PROD"
    ACTOR_URN = "urn:li:corpuser:datahub"
    platform_instance = str.replace(str.replace(str.replace(str.replace(str.replace( instance, ',', '-'), ':', '-'), '(', ''), ')', ''), '.', '_')

    dataset_urn = dataset_urn = make_dataset_urn_with_platform_instance(platform=platform, name=str.lower(dataset_name), env=ENV, platform_instance= platform_instance)
    glossary_term_urn = f"urn:li:glossaryTerm:{GLOSSARY_TERM}"

    now_millis = int(time.time() * 1000)
    audit_stamp = AuditStamp(time=now_millis, actor=ACTOR_URN)

    glossary_terms_aspect = GlossaryTermsClass(
        auditStamp=audit_stamp,
        terms=[
            GlossaryTermAssociationClass(
                urn=glossary_term_urn,
                actor=ACTOR_URN,
                context= f'"fieldPath": "{COLUMN_NAME}"'
                
                ,  # use SchemaFieldKey
                attribution=None,
            )
        ],
    )

    mcp = MetadataChangeProposalWrapper(
        entityUrn=dataset_urn,
        aspect=glossary_terms_aspect,
        aspectName="glossaryTerms",
    )

    emitter = DatahubRestEmitter(gms_server=gms_server)
    emitter.emit(mcp)

    print(f" Linked column '{COLUMN_NAME}' in dataset '{dataset_name}' to glossary term '{GLOSSARY_TERM}'")