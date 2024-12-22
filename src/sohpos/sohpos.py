import enum
import html
import logging
import xml
import xml.etree
import xml.etree.ElementTree
from time import time_ns
from typing import Self

import httpx
from pydantic import BaseModel, Field, field_serializer, model_validator

from .strings import SohposStrings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SohposError(Exception):
    """Sohpos base exception class"""


class SohposConnectionError(SohposError):
    """Sohpos network error"""


class SohposClientError(SohposError):
    """Sohpos client problem"""


class SohposServerError(SohposError):
    """Sohpos server problem"""


class SohposParseError(SohposClientError):
    """Sohpos unrecognizable XML"""


class SohposMode(enum.IntEnum):
    """Enumeration for Sohpos mode

    These are the different modes that the Sohpos endpoint accepts.
    """

    LOGIN = 191
    LOGOUT = 193


class SohposStatus(enum.StrEnum):
    """Enumeration for Sohpos status

    These are the different statuses that the Sohpos endpoint treats client as.
    """

    # NOTE
    # We don't have a use case for this yet
    LIVE = enum.auto()
    LOGIN = enum.auto()


class SohposProductType(enum.IntEnum):
    """Enumeration for Sohpos product type

    These are the different types of products that the Sohpos accepts.
    There are several like **iOS**, **Android**, etc.
    """

    # NOTE
    # We only need to worry about the web version
    WEB = 0


def time_ms():
    return int(time_ns() / 1_00_000)


class SohposBaseModel(BaseModel):
    """Base model for Sohpos form data"""

    username: str = Field(min_length=1, max_length=32)
    password: str = Field(min_length=1, max_length=32)
    producttype: SohposProductType = Field(default=SohposProductType.WEB)
    a: int = Field(default_factory=time_ms)
    # NOTE
    # This may seem unnecessary, but we can now reuse the model
    # for data validation at different places.
    # Albeit, we need to be careful with the mode.
    mode: SohposMode = Field(default=SohposMode.LOGOUT)

    @field_serializer("username", when_used="always")
    def strip_username(self, username: str):
        return username.strip()

    @field_serializer("password", when_used="always")
    def strip_password(self, password: str):
        return password.strip()

    @model_validator(mode="after")
    def sanitize(self) -> Self:
        if (
            not self.username.isprintable()
            or self.username.isspace()
            or not self.password.isprintable()
            or self.password.isspace()
        ):
            raise ValueError("Please check your username and password")
        else:
            return self


async def sohpos_form_action(model: SohposBaseModel):
    """Sends a POST request to the Sohpos endpoint.

    :param model: The form data to be sent to the Sohpos endpoint encapsulated in a model
    :type model: SohposBaseModel
    :return: The response from the Sohpos endpoint
    :rtype: str
    :raises SohposConnectionError: If there is a network *(theirs)* error
    :raises SohposClientError: If there is a client *(ours)* error
    """
    logger.info(model.model_dump_json())
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url=SohposStrings.SOHPOS_ENDPOINT, data=model.model_dump()
            )
            response.raise_for_status()
    except httpx.RequestError:
        raise SohposConnectionError
    except httpx.HTTPStatusError:
        raise SohposClientError
    else:
        return response.text


def sohpos_parse(data: str, **kwargs) -> str:
    """
    Parses the XML response.

    The XML reponse is parsed using the xml package. Specifically, we find the
    tag **message** and get its **text** attribute.

    :param data: The raw XML response
    :type data: str
    :return: The parsed string in the XML response
    :rtype: str
    :raises SohposParseError: If the XML response is unrecognizable
    """
    # TODO
    # xml has a non-blocking Pull API
    root = xml.etree.ElementTree.fromstring(data)
    logger.info(data)
    logger.info(root.tag)
    logger.info(root.attrib)
    message = root.find("message")
    if message is not None:
        logger.info(message.text)
        if message.text:
            parsed: str = html.unescape(message.text)
        else:
            raise SohposParseError
        return parsed.format(**kwargs) if len(kwargs) else parsed
    else:
        raise SohposParseError
