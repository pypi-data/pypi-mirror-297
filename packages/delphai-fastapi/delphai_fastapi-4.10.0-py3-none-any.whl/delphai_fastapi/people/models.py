import datetime
from ..models import CamelModel
from typing import Optional

from pydantic import Field


class Transition(CamelModel):
    date: Optional[datetime.date] = Field(
        None,
        description="Date of the transition",
        examples=["2023-12-31"],
    )
    company_url: Optional[str] = Field(
        None,
        description="Webpage of the company where either the preceding or successive job position was held, depending on which is not null",  # noqa: E501
        examples=["intapp.com"],
    )
    person_name: Optional[str] = Field(
        default=None,
        description="Name of the person that transitioned positions",
        examples=["John Doe"],
    )
    preceding_title: Optional[str] = Field(
        default=None,
        description="Preceeding job title the person transitioned to",
        examples=["Software Engineer"],
    )
    successive_title: Optional[str] = Field(
        default=None,
        description="Successive job title the person transitioned out of",
        examples=["Senior Software Engineer"],
    )
    data_provider: Optional[str] = Field(
        default="Intapp",
        description="Indicates whether the transition data was sourced internally by Intapp or from a third-party provider",  # noqa: E501
        examples=["Intapp"],
    )
