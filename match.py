import pandas as pd
from utils import documentSimilarity

# import chromadb
# client = chromadb.Client()
import pandas as pd


def get_Scores_Cosine( 
    instaData = None,
    facebookData = None,
    linkedinData = None,prof_name=" "):
    
    # if "instagram" in  d.keys():
    #   instaData = d["instagram"]
    # if "facebook" in  d.keys():
    #   facebookData = d["facebook"]
    # if "linkedin" in  d.keys():
    #   linkedindata = d["linkedin"]
    def check_type(ele):
      if ele==None:
        return None
      if ele=="None":
         return None
      if type(ele) == list:
        if ele==[]:
           return " " 
        return " ".join(ele)
      ele_Str = ""
      for i in ele:
         if i.isalnum():
            ele_Str +=i
      if ele_Str=="":
         return None
      elif type(ele)==str:
        return ele
      
      
    df = {"Positions":[],"Scores":[]}
    f_entities = ["bio","current_city", "Birth_year","Email","hometown","Address","education","work","Website"]
    link_entities = ["education","work","biography"]
    penalty = 1.58
    name = ""
    
    if linkedinData and facebookData and instaData:
      for pos,i in enumerate(linkedinData):
          for pos2,v in enumerate(facebookData):
                                 
                None1 = ["Painter based in the city of Leiden\nAll paintings are for sale\nContact: guido.marsman@gmail.com"]
                for pos3,k in enumerate(instaData):
                #   myscore1 = 0
                
                #   for name11 in prof_name.split(" "):
                #       # if name11.lower()=="sharuiq" :
                #       print("????????????????????????????????????????????????????????????????????????????????????????????????????")
                #       print(prof_name.split(" "),instaData[pos3]["fullName"].lower())
                #       for my_pos,my_insta_name in enumerate(instaData[pos3]["fullName"].lower().split(" ")):
                #         if name11.lower() in instaData[pos3]["fullName"].lower() or  instaData[pos3]["fullName"].lower().split(" ")[my_pos] == name11.lower() :
                #             myscore1 +=1
                #   if myscore1==0:
                #       continue
                  if  k["biography"] in None1:
                    continue
                  scores = []
                  for link_entity in i.keys():
                    if i[link_entity]!=None and link_entity in link_entities:
                      if link_entity == "biography":
                          # print( link_entity,"*******************" ,v)
                          # if check_type(i[link_entity])==None or check_type(v["bio"])==None:
                          #     # print(f" faebook{pos2} bio == {check_type(v['bio']) }  ")
                          #     # df["Positions"].append(("linkedin"+str(pos),"facebook"+str(pos2)))
                          #     # df["Scores"].append(penalty)
                          #     scores.append(penalty)
                          #     continue
                          my_score = 0
                          link_bio = True
                          insta_bio = True
                          facebook_bio = True
                          if check_type(i[link_entity])==None :
                            my_score += penalty
                            link_bio = False
                          if check_type(v["bio"])==None :
                            my_score += penalty
                            facebook_bio = False
                          if check_type(k["biography"])==None :
                            my_score += penalty
                            insta_bio = False
                          if link_bio and insta_bio:
                            # print(check_type(i[link_entity]),"------",check_type(k["biography"]),"???????????????????????????????????????????")
                            score = documentSimilarity(check_type(i[link_entity]),check_type(k["biography"]))
                            my_score += score
                          if link_bio and facebook_bio:
                            score = documentSimilarity(check_type(i[link_entity]),check_type(v["bio"]))
                            my_score += score

                          if insta_bio and facebook_bio:
                            score = documentSimilarity(check_type(k["biography"]),check_type(v["bio"]))
                            my_score += score
                          
                            
                          # print(check_type(i[link_entity]),"&&&&&",check_type(v["bio"]),"******************************")
                          # score = documentSimilarity(check_type(i[link_entity]),check_type(v["bio"]))
                          # df["Positions"].append(("linkedin"+str(pos),"facebook"+str(pos2)))
                          # df["Scores"].append(score)
                          scores.append(my_score)
                      elif link_entity == "education":
                        
                          if check_type(i[link_entity])==None or check_type(v["education"])==None:
                              # print(f" faebook{pos2} education == {check_type(v['education']) }  ")
                              # df["Positions"].append(("linkedin"+str(pos),"facebook"+str(pos2)))
                              # df["Scores"].append(penalty)
                              scores.append(penalty)
                              continue
                        
                          score = documentSimilarity(check_type(i[link_entity]),check_type(v["education"]))
                          # df["Positions"].append(("linkedin"+str(pos),"facebook"+str(pos2)))
                          # df["Scores"].append(score)
                          scores.append(score)
                      elif link_entity == "work":
                        
                          if check_type(i[link_entity])==None or check_type(v["work"])==None:
                              # print(f" faebook{pos2} work == {check_type(v['work']) }  ")
                              # df["Positions"].append(("linkedin"+str(pos),"facebook"+str(pos2)))
                              # df["Scores"].append(penalty)
                              scores.append(penalty)
                              continue
                          if v["work"] ==[]:
                              # print(f" faebook{pos2} work == {check_type(v['work']) }  ")
                              # df["Positions"].append(("linkedin"+str(pos),"facebook"+str(pos2)))
                              # df["Scores"].append(penalty)
                              scores.append(penalty)
                              continue
                          score = documentSimilarity(check_type(i[link_entity]),check_type(v["work"]))
                          # df["Positions"].append(("linkedin"+str(pos),"facebook"+str(pos2)))
                          # df["Scores"].append(score)
                          scores.append(score)
                          
                      
                  df["Positions"].append(("linkedin"+str(pos),"facebook"+str(pos2),"insta"+str(pos3)))
                  df["Scores"].append(sum(scores))
                  name = "linkedin-"+"facebook-"+"insta"
             
                
    elif linkedinData and facebookData:
      for pos,i in enumerate(linkedinData):
          for pos2,v in enumerate(facebookData):
              
                scores = []
                
                for link_entity in i.keys():
                  if i[link_entity]!=None and link_entity in link_entities:
                    if link_entity == "biography":
                        # print( link_entity,"*******************" ,v)
                        if check_type(i[link_entity])==None or check_type(v["bio"])==None:
                            # print(f" faebook{pos2} bio == {check_type(v['bio']) }  ")
                            # df["Positions"].append(("linkedin"+str(pos),"facebook"+str(pos2)))
                            # df["Scores"].append(penalty)
                            scores.append(penalty)
                            continue
                        # print(check_type(i[link_entity]),"&&&&&",check_type(v["bio"]),"******************************")
                        score = documentSimilarity(check_type(i[link_entity]),check_type(v["bio"]))
                        # df["Positions"].append(("linkedin"+str(pos),"facebook"+str(pos2)))
                        # df["Scores"].append(score)
                        scores.append(score)
                    elif link_entity == "education":
                       
                        if check_type(i[link_entity])==None or check_type(v["education"])==None:
                            # print(f" faebook{pos2} education == {check_type(v['education']) }  ")
                            # df["Positions"].append(("linkedin"+str(pos),"facebook"+str(pos2)))
                            # df["Scores"].append(penalty)
                            scores.append(penalty)
                            continue
                       
                        score = documentSimilarity(check_type(i[link_entity]),check_type(v["education"]))
                        # df["Positions"].append(("linkedin"+str(pos),"facebook"+str(pos2)))
                        # df["Scores"].append(score)
                        scores.append(score)
                    elif link_entity == "work":
                       
                        if check_type(i[link_entity])==None or check_type(v["work"])==None:
                            # print(f" faebook{pos2} work == {check_type(v['work']) }  ")
                            # df["Positions"].append(("linkedin"+str(pos),"facebook"+str(pos2)))
                            # df["Scores"].append(penalty)
                            scores.append(penalty)
                            continue
                        if v["work"] ==[]:
                            # print(f" faebook{pos2} work == {check_type(v['work']) }  ")
                            # df["Positions"].append(("linkedin"+str(pos),"facebook"+str(pos2)))
                            # df["Scores"].append(penalty)
                            scores.append(penalty)
                            continue
                        score = documentSimilarity(check_type(i[link_entity]),check_type(v["work"]))
                        # df["Positions"].append(("linkedin"+str(pos),"facebook"+str(pos2)))
                        # df["Scores"].append(score)
                        scores.append(score)
                        
                    
                df["Positions"].append(("linkedin"+str(pos),"facebook"+str(pos2)))
                df["Scores"].append(sum(scores))
                name = "linkedin"+"facebook"

    elif instaData and facebookData:
        for pos,i in enumerate(instaData):
            for pos2,v in enumerate(facebookData):
                if (i["username"]!=None and v["Instagram"]!=None) and  (i["username"]==v["Instagram"]):
                  df["Positions"].append(("insta"+str(pos),"facebook"+str(pos2)))
                  df["Scores"].append(0)
                else:
                  scores = []
                
                  for facebook_entity in v.keys():
                    
                      if v[facebook_entity]!=None and facebook_entity in f_entities:
                        if type(v[facebook_entity])==list and len(v[facebook_entity])>0:
                          score = documentSimilarity(i["biography"] ," ".join(v[facebook_entity]))
                          scores.append(score)
                        else:
                          if len(v[facebook_entity])>0:
                            score = documentSimilarity(i["biography"] ,v[facebook_entity])
                            scores.append(score)
                          else:
                            
                            scores.append(penalty)
                      else:
                        if v[facebook_entity]==None and facebook_entity in f_entities:
                          scores.append(penalty)
                    
                  df["Positions"].append(("facebook"+str(pos2),"insta"+str(pos)))
                  df["Scores"].append(sum(scores))
                  name = "facebook"+"insta"

    elif instaData and linkedinData:
        #comment this code if its not worked
        None1 = ["Painter based in the city of Leiden\nAll paintings are for sale\nContact: guido.marsman@gmail.com"]
        for pos,i in enumerate(instaData):
            
            # if (prof_name!=" " )and (i["biography"] in None1 ):
        
            #   myscore = 0
            #   for name11 in prof_name.split(" "):
            #       if name11.lower() in instaData[pos]["fullName"].lower():
            #           myscore +=1
            #   t_score = myscore/len(prof_name.split(" "))
            #   if t_score<0.9 :
            #       print("not matched")
                  
            #       continue
            if check_type(i["fullName"]) != None or check_type(i["fullName"]) != "":
                if i["biography"] in None1:
                   continue
            else:
               continue
            for pos2,v in enumerate(linkedinData):
                
                scores = []
                
                for linkedin_entity in v.keys():
                  
                    if v[linkedin_entity]!=None and linkedin_entity in link_entities:
                      if type(v[linkedin_entity])==list and len(v[linkedin_entity])>0:
                        score = documentSimilarity(i["biography"] ," ".join(v[linkedin_entity]))
                        scores.append(score)
                      else:
                        if len(v[linkedin_entity])>0:
                          score = documentSimilarity(i["biography"] ,v[linkedin_entity])
                          scores.append(score)
                        else:
                          
                          scores.append(penalty)
                    else:
                      if v[linkedin_entity]==None and linkedin_entity in link_entities:
                        scores.append(penalty)
                  
                df["Positions"].append(("linkedin"+str(pos2),"insta"+str(pos)))
                df["Scores"].append(sum(scores))
                name = "linkedin"+"insta"


    else:
      print(instaData,facebookData)
      # print(facebookData)
      return "Incorrect Fomat"
   
    df = pd.DataFrame(df)
    df["Match Columns"] = [name]*len(df)
    # print("YESSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",name,len(df),df["Match Columns"].iloc[0])
    return pd.DataFrame(df)



