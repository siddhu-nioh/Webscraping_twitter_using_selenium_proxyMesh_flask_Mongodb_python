from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient
import time  
import uuid
from datetime import datetime
import requests
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


service = Service(r"C:\Windows\chromedriver.exe")


driver = webdriver.Chrome(service=service)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


MONGO_URI = "mongodb+srv://<username>:<password>@clusters0.pwmqglw.mongodb.net/?retryWrites=true&w=majority&appName=clusters0"
client = MongoClient(MONGO_URI)
db = client.get_database("database_name")  
collection = db.get_collection("trending_topics")  

# Proxy and Selenium Setup
PROXY = "http://sid:@HVNSking.123@us-ca.proxymesh.com:31280"
options = Options()
options.add_argument(f"--proxy-server={PROXY}")
options.add_argument("--headless")  
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# driver = webdriver.Chrome("C:\Windows\chromedriver.exe")

def fetch_trends():
    try:
        logging.info("Navigating to Twitter login page...")
        driver.get("https://x.com/i/flow/login")
        time.sleep(6)  

        
        logging.info("Locating username field...")
        username = driver.find_element(By.XPATH, "//input[@name='text']")
        username.send_keys("YOUR USERNAME")
        
        
        logging.info("Clicking Next button after entering username...")
        next_button = driver.find_element(By.XPATH, "//span[text()='Next']")
        
        next_button.click()
        time.sleep(3)  

         
        try:
            logging.info("Checking for password field...")
            password_field = driver.find_element(By.XPATH, "//input[@name='password']")
            logging.info("Password field found, entering password...")
            password_field.send_keys("YOUR PASSWORD")
        except:
            
            logging.info("Password field not found, entering email due to unusual activity...")
            email_field = driver.find_element(By.XPATH, "//input[@name='text']")
            email_field.send_keys("YOURGMAIL@gmail.com")
            logging.info("Clicking Next button after entering email...")
            next_button = driver.find_element(By.XPATH, "//span[text()='Next']")
        
            next_button.click()
            time.sleep(2)  
            password_field = driver.find_element(By.XPATH, "//input[@name='password']")
            password_field.send_keys("@HVNSking.123")

        
        # logging.info("Locating password field...")
        # password = driver.find_element(By.XPATH, "//input[@name='password']")
        # password.send_keys("@HVNSking.123")
        
        
        logging.info("Clicking Login button after entering password...")
        login_button = driver.find_element(By.XPATH, "//span[text()='Log in']")

        login_button.click()
        time.sleep(5)  

        
        logging.info("Waiting for home section to load...")
        WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH, "//span[text()='Home']"))
)
        logging.info("as for the whats happening section contains only 4 hastags lets click on show more as it red directs to for you section to load...")

        logging.info("same as whats happeing section by clicking on show more it redirects to   for you  section to load...")
        explore_button = driver.find_element(By.XPATH, "//span[contains(text(),'Explore')]")
        explore_button.click()


        logging.info("Waiting for for you section to load...")
        WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH, "//span[text()='For You']"))
)


        logging.info("Waiting for top  for you section to load...")
        trending_section = driver.find_element(By.XPATH, "//div[contains(@class, 'css-146c3p1') and contains(., 'For You')]")
        trending_section.click()



        # logging.info("Waiting for top trending in india  section to load...")
        
       
        logging.info("Fetching the top trending section...")

        try:
    
            WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//section[contains(@aria-labelledby, 'accessible-list')]"))
    )

    
            trends_container = driver.find_element(By.XPATH, "//section[contains(@aria-labelledby, 'accessible-list')]")

    
            trend_items = trends_container.find_elements(By.XPATH, ".//div[contains(@data-testid, 'trend')]")

    
            top_trends = []
            unwanted_texts = {'·', 'Trending in India'}  
            for item in trend_items[:5]:  
                try:
        
                    span_tags = item.find_elements(By.XPATH, ".//span")
                         
                    seen_texts = set()  
                    trend_texts = []
        
                    for span in span_tags:
                        text = span.text.strip()
                        if text and text not in unwanted_texts and text not in seen_texts:
                            trend_texts.append(text)
                            seen_texts.add(text)
        
        
                    if trend_texts:  
                        top_trends.append(trend_texts)

                    # trend_texts = [span.text for span in span_tags if span.text.strip()]  
        #             trend_texts = [
        #     span.text for span in span_tags
        #     if span.text.strip() and span.text.strip() not in unwanted_texts
        # ]
        
        
                    # top_trends.append(trend_texts)
                except Exception as trend_extraction_error:

                    logging.warning(f"Could not extract trend text for an item: {trend_extraction_error}")

            logging.info(f"Top 5 trends fetched: {top_trends}")

    
            unique_id = str(uuid.uuid4())
            ip_address = requests.get("https://api.ipify.org").text
            data = {
        "_id": unique_id,
        "nameoftrend1": top_trends[0] if len(top_trends) > 0 else None,
        "nameoftrend2": top_trends[1] if len(top_trends) > 1 else None,
        "nameoftrend3": top_trends[2] if len(top_trends) > 2 else None,
        "nameoftrend4": top_trends[3] if len(top_trends) > 3 else None,
        "nameoftrend5": top_trends[4] if len(top_trends) > 4 else None,
        "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ip_address": ip_address
    }
            collection.insert_one(data)
            logging.info("Data stored successfully in MongoDB.")
            return data

        except Exception as e:
            logging.error(f"An error occurred while fetching trends: {e}", exc_info=True)
            return {"error": str(e)}


    finally:
        logging.info("Closing the browser...")
        driver.quit()

if __name__ == "__main__":
    result = fetch_trends()
    logging.info(f"Script execution completed. Result: {result}")
