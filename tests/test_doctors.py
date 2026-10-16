import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()

    yield driver

    driver.quit()


def login_as_patient(driver):
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

    WebDriverWait(driver, 10).until(
        EC.url_contains("/patient/dashboard")
    )


def test_doctors_page_displays_doctors(driver):
    login_as_patient(driver)

    driver.get("http://127.0.0.1:5000/patient/doctors")

    wait = WebDriverWait(driver, 10)

    heading = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//h2[contains(., 'Find Doctors')]")
        )
    )

    assert "Find Doctors" in heading.text

    doctor_cards = driver.find_elements(
        By.XPATH,
        "//a[contains(., 'Book Appointment')]"
    )

    assert len(doctor_cards) > 0


def test_search_doctor_by_name(driver):
    login_as_patient(driver)

    driver.get("http://127.0.0.1:5000/patient/doctors")

    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys("Rajesh")

    driver.find_element(
        By.XPATH, "//button[@type='submit']"
    ).click()

    wait = WebDriverWait(driver, 10)

    wait.until(
        EC.url_contains("/patient/doctors")
    )

    doctor_cards = driver.find_elements(
        By.XPATH,
        "//a[contains(., 'Book Appointment')]"
    )

    assert len(doctor_cards) > 0

    page_text = driver.find_element(By.TAG_NAME, "body").text

    assert "Rajesh" in page_text


def test_department_dropdown_is_available(driver):
    login_as_patient(driver)

    driver.get("http://127.0.0.1:5000/patient/doctors")

    department_dropdown = Select(
        driver.find_element(By.NAME, "department_id")
    )

    assert len(department_dropdown.options) > 1


def test_book_appointment_button_is_available(driver):
    login_as_patient(driver)

    driver.get("http://127.0.0.1:5000/patient/doctors")

    wait = WebDriverWait(driver, 10)

    book_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "(//a[contains(., 'Book Appointment')])[1]")
        )
    )

    assert book_button.is_displayed()
    assert book_button.is_enabled()