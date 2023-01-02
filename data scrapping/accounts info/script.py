from requests import get 
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
from random import randint
import pandas as pd

path = r'C:\Users\ends0\Downloads\chromedriver'
driver = webdriver.Chrome(path)
platform = "twitter"
brand_dict_reps = {"Samsung" : ["SamsungMobile","Samsung"],
             "Amazon" : ["amazon","alexa99"]}
brand_dict_ft = {"Samsung" : ["5","87,689","+17%","RANK UNCHANGED"],
             "Amazon" : ["3","274,819","+10%","DOWN 1 PLACE"]}
brands = brand_dict_ft.keys()
count = 0
for brand in brands:
    brand_growth = brand_dict_ft.get(brand)[2]
    rank_delta = brand_dict_ft.get(brand)[3]
    idx = brand_dict_ft.get(brand)[0]
    brand_value = brand_dict_ft.get(brand)[1]
    brands_reps = brand_dict_reps.get(brand)
    for brand_rep in brands_reps:
      url = f"https://socialblade.com/{platform}/user/{brand_rep}"
      print(url)
      driver.get(url)
      sleep(randint(1,15))
      html_soup = BeautifulSoup(driver.page_source, features='html.parser')
      posts_content = {"Ranking number" : idx, "Brand": brand, "Brand Value" : brand_value,"Platform" : platform, "Brand Representation" : brand_rep,"Brand Growth" : brand_growth, "Rank Change" : rank_delta}
      posts_top = html_soup.find_all('div', class_= "YouTubeUserTopInfo")
      post_top_content = ''
      for post in posts_top:
        post_top_content = post_top_content + post.text
      post_top_content_split = post_top_content.splitlines(False)
      post_top_content_split = [word for word in post_top_content_split if word!=""]
      followers = post_top_content_split[1]
      following = post_top_content_split[3]
      likes = post_top_content_split[5]
      posts = post_top_content_split[7]
      date = post_top_content_split[9]
      post_top_content_ = {"Followers" : followers, "Following" : following, "Likes" : likes, "Date created" : date, "Posts" : posts}
      posts_content.update(post_top_content_)
      acc_ranks = html_soup.find_all('div', style="float: left; width: 900px; height: 150px;")
      acc_rank_content = ""
      for acc_rank in acc_ranks:
          acc_rank_content = acc_rank_content + acc_rank.text
      acc_rank_content_split = acc_rank_content.splitlines(False)
      acc_rank_content_split = [word for word in acc_rank_content_split if word!=""]
      acc_rank_grade = acc_rank_content_split[1].strip()
      acc_rank_followers = acc_rank_content_split[4]
      acc_rank_following = acc_rank_content_split[6]
      acc_rank_posts = acc_rank_content_split[8]  
      post_rank_content = {"Account Grade" : acc_rank_grade, "Followers Rank" : acc_rank_followers, "Following Rank" : acc_rank_following, "Posts Rank" : acc_rank_posts}
      posts_content.update(post_rank_content)
      posts_left = html_soup.find('div', style="width: 280px; height: 80px; float: left; background: #fff; padding: 10px; margin-right: 10px; border-bottom: 2px solid #e2e2e2; text-align: center;").text
      posts_left_splitted  = posts_left.splitlines(False)
      delta_followers = posts_left_splitted[2].strip()
      posts_center = html_soup.find('div', style = "width: 270px; height: 80px; float: left; background: #fff; padding: 10px; margin-right: 10px; border-bottom: 2px solid #e2e2e2; text-align: center;").text
      posts_center_splitted  = posts_left.splitlines(False)
      delta_following = posts_center_splitted[2].strip() 
      posts_right = html_soup.find('div', style = "width: 270px; height: 80px; float: left; background: #fff; padding: 10px; border-bottom: 2px solid #e2e2e2; text-align: center;").text
      posts_right_splitted  = posts_right.splitlines(False)
      delta_posts = posts_right_splitted[2].strip()
      post_delta_content = {"Followers 30 Days" : delta_followers, "Following 30 Days" : delta_following, "Posts 30 Days" : delta_posts}
      posts_content.update(post_delta_content)
      #print(posts_content)
      if (count == 0):
          results = pd.DataFrame(posts_content, index=[count])
          count = 1
      else:
          temp_results = pd.DataFrame(posts_content, index=[count])
          #print(temp_results.head())
          results = results.append(temp_results)
          count = count + 1
results.to_csv("./results.csv")
