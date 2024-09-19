import os.path
from datetime import datetime, timezone
from typing import Dict, List
from urllib.error import HTTPError

import requests
import tenacity
from google.auth.exceptions import RefreshError
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from loguru import logger
from pydantic import BaseModel, Field

from plurally.models.misc import Table
from plurally.models.node import Node


class Google(Node):
    SCOPES: List[str] = None
    SERVICE: str = None

    class InitSchema(Node.InitSchema): ...

    class InputSchema(Node.InputSchema): ...

    def __init__(self, init_inputs: InitSchema, outputs=None):
        assert self.SCOPES is not None, "SCOPES must be defined in the subclass"
        assert self.SERVICE is not None, "SERVICE must be defined in the subclass"

        self._token = None
        self._token_expiry = None
        self._service = None
        super().__init__(init_inputs, outputs)

    def token(self):
        now = datetime.now(tz=timezone.utc).replace(tzinfo=None)
        if self._token is None or self._token_expiry < now:
            self.reset()
            self._token, self._token_expiry = self._get_access_token()
        return self._token

    def _get_access_token(self):
        token_url = os.environ.get("PLURALLY_TOKEN_URL")
        assert token_url, "PLURALLY_TOKEN_URL must be set in the environment"

        api_key = os.environ.get("PLURALLY_API_KEY")
        assert api_key, "PLURALLY_API_KEY must be set in the environment"

        headers = {
            "Authorization": f"Bearer {api_key}",
        }
        res = requests.get(
            token_url, headers=headers, params={"scopes": " ".join(self.SCOPES)}
        )
        res.raise_for_status()

        data = res.json()
        token_expiry = datetime.fromisoformat(data["expires_at"])
        return data["access_token"], token_expiry

    @property
    def service(self):
        if self._service is None:
            creds = Credentials(token=self.token())
            self._service = build(self.SERVICE, "v4", credentials=creds)
        return self._service

    def reset(self):
        self._token = None
        self._token_expiry = None
        self._service = None

    @tenacity.retry(
        stop=tenacity.stop_after_attempt(2),
        retry=tenacity.retry_if_exception_type(RefreshError),
    )
    def forward(self, input_schema: InputSchema):
        try:
            self._forward(input_schema)
        except RefreshError:
            # resetting will request a new token
            self.reset()
            raise


class SheetsRead(Google):
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
    SERVICE = "sheets"

    class InitSchema(Google.InitSchema):
        """Read data from a Google Sheet."""

        sheet_id: str = Field(
            title="Sheet ID",
            description="The ID of the Google Sheet.",
            examples=["1CM29gwKIzeXsAppeNwrc8lbYaVcmUclprLuLYuHog4k"],
        )
        range_name: str = Field(
            title="Range Name",
            description="The range of the sheet to read.",
            examples=["Sheet1!A1:B2"],
        )

    class InputSchema(Node.InputSchema): ...

    class OutputSchema(BaseModel):
        values: Table = Field(
            title="Values",
            description="The values in the spreadsheet.",
        )

    DESC = InitSchema.__doc__

    def __init__(self, init_inputs: InitSchema, outputs=None):
        self.sheet_id = init_inputs.sheet_id
        self.range_name = init_inputs.range_name
        super().__init__(init_inputs, outputs)

    def _read_values(self):
        sheet = self.service.spreadsheets()
        try:
            result = (
                sheet.values()
                .get(spreadsheetId=self.sheet_id, range=self.range_name)
                .execute()
            )
        except HTTPError as e:
            if e.response.status_code == 403:
                raise ValueError("You do not have permission to read this sheet")
            elif e.response.status_code == 404:
                raise ValueError(str(e))
            raise
        return result.get("values", [])

    def _forward(self, _: InputSchema):
        values = self._read_values()
        # turn into list of dicts
        if values:
            values = [dict(zip(values[0], row)) for row in values[1:]]

        self.outputs = {"values": Table(data=values)}

    def serialize(self):
        return super().serialize() | {
            "sheet_id": self.sheet_id,
            "range_name": self.range_name,
        }


class SheetsWrite(Google):
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
    SERVICE = "sheets"

    class InitSchema(Google.InitSchema):
        """Read data from a Google Sheet."""

        sheet_id: str = Field(
            title="Sheet ID",
            description="The ID of the Google Sheet.",
            examples=["1CM29gwKIzeXsAppeNwrc8lbYaVcmUclprLuLYuHog4k"],
        )
        append: bool = Field(
            True,
            title="Append",
            description="Whether to append to the sheet or overwrite.",
        )
        range_name: str = Field(
            title="Range Name",
            description="The range of the sheet to write.",
            examples=["Sheet1!A1:B2"],
        )

    class InputSchema(Node.InputSchema):
        values: Table

    class OutputSchema(BaseModel): ...

    DESC = InitSchema.__doc__

    def __init__(self, init_inputs: InitSchema, outputs=None):
        self.sheet_id = init_inputs.sheet_id
        self.append = init_inputs.append
        self.range_name = init_inputs.range_name
        self.value_input_option = "RAW"

        super().__init__(init_inputs, outputs)

    def _write_values(self, data: List[Dict[str, str]]):
        if not data:
            logger.debug("No data to write")
            return

        sheet = self.service.spreadsheets()
        headers = list(data[0].keys())

        # Get the first row of the sheet to check if headers are present
        result = (
            sheet.values()
            .get(
                spreadsheetId=self.sheet_id,
                range=self.range_name,
                majorDimension="ROWS",
            )
            .execute()
        )
        current_values = result.get("values", [])

        rows = [
            list(data[0].keys()),
            *[[row[col] for col in data[0].keys()] for row in data],
        ]
        if current_values and current_values[0] == headers:
            logger.debug("Headers already present, skipping header row")
            body = {"values": rows[1:]}
        else:
            logger.debug("Headers not present, writing headers and data")
            body = {"values": rows}

        try:
            if self.append:
                sheet.values().append(
                    spreadsheetId=self.sheet_id,
                    range=self.range_name,
                    valueInputOption=self.value_input_option,
                    body=body,
                ).execute()
            else:
                sheet.values().update(
                    spreadsheetId=self.sheet_id,
                    range=self.range_name,
                    valueInputOption=self.value_input_option,
                    body=body,
                ).execute()
        except HTTPError as e:
            if e.response.status_code == 403:
                raise ValueError("You do not have permission to write to this sheet")
            raise

    def _forward(self, node_input: InputSchema):
        self._write_values(node_input.values.data)

    def serialize(self):
        return super().serialize() | {
            "sheet_id": self.sheet_id,
            "range_name": self.range_name,
            "append": self.append,
        }
