"""
Content Automation module — Google Sheets integration and Nano Banana webhooks.

Enables:
  - Batch prompt generation from a Google Sheet content calendar
  - Exporting generated prompts back to Google Sheets
  - Nano Banana webhook triggers for automated content pipelines
  - Content batch scheduling
"""
from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Optional

import httpx


# ─────────────────────────────────────────────────────────────────────────────
# Google Sheets integration
# ─────────────────────────────────────────────────────────────────────────────

class GoogleSheetsClient:
    """
    Lightweight Google Sheets client using the Sheets API v4.
    Requires a service account JSON key with Sheets access, or OAuth credentials.
    """

    SHEETS_BASE = "https://sheets.googleapis.com/v4/spreadsheets"

    def __init__(self, credentials_path: Optional[str] = None):
        self.credentials_path = (
            credentials_path
            or os.environ.get("GOOGLE_CREDENTIALS_PATH")
            or os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        )
        self._token: Optional[str] = None
        self._token_expiry: Optional[datetime] = None

    def _get_token(self) -> str:
        """Get a valid OAuth2 access token from service account credentials."""
        if self._token and self._token_expiry and datetime.utcnow() < self._token_expiry:
            return self._token

        if not self.credentials_path or not os.path.exists(self.credentials_path):
            raise ValueError(
                "Google credentials not found. Set GOOGLE_CREDENTIALS_PATH env var "
                "pointing to your service account JSON key file."
            )

        # Use google-auth to get a token
        try:
            from google.oauth2 import service_account
            import google.auth.transport.requests

            scopes = ["https://www.googleapis.com/auth/spreadsheets"]
            creds = service_account.Credentials.from_service_account_file(
                self.credentials_path, scopes=scopes
            )
            request = google.auth.transport.requests.Request()
            creds.refresh(request)
            self._token = creds.token
            self._token_expiry = creds.expiry
            return self._token
        except ImportError:
            raise ImportError(
                "google-auth package required. Run: pip install google-auth google-auth-oauthlib"
            )

    def _headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self._get_token()}",
            "Content-Type": "application/json",
        }

    def read_range(self, spreadsheet_id: str, range_notation: str) -> list[list]:
        """
        Read a range from a Google Sheet.

        Parameters
        ----------
        spreadsheet_id : str
            The spreadsheet ID (from the URL: /d/{SPREADSHEET_ID}/edit)
        range_notation : str
            A1 notation e.g. "Sheet1!A1:G100"

        Returns
        -------
        list[list] — rows of cell values
        """
        url = f"{self.SHEETS_BASE}/{spreadsheet_id}/values/{range_notation}"
        with httpx.Client() as client:
            resp = client.get(url, headers=self._headers())
            resp.raise_for_status()
            data = resp.json()
            return data.get("values", [])

    def write_range(
        self,
        spreadsheet_id: str,
        range_notation: str,
        values: list[list],
        value_input_option: str = "USER_ENTERED",
    ) -> dict:
        """
        Write values to a Google Sheet range.

        Parameters
        ----------
        spreadsheet_id : str
        range_notation : str
            e.g. "Sheet1!A1"
        values : list[list]
            Rows of cell values
        value_input_option : str
            'USER_ENTERED' or 'RAW'

        Returns
        -------
        dict — API response
        """
        url = (
            f"{self.SHEETS_BASE}/{spreadsheet_id}/values/{range_notation}"
            f"?valueInputOption={value_input_option}"
        )
        body = {"range": range_notation, "majorDimension": "ROWS", "values": values}
        with httpx.Client() as client:
            resp = client.put(url, headers=self._headers(), json=body)
            resp.raise_for_status()
            return resp.json()

    def append_rows(
        self,
        spreadsheet_id: str,
        range_notation: str,
        values: list[list],
    ) -> dict:
        """Append rows to the end of a sheet."""
        url = (
            f"{self.SHEETS_BASE}/{spreadsheet_id}/values/{range_notation}:append"
            f"?valueInputOption=USER_ENTERED&insertDataOption=INSERT_ROWS"
        )
        body = {"range": range_notation, "majorDimension": "ROWS", "values": values}
        with httpx.Client() as client:
            resp = client.post(url, headers=self._headers(), json=body)
            resp.raise_for_status()
            return resp.json()


