from enum import Enum, IntEnum
from pydantic import BaseModel

class Credentials(BaseModel):
    account_id : int
    workspace : str | None = ""
    md_api_key : str | None = ""
    extra_tags : str | None = ""

def CreateCredentials(account_id, workspace, md_api_key, extra_tags):

    json_input = {}
    json_input["account_id"] = account_id
    json_input["workspace"] = workspace
    json_input["md_api_key"] = md_api_key
    json_input["extra_tags"] = extra_tags

    return json_input

