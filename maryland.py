# Import module
import time
import csv
import re
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller



# Input County Name
# Please input as given format : ALLEGANY COUNTY, ANNE ARUNDEL COUNTY, BALTIMORE CITY, BALTIMORE COUNTY, CALVERT COUNTY, CAROLINE COUNTY, CARROLL COUNTY, CECIL COUNTY, CHARLES COUNTY, DORCHESTER COUNTY, FREDERICK COUNTY, GARRETT COUNTY, HARFORD COUNTY, HOWARD COUNTY, KENT COUNTY, MONTGOMERY COUNTY, PRINCE GEORGE'S COUNTY, QUEEN ANNE'S COUNTY, ST. MARY'S COUNTY, SOMERSET COUNTY, TALBOT COUNTY, WASHINGTON COUNTY, WICOMICO COUNTY, WORCESTER COUNTY
county_name = 'CHARLES COUNTY'

# CSV File location and Name
csv_file_name = 'Test Input CSV.csv'

# Address Column Index - started from 0, 1, 2, 3, 4..
address_column_index = 3

# Output CSV File Name
output_filename = 'output.csv'


base_url = 'https://sdat.dat.maryland.gov/RealProperty/Pages/default.aspx'


# write csv File
def write_csv_headline(output_filename):
    header = ['First Name', 'Last Name', 'Street', 'City', 'Zip']
    with open(output_filename, 'w', encoding='utf-8', newline='') as csv_file:
        csv_write = csv.writer(csv_file)
        csv_write.writerow(header)


# write csv Data
def write_csv_data(output_filename, data_list):
    with open(output_filename, 'a', encoding='utf-8', newline='') as csv_file:
        csv_write = csv.writer(csv_file)
        csv_write.writerow(data_list)


# This Function will take csv_file name as input and output will be data
def read_input_csv(csv_file_name):
    print(f"STEP 01: Reading Input CSV - {csv_file_name}")
    with open(csv_file_name, encoding='utf-8') as file:
        csv_objects = csv.reader(file)
        
        rows = []
        for csv_object in csv_objects:
            rows.append(csv_object)

        csv_header = rows[0]
        csv_datas = rows[1:]
    return csv_datas


# extract all address from the CSV
def get_address(data_list, address_column_index):
    print('>>> Extracting address from CSV')
    rows =  [line[address_column_index] for line in data_list]
    
    return rows


# Replace all suffixes like (Avenue, Street, Lane, etc.)
def suffixes_replace(text):
    lower_text = text.lower()
    replace_texts = [' road', ' rd', ' highway', ' hwy', ' court', ' ct', ' street', ' st', ' avenue', ' ave', ' boulevard', ' blvd',
                     ' lane', ' ln', ' drive', ' dr', ' way', ' circle', ' cir', ' place', ' pl']
    for replace_text in replace_texts:
        if lower_text.endswith(replace_text):
            split_text = lower_text.rsplit(replace_text, 1)[0]
            if split_text.endswith('.'):
                split_text = split_text.rsplit(replace_text, 1)[0]
                
            return split_text
            
    return lower_text



# Browser define
def driver_define():
    print(f"STEP 02: Connecting Driver.")
    print('>>> Chromedriver Installing')
    driver_path = chromedriver_autoinstaller.install()
    
    print('>>> Chrome Browser Opening')
    options = Options()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    s = Service(driver_path)
    driver = webdriver.Chrome(service=s, options =options)
    driver.maximize_window()
    
    return driver



# Function will take county_name and prepare for search
def filter_apply(driver, base_url, county_name):
    driver.get(base_url) # Visiting Page
    time.sleep(0.2)

    # County Drp Select
    county_select_ele = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[id="cphMainContentArea_ucSearchType_wzrdRealPropertySearch_ucSearchType_ddlCounty"]')))
    county_select = Select(county_select_ele)
    county_select.select_by_visible_text(county_name) # select by visible County text
    time.sleep(0.2)


    # Search Method Select
    search_method_ele = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[id="cphMainContentArea_ucSearchType_wzrdRealPropertySearch_ucSearchType_ddlSearchType"]')))
    search_method = Select(search_method_ele)
    search_method.select_by_visible_text('STREET ADDRESS') # select by STREET ADDRESS text
    time.sleep(0.5)
    
    # Click on continue
    continue_ele = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[value="Continue"]')))
    #driver.execute_script("arguments[0].scrollIntoView();", continue_ele)
    #driver.execute_script("scrollBy(0,-100);")
    driver.execute_script("arguments[0].click();", continue_ele)
    #time.sleep(0.5)
    #continue_ele.click()

    # Wait until next page appears
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[id="cphMainContentArea_ucSearchType_wzrdRealPropertySearch_StartNavigationTemplateContainerID_btnContinue"]')))
    time.sleep(0.5)



