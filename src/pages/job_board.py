from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time

import streamlit as st

import subprocess

# /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=8989 --user-data-dir=/Users/rafaelfonseca/Documents/workspace/chrome_folder

def kill_chrome(remote_debugging_port, user_data_dir):
    # Escape spaces for the command-line
    user_data_dir_escaped = user_data_dir.replace(" ", "\ ")
    kill_command = f"pkill -f '/Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome --remote-debugging-port={remote_debugging_port} --user-data-dir={user_data_dir_escaped}'"
    try:
        subprocess.run(kill_command, shell=True, check=True)
        print("Chrome process terminated successfully.")
    except subprocess.CalledProcessError as e:
        print("Failed to terminate Chrome process:", e)

def open_browser_in_debug_mode():
  command = """/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=8989 --user-data-dir=/Users/rafaelfonseca/Documents/workspace/chrome_folder"""
  process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def fill_field(driver, type, field, value):
  try:
    wait = WebDriverWait(driver, 2)
    element = wait.until(EC.presence_of_element_located((By.ID,field)))
    if type == 'input':
      element.clear()  
      element.send_keys(value)
    
    if type == 'select':
      select = Select(element)
      select.select_by_visible_text(value)
      return
    
  except: 
    pass

def fill_form(driver):
  
  fields = [
    ['input','first_name', 'Rafael'],
    ['input','last_name', 'Fonseca'],
    ['input','email', 'rfonseca85@yahoo.ca'],
    ['input','phone', '6479632054'],
    ['select',"job_application_gender", 'Male'],
    ['select',"job_application_gender", 'M'],
    ['select',"job_application_hispanic_ethnicity", 'Yes'],
    ['select',"job_application_veteran_status", 'I am not a protected veteran'],
    ['select',"job_application_disability_status", 'No, I do not have a disability and have not had one in the past'],
    
    #disability_status_dropdown_container
    ]

  for field in fields:
    fill_field(driver, field[0], field[1], field[2])


def apply_to_job():

  chrome_options = Options()
  chrome_options.add_experimental_option("debuggerAddress", "localhost:8989")
  driver = webdriver.Chrome(chrome_options)
  wait = WebDriverWait(driver, 3)


  # Open Job
  # driver.get('https://www.linkedin.com/jobs/collections/recommended/?currentJobId=3815294908&eBP=CwEAAAGOa5Z4ilc1Syb2TX7veTaQZKRVVw5SCEhMtkWNSTOg-ORTGRMo-ZVHxMj8RhXR2A02xUzRBD_CfMv2KJHOk6TivG6MtfXDSULxigHWMxrc4xV2psDfOyi07PZFQTO3VvKHxD7AI6Mg6xWj2uptyaYau-0J1O6B7_cd_-kyOQxfBYElUZsuPLhDM-P3NHWjta6jW7NxbG2grBirzHbZJX50tQah1Z12swEW-zEWxShKgvWuPCuKJW6WyUJSaHXKyAPNltNKUZD6Z_ASeQqUJtcJOF_wCXvldwLcdEuR9LDF_B_9WFd0ynPeRD-CAk70RPunLBhrbUlPCI0gP5uOsZKP8azsZv310cvG6--FDuWiRTb5JDPdXmAi&refId=m0m0cpMlma3jn4RHX2Tn8g%3D%3D&trackingId=erIMdSv9LzEOZUqAI0Yh0A%3D%3D')
  # apply = driver.find_element(By.XPATH,"//span[contains(.,'Apply')]")
  # apply.click()

  # Fill Form
  driver.get('https://www.ixl.com/company/careers/apply?gh_jid=7057817002&gh_src=9ab9c2a12')
  time.sleep(5)

  #Try to switch to iframe if exist
  try:
    driver.switch_to.frame(driver.find_element(By.XPATH, "//iframe[@id='grnhse_iframe']"))
  except:
    pass
  
  # Fill Form
  fill_form(driver)

  


def main():
  st.title('Job Board')
  process = None

  if st.button("Open Browser in Debug Mode"):
    kill_chrome(8989, "/Users/rafaelfonseca/Documents/workspace/chrome_folder")
    open_browser_in_debug_mode()


  if st.button("Apply for Job"):
    apply_to_job()
    st.success("Job application completed successfully.")

  if st.button("Close Browser in Debug Mode"):
    kill_chrome(8989, "/Users/rafaelfonseca/Documents/workspace/chrome_folder")
      
# apply_to_job()