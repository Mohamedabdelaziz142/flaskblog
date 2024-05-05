from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver = webdriver.Chrome()
app_url = "http://localhost:5000/"

email = "testuser@example.com"
password = "testpassword"


def login():
    driver.get(f"{app_url}/login")

    email_field = driver.find_element(By.ID, "email")  
    password_field = driver.find_element(By.ID, "password")  
    login_button = driver.find_element(By.ID, "login_button")  
    email_field.send_keys(email)
    password_field.send_keys(password)
    login_button.click()

    WebDriverWait(driver, 10).until(EC.title_contains("Welcome"))


def create_post(title, content):
    driver.get(f"{app_url}/post/new")

    title_field = driver.find_element(By.ID, "title")  
    content_field = driver.find_element(By.ID, "content")  
    submit_button = driver.find_element(By.ID, "submit_button")  
    title_field.send_keys(title)
    content_field.send_keys(content)
    submit_button.click()

    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, "h1"), title)
    )


def read_post(title):
    driver.get(f"{app_url}/posts")
    post_element = driver.find_element(
        By.XPATH, f"//h2[text()='{title}']/.."  
    )
    content_text = post_element.find_element(By.CLASS_NAME, "post-content").text
    assert title in content_text


def update_post(title, new_title, new_content):
    driver.get(f"{app_url}/posts")
    post_element = driver.find_element(
        By.XPATH, f"//h2[text()='{title}']/../a[@href='/post/{post_id}/edit']"
    )
    post_id = post_element.get_attribute("href").split("/")[-2]  
    post_element.click()
    title_field = driver.find_element(By.ID, "title")  
    content_field = driver.find_element(By.ID, "content")  
    submit_button = driver.find_element(By.ID, "submit_button")  
    title_field.clear()
    title_field.send_keys(new_title)
    content_field.clear()
    content_field.send_keys(new_content)
    submit_button.click()

    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, "h1"), new_title)
    )

def delete_post(title, expected_status_code=200):
    driver.get(f"{app_url}/posts")
    post_element = driver.find_element(
        By.XPATH, f"//h2[text()='{title}']/../a[@href='/post/{post_id}/delete']"
    )
    post_id = post_element.get_attribute("href").split("/")[-2] 
    post_element.click()
    if expected_status_code != 200:
        error_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "alert-danger"))
        )
        assert "You are not authorized to delete this post" in error_message.text
        return
    WebDriverWait(driver, 10).until(
        lambda driver: driver.current_url != f"{app_url}/post/{post_id}/delete"
    )
