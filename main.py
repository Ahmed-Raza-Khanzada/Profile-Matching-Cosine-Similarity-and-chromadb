import pandas as pd
from match import get_Scores_Cosine, get_Matched
from utils import deduplicate_tuple
from pdf_converter import make_html_pdf
from utils import clean_text
import time
import shutil
import pdfkit
from utils import documentSimilarity,get_profile_Data4Semantic
import os
import threading
from my_call_serp import serach_serp
from my_site_scraper import  scrape_first_paragraph_and_linkedin
from html_contetss import my_html,my_blur_html,my_peoplecard
from LLM import LLM_MAtching
from my_unique_file import make_unique_file
import re
def check_None(text):
    if text == None or text == "None":
        return ""
    if type(text)==list:
        return ' '.join(text)
    return text

def make_pdfs(k,options):
    print(""*20,"Inside threading",""*20)
    for file_no,html_file in enumerate(k):
        print(html_file.split('/')[-1][:-4]+".pdf")
        pdfkit.from_file(k[file_no], f"pdfs/{html_file.split('/')[-1][:-4]}.pdf", options=options)
def get_name(facebook,linkedin,insta,data):
    if linkedin.get("firstName") and linkedin.get("lastName"): 
        name = linkedin["firstName"]+" "+linkedin["lastName"]
    elif linkedin.get("firstName") : 
        name = linkedin["firstName"]
    elif linkedin.get("lastName"):
        name = linkedin["lastName"]
    elif facebook.get("username"):
        name = facebook["username"]
    elif insta.get("fullName"):
        name = insta["fullName"]
    else  :
        name = data['data']['profile_name'].replace(" ","_")
    return name
    
def short_url(url1):
    for i in [".com",".in",".org",".co",".net",".edu",".gov",]:
        if i in url1 :
            if url1[url1.index(i)-3:url1.index(i)]!="www":
                new_url = url1.split(i)[0]
                # print(new_url,"***********")
                if "www." in new_url:
                    return new_url.split("www.")[-1]
                else:
                    return new_url
    return url1[:25]
   

def remove_redudancy(array_of_dicts):
    if array_of_dicts==None or array_of_dicts==[]:
        return None
    seen = set()
    new_l = []
    for d in array_of_dicts:
        t = list(d.values())
        t = [str(x) if not isinstance(x, str) else x for x in t]
        t = str(t)
        if t not in seen:
            seen.add(t)
            new_l.append(d)
        
    return new_l



def make_split(input_string):
    # Use regular expression to split the string into characters and numbers
    matches = re.match(r"([a-zA-Z]+)([0-9]+)", input_string)

    if matches:
        characters_part = matches.group(1)
        numbers_part = matches.group(2)
        return characters_part,int( numbers_part)
    else:
        print("No match found.")

def make_match_data(clusters,linkedinData,facebookData,instaData):
    l = []
    linkedin = None
    facebook = None
    insta = None
    twitter = None
    linkedin_idx = None
    facebook_idx = None
    insta_idx = None
    twitter_idx = None
    k = []
    for i in clusters:
        k.append((make_split(i[1:-1])))
    # print(k)
    for i in k:

        if i[0]=='linkedin':
            linkedin = linkedinData[i[1]]
            linkedin_idx = i[1]
        if i[0]=='insta':
            insta = instaData[i[1]]
            insta_idx= i[1]
        if i[0]=='facebook':
            facebook = facebookData[i[1]]
            facebook_idx = i[1]
        if i[0]=='twitter':
            twitter = twitter[i[1]]
            twitter_idx = i[1]
    return linkedin,facebook,insta,twitter,linkedin_idx,facebook_idx,insta_idx,twitter_idx
        

def re_create_data_recursion(linkedin,facebook,insta,linkedin_indices1,facebook_indices1,insta_indices1,profile_name1,city1):
        data = {
        "data": {
            "profile_name": profile_name1,
            "profile_city": city1,
            "instagram": None,
            "facebook": None,
            "linkedin": None
        }
            }
        linkedin_new = []
        facebook_new = []
        insta_new = []
        old_indixes = [linkedin_indices1,facebook_indices1,insta_indices1]
        for my_idx, socials_data in enumerate([linkedin,facebook,insta]):
            if socials_data!=None:
                for i in range(len(socials_data)):
                    if i not in old_indixes[my_idx]:
                        if my_idx==0:
                            linkedin_new.append(linkedin[i])
                        elif my_idx==1:
                            facebook_new.append(facebook[i])
                        elif my_idx==2:
                            insta_new.append(insta[i])
        if len(linkedin_new)>0:
            data["data"]["linkedin"] = linkedin_new
        if len(facebook_new)>0:
            data["data"]["facebook"] = facebook_new
        if len(insta_new)>0:
            data["data"]["instagram"] = insta_new
        return data
               