# Performing searches
def searching(driver, address):
    print(f'Working at: {address}')

    s_number = address.split(' ')[0] # Street Number
    s_name = address.split(' ', 1)[-1] # Street Name

    # IF Street number is not available
    if not address[0].isnumeric():
        s_number = ''
        s_name = address

    s_name = suffixes_replace(s_name) # Suffix Replace

    try: filter_apply(driver, base_url, county_name) # Dropdown Apply
    except: filter_apply(driver, base_url, county_name) # Dropdown Apply
    print(f'>>> DropDown Filter was used.')

    # Submit Street Number 
    s_number_ele = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'cphMainContentArea_ucSearchType_wzrdRealPropertySearch_ucEnterData_txtStreenNumber')))
    s_number_ele.send_keys(s_number)

    # Submit Street Name
    s_name_ele = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'cphMainContentArea_ucSearchType_wzrdRealPropertySearch_ucEnterData_txtStreetName')))
    s_name_ele.send_keys(s_name)

    # Click On next
    next_ele = driver.find_element(By.CSS_SELECTOR, '[value="Next"]')
    driver.execute_script("arguments[0].click();", next_ele)
    #next_ele.click()

    print(f'>>> Searching...')


# Extract Data from the page & data write on csv
def extract_data(has_result, driver):

    if has_result:

        # multiple Names get
        page_name_ele = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[id^="cphMainContentArea_ucSearchType_wzrdRealPropertySearch_ucDetailsSearch_dlstDetaisSearch_lblOwnerName"]')))
        page_name_ele_text = [line.text for line in page_name_ele]
        page_names = [line for line in page_name_ele_text if len(line)!=0]
        
        # Analysis Name if have &
        if len(page_names) == 1:
            single_page_name = page_names[0].replace(' and ', ' & ')
            single_page_name_list = single_page_name.split(' & ')
            if len(single_page_name_list) == 2:
                if len(single_page_name_list[0].split(' ')) > 1 and len(single_page_name_list[1].split(' ')) > 1: # Both list have first & last name
                    page_names = single_page_name_list
                if len(single_page_name_list[0].split(' ')) > 1 and len(single_page_name_list[1].split(' ')) == 1: # First list have both name & secound list have only first name
                    last_list_fullname = f"{single_page_name_list[0].split(' ')[0]} {single_page_name_list[1]}"
                    page_names = [single_page_name_list[0], last_list_fullname]
        #loop over multiple name
        for page_name in page_names:

            try:
                first_name = page_name.split(' ')[1]
                last_name = page_name.split(' ')[0]
            except:
                #print(traceback.format_exc())
                first_name = page_name
                last_name = ''
                
            print(f"first_name: {first_name}")
            print(f"last_name: {last_name}")
            
            # Address
            try:
                page_address_ele = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'cphMainContentArea_ucSearchType_wzrdRealPropertySearch_ucDetailsSearch_dlstDetaisSearch_lblPremisesAddress_0')))
                page_address = page_address_ele.text
            except:
                #print(traceback.format_exc())
                page_address = ''

            try:
                output_address = re.match(r"(.*?)\n", page_address).group(1)
            except:
                #print(traceback.format_exc())
                output_address = page_address
            print(f"output_address: {output_address}")

            try:
                city_name = page_address.split('\n')[-1].rsplit(' ', 1)[0]
            except:
                #print(traceback.format_exc())
                city_name = ""
            print(f"city_name: {city_name}")

            try:
                zip_code = page_address.split(' ')[-1].split('-')[0]
            except:
                #print(traceback.format_exc())
                zip_code = ""
            print(f"zip_code: {zip_code}")

            data_list = [first_name, last_name, output_address, city_name, zip_code] # list to write

            write_csv_data(output_filename, data_list) # Data write



write_csv_headline(output_filename) # Write output csv file
csv_datas = read_input_csv(csv_file_name) # CSV Read
addresses = get_address(csv_datas, address_column_index) # Get Address
driver = driver_define() # Driver Open


for address in addresses:
#     address = '18072 CYPRESS DR'
    try:
        searching(driver, address) # Performing searches

        # Checking if result found
        result = WebDriverWait(driver, 8).until(EC.presence_of_element_located((By.XPATH, '//*[text()="Owner Name:" or contains(text(), "There are no records that match") or @id="cphMainContentArea_ucSearchType_wzrdRealPropertySearch_ucSearchResult_gv_SearchResult_lnkDetails_0"]'))).text
        if 'Owner Name' in result:
            has_result = True
        else:
            has_result = False
            print('>>> No result found')

        extract_data(has_result, driver) # Data Extract and write on CSV
    except:
        print(traceback.format_exc())

driver.quit() # Driver close
