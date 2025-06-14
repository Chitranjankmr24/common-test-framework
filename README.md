### UI and API Automation using Python, Selenium, and requests module
This is the UI and API Automation framework using python, selenium and pytest and it is a data driven framework where page object model is the design pattern.
## Pre-requisites:
- Install Python 3.7 and up
    - for required packages read [requirements.txt](https://github.com/Chitranjankmr24/rr-qa-automation-assignment/blob/main/requirements.txt)
    and for installation run this command on terminal: 
    ```bash
    pip install -r requirements.txt
    ```
- Google Chrome
- Firefox
- Edge

## Understanding folder structure:
### Structure of framework:

* config.ini : is the configuration file that contains the details of tenant, username, password, browser type, headless or headed execution and har collection   
* conftest.py : is the starting point of framework execution  
* test cases are created under the tests folder  
* test data files are store under resourses/data file name  
* Core functionalities like selenium wrapper methods, json utilities, logs, base locators are under helper folder  
* page object action methods are there under pages folder  
* locators are available under locators folder  
* html report will be store in report folder  
* logs will be there in logs folder with timestamp  
* screenshots will be there in screenshot folder with the name of failed test case 
* Vedio files will be store in screenrecorder folder with the name of test cases 

## How to Run the Framework

### How to run all the tests in this repo
pytest -vv -rA  -n  <no. of browser>  
it will run the all the tests in project in parallel mode where n is the no. of instance of the browser  

pytest -vv -rA  
it will run the all the tests in project in sequential mode  

### How to run 1 test- After a relative test module path add 2 colons and the test name:
pytest -vv -rA tests/feature_file_name::name of test case
### How to run one feature file all tests
pytest -vv -rA tests/feature_file_name.py
### How to run all tests
pytest -vv -rA tests

### Run test with marker
pytest -vv -rA -m "UI"

## Jenkins Run
 You can choose the application url and one specific feature

## Execution Report:  

![image](https://user-images.githubusercontent.com/105901438/170267501-e5f575da-d6d5-43b6-ad85-12040201a167.png)

## Slack Report: 

![image](https://user-images.githubusercontent.com/105901438/170272528-4b17bb74-5c87-4c2b-9fe1-42999f8bc704.png)


### Defects:
1.	SSN, phone number and Pin code is field is not strict to number only
2.	Able to transfer more amount than balance amount
3.	Update details not reflecting in username
