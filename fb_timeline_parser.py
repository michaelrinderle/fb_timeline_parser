import time
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
from google import google
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

TARGET = 'https://www.facebook.com/*'

def fb_login(browser):
    browser.get("http://www.facebook.com")
    email = browser.find_element_by_id("email")
    password = browser.find_element_by_id("pass")
    login   = browser.find_element_by_id("loginbutton")
    email.send_keys("*")
    password.send_keys("*")
    login.click()

def fb_logout(browser):
    logout = browser.find_element_by_id('userNavigationLabel')
    logout.click()
    time.sleep(1)
    signout = browser.find_element_by_partial_link_text('Log Out')
    signout.click()
    browser.close()

def fb_page_capture(browser, scrollCount):
    browser.get(TARGET)
    scrolls = scrollCount
    while True:
        scrolls -= 1
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(2)
        if scrolls < 0:
            break  
    return BeautifulSoup(browser.page_source, 'lxml')

def fb_parse_bg_posts(soup):
    bg_posts = []
    # get timeline
    timeline = soup.find('div', {'class': 'rq0escxv l9j0dhe7 du4w35lb d2edcug0 gile2uim buofh1pr g5gj957u hpfvmrgz aov4n071 oi9244e8 bi6gxh9e h676nmdw aghb5jc5'})
    # get post divs 
    for posts in timeline.find_all('div', {'class': 'du4w35lb k4urcfbm l9j0dhe7 sjgh65i0'}):
        try:
            # locate bg type posts in facebook obfuscated class names
            outerpost = posts.find('div', {'class': 'k4urcfbm kr520xx4 j9ispegn pmk7jnqg taijpn5t datstx6m cbu4d94t j83agx80 bp9cbjyn'})
            post = outerpost.find('div', {'class': 'kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x c1et5uql'}).text
            bg_posts.append(post)
        except:
            # couldnt find, passing
            continue
    return bg_posts

def fb_probability_bg_post(bg_posts):
    for bg_post in bg_posts:
        probability_score = 50
        link = ''
        link_description = ''
        results = google.search(bg_post, 2)
        for result in results:
            ratio = fuzz.ratio(bg_post, result.description)
            if ratio > probability_score:
                probability_score = ratio
                link = result.link
                link_description = result.description
    
        print(f'[{probability_score}]{bg_post[0:30]}')
        print(f'{link} \n{link_description[0:75]}')

def main():
    try:
        browser = webdriver.Firefox()
        fb_login(browser)       
        soup = fb_page_capture(browser, 3)
        bg_posts = fb_parse_bg_posts(soup)
        fb_logout(browser)
        fb_probability_bg_post(bg_posts)      
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
