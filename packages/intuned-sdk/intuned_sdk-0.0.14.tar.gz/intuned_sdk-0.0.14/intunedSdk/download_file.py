from playwright.async_api import Page, Locator, ElementHandle
from typing import Union, Callable
import validators
import validators.uri

async def download_file(
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
    from intunedSdk import download_file

    context, page = await launch_chromium(headless=False)
    url = await download_file(page, "https://sandbox.intuned.dev/pdfs")
    ```
    
    ```python
    from intunedSdk import download_file

    context, page = await launch_chromium(headless=False)
    url = await download_file(page, page.locator("[href='/download/file.pdf']"))
    ```


    ```python
    from intunedSdk import download_file

    context, page = await launch_chromium(headless=False)
    url = await download_file(page, page.locator("button:has-text('Download')"))
    ```

    ```python
    from intunedSdk import download_file

    context, page = await launch_chromium(headless=False)
    url = await download_file(page, lambda page: page.locator("button:has-text('Download')").click())
    ```

    Note:
        If a URL is provided as the trigger, a new page will be created and closed
        after the download is complete.
        If a locator is provided as the trigger, the page will be used to click the element and initiate the download.
        If a callback function is provided as the trigger, the function will be called with the page object as an argument and will be responsible for initiating the download.
    """
    page_to_download_from = page
    should_close_after_download = False
    
    def is_url() -> bool:
        return isinstance(trigger, str)
    
    def is_locator() -> bool:
        return isinstance(trigger, Locator) or isinstance(trigger, ElementHandle)

    def is_callable() -> bool:
        return callable(trigger)

    if is_url():
        page_to_download_from = await page.context.new_page()
        should_close_after_download = True
    print(f"start to download from {trigger}")
    try:
        async with page_to_download_from.expect_download(timeout=timeout) as download_info:
            if is_url():
                is_valid = validators.url(trigger)
                if not is_valid:
                    raise ValueError(f"Invalid URL: {trigger}")
                try:
                    await page_to_download_from.goto(trigger, wait_until="load", timeout=timeout)
                except Exception:
                    pass

            if is_locator():
                await trigger.click()

            if is_callable():
                await trigger(page)
            
    # these errors are designed to give a user friendly feedback and hence a friendly message to the llm
    except TimeoutError as e:
        if is_url():
            await page_to_download_from.close()
            raise TimeoutError(f"Download timeout for url:{trigger}. Download was never triggered.")
        if is_locator():
            raise TimeoutError(f"Download timeout for locator:{trigger}. Download was never triggered.")
        if is_callable():
            raise TimeoutError(f"Download timeout for callable:{trigger}. Download was never triggered.")

    download = await download_info.value
    print(f"Downloaded file successfully by {trigger}")
    if should_close_after_download:
        await page_to_download_from.close()

    return download
