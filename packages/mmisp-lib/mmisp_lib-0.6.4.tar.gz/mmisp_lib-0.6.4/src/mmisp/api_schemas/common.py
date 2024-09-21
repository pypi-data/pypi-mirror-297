from pydantic import BaseModel


class TagAttributesResponse(BaseModel):
    id: str
    name: str
    colour: str
    exportable: bool
    org_id: str | None = None
    user_id: str | None = None
    hide_tag: bool | None = None
    numerical_value: str | None = None
    is_galaxy: bool | None = None
    is_custom_galaxy: bool | None = None
    local_only: bool | None = None
