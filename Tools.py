import json
import os
import random
import time
from selenium.webdriver.common.by import By
from settings import *
import requests
import urllib3.request

def create_account(driver, account_number):
    print("=============================")
    print("Creating account: " + str(account_number))

    driver.get(tempmail_url)

    email_field = driver.find_element(By.ID, "email-address")
    email = email_field.get_attribute("placeholder")
    print("generated email: " + email)

    # back to tsarvar
    tsarvar_register_data = {
        "meta": {},
        "act": {"user/register": {"email": email}}
    }
    request = requests.post(url=tsarvar_api_url, json=tsarvar_register_data)
    if not request.text.__contains__("success"):
        raise ValueError("error registering emaik: " + email)

    print("Confirmation mail sended !!")

    # account confirmation process
    print("waiting for confirmation mail...")
    wait_try = 0
    max_tries = 15
    mail_found = False

    while wait_try < max_tries:
        time.sleep(1)
        links_elements = driver.find_elements(By.TAG_NAME, "a")
        for a in links_elements:
            if a.get_attribute("href").__contains__("message/"):
                mail_content_url = a.get_attribute("href")
                print("email activation link: " + mail_content_url)
                driver.get(mail_content_url)
                mail_found = True
                break

        if mail_found:
            break
        else:
            wait_try += 1

    if not mail_found:
        raise ValueError("Can't find confirmation mail !!")

    print("confirming email...")
    activate_links_elements = driver.find_elements(By.TAG_NAME, "a")
    for a in activate_links_elements:
        if a.get_attribute("href").__contains__("tsarvar.com/en/auth"):
            activate_link = a.get_attribute("href")
            driver.get(activate_link)
            break
        if a == activate_links_elements[len(activate_links_elements) - 1]:
            raise ValueError("Can't find activation link")

    # done change account password
    driver.get(tsarvar_profile_url)
    pass_field = driver.find_element(By.NAME, "psw")
    pass_field2 = driver.find_element(By.NAME, "psw2")
    pass_field.send_keys(email)
    pass_field2.send_keys(email)

    btns = driver.find_elements(By.CSS_SELECTOR, ".buttonStyle")
    for btn in btns:
        if str(btn.text).lower().__contains__("change"):
            btn.click()
            break
        if btn == btns[len(btns) - 1]:
            raise ValueError("Can't change password")

    accounts_file = open("accounts.txt", "a", encoding="utf-8")
    accounts_file.write("\n" + email)
    accounts_file.close()
    print("account created !!")


def vote_server(likes):
    accounts_file = open("accounts.txt", "r", encoding="utf-8")
    accounts_file_content = accounts_file.readlines()

    for account in accounts_file_content:
        print("===============================")
        print("account: "+account)
        account=account.strip()

        try:
            email = account[:account.index(':')]
            password = account[account.index(':') + 1:]
        except:
            # email is the password
            email = account
            password = account
            pass


        login_data = {"meta": {}, "act": {"user/login": {"email": email, "psw": password}}}
        response = requests.post(url=tsarvar_api_url, json=login_data)
        cookies=response.cookies



        # change profile name
        names_file=open("names.txt","r",encoding="utf-8")
        names_content=names_file.readlines()
        random_name=names_content[random.randrange(0,len(names_content)-1)].strip()
        random_name2 = names_content[random.randrange(0, len(names_content) - 1)].strip()
        profile_data={"meta":{},"act":{"user/saveProfileData":{"firstName":random_name,"lastName":random_name2,"nickname":random_name+random_name2,"site":"","skype":"","discord":"","countryCode":random.randrange(0,100),"cityName":"","games":"","interests":"","music":""}}}
        response=requests.post(url=tsarvar_api_url,json=profile_data,cookies=cookies)
        if response.text.__contains__("success"):
            print("Profile updated !!")
        else:
            print("Profile update failed")

        # send like + favorite + join + review
        like_data={"meta":{},"act":{"server/addUserLikeServer":{"serverId":server_id}}}
        response=requests.post(url=tsarvar_api_url,json=like_data,cookies=cookies)
        if response.text.__contains__("success"):
            print("Like sent !!")
            liked=True
        else:
            print("Like failed")
            liked = False

        like_data={"meta":{},"act":{"server/addUserFavoriteServer":{"serverId":server_id}}}
        response=requests.post(url=tsarvar_api_url,json=like_data,cookies=cookies)
        if response.text.__contains__("success"):
            print("Favorite sent !!")
            favorited=True
        else:
            print("Favorite failed")
            favorited = False


        reviews_file=open("reviews.txt","r",encoding="utf-8")
        reviews_content=reviews_file.readlines()
        random_review=reviews_content[random.randrange(0,len(reviews_content)-1)].strip()
        join_data = {"meta": {}, "act": {"server/addMember": {"serverId": server_id, "nickname": random_review}}}
        response = requests.post(url=tsarvar_api_url, json=join_data, cookies=cookies)
        if response.text.__contains__("success"):
            print("Join sent !!")
            joined = True
        else:
            print("Join failed")
            joined = False

        """
        random_review = reviews_content[random.randrange(0,len(reviews_content) - 1)].strip()
        review_data = {"meta":{},"act":{"server/addReview":{"serverId":238341,"rate":random.randrange(0,4),"text":random_review}}}
        response = requests.post(url=tsarvar_api_url, json=review_data, cookies=cookies)
        if response.text.__contains__("success"):
            print("Review sent !!")
            reviewed = True
        else:
            print("Review failed")
            reviewed = False
        """
        # add to used accounts
        used_accounts_file=open("used_accounts.txt","a",encoding="utf-8")
        used_accounts_file.write("\n"+account)
        used_accounts_file.close()

    if liked or favorited or joined:
        likes+=1







def option1():
    created_accounts = 0
    accounts_num = int(input("How many accounts: "))
    for a in range(accounts_num):
        driver = WebDriver.SetupWebDriver(driver_options, "windows")

        try:
            create_account(driver, a + 1)
            created_accounts += 1

            if a + 1 % 10 == 0:
                cls()
        except Exception as error:
            print(error)
            pass


    print("created accounts: " + str(created_accounts) + " / " + str(accounts_num))


def option2():
    likes = 0
    try:
        vote_server(likes)
        print("likes given: " + str(likes))

        if likes % 10 == 0:
            cls()

        os.remove("accounts.txt")
    except:
        pass




def cls():
    os.system('cls' if os.name == 'nt' else 'clear')