def get_Matched(df,reversed=False):
  if reversed:
    df_sorted = df.sort_values(by='Scores',ascending=False)
  else:
    df_sorted = df.sort_values(by='Scores')

  name= str(list(df["Match Columns"])[0])

  output_df = df_sorted[['Positions', 'Scores']].reset_index(drop=True)
  if len(name.split("-"))==3:
    d = {"Positions":[],"Scores" : []}
    unique_document3 = set()
    unique_document2 = set()
    unique_document1 = set()
    for i,s in zip(output_df["Positions"],output_df["Scores"]):
          if i[0] not in unique_document1:
            if i[1] not in unique_document2:
                if i[2] not in unique_document3:
                  d["Positions"].append((i[0],i[1],i[2]))
                  d["Scores"].append(s)
                  unique_document1.add(i[0])
                  unique_document2.add(i[1])
                  unique_document3.add(i[2])
                
    df = pd.DataFrame(d)
    df["Match Columns"] = [name]*len(df)
  else:
    d = {"Positions":[],"Scores" : []}
    unique_document2 = set()
    unique_document1 = set()
    for i,s in zip(output_df["Positions"],output_df["Scores"]):
          if i[0] not in unique_document1:
            if i[1] not in unique_document2:
                d["Positions"].append((i[0],i[1]))
                d["Scores"].append(s)
                unique_document1.add(i[0])
                unique_document2.add(i[1])
    df = pd.DataFrame(d)
    df["Match Columns"] = [name]*len(df)
  return df

    


