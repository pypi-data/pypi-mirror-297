import requests
from pydantic import BaseModel, Field
from typing import Any, Optional, List, Dict
from datetime import datetime


class FunctionSchema(BaseModel):
    type: str
    function: Dict[str, Any]


class Tool(BaseModel):
    key: str
    name: str
    tags: Optional[List[str]] = None
    code: str
    function_schema: dict
    raw_schema: dict = Field(..., alias="schema")
    created_at: datetime
    updated_at: datetime


class Set(BaseModel):
    key: str
    name: str
    number_of_tools: int
    tools: Optional[List[Tool]] = None
    created_at: datetime
    updated_at: datetime


class APIError(Exception):
    """Base class for API exceptions."""


class ToolNotFoundError(APIError):
    """Raised when a tool is not found."""


class SetNotFoundError(APIError):
    """Raised when a set is not found."""


class APIClient:
    def __init__(self, base_url="http://localhost:2121"):
        self.base_url = base_url
        self.session = requests.Session()

    def fetch_tool_data(self, tool_key: str) -> Tool:
        response = self.session.get(f"{self.base_url}/tools/{tool_key}")
        if response.status_code == 404:
            raise ToolNotFoundError(f"Tool '{tool_key}' not found.")
        response.raise_for_status()
        tool_data = response.json()
        return Tool(**tool_data)

    def fetch_all_tools(
        self, tags: Optional[List[str]] = None, logic_or: bool = True
    ) -> List[Tool]:
        """
        Fetch all tools, optionally filtered by tags with specified logic.

        :param tags: A list of tag keys to filter tools.
        :param logic_or: If True, applies 'OR' logic; if False, applies 'AND' logic. Default is True.
        :return: A list of Tool instances.
        """
        params = {}
        if tags:
            if logic_or:
                params["tags"] = ",".join(tags)  # 'OR' logic using commas
            else:
                params["tags"] = "%2B".join(tags)  # 'AND' logic using plus signs
        response = self.session.get(f"{self.base_url}/tools", params=params)
        response.raise_for_status()
        tools_data = response.json().get("tools", [])
        return [
            Tool(
                function_schema=FunctionSchema(
                    type="function", function=data["schema"]
                ).model_dump(),
                **data,
            )
            for data in tools_data
        ]

    def fetch_set_data(self, set_key: str) -> Set:
        response = self.session.get(f"{self.base_url}/sets/{set_key}")
        if response.status_code == 404:
            raise SetNotFoundError(f"Set '{set_key}' not found.")
        response.raise_for_status()
        set_data = response.json()
        return Set(**set_data)

    def fetch_all_sets(self) -> List[Set]:
        response = self.session.get(f"{self.base_url}/sets")
        response.raise_for_status()
        sets_data = response.json().get("sets", [])
        return [Set(**data) for data in sets_data]

    def fetch_function_schemas(
        self, tags: Optional[List[str]] = None, logic_or: bool = True
    ) -> List[FunctionSchema]:
        """
        Fetch all function schemas, optionally filtered by tags with specified logic.

        :param tags: A list of tag keys to filter schemas.
        :param logic_or: If True, applies 'OR' logic; if False, applies 'AND' logic. Default is True.
        :return: A list of FunctionSchema instances.
        """
        params = {}
        if tags:
            if logic_or:
                params["tags"] = ",".join(tags)  # 'OR' logic using commas
            else:
                params["tags"] = "+".join(tags)  # 'AND' logic using plus signs
        response = self.session.get(f"{self.base_url}/tools/schemas", params=params)
        response.raise_for_status()
        tools_data = response.json()
        return [FunctionSchema(**data) for data in tools_data]


class ToolsManager:
    def __init__(self, api_client: APIClient):
        self.api_client = api_client

    def get(self, tool_key: str) -> Tool:
        try:
            return self.api_client.fetch_tool_data(tool_key)
        except ToolNotFoundError:
            return None

    def list(
        self, tags: Optional[List[str]] = None, logic_or: bool = True
    ) -> List[Tool]:
        """
        List all tools, optionally filtered by tags with specified logic.

        :param tags: A list of tag keys to filter tools.
        :param logic_or: If True, applies 'OR' logic; if False, applies 'AND' logic. Default is True.
        :return: A list of Tool instances.
        """
        return self.api_client.fetch_all_tools(tags=tags, logic_or=logic_or)

    def function_schemas(
        self, tags: Optional[List[str]] = None, logic_or: bool = True
    ) -> List[dict]:
        """
        Fetch all function schemas, optionally filtered by tags with specified logic.

        :param tags: A list of tag keys to filter schemas.
        :param logic_or: If True, applies 'OR' logic; if False, applies 'AND' logic. Default is True.
        :return: A list of dict representations of FunctionSchema.
        """
        return [
            f.model_dump()
            for f in self.api_client.fetch_function_schemas(
                tags=tags, logic_or=logic_or
            )
        ]

    def __getitem__(self, tool_key: str) -> Tool:
        return self.get(tool_key)

    def __iter__(self):
        return iter(self.list())

    def __contains__(self, tool_key: str) -> bool:
        try:
            self.get(tool_key)
            return True
        except ToolNotFoundError:
            return False


class SetsManager:
    def __init__(self, api_client: APIClient):
        self.api_client = api_client

    def get(self, set_key: str) -> Set:
        try:
            return self.api_client.fetch_set_data(set_key)
        except SetNotFoundError:
            return None

    def list(self) -> List[Set]:
        sets_data = self.api_client.fetch_all_sets()
        sets = [self.get(set_obj.key) for set_obj in sets_data]
        return sets

    def __getitem__(self, set_key: str) -> Set:
        return self.get(set_key)

    def __iter__(self):
        return iter(self.list())

    def __contains__(self, set_key: str) -> bool:
        try:
            self.get(set_key)
            return True
        except SetNotFoundError:
            return False


class ToolStore:
    def __init__(self, base_url="http://localhost:2121"):
        self.api_client = APIClient(base_url)
        self.tools = ToolsManager(self.api_client)
        self.sets = SetsManager(self.api_client)
