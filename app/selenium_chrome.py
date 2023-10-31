from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

def get_imo_from_google_chrome(vessel_name):
    vessel_name = "34lkjwer"
    url = f"https://www.google.com/search?q=vessel+name%3A+{vessel_name}+imo"
    driver.get(url)

    # Grab the top result title and URL
    top_result = driver.find_element(By.CLASS_NAME, "IZ6rdc")
    top_result_title = top_result.text.replace("IMO", "").strip()

    return top_result_title