# def get_Scores_chroma(d1,d2):
#     res1 = identify_documents(d1)
#     res2 = identify_documents(d2)
#     if res1 ==  "Incorrect format":
#         return "Incorrect Format document1"
#     if res2 ==  "Incorrect format":
#         return "Incorrect Format document2"
#     linkedindata = None
#     instaData = None
#     facebookData = None
#     if res1=="Linkedin":
#       linkedindata = d1
#     elif res1=="insta":
#       instaData = d1
#     elif res1=="facebook":
#         facebookData = d1

#     if res2=="Linkedin":
#       linkedindata = d2
#     elif res2=="insta":
#       instaData = d2
#     elif res2=="facebook":
#         facebookData = d2
 

#     df = {"Positions":[],"Scores":[]}
#     if linkedindata and instaData:
#       for pos,i in enumerate(linkedindata):
#               # Add docs to the collection. Can also update and delete. Row-based API coming soon!
#               # docs2 = [x["discription"].strip().lower() for x in instaData]
#               for pos2,v in enumerate(instaData):
#                 c = client.delete_collection("all-my-documents")
#                 collection = client.create_collection("all-my-documents")
#                 collection.add(
#                     documents=[v["discription"].strip().lower()], # we handle tokenization, embedding, and indexing automatically. You can skip that and add your own embeddings as well
#                     metadatas=[{"source": "google-docs"} ], # filter on these!
#                     ids=["docs"], # unique for each doc
#                 )

