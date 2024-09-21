import os
import pytest
import uuid
from pathlib import Path
from intunedSdk.launch_chromium import launch_chromium
from intunedSdk.download_file import download_file
from intunedSdk import upload_file_to_s3

from dotenv import load_dotenv

load_dotenv()


@pytest.mark.asyncio
async def test_upload_file_to_s3():
    [context, page] = await launch_chromium(headless=False)
    await page.goto("https://sandbox.intuned.dev/pdfs")

    download = await download_file(
        page,
        page.locator(
            "xpath=/html/body/div/div/main/div/div/div/table/tbody/tr[1]/td[4]/a"
        ),
    )

    uploaded_file = await upload_file_to_s3(
        download, fileNameOverride="okokokokokokok.pdf"
    )
    
    signed_url = uploaded_file.get_signed_url()
    assert signed_url is not None
    assert signed_url.startswith("https://")
    assert uploaded_file.file_name is not None

@pytest.mark.asyncio
async def test_download_url():
    [context, page] = await launch_chromium(headless=True)
    await page.goto("https://sandbox.intuned.dev/pdfs")

    download = await download_file(
        page,
        "https://intuned-docs-public-images.s3.amazonaws.com/27UP600_27UP650_ENG_US.pdf",
    )
    assert download is not None

@pytest.mark.asyncio
async def test_download_locator():
    [context, page] = await launch_chromium(headless=True)
    await page.goto("https://sandbox.intuned.dev/pdfs")

    download = await download_file(
        page,
        lambda page: page.locator(
            "xpath=/html/body/div/div/main/div/div/div/table/tbody/tr[1]/td[4]/a"
        ).click(),
    )
    assert download is not None