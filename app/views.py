from django.shortcuts import render
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time
import requests

# Create your views here.
def index(request):
    return render(request, 'trail.html')

def runpyfile(request):
    if(request.method=='POST'):
        if(request.POST.get('inputString')):
            user_input = request.POST.get('inputString')
            chrome_options = Options()
            # chrome_options.add_argument('--headless')
            driver = webdriver.Chrome(service=Service(
                ChromeDriverManager().install()), options=chrome_options)

            # taking the name of the song from the user
            final_input = user_input + " saavn"

            # searches for the song on google
            url = 'https://www.google.co.in/'
            driver.get(url)
            search_box = driver.find_element(By.NAME, 'q')
            search_box.send_keys(final_input)
            search_box.send_keys(Keys.RETURN)

            wait = WebDriverWait(driver, 10)
            search_results = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'h3')))
            first_result = search_results[0]
            first_result.click()
            


            # click the play button
            try:
                play_button = wait.until(EC.element_to_be_clickable(
                    (By.CLASS_NAME, 'c-btn--primary')))
                play_button.click()

                import time
                time.sleep(30)

            except Exception as e:
                print(f"An error occurred: {str(e)}")

            #click the mute button
            try:
            #     mute_button = wait.until(EC.element_to_be_clickable(
            #         (By.ID, 'player_volume')))
            #     mute_button.click()
                    mute_button = driver.find_element(By.ID,'player_volume')
                    mute_button.click()   

            except Exception as e:
                print(f"An error occurred while pausing: {str(e)}")   
                              

            # get the audio url
            # required_url =''
            for request in driver.requests:
                if request.url.endswith('.mp4'):
                    required_url = request.url


            # download the audio
            output_filename = user_input + ".mp4"

            try:
                response = requests.get(required_url, stream=True)
                if response.status_code == 200:
                    with open(output_filename, 'wb') as file:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                file.write(chunk)
                    print(f"Downloaded {output_filename} successfully!")
                else:
                    print(f"Failed to download. Status code: {response.status_code}")
            except Exception as e:
                print(f"An error occurred: {str(e)}")
            finally:
                driver.quit()
                
            return render(request, 'trail.html')
        

            
                