#                 # Query/search 2 most similar results. You can also .get by id
#                 q = i[0]["about"] +" "+i[0]["education"][0]["title"] +" "+i[0]["education"][0]["degree"].strip().lower()
               
#                 results = collection.query(
#                     query_texts=[q],
#                     n_results=2,
#                     # where={"metadata_field": "is_equal_to_this"}, # optional filter
#                     # where_document={"$contains":"search_string"}  # optional filter
#                 )
#                 result = map(lambda x:float(x),results["distances"][0])
#                 score =  min(result)
#                 # pos2 = results["distances"][0].index(score)
#                 df["Positions"].append(("linkedin"+str(pos),"insta"+str(pos2)))
#                 df["Scores"].append(score)

    
#     elif linkedindata and facebookData:
#         # docs2 = [" ".join(v["details"]).strip().lower() for v in facebookData]
#         for pos,i in enumerate(linkedindata):
#             for pos2,v in enumerate(facebookData):
              
#               # Add docs to the collection. Can also update and delete. Row-based API coming soon!
#               q = i[0]["about"] +" "+i[0]["education"][0]["title"] +" "+i[0]["education"][0]["degree"].strip().lower()
#               c = client.delete_collection("all-my-documents")
#               collection = client.create_collection("all-my-documents")

#               collection.add(
#                   documents=[" ".join(v["details"]).strip().lower()], # we handle tokenization, embedding, and indexing automatically. You can skip that and add your own embeddings as well
#                   metadatas=[{"source": "google-docs"} ], # filter on these!
#                   ids=["docs"], # unique for each doc
#               )

#               # Query/search 2 most similar results. You can also .get by id
#               results = collection.query(
#                   query_texts=[q],
#                   n_results=2,
#                   # where={"metadata_field": "is_equal_to_this"}, # optional filter
#                   # where_document={"$contains":"search_string"}  # optional filter
#               )
#               result = map(lambda x:float(x),results["distances"][0])
#               score =  min(result)
#               # pos2 = results["distances"][0].index(score)
       
#               df["Positions"].append(("linkedin"+str(pos),"facebook"+str(pos2)))
#               df["Scores"].append(score)
#     elif instaData and facebookData:
#       # docs2 = [" ".join(v["details"]).strip().lower() for v in facebookData]
#       for pos,i in enumerate(instaData):
#        for pos2,v in enumerate(facebookData):
#               # Add docs to the collection. Can also update and delete. Row-based API coming soon!
#               q =  i["discription"].strip().lower()
#               c = client.delete_collection("all-my-documents")
#               collection = client.create_collection("all-my-documents")
#               collection.add(
#                   documents=[" ".join(v["details"]).strip().lower()], # we handle tokenization, embedding, and indexing automatically. You can skip that and add your own embeddings as well
#                   metadatas=[{"source": "google-docs"} ], # filter on these!
#                   ids=["docs"], # unique for each doc
#               )

#               # Query/search 2 most similar results. You can also .get by id
#               results = collection.query(
#                   query_texts=q,
#                   n_results=2,
#                   # where={"metadata_field": "is_equal_to_this"}, # optional filter
#                   # where_document={"$contains":"search_string"}  # optional filter
#               )
#               result = map(lambda x:float(x),results["distances"][0])
#               score =  min(result)
#               # pos2 = results["distances"][0].index(score)

#               df["Positions"].append(("insta"+str(pos),"facebook"+str(pos2)))
#               df["Scores"].append(score)

#     else:

#       # print(facebookData)
#       return res1 +res2
#     name = res1+res2
#     df = pd.DataFrame(df)
#     df["Match Columns"] = [name]*len(df)
#     return pd.DataFrame(df)

