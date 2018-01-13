from selenium import webdriver
DRIVER = 'chromedriver'

def get_screenshot(url):
    driver = webdriver.Chrome(executable_path='/Users/mac/webprojects/telegram/chromedriver')
    driver.set_window_size(1084, 1084)
    driver.get(url)
    screenshot = driver.get_screenshot_as_png()

    driver.quit()
    return screenshot





