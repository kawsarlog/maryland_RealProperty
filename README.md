# Maryland Real Property Data Extraction

[![Python Version](https://img.shields.io/badge/python-3.9.7-blue.svg)](https://www.python.org/downloads/release/python-397/)
[![Selenium Version](https://img.shields.io/badge/selenium-4.9.0-green.svg)](https://pypi.org/project/selenium/4.9.0/)
[![chromedriver-autoinstaller Version](https://img.shields.io/badge/chromedriver--autoinstaller-0.4.0-orange.svg)](https://pypi.org/project/chromedriver-autoinstaller/0.4.0/)

This Python script allows you to extract real property data from the Maryland State Department of Assessments and Taxation (SDAT) website. It uses Selenium, chromedriver-autoinstaller, and other modules to automate the process.

## Requirements

- [Python 3.9.7](https://www.python.org/downloads/release/python-397/)
- [Selenium 4.9.0](https://pypi.org/project/selenium/4.9.0/)
- [chromedriver-autoinstaller 0.4.0](https://pypi.org/project/chromedriver-autoinstaller/0.4.0/)

#### Python Installation
Install the right Python version from https://www.python.org/downloads/
![make Sure to Enable this option](https://img001.prntscr.com/file/img001/TN-mbdzyTxqvq0Tjozh9YQ.jpeg)

## Installation

1. Clone the repository:

   ```shell
   git clone https://github.com/kawsarlog/maryland_RealProperty.git
   ```
2. Navigate to the project directory:

  ```shell
  cd maryland_RealProperty
  ```
3. Install the required dependencies:

  ```shell
  pip install selenium==4.9.0
  pip install chromedriver-autoinstaller==0.4.0
  ```


#Run the script:

  ```shell
  python maryland.py
  ```
The script will read the input CSV file, extract the real property data from the Maryland SDAT website, and write the output to a CSV file.

Contact
For any questions or inquiries, please contact:

- Email: kawsar@kawsarlog.com
- Website: http://kawsarlog.com/
- GitHub: https://github.com/kawsarlog/maryland_RealProperty
