from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def convert_amharic_number(number, number_type='General'):
    url = 'https://www.metaappz.com/Numbers_to_Amharic_Words_Converter/Default.aspx'
    
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
       
        driver.get(url)
     
        input_box = driver.find_element(By.ID, 'article_InputTextBox1')
        input_box.clear()
        input_box.send_keys(str(number))
        
        if number_type == 'Birr':
            birr_radio = driver.find_element(By.ID, 'article_Currency')
            birr_radio.click()
        else:
            general_radio = driver.find_element(By.ID, 'article_General')
            general_radio.click()
       
        convert_button = driver.find_element(By.ID, 'article_ConvertButton1')
        convert_button.click()
        
    
        result = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'article_StatusLabel1'))
        )
        
        return result.text.strip()
    
    finally:
        driver.quit()


def convert_to_geez(number):
    url = 'https://www.metaappz.com/Geez_Numbers_Converter/Default.aspx'
    
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        driver.get(url)
        
        input_box = driver.find_element(By.ID, 'article_InputTextBox1')
        input_box.clear()
        input_box.send_keys(str(number))
        
        convert_button = driver.find_element(By.ID, 'article_ConvertButton1')
        convert_button.click()
        
        geez_result = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'article_StatusLabel1'))
        )
        
        geez_month = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'article_StatusLabel2'))
        )
        
        result = geez_result.text.strip() + " : " + geez_month.text.strip()
        
        return result
        
    finally:
        driver.quit()


def convert_from_geez(geez_number):
    url = 'https://www.metaappz.com/Geez_Numbers_Converter/Default.aspx'
    
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        driver.get(url)
        
        input_box = driver.find_element(By.ID, 'article_InputTextBox2')
        input_box.clear()
        input_box.send_keys(geez_number)
        
        convert_button = driver.find_element(By.ID, 'article_ConvertButton2')
        convert_button.click()
        
        converted_number = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'article_statusLabel3'))
        )
        
        return converted_number.text.strip()
        
    finally:
        driver.quit()