def Get_Profile_clusters(data,use_LM=False,recursive_redaduncy=False):
    
    instaData = None
    facebookData = None
    linkedinData = None
    twitterData = None
    # print(d)
    print("-"*80)
    print(f"Profile {data['data']['profile_name']} is Starts Processing from Search city: {data['data']['profile_city']}")
    print("-"*80)
    
    if "instagram" in  data["data"].keys():
        instaData = data["data"]["instagram"]
        if instaData and not recursive_redaduncy:
            print("Insta before length : ",len(instaData))
            instaData = remove_redudancy(instaData)
            print("After length instaData: ",len(instaData))
            data["data"]["instagram"] = instaData
    if "facebook" in  data["data"].keys():
        facebookData = data["data"]["facebook"]
        if facebookData and not recursive_redaduncy:
            print("Facebook before length : ",len(facebookData))
            facebookData = remove_redudancy(facebookData)
            print("After length facebookData: ",len(facebookData))
            data["data"]["facebook"] = facebookData
    if "linkedin" in  data["data"].keys():
        linkedinData = data["data"]["linkedin"]
        if linkedinData and not recursive_redaduncy:
            print("Linkedin before length : ",len(linkedinData))
            linkedinData = remove_redudancy(linkedinData)
            print("After Length linkedinData: ",len(linkedinData))
            data["data"]["linkedin"] = linkedinData
        
    if "twitter" in  data["data"].keys():
      twitterData = data["data"]["twitter"]
   
    
   

    response_data = []
    # # print("Output Matched Profiles using Cosine")
    if linkedinData!=None and facebookData!=None and instaData!=None:
        if use_LM:
            
            insta_prof_data = get_profile_Data4Semantic(data["data"]["instagram"],['username',
            'fullName',
            'biography','businessCategory','link'])
            linkedin_prof_data = get_profile_Data4Semantic(data["data"]["linkedin"],['image',
            'firstName',
            'lastName',
            'location',
            'about',
            'biography',
            'work',
            'education',
            'link',])
            facebook_prof_data = get_profile_Data4Semantic(data["data"]["facebook"],['username',
            'bio',
            'education',
            'work',
            'hometown',
            'Address',
            'current_city',
            'category',
            'Email',
            'Gender',
            'Birth_year',
            'Languages',
            'Instagram',
            'Website',
            'link',])
            df = LLM_MAtching(linkedin_prof_data=linkedin_prof_data, facebook_prof_data=facebook_prof_data,insta_prof_data = insta_prof_data)
            # print(len(df))
            # print(df,"****************************&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
            
            df3 = get_Matched(df,reversed=True)
            df3['Positions'] = df3['Positions'].astype(str).str.strip('()')
            df3[['Position1','Position2', 'Position3']] = df3['Positions'].str.split(', ', expand=True)
            
        else:
            d = get_Scores_Cosine(prof_name=data["data"]["profile_name"],facebookData=facebookData,linkedinData=linkedinData,instaData=instaData)
            
            final_df1  =get_Matched(d)
            
            # d = get_Scores_Cosine(prof_name=data["data"]["profile_name"],linkedinData=linkedinData,instaData=instaData)
            
            # final_df2  =get_Matched(d)
            final_df1['Positions'] = final_df1['Positions'].astype(str).str.strip('()')

            final_df1[['Position1', 'Position2','Position3']] = final_df1['Positions'].str.split(', ', expand=True)
            final_df1 = final_df1.iloc[:,1:]
            df3 = final_df1

        
    elif linkedinData!=None and facebookData!=None:
        if use_LM:
           
            linkedin_prof_data = get_profile_Data4Semantic(data["data"]["linkedin"],['image',
            'firstName',
            'lastName',
            'location',
            'about',
            'biography',
            'work',
            'education',
            'link',])
            facebook_prof_data = get_profile_Data4Semantic(data["data"]["facebook"],['username',
            'bio',
            'education',
            'work',
            'hometown',
            'Address',
            'current_city',
            'category',
            'Email',
            'Gender',
            'Birth_year',
            'Languages',
            'Instagram',
            'Website',
            'link',])
            df = LLM_MAtching(linkedin_prof_data=linkedin_prof_data ,facebook_prof_data=facebook_prof_data)
            print(len(df))
            df3 = get_Matched(df,reversed=True)
            df3['Positions'] = df3['Positions'].astype(str).str.strip('()')
            df3[['Position1','Position3']] = df3['Positions'].str.split(', ', expand=True)
            
        else:
            d = get_Scores_Cosine(prof_name=data["data"]["profile_name"],facebookData=facebookData,linkedinData=linkedinData)
        
            final_df2 =get_Matched(d)
            # print(final_df2)
            final_df2['Positions'] = final_df2['Positions'].astype(str).str.strip('()')
            final_df2[['Position1', 'Position3']] = final_df2['Positions'].str.split(', ', expand=True)
            df3 = final_df2
    elif linkedinData!=None and instaData!=None:
        if use_LM:
            insta_prof_data = get_profile_Data4Semantic(data["data"]["instagram"],['username',
            'fullName',
            'biography','businessCategory','link'])
            linkedin_prof_data = get_profile_Data4Semantic(data["data"]["linkedin"],['image',
            'firstName',
            'lastName',
            'location',
            'about',
            'biography',
            'work',
            'education',
            'link',])
            df = LLM_MAtching(linkedin_prof_data=linkedin_prof_data ,insta_prof_data= insta_prof_data)
            print(len(df))
            df3 = get_Matched(df,reversed=True)
            df3['Positions'] = df3['Positions'].astype(str).str.strip('()')
            df3[['Position1','Position3']] = df3['Positions'].str.split(', ', expand=True)
            
        else:
            d = get_Scores_Cosine(prof_name=data["data"]["profile_name"],linkedinData=linkedinData,instaData=instaData)
            final_df2  =get_Matched(d)
            final_df2['Positions'] = final_df2['Positions'].astype(str).str.strip('()')
            final_df2[['Position1', 'Position3']] = final_df2['Positions'].str.split(', ', expand=True)
            df3 = final_df2
    elif facebookData!=None and instaData!=None:
        if use_LM:
            insta_prof_data = get_profile_Data4Semantic(data["data"]["instagram"],['username',
            'fullName',
            'biography','businessCategory','link'])
            facebook_prof_data = get_profile_Data4Semantic(data["data"]["facebook"],['username',
            'bio',
            'education',
            'work',
            'hometown',
            'Address',
            'current_city',
            'category',
            'Email',
            'Gender',
            'Birth_year',
            'Languages',
            'Instagram',
            'Website',
            'link',])
            df = LLM_MAtching(facebook_prof_data=facebook_prof_data ,insta_prof_data= insta_prof_data)
            print(len(df))
            df3 = get_Matched(df,reversed=True)
            df3['Positions'] = df3['Positions'].astype(str).str.strip('()')
            df3[['Position1','Position3']] = df3['Positions'].str.split(', ', expand=True)
            
        else:
            d = get_Scores_Cosine(prof_name=data["data"]["profile_name"],facebookData=facebookData,instaData=instaData)
            final_df2  =get_Matched(d)
            final_df2['Positions'] = final_df2['Positions'].astype(str).str.strip('()')
            final_df2[['Position1', 'Position3']] = final_df2['Positions'].str.split(', ', expand=True)
            df3 = final_df2
    
    print("*"*30,data["data"]["profile_name"],"*"*30)
    print(df3)
    
    websites_links,snippets,search_images,my_people_data = serach_serp(data["data"]["profile_name"],data["data"]["profile_city"])
    if my_people_data!={} and my_people_data["bio"]!=None and my_people_data["bio"]!="":
        post_images1 = ""
        prof_images1 = ""
       
        if my_people_data.get("post_images")!=None:
            for image_link in my_people_data["post_images"]:
                post_images11= f'''<img alt="profileImage" class="profileImage" width="190" height="190"
                        src="{image_link}" />
                    '''
                
                post_images1 += post_images11
        if  my_people_data.get("profile_images")!=None:
            prof_images1 +=f"""<img src='{my_people_data['profile_images']}'
                alt="Profile Image">"""
        if my_people_data.get("websites")!=None:
            websites1 = []
            for m in my_people_data["websites"]:
                if m!=None or m!="":
                    # print(len(my_people_data["websites"]))
                    websites1.append(m)
            if len(websites1)>0:
                websites1 = "\n".join(websites1)
        else:
            websites1 = None
        print("............................................................................................")
        print(f"Famous Persponality Found with name {data['data']['profile_name']} Making People Card")
        print("............................................................................................")
        # print("<<<<<<<<<<<<<<<",my_people_data["post_images"],">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
      
        html_people_card = my_peoplecard(my_people_data,websites=websites1,post_images=post_images1,profile_images=prof_images1)
        pdf_file_name  = make_unique_file()

        make_html_pdf(pdf_file_name,html_content=html_people_card,main_path="pdfs")
        make_html_pdf(pdf_file_name,html_content=html_people_card,main_path="blur_pdfs2")
        my_save_pdf =data['data']['profile_name'].replace(" ","_")
        response_data.append({"post_images": my_people_data.get("post_images"),"websites":websites1,"website_data":None,"facebooklink":my_people_data.get("face_link"),"instalink":my_people_data.get("insta_link"),"linkedinlink":my_people_data.get("linkedin_link"),"name": my_save_pdf , "bio": my_people_data.get("bio"), "work": my_people_data.get("work"), "main_image": my_people_data.get("profile_images"), "pdf_path": "pdfs/"+pdf_file_name+".pdf", "Blured_pdf_path": f"blur_pdfs2/{pdf_file_name}.pdf"})
    # my_snippets =[]
    t_websites = []
    linkedin_indices = []
    insta_indices = []
    facebook_indices = []
    # twitter_indices = []
    if facebookData!=None and instaData!=None and linkedinData!=None:
        for poss,cluster in enumerate(zip(df3["Position1"],df3["Position2"],df3["Position3"])):
            print(poss,"--------------")
           
            linkedin,facebook,insta,twitter,linkedin_idx,facebook_idx,insta_idx,twitter_idx  =make_match_data(cluster,linkedinData,facebookData,instaData)
        
            prof_name = data["data"]["profile_name"]
            if facebook !=None:
                facebook_indices.append(facebook_idx)
                if facebook.get("username"):
                    prof_name = facebook["username"] 
               
            if insta !=None:
                insta_indices.append(insta_idx)
                if insta.get("fullName"):
                    prof_name = insta["fullName"]
                
            if linkedin !=None:
                if linkedin.get("firstName") and linkedin.get("lastName"): 
                    prof_name = linkedin["firstName"]+" "+linkedin["lastName"]
                elif linkedin.get("firstName") :
                    prof_name = linkedin["firstName"]
               
                linkedin_indices.append(linkedin_idx)
              

            post_images = ""
            if insta!=None:
                for image_link in insta["postImages"]:
                    post_image= f'''<img alt="profileImage" class="profileImage" width="190" height="190"
                            src="{image_link}" />
                        '''
                    post_images += post_image
                namess = prof_name.split(" ")
               
                for post_link in search_images:
                    go_add = False
                    names_in_post = []
                    for namee in namess:
                        if len(namee)==2:
                            if namee[0].lower() in post_link.lower() and namee[1]==".":
                                names_in_post.append(namee)
                        elif namee.lower() in post_link.lower():
                            names_in_post.append(namee)
                    if len(names_in_post)==len(namess):
                        go_add = True
                    if go_add:
                         post_image= f'''<img alt="profileImage" class="profileImage" width="190" height="190"
                            src="{post_link}" />
                        '''
                         post_images += post_image
            

            if linkedin== {} or linkedin== None:
                linkedin  = {}
                linkedin["image"] = ""
                linkedin["biography"] = ""
                linkedin["work"] = ""
                linkedin["link"] = ""
                linkedin["about"] = ""
            if insta== {} or insta == None:
                insta = {}
                insta["image"] = ""
                insta["biography"] = ""
                insta["work"] = ""
                insta["link"] = ""
            if facebook== {} or facebook == None:
                facebook = {}
                facebook["image"] = ""
                facebook["bio"] = ""
                facebook["work"] = ""
                facebook["link"] = ""
                facebook["education"] = ""
            if twitter == {} or twitter== None:
                twitter = {}
                twitter["image"] = ""
                twitter["biography"] = ""
                twitter["work"] = ""
                twitter["link"] = ""
            if facebook.get("image") == None:
                facebook["image"] = ""
                # facebookData["link"] = ""
            if facebook.get("hometown") ==None:
                facebook["hometown"] = ""
            if insta.get("work") == None:
                insta["work"] = ""
            websites = ""
          
        
            my_sites = {}
            for website1,snippet1 in zip(websites_links,snippets):
                if website1 in t_websites:
                    continue
                try:
                    first_para,lines,linkedin_link=scrape_first_paragraph_and_linkedin(website1)
                except:
                    first_para,lines,linkedin_link = None,None,None
                if linkedin_link!=None and linkedin["link"]!=None and linkedin["link"]!="" and linkedin["link"]!=" ":
                    if linkedin["link"].strip().lower() ==linkedin_link.strip().lower() and website1 not in t_websites:
                        t_websites.append(website1)
                        my_sites[website1] = (0,snippet1)
                        if lines:
                            if linkedin.get("seacrh_image")==None:
                                linkedin["search_image"] = search_images[0]
                            linkedin["website_data"] = lines
                        else:
                            if first_para:
                                if linkedin.get("seacrh_image")==None:
                                    linkedin["search_image"] = search_images[0]
                                linkedin["website_data"] = first_para
                        continue
            if my_sites=={}:
                for website1,snippet1 in zip(websites_links,snippets):
                    if website1 in t_websites:
                        continue
                    
                    myscore = 0
                    for name11 in prof_name.split(" "):
                        if len(name11)==2:
                            if name11[0].lower() in website1.lower() and name11[1]==".":
                                myscore +=1
                        elif name11.lower() in website1.lower():
                            myscore +=1
                    
                    # if myscore>0:
                    #     t_score = myscore/len(prof_name.split(" "))
                    #     if (float(1-t_score)==0.0 or float(1-t_score)<=0.1) and website1 not in t_websites:
                    #                 t_websites.append(website1)
                    #                 my_sites[website1] = (1-t_score,snippet1)
                    #                 continue
                    if linkedin["about"] !=None and linkedin["about"] !="" and linkedin["about"]!=" ": 
                        my_sites[website1] = (documentSimilarity(website1+"\n"+snippet1,prof_name+"\n"+check_None(linkedin["about"])+"\n"+check_None(linkedin.get("biography"))+"\n"+check_None(facebook.get("bio"))+"\n"+check_None(insta.get("biography"))),snippet1)

                        t_websites.append(website1)
                    else:
                        my_sites[website1] = (documentSimilarity(website1+"\n"+snippet1,prof_name ),snippet1)
                        t_websites.append(website1)
            sorted_data = sorted(my_sites.items(), key=lambda x: x[1][0])
            if len(sorted_data)>3:  
                for web_link in sorted_data[:3]:
                    website =f'''<a href="{web_link[0]}">{short_url(web_link[0])}</a><br/>'''
                    websites += website
            else:
                for web_link in sorted_data:
                    website =f'''<a href="{web_link[0]}">{short_url(web_link[0])}</a><br/>'''
                    websites += website

            profile_images = ""
           
            score_image = 0
            
            for socials in [linkedin,facebook,insta,twitter]:
                if socials.get("image")==None or socials.get("image")=="" or socials.get("image")==" ":
                    score_image +=1
            if score_image>2:
                
                for socials in [linkedin,facebook,insta,twitter]:
                    if (socials.get("image")==None or socials.get("image")=="" or socials.get("image")==" ") and (linkedin.get("search_image")!=None) :
                        socials["image"] = linkedin["search_image"]
                        break
            if  insta.get("image") != None  and  insta.get("image") != "" and  insta.get("image") != " ":
                profile_images +=f"""<img src='{insta['image']}'
                    alt="Profile Image">"""
            if  facebook.get("image") != None and  facebook.get("image") != "" and  facebook.get("image") != " ":
                profile_images +=f"""<img src='{facebook['image']}'
                    alt="Profile Image">"""
            if  linkedin.get("image") != None and  linkedin.get("image") != "" and  linkedin.get("image") != " ":
                profile_images += f"""<img src='{linkedin['image']}'
                    alt="Profile Image">"""
            if  twitter.get("image") != None and  twitter.get("image") != "" and  twitter.get("image") != " ":
                
                profile_images += f"""<img src='{twitter['image']}'
                    alt="Profile Image">"""
            if twitter.get("image")==None and linkedin.get("image")==None and facebook.get("image")==None and insta.get("image")==None and profile_images=="":
                for pos,i in enumerate(search_images):
                    profile_images += f"""<img src='{i}'
                    alt="Profile Image">"""
                    if pos==3:
                        break
            elif facebook.get("image")==None and insta.get("image")==None :
                for pos,i in enumerate(search_images):
                    profile_images += f"""<img src='{i}'
                    alt="Profile Image">"""
                    break
            elif facebook.get("image")==None and linkedin.get("image")==None :
                for pos,i in enumerate(search_images):
                    profile_images += f"""<img src='{i}'
                    alt="Profile Image">"""
                    break
            elif linkedin.get("image")==None and insta.get("image")==None :
                for pos,i in enumerate(search_images):
                    profile_images += f"""<img src='{i}'
                    alt="Profile Image">"""
                    break
            if  linkedin.get("website_data")!=None :
                
                twitter["biography"] = linkedin["website_data"]
       
            if linkedin.get("image")!=None and linkedin.get("image")!="" and linkedin.get("image")!=" ":
                main_image = linkedin.get("image")
            elif insta.get("image")!=None and insta.get("image")!="" and insta.get("image")!=" ":
                main_image = insta.get("image")
            elif facebook.get("image")!=None and facebook.get("image")!="" and facebook.get("image")!=" ":
                main_image = facebook.get("image")
            elif twitter.get("image")!=None and twitter.get("image")!="" and twitter.get("image")!=" ":
                main_image = twitter.get("image")
            else:
                if len(search_images)>0:
                    main_image = search_images[0]
                else:
                    main_image = None
            

            html_content = my_html(insta,facebook,linkedin,twitter,websites=websites,post_images=post_images,profile_images=profile_images)
            html_content_blur = my_blur_html(insta,facebook,linkedin,twitter,websites=websites,post_images=post_images,profile_images=profile_images)
          
            my_save_pdf =get_name(facebook,linkedin,insta,data)
            pdf_file_name = make_unique_file()
            # pdf_blur_file_name = make_unique_file()
            
            make_html_pdf(pdf_file_name,html_content=html_content,main_path="pdfs")
            make_html_pdf(pdf_file_name,html_content=html_content_blur,main_path="blur_pdfs2")

            Bio = check_None( facebook.get("bio"))+check_None(insta.get("biography"))+check_None(linkedin.get("biography"))+check_None(linkedin.get("about"))+check_None(facebook.get("education"))
            work = check_None( facebook.get("work"))+check_None(insta.get("work"))+check_None(linkedin.get("work"))
           
            response_data.append({"post_images":insta.get("postImages"),"websites":sorted_data,"website_data":linkedin.get("website_data"),"facebooklink":facebook.get("link"),"instalink":insta.get("link"),"linkedinlink":linkedin.get("link"),"name": my_save_pdf, "bio": Bio, "work": work, "main_image": main_image, "pdf_path": "pdfs/"+pdf_file_name+".pdf", "Blured_pdf_path": f"blur_pdfs2/{pdf_file_name}.pdf"})
            print("Data Added for Response")
    else:
            
        for poss,cluster in enumerate(zip(df3["Position1"],df3["Position3"])):
            print(poss,"--------------")
            
            linkedin,facebook,insta,twitter,linkedin_idx,facebook_idx,insta_idx,twitter_idx  =make_match_data(cluster,linkedinData,facebookData,instaData)
            prof_name = data["data"]["profile_name"]
            if facebook !=None:
                facebook_indices.append(facebook_idx)
                if facebook.get("username"):
                    prof_name = facebook["username"] 
               
            if insta !=None:
                insta_indices.append(insta_idx)
                if insta.get("fullName"):
                    prof_name = insta["fullName"]
                
            if linkedin !=None:
                if linkedin.get("firstName") and linkedin.get("lastName"): 
                    prof_name = linkedin["firstName"]+" "+linkedin["lastName"]
                elif linkedin.get("firstName") :
                    prof_name = linkedin["firstName"]
               
                linkedin_indices.append(linkedin_idx)
                
            post_images = ""
            if insta!=None:
                for image_link in insta["postImages"]:
                    post_image= f'''<img alt="profileImage" class="profileImage" width="190" height="190"
                            src="{image_link}" />
                        '''
                    post_images += post_image    
                namess = prof_name.split(" ")
               
                for post_link in search_images:
                    go_add = False
                    names_in_post = []
                    for namee in namess:
                        if len(namee)==2:
                            if namee[0].lower() in post_link.lower() and namee[1]==".":
                                names_in_post.append(namee)
                        elif namee.lower() in post_link.lower():
                            names_in_post.append(namee)
                    
                    if len(names_in_post)==len(namess):
                        go_add = True
                    if go_add:
                         post_image= f'''<img alt="profileImage" class="profileImage" width="190" height="190"
                            src="{post_link}" />
                        '''
                         post_images += post_image
           

            if linkedin== {} or linkedin== None:
                linkedin = {}
                linkedin["image"] = ""
                linkedin["biography"] = ""
                linkedin["work"] = ""
                linkedin["link"] = ""
                linkedin["about"] = ""
            if insta== {} or insta == None:
                insta = {}
                insta["image"] = ""
                insta["biography"] = ""
                insta["work"] = ""
                insta["link"] = ""
            if facebook== {} or facebook == None:
                facebook = {}
                facebook["image"] = ""
                facebook["bio"] = ""
                facebook["work"] = ""
                facebook["link"] = ""
                facebook["education"] = ""
            if twitter == {} or twitter== None:
                twitter = {}
                twitter["image"] = ""
                twitter["biography"] = ""
                twitter["work"] = ""
                twitter["link"] = ""
            if facebook.get("image") == None:
                facebook["image"] = ""
                # facebookData["link"] = ""
            if facebook.get("hometown") ==None:
                facebook["hometown"] = ""
            if insta.get("work") == None:
                insta["work"] = ""
            websites = ""
       
        
            my_sites = {}
            for website1,snippet1 in zip(websites_links,snippets):
                if website1 in t_websites:
                    continue
                try:
                    first_para,lines,linkedin_link=scrape_first_paragraph_and_linkedin(website1)
                except:
                    first_para,lines,linkedin_link = None,None,None
                if linkedin_link!=None and linkedin["link"]!=None :
                    if linkedin_link.strip().lower()[-1]=="/":
                        linkedin_link = linkedin_link.strip().lower()[:-1]
                    if linkedin["link"].strip().lower() ==linkedin_link.strip().lower() and website1 not in t_websites:
                        t_websites.append(website1)
                        my_sites[website1] = (0,snippet1)
                        if lines:
                            
                            linkedin["website_data"] = lines
                            if linkedin.get("seacrh_image")==None:
                                linkedin["search_image"] = search_images[0]
                        else:
                            if first_para:
                                linkedin["website_data"] = first_para
                                if linkedin.get("seacrh_image")==None:
                                    linkedin["search_image"] = search_images[0]
                        continue
            if my_sites=={}:
                for website1,snippet1 in zip(websites_links,snippets):
                    if website1 in t_websites:
                        continue
                    
                    myscore = 0
                    for name11 in prof_name.split(" "):
                        if len(name11)==2:
                            if name11[0].lower() in website1.lower() and name11[1]==".":
                                myscore +=1
                        elif name11.lower() in website1.lower():
                            myscore +=1
                    
                    # if myscore>0:
                    #     t_score = myscore/len(prof_name.split(" "))
                    #     if (float(1-t_score)==0.0 or float(1-t_score)<=0.1) and website1 not in t_websites:
                    #                 t_websites.append(website1)
                    #                 my_sites[website1] = (1-t_score,snippet1)
                    #                 continue
                    
                    if linkedin["about"] !=None and linkedin["about"] !="" and linkedin["about"]!=" ": 
                        my_sites[website1] = (documentSimilarity(website1+"\n"+snippet1,prof_name+"\n"+check_None(linkedin["about"])+"\n"+check_None(linkedin.get("biography"))+"\n"+check_None(facebook.get("bio"))+"\n"+check_None(insta.get("biography"))),snippet1)
                        t_websites.append(website1)
                    
                    else:
                        my_sites[website1] = (documentSimilarity(website1+"\n"+snippet1,prof_name ),snippet1)
                        t_websites.append(website1)
            sorted_data = sorted(my_sites.items(), key=lambda x: x[1][0])

            if len(sorted_data)>3:
                for web_link in sorted_data[:3]:
                    website =f'''<a href="{web_link[0]}">{short_url(web_link[0])}</a><br/>'''
                    websites += website
            else:
                for web_link in sorted_data:
                    website =f'''<a href="{web_link[0]}">{short_url(web_link[0])}</a><br/>'''
                    websites += website
            score_image = 0
            for socials in [linkedin,facebook,insta,twitter]:
                if socials.get("image")==None or socials.get("image")=="" or socials.get("image")==" ":
                    score_image +=1
            

            if score_image>2:
                for socials in [linkedin,facebook,insta,twitter]:
                    if (socials.get("image")==None or socials.get("image")=="" or socials.get("image")==" " )and (linkedin.get("search_image")!=None):
                        socials["image"] = linkedin["search_image"]
                        break
            profile_images = ""
            if  insta.get("image") != None  and  insta.get("image") != "" and  insta.get("image") != " ":
                profile_images +=f"""<img src='{insta['image']}'
                    alt="Profile Image">"""
            if  facebook.get("image") != None and  facebook.get("image") != "" and  facebook.get("image") != " ":
                profile_images +=f"""<img src='{facebook['image']}'
                    alt="Profile Image">"""
            if  linkedin.get("image") != None and  linkedin.get("image") != "" and  linkedin.get("image") != " ":
                profile_images += f"""<img src='{linkedin['image']}'
                    alt="Profile Image">"""
            if  twitter.get("image") != None and  twitter.get("image") != "" and  twitter.get("image") != " ":
                profile_images += f"""<img src='{twitter['image']}'
                    alt="Profile Image">"""
            if twitter.get("image")==None and linkedin.get("image")==None and facebook.get("image")==None and insta.get("image")==None and profile_images=="":
                for pos,i in enumerate(search_images):
                    profile_images += f"""<img src='{i}'
                    alt="Profile Image">"""
                    if pos==3:
                        break
            elif facebook.get("image")==None and insta.get("image")==None :
                for pos,i in enumerate(search_images):
                    profile_images += f"""<img src='{i}'
                    alt="Profile Image">"""
                    break
            elif facebook.get("image")==None and linkedin.get("image")==None :
                for pos,i in enumerate(search_images):
                    profile_images += f"""<img src='{i}'
                    alt="Profile Image">"""
                    break
            elif linkedin.get("image")==None and insta.get("image")==None :
                for pos,i in enumerate(search_images):
                    profile_images += f"""<img src='{i}'
                    alt="Profile Image">"""
                    break
            if  linkedin.get("website_data")!=None :
                twitter["biography"] = linkedin["website_data"]

            
            if linkedin.get("image")!=None and linkedin.get("image")!="" and linkedin.get("image")!=" ":
                main_image = linkedin.get("image")
            elif insta.get("image")!=None and insta.get("image")!="" and insta.get("image")!=" ":
                main_image = insta.get("image")
            elif facebook.get("image")!=None and facebook.get("image")!="" and facebook.get("image")!=" ":
                main_image = facebook.get("image")
            elif twitter.get("image")!=None and twitter.get("image")!="" and twitter.get("image")!=" ":
                main_image = twitter.get("image")
            else:
                if len(search_images)>0:
                    main_image = search_images[0]
                else:
                    main_image = None
            
            
            html_content = my_html(insta,facebook,linkedin,twitter,websites=websites,post_images=post_images,profile_images=profile_images)
            html_content_blur = my_blur_html(insta,facebook,linkedin,twitter,websites=websites,post_images=post_images,profile_images=profile_images)
          
            my_save_pdf =get_name(facebook,linkedin,insta,data)
            pdf_file_name = make_unique_file()
            # pdf_blur_file_name = make_unique_file()
            make_html_pdf(pdf_file_name,html_content=html_content,main_path="pdfs")
            make_html_pdf(pdf_file_name,html_content=html_content_blur,main_path="blur_pdfs2")
     
            Bio = check_None( facebook.get("bio"))+check_None(insta.get("biography"))+check_None(linkedin.get("biography"))+check_None(linkedin.get("about"))+check_None(facebook.get("education"))
            work = check_None( facebook.get("work"))+check_None(insta.get("work"))+check_None(linkedin.get("work"))
            
            response_data.append({"post_images":insta.get("postImages"),"websites":sorted_data,"website_data":linkedin.get("website_data"),"facebooklink":facebook.get("link"),"instalink":insta.get("link"),"linkedinlink":linkedin.get("link"),"name": my_save_pdf, "bio": Bio, "work": work, "main_image": main_image, "pdf_path": "pdfs/"+pdf_file_name+".pdf", "Blured_pdf_path": f"blur_pdfs2/{pdf_file_name}.pdf"})

            print("Data Added for Response")
    # try:
    data = re_create_data_recursion(linkedinData,facebookData,instaData,linkedin_indices,facebook_indices,insta_indices,data['data']['profile_name'],data['data']['profile_city'])
    if (data["data"]["linkedin"]!=None and data["data"]["facebook"]!=None ) or (data["data"]["linkedin"]!=None and data["data"]["instagram"]!=None ) or (data["data"]["facebook"]!=None and data["data"]["instagram"]!=None ):
        recusrsive_response_data =  Get_Profile_clusters(data,use_LM=use_LM,recursive_redaduncy=True)
        if recusrsive_response_data !=None: 
            response_data.extend(recusrsive_response_data)
    # except Exception as e:
    #     print("Error in Recrusion",e)
    try:
        print("*"*20)
        print(f"Pdf Generated : pdfs/{my_save_pdf}.pdf")
        print("*"*20)
    except Exception as e:
        print(f"Error {e}")
        print(data["data"]["profile_name"])
        print(df3)
    return response_data