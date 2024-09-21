import os
import pytest
import uuid
from pathlib import Path
from intunedSdk.launch_chromium import launch_chromium
from intunedSdk import extract_structured_data_from_page
from dotenv import load_dotenv
import logging

load_dotenv()


@pytest.mark.asyncio
async def test_upload_file_to_s3():
    [_, page] = await launch_chromium(headless=False)
    await page.goto("https://sandbox.intuned.dev/pdfs")
    res = await extract_structured_data_from_page(
        page,
        {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {"name": {"type": "string"}},
            },
        },
        model="gpt-4o-mini-2024-07-18",
    )
    logging.info(res)
    assert res is not None
