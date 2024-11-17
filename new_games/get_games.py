from asyncio import timeout

import playwright
from playwright.sync_api import sync_playwright
from datetime import datetime, timedelta
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    url = "https://barbora.lt/darzoves-ir-vaisiai?order=SortByPopularity"
    page.goto(url)

    page.wait_for_selector("body > div.b-app > div > header > div.b-header-bottom > div > div > div.b-header-bottom--block > a > svg", strict=True)

    stuff = page.locator("#category-page-results-placeholder > div > ul").locator("li").all()
    index = 0

    start_nr = 32

    while index < len(stuff):
        try:
            name_locator = stuff[index].locator("#fti-product-title-category-page-"+str(index))
            name_locator.wait_for(timeout=2000)
            name = name_locator.text_content()
            
            image_locator = stuff[index].locator("//div//div//div[1]//div[1]//a//img")
            image_locator.wait_for(timeout=2000)
            image = image_locator.get_attribute("src")
            
            price_locator = page.locator("#fti-product-price-category-page-"+str(index)+" > div.tw-mb-\[2px\].tw-w-fit.tw-rounded-lg.tw-border.tw-border-solid.tw-border-neutral-200.tw-bg-white.tw-p-2 > div.tw-mb-\[2px\].tw-flex.tw-align-top.tw-text-neutral-900")
            price_locator.wait_for(timeout=2000)
            price = price_locator.text_content()
            
            # update games json
            print(f"    \"game-{start_nr}\":{{")
            print(f"      \"name\": \"{name}\",")
            print(f"      \"price\": \"{price}\",")
            print(f"      \"image\": \"{image.replace("_s", "_m")}\"")
            print(f"    }},")
            start_nr = start_nr + 1
        except playwright._impl._errors.TimeoutError:
            pass
        index = index + 1
        
    browser.close()
