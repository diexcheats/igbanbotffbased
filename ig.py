from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import getpass

# Order of report types as per your preference
REPORT_SEQUENCE = [
    ("impersonating_freefire_ssa", 7),
    ("impersonating_freefirebr_official", 6),
    ("violence_and_threats", 3),
    ("hate_speech", 5),
    ("bullying", 2),
    ("scam_or_fraud", 2)
]

def login_instagram(driver, username, password):
    """Logs into Instagram."""
    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(5)

    username_input = driver.find_element(By.NAME, "username")
    password_input = driver.find_element(By.NAME, "password")

    username_input.send_keys(username)
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)

    time.sleep(10)  # Wait for login to complete

def report_account(driver, fake_account, reason):
    """Reports an Instagram account for a given reason."""
    report_url = f"https://www.instagram.com/{fake_account}/"
    driver.get(report_url)
    time.sleep(5)

    try:
        # Click the three-dot menu on the profile
        menu_button = driver.find_element(By.XPATH, "//button[contains(@aria-label, 'More options')]")
        menu_button.click()
        time.sleep(2)

        # Click "Report"
        report_option = driver.find_element(By.XPATH, "//span[contains(text(), 'Report')]")
        report_option.click()
        time.sleep(2)

        # Select the report reason
        if reason == "impersonating_freefire_ssa" or reason == "impersonating_freefirebr_official":
            reason_option = driver.find_element(By.XPATH, "//span[contains(text(), 'It’s impersonating someone I know')]")
        elif reason == "violence_and_threats":
            reason_option = driver.find_element(By.XPATH, "//span[contains(text(), 'Violence or threat of violence')]")
        elif reason == "hate_speech":
            reason_option = driver.find_element(By.XPATH, "//span[contains(text(), 'Hate speech or symbols')]")
        elif reason == "bullying":
            reason_option = driver.find_element(By.XPATH, "//span[contains(text(), 'Bullying or harassment')]")
        elif reason == "scam_or_fraud":
            reason_option = driver.find_element(By.XPATH, "//span[contains(text(), 'Scam or fraud')]")
        else:
            print(f"Invalid report reason: {reason}")
            return

        reason_option.click()
        time.sleep(2)

        # Submit the report
        submit_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Submit')]")
        submit_button.click()

        print(f"Successfully reported {fake_account} for {reason}")

    except Exception as e:
        print(f"Error reporting {fake_account}: {e}")

def main():
    """Main function to execute automation."""
    username = input("Enter your Instagram username: ")
    password = getpass.getpass("Enter your Instagram password: ")  # Hides password input for security
    victim_username = input("Enter the impersonating account's username: ")

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        login_instagram(driver, username, password)

        # Report using each method in order
        for reason, count in REPORT_SEQUENCE:
            for _ in range(count):
                report_account(driver, victim_username, reason)
                time.sleep(5)  # Small delay to mimic human behavior

    finally:
        driver.quit()
        print("All reports submitted successfully.")

if __name__ == "__main__":
    main()