
from bs4 import BeautifulSoup
import requests
import pandas as pd
import lxml



#function to extract all the jobs listed in a single page
def find_jobs_in_page(html_page):   #variable html_page cntains the html of a single page

    #Creating BeautifulSoup instance with lxml parsing method
    page_soup= BeautifulSoup(html_page, 'lxml') 

    #find all the 'li' html tags with 'clearfix job-bx wht-shd-bx' class
    jobs= page_soup.find_all('li', class_="clearfix job-bx wht-shd-bx" )

    return jobs



#function to extract job details of all the jobs in
def find_job_detail(jobs):

    #traversing through the html tree till we get the required information
    #header-tag > h2-tag > a-tag
    position= job.header.h2.a.text.strip()

    #using tags and classes to we required information
    company_name= job.find('h3', class_= "joblist-comp-name").text.strip()
    skills= job.find('span', class_= "srp-skills").text.strip().replace("  , ",",")
    published= job.find('span', class_= "sim-posted").text.strip()
    more_info= job.header.h2.a['href']

    #creating a dictionary which will be added as a row in our dataframe
    job_detail_dictionary= {'Position': position, 'CompanyName': company_name, 'Skills': skills, 'Published': published, 'MoreInfo': more_info}
    return job_detail_dictionary



#--Start--
if __name__=="__main__":

    df = pd.DataFrame(columns = ['Position', 'CompanyName', 'Skills', 'Published', 'MoreInfo'])


    # Enter the link here
    link= "https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=Data+Analyst&txtLocation=India"

    # we slice off the "sequence=1&startPage=1" part of the link as it changes with every page
    # for that we find the position of "sequence="
    pos= link.find('&sequence=')
    if pos!=-1: 
      link= link[:pos] 

    # Enter the number of pages to be scraped
    number_of_pages= 5



    #iterate through all the jobs and pages; and storing it in the dataframe
    for page_number in range(1,number_of_pages+1):

          #formula to calculate the start page number
          start_page_number= (page_number//10)*10 + 1

          #adding the sequence and startPage param of the link
          page_link= link+f"&sequence={page_number}&startPage={start_page_number}"

          #request for a html response of the given link
          html_page= requests.get(page_link).text

          #calling a function to find all the jobs listed in the current page
          jobs= find_jobs_in_page(html_page)

          #iterating through all the jobs returned by the find_jobs_in_page fuction
          for job in jobs:

                #calling a function that will extract the job details and return a dictionary
                job_details=  find_job_detail(job)

                #adding the job details to the dataframe
                df= df.append(job_details, ignore_index=True)


    df.to_csv("job_dataset.csv", sep='\t')
