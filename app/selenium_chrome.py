import re
import tkinter as tk

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def get_imo_from_google_chrome(vessel_name):

    chrome_options = Options()
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

    vessel_name = vessel_name.replace(" ", "+")

    url = f"https://www.google.com/search?q=vessel+name%3A+{vessel_name}+vessel+imo"
    driver.get(url)
    
    list_of_possible_classes = ["hgKElc", "IZ6rdc", "ztXv9"]

    top_result = ""
    for class_name in list_of_possible_classes:
        try:
            top_result = driver.find_element(By.CLASS_NAME, class_name)
            
            if top_result:
                break
        except Exception:
            continue

    if not top_result:
        tk.messagebox.showinfo(title=None, message=f"Vessel IMO not found.\n")
        return

    top_result_title = top_result.text

    imo_found = re.search(r"(\d{7})", top_result_title)

    if not imo_found:
        return

    imo_found = imo_found.group()
    
    return imo_found
