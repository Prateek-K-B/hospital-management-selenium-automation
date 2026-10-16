import uuid

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_patient_registration():
    driver = webdriver.Chrome()
    driver.maximize_window()

    try:
        driver.get("http://127.0.0.1:5000/register")

        # Generate a unique email for each test run
        unique_id = uuid.uuid4().hex[:8]
        email_address = f"testpatient_{unique_id}@example.com"

        # Fill in the registration form
        driver.find_element(By.NAME, "name").send_keys(
            "Test Patient"
        )
        driver.find_element(By.NAME, "email").send_keys(
            email_address
        )
        driver.find_element(By.NAME, "password").send_keys(
            "TestPass123"
        )
        driver.find_element(By.NAME, "phone").send_keys(
            "9876543210"
        )
        driver.find_element(By.NAME, "address").send_keys(
            "Bengaluru"
        )

        # Submit the registration form
        driver.find_element(
            By.XPATH, "//button[@type='submit']"
        ).click()

        wait = WebDriverWait(driver, 10)

        # Verify that registration redirects to the login page
        wait.until(EC.url_contains("/login"))

        assert "/login" in driver.current_url

    finally:
        driver.quit()