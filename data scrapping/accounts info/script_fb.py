path = r'C:\Users\ends0\Downloads\chromedriver'
driver = webdriver.Chrome(path)
platform = "facebook"
brand_dict_reps = {"Samsung" : ["samsungus"],
                   "Apple" : ["apple"],
                 "Microsoft" : ["microsoft"],
                 "Amazon" : ["amazon"],
                 "Google" : ["google"]}
brand_dict_ft = {"Samsung" : ["5","87,689","+17%","RANK UNCHANGED"],
                "Apple" : ["1","482,215","+18%","RANK UNCHANGED"],
                 "Microsoft" : ["2","278,288","+32%","UP 1 PLACE"],
                 "Amazon" : ["3","274,819","+10%","DOWN 1 PLACE"],
                 "Google" : ["4","251,751","+28%","RANK UNCHANGED"]}
count = 0
brands = brand_dict_ft.keys()
for brand in brands:
    brand_growth = brand_dict_ft.get(brand)[2]
    rank_delta = brand_dict_ft.get(brand)[3]
    idx = brand_dict_ft.get(brand)[0]
    brand_value = brand_dict_ft.get(brand)[1]
    brands_reps = brand_dict_reps.get(brand)
    for brand_rep in brands_reps:
      url = f"https://socialblade.com/{platform}/page/{brand_rep}"
      print(url)
      driver.get(url)
      sleep(randint(1,15))
      html_soup = BeautifulSoup(driver.page_source, features='html.parser')
      posts_content = {"Ranking number" : idx, "Brand": brand, "Brand Value" : brand_value,"Platform" : platform, "Brand Representation" : brand_rep,"Brand Growth" : brand_growth, "Rank Change" : rank_delta}
      posts_top = html_soup.find_all('p', style= "color:#aaa; font-size: 10pt;")
      post_top_content = ''
      for post in posts_top:
          post_top_content = post_top_content + post.text
      post_top_content_split = post_top_content.split(" ")
      post_likes = post_top_content_split[1]
      post_tlkng = post_top_content_split[4]
      posts_left = html_soup.find('p', style= "font-size: 2.5em; font-weight: bold; color: #666; margin-top: -15px;")
      grade = posts_left.text
      posts_center = html_soup.find_all('p', style = 'font-size: 1.6em; color: #41a200; padding-top: 10px; font-weight: 600; margin-top: -15px;')
      tlkng_rank = posts_center[1].text
      likes_rank = posts_center[0].text
      post_content = {"Page Likes": post_likes,"Talking About This" : post_tlkng,"Grade" : grade,"Talking Rank" : tlkng_rank,"Likes Rank" : likes_rank}  
      posts_content.update(post_content)
      if (count == 0):
          results = pd.DataFrame(posts_content, index=[count])
          count = 1
      else:
          temp_results = pd.DataFrame(posts_content, index=[count])
          #print(temp_results.head())
          results = results.append(temp_results)
          count = count + 1
results.to_csv("./results_fb.csv")