# ─────────────────────────────────────────────────────────────────────────────
# Content calendar schema
# ─────────────────────────────────────────────────────────────────────────────

CONTENT_CALENDAR_HEADERS = [
    "Date",
    "Status",
    "Brief",
    "Shot Type",
    "Target Platform",
    "Social Format",
    "Generated Prompt (Positive)",
    "Generated Prompt (Negative)",
    "MidJourney Command",
    "Runway Prompt",
    "Pika Prompt",
    "Creative Notes",
    "Performance Score",
    "Notes",
]


def create_content_calendar_template() -> list[list]:
    """Return the header row for a new content calendar sheet."""
    return [CONTENT_CALENDAR_HEADERS]


def parse_brief_rows(rows: list[list]) -> list[dict]:
    """
    Parse rows from a Google Sheet into a list of brief dicts.
    Expects the sheet to have CONTENT_CALENDAR_HEADERS as the first row.

    Returns rows where Status is 'TODO' or empty.
    """
    if not rows or len(rows) < 2:
        return []

    headers = rows[0]
    briefs = []
    for row in rows[1:]:
        # Pad row to header length
        padded = row + [""] * (len(headers) - len(row))
        record = dict(zip(headers, padded))

        status = record.get("Status", "").strip().upper()
        if status in ("TODO", "QUEUE", ""):
            brief = record.get("Brief", "").strip()
            if brief:
                briefs.append({
                    "brief": brief,
                    "date": record.get("Date", ""),
                    "shot_type": record.get("Shot Type", "").lower() or None,
                    "platform": record.get("Target Platform", "").lower() or None,
                    "social_format": record.get("Social Format", ""),
                })
    return briefs


def format_results_for_sheet(results: list[dict]) -> list[list]:
    """
    Convert a list of interpretation results into rows ready to write
    back to the Google Sheet.

    Parameters
    ----------
    results : list[dict]
        Each dict from ai_interpreter.interpret_async()

    Returns
    -------
    list[list] — rows matching CONTENT_CALENDAR_HEADERS
    """
    rows = []
    for r in results:
        built = r.get("built_prompt")
        platforms = r.get("platforms", {})
        mj = platforms.get("midjourney")
        runway = platforms.get("runway")
        pika = platforms.get("pika")

        row = [
            r.get("date", datetime.now().strftime("%Y-%m-%d")),
            "GENERATED",
            r.get("brief", ""),
            r.get("raw_claude", {}).get("shot_type", ""),
            r.get("raw_claude", {}).get("target_platforms", [""])[0] if r.get("raw_claude", {}).get("target_platforms") else "",
            r.get("content_format", ""),
            built.positive if built else "",
            built.negative[:200] if built else "",
            mj.copy_paste if mj else "",
            runway.positive if runway else "",
            pika.positive if pika else "",
            r.get("creative_notes", ""),
            "",  # Performance Score — filled in later
            r.get("reasoning", ""),
        ]
        rows.append(row)
    return rows


# ─────────────────────────────────────────────────────────────────────────────
# Batch generation pipeline
# ─────────────────────────────────────────────────────────────────────────────

