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


def test_appointment_booking_page_loads(driver):
    login_as_patient(driver)

    driver.get("http://127.0.0.1:5000/patient/doctors")

    wait = WebDriverWait(driver, 15)

    book_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "(//a[contains(., 'Book Appointment')])[1]")
        )
    )

    book_button.click()
    print("URL after click:", driver.current_url)
    print("Browser handles:", driver.window_handles)
    print("Browser title:", driver.title)

    try:
        wait.until(
            lambda d: "/patient/book/" in d.current_url
            or "/login" in d.current_url
        )
    except Exception:
        print("URL after clicking Book Appointment:", driver.current_url)
        print("Page title:", driver.title)
        print("Browser alert present:", bool(driver.find_elements(By.TAG_NAME, "body")))
        raise

    print("Current URL:", driver.current_url)

    heading = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//h2[contains(., 'Book Appointment')]")
        )
    )

    assert "Book Appointment" in heading.text


def test_appointment_date_selection(driver):
    login_as_patient(driver)

    driver.get("http://127.0.0.1:5000/patient/doctors")

    driver.find_element(
        By.XPATH, "(//a[contains(., 'Book Appointment')])[1]"
    ).click()

    wait = WebDriverWait(driver, 10)

    print("Current URL:", driver.current_url)
    print("Page title:", driver.title)
    print("Page source contains dateSelect:", "dateSelect" in driver.page_source)

    date_dropdown = wait.until(
        EC.presence_of_element_located(
            (By.ID, "dateSelect")
        )
    )

    print("Current URL:", driver.current_url)
    print("Page title:", driver.title)
    print("Date dropdown found:", date_dropdown.is_displayed())
    print("Number of date options:", len(date_dropdown.find_elements(By.TAG_NAME, "option")))
    print("Page contains dateSelect:", "dateSelect" in driver.page_source)

    date_select = Select(date_dropdown)

    assert len(date_select.options) > 1

    # Select the first available date
    date_select.select_by_index(1)

    # Verify that the time-slot section becomes visible
    slots_container = wait.until(
        EC.visibility_of_element_located(
            (By.ID, "timeSlotsContainer")
        )
    )

    assert slots_container.is_displayed()

    # Verify that time-slot radio buttons are available
    time_slots = wait.until(
        EC.presence_of_all_elements_located(
            (By.NAME, "time_slot")
        )
    )

    assert len(time_slots) > 0

    driver.execute_script("arguments[0].click();", time_slots[0])

    print("Radio button selected:", time_slots[0].is_selected())
    print("Radio button HTML:", time_slots[0].get_attribute("outerHTML"))
    print("Submit button disabled:", driver.find_element(
        By.ID, "submitBtn"
    ).get_attribute("disabled"))

    submit_button = driver.find_element(
        By.ID, "submitBtn"
    )

    wait.until(
        lambda d: d.find_element(
            By.ID, "submitBtn"
        ).is_enabled()
    )

    assert submit_button.is_enabled()