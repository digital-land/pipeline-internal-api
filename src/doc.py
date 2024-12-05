import os

from pydantic import BaseModel


class License(BaseModel):
    name: str
    url: str


class App(BaseModel):
    title: str
    summary: str
    version: str
    contact: str
    license: License


app_info = App(
    title="Pipeline API - Internal",
    summary="""Provides access to the metadata consumed and produced by the data collection pipelines. 
                 These pipelines are responsible for ETL (extract, transform and load) from providers,  
                 including Local Planning Authorities, into the Planning Data Platform 
                 (see https://www.planning.data.gov.uk/).""",
    version=os.environ.get("GIT_COMMIT", "unknown"),
    contact="digitalland@communities.gov.uk",
    license=License(
        name="Open Government Licence v3.0",
        url="https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/",
    ),
)
