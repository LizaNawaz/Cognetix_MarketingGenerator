from typing import List

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator
)


class MarketingVariation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    headline: str = Field(
        min_length=1,
        max_length=180
    )

    content: str = Field(
        min_length=1,
        max_length=6000
    )

    hashtags: List[str] = Field(
        default_factory=list,
        max_length=10
    )

    @field_validator("headline", "content")
    @classmethod
    def validate_text(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("Text fields cannot be blank.")

        return value

    @field_validator("hashtags")
    @classmethod
    def validate_hashtags(cls, values):
        cleaned = []

        for value in values:
            value = value.strip()

            if not value:
                continue

            if not value.startswith("#"):
                value = "#" + value

            cleaned.append(value)

        return cleaned


class MarketingResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    variations: List[MarketingVariation] = Field(
        min_length=1,
        max_length=5
    )