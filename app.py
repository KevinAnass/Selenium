import json
import time

import pyfiglet
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

fireFoxOptions = FirefoxOptions()
fireFoxOptions.add_argument("--headless")

driver = webdriver.Firefox()
lsData = []


def big_Text(value):
    big_text = pyfiglet.figlet_format(value)
    print(big_text)


def convert_html_to_data(div: WebElement):
    title = div.find_element(By.CSS_SELECTOR, "#video-title").text
    length = div.find_element(By.CSS_SELECTOR, ".badge-shape-wiz__text").text
    metaData = div.find_element(By.CSS_SELECTOR, "#metadata-line")
    views = metaData.find_element(By.XPATH, ".//span[1]").text
    time = metaData.find_element(By.XPATH, ".//span[2]").text
    lsData.append({"Title": title, "Length": length, "Views": views, "Time": time})


def export_into_json(nameChannel):
    with open("videos_" + nameChannel + ".jsonl", "w", encoding="utf-8") as jsonl_file:
        for item in lsData:
            jsonl_file.write(json.dumps(item, ensure_ascii=False) + "\n")


def get_youtube_channel_data():
    big_Text("Welcome To Selenium Scarper")
    notFound = True
    while notFound:
        chanelId = input("Please Enter your youtube channel UserId: ")
        driver.get("https://www.youtube.com/@" + chanelId + "/videos")
        try:
            driver.find_element(By.ID, "contentContainer")
            divs_with_content_id = driver.find_elements(By.ID, "content")
            for div in divs_with_content_id:
                convert_html_to_data(div)
            export_into_json(chanelId)
        except:
            print("not found")
            notFound = True


def main():
    to_continue = True
    while to_continue:
        get_youtube_channel_data()
        if input("Would you like to continue?\n").strip().upper() == "NO":
            to_continue = False


if __name__ == "__main__":
    main()
