import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(5)

    yield driver

    driver.quit()


def test_patient_login(driver):
    driver.get("http://127.0.0.1:5000/login")

    driver.find_element(By.NAME, "email").send_keys(
        "patient1@email.com"
    )
    driver.find_element(By.NAME, "password").send_keys(
        "patient123"
    )

    driver.find_element(
        By.XPATH, "//button[@type='submit']"
    ).click()

    wait = WebDriverWait(driver, 10)

    wait.until(EC.url_contains("/patient/dashboard"))

    assert "/patient/dashboard" in driver.current_url

    heading = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//*[contains(normalize-space(), 'Welcome,')]")
        )
    )

    assert "Welcome," in heading.text


def test_login_with_invalid_password(driver):
    driver.get("http://127.0.0.1:5000/login")

    driver.find_element(By.NAME, "email").send_keys(
        "patient1@email.com"
    )
    driver.find_element(By.NAME, "password").send_keys(
        "wrongpassword"
    )

    driver.find_element(
        By.XPATH, "//button[@type='submit']"
    ).click()

    wait = WebDriverWait(driver, 10)

    wait.until(EC.url_contains("/login"))

    assert "/login" in driver.current_url

    alert = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//div[contains(@class, 'alert')]")
        )
    )

    assert alert.text.strip() != ""


def test_login_with_invalid_email(driver):
    driver.get("http://127.0.0.1:5000/login")

    driver.find_element(By.NAME, "email").send_keys(
        "invalid@email.com"
    )
    driver.find_element(By.NAME, "password").send_keys(
        "patient123"
    )

    driver.find_element(
        By.XPATH, "//button[@type='submit']"
    ).click()

    wait = WebDriverWait(driver, 10)

    wait.until(EC.url_contains("/login"))

    assert "/login" in driver.current_url

    alert = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//div[contains(@class, 'alert')]")
        )
    )

    assert alert.text.strip() != ""