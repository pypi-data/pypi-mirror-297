from playwright.async_api import Page, Locator, ElementHandle
from typing import Union, Callable

from .upload_file import UploadedFile
from .download_file import download_file
from .upload_file import upload_file_to_s3

async def save_file_to_s3(
    page: Page,
    trigger: Union[
        str,
        Locator,
        Callable[[Page], None],
    ],
    timeout: int = 5000,
):
    """
    Download a file from a web page using a trigger.

    This function supports three different ways to trigger a download:
    1. By URL
    2. By clicking on a playwright locator
    3. By executing a callback function that takes a page object as an argument and uses it to initiate the download.

    Args:
        page (Page): The Playwright Page object to use for the download.
        trigger (Union[str, Locator, Callable[[Page], None]]):
            - If str: URL to download from.
            - If Locator: playwright locator to click to download.
            - If Callable: callback function that takes a page object as an argument and uses it to initiate the download.

    Returns:
        url (str): The url of the attachment file.

    Example:
    ```python
    from intunedSdk import save_file_to_s3

    context, page = await launch_chromium(headless=False)
    url = await save_file_to_s3(page, "https://sandbox.intuned.dev/pdfs")
    ```
    
    ```python
    from intunedSdk import save_file_to_s3

    context, page = await launch_chromium(headless=False)
    url = await save_file_to_s3(page, page.locator("[href='/download/file.pdf']"))
    ```


    ```python
    from intunedSdk import save_file_to_s3

    context, page = await launch_chromium(headless=False)
    url = await save_file_to_s3(page, page.locator("button:has-text('Download')"))
    ```

    ```python
    from intunedSdk import save_file_to_s3

    context, page = await launch_chromium(headless=False)
    url = await save_file_to_s3(page, lambda page: page.locator("button:has-text('Download')").click())
    ```

    Note:
        If a URL is provided as the trigger, a new page will be created and closed
        after the download is complete.
        If a locator is provided as the trigger, the page will be used to click the element and initiate the download.
        If a callback function is provided as the trigger, the function will be called with the page object as an argument and will be responsible for initiating the download.
    """
    download = await download_file(page, trigger, timeout)
    uploaded: UploadedFile = await upload_file_to_s3(download)
    return uploaded.get_s3_key()