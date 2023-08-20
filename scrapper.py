from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import requests, io, time
from PIL import Image
 
driver_path = r"C:\Users\czean\Documents\ChromeDriver\chromedriver.exe"
vivaldi_path = r"C:\Users\czean\AppData\Local\Vivaldi\Application\vivaldi.exe"

options = webdriver.ChromeOptions()
options.binary_location = vivaldi_path

# Got help from ChatGPT to make it work using Vivaldi
# Create a Chrome service with the executable path
service = webdriver.chrome.service.Service(driver_path)

# Initialize the Chrome webdriver with the service and options
driver = webdriver.Chrome(service=service, options=options)

image_url = r"https://progressivecrop.com/wp-content/uploads/2020/11/1-1-1-Bacterial-Leaf-Spot.jpg"

def get_images(driver, delay, max_images):
    def scroll_down(driver):
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        time.sleep(delay)
        
    url = "https://www.google.com/search?sca_esv=558490629&q=lettuce+bacterial+leaf+spot&tbm=isch#imgrc=Ed7Q09P1YBFz6M"
    driver.get(url)
    
    image_urls = set()
    
    while len(image_urls) < max_images:
        scroll_down(driver)
            
        thumbnails = driver.find_elements(By.CLASS_NAME, "Q4LuWd")
        
        for image in thumbnails[len(image_urls): max_images]:
            try:
                image.click()
                time.sleep(delay)
            except:
                continue
            
            images = driver.find_elements(By.CLASS_NAME, "r48jcc pT0Scc iPVvYb")
            for img in images:
                if img.get_attribute('src') and 'http' in img.get_attribute('src'):
                    image_urls.add(image.get_attribute('src'))
                    print(f"Found {len(image_urls)}")
                    
    return image_urls                       
            
def download_image(download_path, url, file_name):
    try: 
        image_content = requests.get(url).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file)
        file_path = download_path + file_name

        with open(file_path, "wb") as f:
            image.save(f, "JPEG")

        print("Success")
    except Exception as e:
        print('FAILED -', e)
        
urls = get_images(driver, 1, 5)
print(urls)
driver.quit()

# TODO: There are tons of error atm... 
# 1. Terminal says exit_code=0 after running the code (idk why) I expect it to wait for the "Found " before exiting
# 2. Browser opens, scrolls down the page, and clicks on images, but I don't know if it is saving it in the image_urls.
# 3. Fix clicking the same image so it does not indefinitely loops through the code.


# TODO: Implement this in CLI for accessibility 