async def run_batch_from_sheet(
    spreadsheet_id: str,
    sheet_range: str = "Sheet1!A1:N200",
    credentials_path: Optional[str] = None,
    api_key: Optional[str] = None,
) -> dict:
    """
    Full pipeline: read briefs from Google Sheet → generate prompts → write results back.

    Parameters
    ----------
    spreadsheet_id : str
        Google Sheet ID
    sheet_range : str
        A1 notation for the data range
    credentials_path : str, optional
        Path to Google service account JSON
    api_key : str, optional
        Anthropic API key

    Returns
    -------
    dict with processed_count and any errors
    """
    from .ai_interpreter import interpret_async

    sheets = GoogleSheetsClient(credentials_path)
    rows = sheets.read_range(spreadsheet_id, sheet_range)
    briefs = parse_brief_rows(rows)

    if not briefs:
        return {"processed_count": 0, "message": "No TODO briefs found in sheet"}

    results = []
    errors = []

    for brief_record in briefs:
        try:
            target_platforms = None
            if brief_record.get("platform"):
                target_platforms = [brief_record["platform"]]

            result = await interpret_async(
                user_brief=brief_record["brief"],
                target_platforms=target_platforms,
                api_key=api_key,
            )
            result["brief"] = brief_record["brief"]
            result["date"] = brief_record.get("date", "")
            results.append(result)
        except Exception as e:
            errors.append({"brief": brief_record["brief"], "error": str(e)})

    # Write results back to sheet
    if results:
        output_rows = format_results_for_sheet(results)
        # Append to sheet after headers (find next empty row)
        sheets.append_rows(spreadsheet_id, sheet_range.split("!")[0] + "!A:N", output_rows)

    return {
        "processed_count": len(results),
        "error_count": len(errors),
        "errors": errors,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Nano Banana webhook integration
# ─────────────────────────────────────────────────────────────────────────────

class NanoBananaWebhook:
    """
    Send generated prompts to Nano Banana automation workflows via webhooks.
    Nano Banana can then trigger downstream actions (post to social, schedule, etc.)
    """

    def __init__(self, webhook_url: Optional[str] = None):
        self.webhook_url = webhook_url or os.environ.get("NANO_BANANA_WEBHOOK_URL")

    async def send_generated_prompts(
        self,
        interpretation_result: dict,
        metadata: Optional[dict] = None,
    ) -> dict:
        """
        Send a prompt generation result to a Nano Banana webhook.

        Parameters
        ----------
        interpretation_result : dict
            Output from ai_interpreter.interpret_async()
        metadata : dict, optional
            Additional context (user_id, campaign_name, schedule_date, etc.)

        Returns
        -------
        dict — Nano Banana response
        """
        if not self.webhook_url:
            raise ValueError(
                "Nano Banana webhook URL not configured. "
                "Set NANO_BANANA_WEBHOOK_URL env var or pass webhook_url."
            )

        built = interpretation_result.get("built_prompt")
        platforms = interpretation_result.get("platforms", {})
        raw = interpretation_result.get("raw_claude", {})

        payload = {
            "event": "prompts_generated",
            "timestamp": datetime.utcnow().isoformat(),
            "subject": raw.get("subject", ""),
            "shot_type": raw.get("shot_type", ""),
            "content_format": interpretation_result.get("content_format", ""),
            "creative_notes": interpretation_result.get("creative_notes", ""),
            "prompts": {
                "positive": built.positive if built else "",
                "negative": built.negative if built else "",
            },
            "platform_prompts": {
                platform: {
                    "positive": fp.positive,
                    "negative": fp.negative,
                    "copy_paste": fp.copy_paste,
                    "parameters": fp.parameters,
                }
                for platform, fp in platforms.items()
            },
            "metadata": metadata or {},
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                self.webhook_url,
                json=payload,
                headers={"Content-Type": "application/json"},
            )
            resp.raise_for_status()
            return {"status": resp.status_code, "response": resp.text}

    async def trigger_batch_complete(
        self,
        batch_results: list[dict],
        spreadsheet_id: Optional[str] = None,
    ) -> dict:
        """
        Notify Nano Banana that a batch generation job is complete.
        """
        if not self.webhook_url:
            raise ValueError("Nano Banana webhook URL not configured.")

        payload = {
            "event": "batch_generation_complete",
            "timestamp": datetime.utcnow().isoformat(),
            "count": len(batch_results),
            "spreadsheet_id": spreadsheet_id,
            "summary": [
                {
                    "subject": r.get("raw_claude", {}).get("subject", ""),
                    "shot_type": r.get("raw_claude", {}).get("shot_type", ""),
                    "platforms": list(r.get("platforms", {}).keys()),
                }
                for r in batch_results
            ],
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                self.webhook_url,
                json=payload,
                headers={"Content-Type": "application/json"},
            )
            resp.raise_for_status()
            return {"status": resp.status_code}


# ─────────────────────────────────────────────────────────────────────────────
# Generic webhook sender (for Zapier, Make, n8n, etc.)
# ─────────────────────────────────────────────────────────────────────────────

async def send_to_webhook(
    webhook_url: str,
    payload: dict,
    headers: Optional[dict] = None,
) -> dict:
    """
    Send any payload to any webhook URL. Compatible with Zapier, Make (Integromat),
    n8n, Pabbly, Nano Banana, or any custom webhook receiver.
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(
            webhook_url,
            json=payload,
            headers=headers or {"Content-Type": "application/json"},
        )
        resp.raise_for_status()
        return {"status": resp.status_code, "body": resp.text}
