#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 10 10:11:34 2021

@author: houping
"""

import os
import re
import csv
import time
import json
import random
import requests
import pandas as pd
import numpy as np

from datetime import date, timedelta, datetime

from bs4 import BeautifulSoup
import selenium
from selenium import webdriver

def sign_in():
    url = 'https://www.glassdoor.com/profile/login_input.htm'
    browser.get(url)

    email_field = browser.find_element_by_name('username')
    password_field = browser.find_element_by_name('password')
    submit_btn = browser.find_element_by_xpath('//button[@type="submit"]')

    with open('credentials.json') as f:
        d = json.loads(f.read())
        username = d['glassdoor'][0]['username']
        password = d['glassdoor'][0]['password']

    email_field.send_keys(username)
    password_field.send_keys(password)
    submit_btn.click()

    time.sleep(1)

def scrape_overview(browser, save_path, overviewUrl):
    browser.get(overviewUrl)
    # overview section
    overview = {}
    reviews = browser.find_element_by_id('EIOverviewContainer')
    # overview = reviews.find_elements_by_class_name('align-items-center')
    
    #website
    try: 
        overview['website'] = reviews.find_element_by_xpath(".//a[@data-test='employer-website']").text
    except Exception:
        pass
    # headquarters
    try:
        overview['headquarters'] = reviews.find_element_by_xpath(".//div[@data-test='employer-headquarters']").text
    except Exception:
        pass
    # size
    try:
        overview['size'] = reviews.find_element_by_xpath(".//div[@data-test='employer-size']").text
    except Exception:
        pass
    # funded
    try:
        overview['funded'] = reviews.find_element_by_xpath(".//div[@data-test='employer-founded']").text
    except Exception:
        pass
    # type
    try:
        overview['ctype'] = reviews.find_element_by_xpath(".//div[@data-test='employer-type']").text
    except Exception:
        pass
    # industry
    try:
        overview['industry'] = reviews.find_element_by_xpath(".//div[@data-test='employer-industry']").text
    except Exception:
        pass
    # revenue
    try:
        overview['revenue'] = reviews.find_element_by_xpath(".//div[@data-test='employer-revenue']").text
    except Exception:
        pass
    # description
    try:
        reviews.find_element_by_xpath(".//span[@data-test='employerDescription']/button").click()
    except Exception:
        pass
    try:
        overview['description'] = reviews.find_element_by_xpath(".//span[@data-test='employerDescription']").text
    except Exception:
        pass
    # affiliated companies
    # employerHierarchies = reviews.find_element_by_xpath("//div[@data-test='employerHierarchies']")
    try:
        employerHierarchiesUrl = reviews.find_element_by_xpath("//div[@data-test='employerHierarchies']/a").get_attribute('href')
        browser.get(employerHierarchiesUrl)
        affiliatedCompanies = browser.find_elements_by_xpath("//a[@data-test='companyInfositeLink']")
        affiliatedAll = {}
        for i in range(len(affiliatedCompanies)):
            a = affiliatedCompanies[i]
            affiliated = {}
            affiliated['url'] = a.get_attribute('href')
            affiliated['companyName'] = a.find_element_by_xpath(".//h3[@data-test='employerName']").text
            affiliated['companyRating'] = a.find_element_by_xpath(".//p[@data-test='companyRating']").text
            affiliated['companyLocation'] = a.find_element_by_xpath(".//p[@data-test='companyLocation']").text
            affiliated['reviewsCount'] = a.find_element_by_xpath(".//p[@data-test='reviewsCount']").text
            affiliated['jobsCount'] = a.find_element_by_xpath(".//p[@data-test='jobsCount']").text
            affiliated['salariesCount'] = a.find_element_by_xpath(".//p[@data-test='salariesCount']").text
            
            affiliatedAll[i] = affiliated
        overview['affiliated'] = affiliatedAll
    except Exception:
        pass
    
    with open(os.path.join(save_path,'overview.json'), 'w') as outfile:
        json.dump(overview, outfile, indent=4)
    

    

def scrape_review(reviewsUrl,browser,save_path):
    def more_pages():
        time.sleep(random.uniform(3,5))
        try:
            footer = browser.find_element_by_class_name('paginationFooter').text
            a = footer.split(' ')
            if (int(a[3]) > int(a[5].replace(",", "").split('.00')[0]) - 9):
                return False
            else:
                return True
        except Exception:
            return False
        
    def last_page():
        try:
            footer = browser.find_element_by_class_name('paginationFooter').text
            a = footer.split(' ')
            if (int(a[3]) >= int(a[5].replace(",", "").split('.00')[0])):
                return True
            else:
                return False
        except Exception:
            return True
    
    def scrape_date(review):
        try:
            date = review.find_element_by_tag_name('time').get_attribute('datetime')
        except Exception:
            date = np.nan
        return date
    
    def scrape_helpful(review):
        try:
            s = review.find_element_by_class_name('helpfulReviews').text.strip('""')
            res = s[s.find("(") + 1:s.find(")")]
        except Exception:
            res = 0
        return res
    
    def scrape_review_title(review):
        try:
            title = review.find_element_by_xpath(".//a[@class='reviewLink']").text
        except Exception:
            title = np.nan
        return title
    
    def scrape_rating(review):
        subRating = {}
        try:
            subRating['Overall'] = review.find_element_by_xpath(".//span[@class='rating']/span").get_attribute('title')
        except Exception:
            pass
        try:
            subratingSection = review.find_elements_by_xpath(".//ul[@class='undecorated']/li")
            for sub in subratingSection:
                rating = sub.find_element_by_class_name('gdBars').get_attribute('title')
                name = sub.find_element_by_tag_name('div').get_attribute("textContent")
                subRating[name] = rating
        except Exception:
            pass
        return subRating
    
    def scrape_employee_status_title(review):
        try:
            employee = review.find_element_by_class_name('authorJobTitle').text
            title = employee.split('-')[1].strip()
            status = employee.split('-')[0].strip()
        except Exception:
            title = np.nan
            status = np.nan
        return status,title
    
    def scrape_location(review):
        try:
            location = review.find_element_by_class_name('authorLocation').text
        except Exception:
            location = np.nan
        return location
    
    def scrape_recommendation(review):
        recommendation = {}
        try:
            recommendationList = review.find_elements_by_xpath(".//div[@class='row reviewBodyCell recommends']/div")
            for rr in recommendationList:
                text = rr.text
                if 'Recommend' in text:
                    recommendation['Recommend']=text
                elif 'Outlook' in text:
                    recommendation['Outlook'] = text
                elif 'CEO' in text:
                    recommendation['CEO'] = text
                else:
                    pass
        except Exception:
            pass
        return recommendation
    
    def scrape_employee_years(review):
        try:
            years = review.find_element_by_class_name('mainText').text.strip('"')
        except Exception:
            years = np.nan
        return years
    
    def scrape_pros_cons_advice(review):
        try:
            expand = review.find_element_by_xpath(".//div[contains(text(),'Continue reading')]").click()
        except Exception:
            pass
        try:
            pros = review.find_element_by_xpath(".//span[@data-test='pros']").text
        except Exception:
            pros = np.nan
        try:
            cons = review.find_element_by_xpath(".//span[@data-test='cons']").text
        except Exception:
            cons = np.nan
        try:
            advice = review.find_element_by_xpath(".//span[@data-test='advice-management']").text
        except Exception:
            advice = np.nan
        return pros,cons,advice
        n = np.nan
        try:
            con = review.find_element_by_class_name('common__EiReviewDetailsStyle__socialHelpfulcontainer').text
            if 'person' in con:
                n = int(con.split(' ')[0])
        except Exception:
            pass
        return n
    
    def scrape_rating_broder(review):
        subRating = {}
        try:
            subRating['Overall'] = review.find_element_by_class_name('ratingNumber').text
        except Exception:
            pass
        try:
            subratingSection = review.find_elements_by_xpath(".//div[@class='content']//li")
            for sub in subratingSection:
                name = sub.find_element_by_xpath("div").get_attribute("textContent")
                subRating[name] = ratingReference[sub.find_element_by_xpath("div/following-sibling::div").get_attribute('class')]
        except Exception:
            pass
        return subRating
    
    def scrape_employee_status_experience_broder(review):
        try:
            se = review.find_element_by_xpath("div/div/div/div/span").text.split(',')
            status = se[0].strip()
            experience = se[1].strip()
        except Exception:
            status = np.nan
            experience = np.nan
        return status,experience
    
    def scrape_review_title_broder(review):
        try:
            title = review.find_element_by_xpath(".//a[@class='reviewLink']").text
        except Exception:
            title = np.nan
        return title
    
    def scrape_date_employee_title_broder(review):
        try:
            info = review.find_element_by_class_name('authorInfo').text.split('-')
            date = info[0].strip()
            title = info[1].strip()
        except Exception:
            date = np.nan
            title = np.nan
        return date,title
    
    def scrape_location_broder(review):
        try:
            location = review.find_element_by_class_name('authorLocation').text
        except Exception:
            location = np.nan
        return location
    
    def scrape_recommendation_broder(review):
        rec = {}
        try:
            recList = review.find_element_by_class_name('recommends').find_elements_by_xpath("div")
            for r in recList:
                score = recomList[r.find_element_by_xpath('span').get_attribute('class')]
                name = r.find_element_by_xpath('span/following-sibling::span').text.strip()
                rec[name] = score
        except Exception:
            pass
        return rec
      
    def scrape_pros_cons_advice_broder(review):
        try:
            expand = review.find_element_by_xpath(".//div[contains(text(),'Continue reading')]").click()
        except Exception:
            pass
        try:
            pros = review.find_element_by_xpath(".//span[@data-test='pros']").text
        except Exception:
            pros = np.nan
        try:
            cons = review.find_element_by_xpath(".//span[@data-test='cons']").text
        except Exception:
            cons = np.nan
        try:
            advice = review.find_element_by_xpath(".//span[@data-test='advice-management']").text
        except Exception:
            advice = np.nan
        return pros,cons,advice
    
    def scrape_helpful_broder(review):
        n = 0
        try:
            con = review.find_element_by_class_name('common__EiReviewDetailsStyle__socialHelpfulcontainer').text
            if 'person' in con:
                n = int(con.split(' ')[0])
        except Exception:
            pass
        return n
    
    def scrape_review_one_page(reviews,j,reviewsAll):
        for i in range(len(reviews)):
            r = reviews[i]
            review = {}
            if 'noBorder' not in r.get_attribute('class'):
                review['date'] = scrape_date(r)
                review['helpful'] = scrape_helpful(r)
                review['review_title'] = scrape_review_title(r)
                review['rating'] = scrape_rating(r)
                review['employee_status'],review['employee_title'] = scrape_employee_status_title(r)
                review['location'] = scrape_location(r)
                review['recommendation'] = scrape_recommendation(r)
                review['pro'],review['con'],review['advice'] = scrape_pros_cons_advice(r)
            else:
                review['rating'] = scrape_rating_broder(r)
                review['status'],review['experience'] = scrape_employee_status_experience_broder(r)
                review['review_title'] = scrape_review_title_broder(r)
                review['date'],review['employee_title'] = scrape_date_employee_title_broder(r)
                review['location'] = scrape_location_broder(r)
                review['recommendation'] = scrape_recommendation_broder(r)
                review['pro'],review['con'],review['advice'] = scrape_pros_cons_advice_broder(r)
                review['helpful'] = scrape_helpful_broder(r)
            
            reviewsAll[i+(j-1)*10] = review
    
        return reviewsAll
        
    reviewsAll = {}
    noFinished = True
    j = 1
    
    browser.get(reviewsUrl)
    
    while noFinished:
        if j % 50 == 0:
            print(len(reviewsAll))
            with open(os.path.join(save_path,'reviews_'+str(j)+'.json'), 'w') as outfile:
                json.dump(reviewsAll, outfile, indent=4)
            reviewsAll={}
            time.sleep(random.uniform(5,10))
        else:
            time.sleep(random.uniform(1,2))
        reviews = browser.find_elements_by_class_name('empReview')
        reviewsAll = scrape_review_one_page(reviews,j,reviewsAll)
        
        j += 1
        nextPage = reviewsUrl.split('.htm')[0]+ '_P'+str(j)+'.htm?filter.iso3Language=eng'
        browser.get(nextPage)
        
        time.sleep(random.uniform(2,3))
        
        if last_page():
            noFinished = False
            reviews = browser.find_elements_by_class_name('empReview')
            reviewsAll = scrape_review_one_page(reviews,j,reviewsAll)
            with open(os.path.join(save_path,'reviews_'+str(j)+'.json'), 'w') as outfile:
                json.dump(reviewsAll, outfile, indent=4)
            break
    

if __name__ == '__main__':
    ratingReference = {}
    ratingReference['css-152xdkl'] = 1
    ratingReference['css-19o85uz'] = 2
    ratingReference['css-1ihykkv'] = 3
    ratingReference['css-1c07csa'] = 4
    ratingReference['css-1dc0bv4'] = 5
    recomList = {}
    recomList['SVGInline css-10xv9lv d-flex'] = np.nan
    recomList['SVGInline css-hcqxoa d-flex'] = 1
    recomList['SVGInline css-1kiw93k d-flex'] = -1
    recomList['SVGInline css-1h93d4v d-flex'] = 0
    # browser = webdriver.Chrome()
    browser = webdriver.Chrome(executable_path = 'E:\Houping\glassdoor\chromedriver_win32\chromedriver')
    sign_in()
    
    allURL = pd.read_csv('E:\Houping\glassdoor\data\company_url_updated3.csv')
    done_list = pd.read_csv('E:\Houping\glassdoor\data\done_list.csv')
    cik = done_list.cik.tolist()
    # url = 'https://www.glassdoor.com/Overview/Working-at-ADC-Telecommunications-EI_IE1075.11,33.htm'
    # url = 'https://www.glassdoor.com/Overview/Working-at-American-Airlines-EI_IE8.11,28.htm'
    allURL = allURL[116:]
    for index,rows in allURL.iterrows():
        if rows['cik'] not in cik:
            url = rows['url']
            name = rows['conm']
            print(url)
            browser.get(url)
            time.sleep(random.uniform(1.5,2))
            path = 'E:\Houping\glassdoor\data'
            # name = 'AAL'
            save_path = os.path.join(path,name)
            try:
                os.stat(save_path)
            except:
                os.mkdir(save_path)
            
            try:
                overviewUrl = browser.find_element_by_xpath("//a[@data-label='Overview']").get_attribute('href')
            except Exception:
                overviewUrl = browser.find_element_by_xpath("//a[@data-selector='orgStructureCompanyOverviewOption']").get_attribute('href')
            
            scrape_overview(browser, save_path, overviewUrl)
        
            reviewsUrl = browser.find_element_by_xpath("//a[@data-label='Reviews']").get_attribute('href')
        
            scrape_review(reviewsUrl,browser,save_path)
            
            cik.append(rows['cik'])

    
    
    
    
























