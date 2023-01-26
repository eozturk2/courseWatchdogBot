import asyncio
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By


# Find elements by XPATH - might need to inspect element in VSB to find them again
# in the future! You should find seats by class name, because there will often
# be multiple courses you will need to track

# TODO: Make ChromeDriver open different tabs
class ChromeDriverHandler:

    driver = None
    continue_button = "/html/body/div[2]/div/input"
    winter_2023_button = "//*[@id='term_202301']"
    course_input_box = "//*[@id='code_number']"
    seats = "seatText"
    right_arrow = "//*[@id='page_results']/div[5]/div[3]/div[3]/div[1]/table/tbody/tr[1]/td[4]/a"
    current_result = "//*[@id='page_results']/div[5]/div[3]/div[3]/div[1]/table/tbody/tr[1]/td[3]/span/span[1]"
    results = "//*[@id='page_results']/div[5]/div[3]/div[3]/div[1]/table/tbody/tr[1]/td[3]/span/span[2]"
    back_to_start_arrow = "//*[@id='page_results']/div[5]/div[3]/div[3]/div[1]/table/tbody/tr[1]/td[1]/a"

    def __init__(self):
        pass

    def initializeDriver(self):
        self.driver = webdriver.Chrome("C:/Program Files/Google/Chrome/Application/chromedriver.exe")
        self.goToVSB()

    def goToVSB(self):
        self.driver.get('https://vsb.mcgill.ca/vsb/welcome.jsp')
        self.driver.maximize_window()
        self.driver.find_element(By.XPATH, value=self.continue_button).click()
        self.driver.find_element(By.XPATH, value=self.winter_2023_button).click()

    async def singleCourseMode(self, courses, image_save_path):
        ...

    # TODO: Rewrite this to calculate "subtotals" of occupancy for each course. This will also take care of the
    #  single course mode!
    async def allScheduleMode(self, courses, image_save_path, called_from_single_course_mode=False, call_order=None,
                              supplied_driver=None):
        if courses is None or len(courses) == 0:
            return ""

        if supplied_driver:
            driver = supplied_driver
        else:
            driver = self.driver

        course_input = driver.find_element(By.XPATH, value=self.course_input_box)
        for course in courses:
            course_input.send_keys(course)
            course_input.send_keys(Keys.ENTER)
            await asyncio.sleep(2)

        schedule_found = False
        while not schedule_found:
            await asyncio.sleep(1)
            # If a certain schedule is full, try the next ones
            current_idx = int(driver.find_element(By.XPATH, value=self.current_result).text)
            total_idx = int(driver.find_element(By.XPATH, value=self.results).text)

            while current_idx < total_idx:

                # Get the amount of seats left in the courses wanted. It's only when
                # there are no lectures/tutorials with zero places that the schedule
                # is valid.
                seats_left_list = driver.find_elements(By.CLASS_NAME, value=self.seats)
                leftnclear = driver.find_elements(By.CLASS_NAME, value="leftnclear")
                course_titles = driver.find_elements(By.CLASS_NAME, value="course_title")
                everything = []

                for i in leftnclear:
                    everything.append(i)
                    print(i.text)
                    size = i.location
                    h = size['y']
                    print(" - y = " + str(h))

                print()

                for i in course_titles:
                    everything.append(i)
                    print(i.text)
                    size = i.location
                    h = size['y']
                    print(" - y = " + str(h))

                everything.sort(key=lambda x: x.location['y'])

                for i in everything:
                    print(i.text)

                all_clear = True
                for idx, element in enumerate(seats_left_list):
                    if int(element.text) <= 0:
                        all_clear = False
                        break

                if all_clear:
                    if called_from_single_course_mode:
                        driver.save_screenshot(image_save_path + "cap" + str(call_order) + "_1.png")
                        driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.CONTROL, Keys.END)
                        driver.save_screenshot(image_save_path + "cap" + str(call_order) + "_2.png")
                    else:
                        driver.save_screenshot(image_save_path + "cap1.png")
                        driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.CONTROL, Keys.END)
                        driver.save_screenshot(image_save_path + "cap2.png")
                    return True

                driver.find_element(By.XPATH, value=self.right_arrow).click()
                await asyncio.sleep(1)
                current_idx = int(driver.find_element(By.XPATH, value=self.current_result).text)
                total_idx = int(driver.find_element(By.XPATH, value=self.results).text)

            # If a schedule is not found, try again in 15 minutes
            if not schedule_found:
                await asyncio.sleep(15 * 60)
                driver.refresh()
                await asyncio.sleep(1)
                driver.find_element(By.XPATH, value=self.back_to_start_arrow).click()
