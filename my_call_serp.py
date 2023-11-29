from serpapi import GoogleSearch
def serach_serp(name,location = "United States"):
    my_links  =[]
    serach_images = []
    snippet = []
    my_data = {}
    l = ["https://www.instagram.com/","https://www.linkedin.com","https://www.facebook.com"]
    try:
        search = GoogleSearch({
            "q": name, 
            "location": location,
            "api_key": "bfb6a982ca50ea5b3fcf6ab3d7f1d73c8cf1499beddd1c4ec7ebdf1e442f9d4b"
        })
        result = search.get_dict()
        for i in result["organic_results"]:

            if  i["link"].startswith(tuple(l)):
                continue
            else:
                # print(i["link"],"******link")
                my_links.append(i["link"])
                # print("$"*80)
            if i.get("snippet")!=None:
                snippet.append(i["snippet"])
                # print(i["snippet"],"******snippet")
            else:
                snippet.append("")

        if result.get("inline_images") == None:
            pass
        else:   
            for k in result["inline_images"]:
                serach_images.append(k["original"])
        try:
            about = ["description","born","height"]

            bio = ""
            hometown = ""
            work = ""
            if result.get("knowledge_graph"):
                print("Getting Data for Peoples Card for Famous Personality")
                for i in result["knowledge_graph"]:
                    if i.lower() in about:
                        if i.lower() =="born":

                            bio = bio+"\nBorn: "+ result["knowledge_graph"][i]
                        else:    
                            bio = bio+"\n"+ result["knowledge_graph"][i]
                    if i.lower() in about:
                        if i.lower() =="height":

                            bio = bio+"\nHeight: "+ result["knowledge_graph"][i]
                        else:    
                            bio = bio+"\n"+ result["knowledge_graph"][i]
                    if i.lower() =="hometown" or i.lower() =="location" or i.lower() =="birthplace" or i.lower() =="city" or i.lower() =="country":
                        hometown += result["knowledge_graph"][i] if type(result["knowledge_graph"][i]) == str else result["knowledge_graph"][i][0]
                    if i.lower()=="eductaion":
                        my_data["education"] = result["knowledge_graph"][i] if type(result["knowledge_graph"][i]) == str else result["knowledge_graph"][i][0]
                    if i.lower()=="occupation" or i.lower()=="work" or i.lower()=="type":
                        work += result["knowledge_graph"][i]
                    if i.lower()=="profiles":
                        wbsites = []
                        for k in result["knowledge_graph"][i]:
                            if k["name"].lower()=="linkedin":
                                my_data["linkedin_link"] = k["link"]
                            elif k["name"].lower()=="instagram":
                                my_data["insta_link"] = k["link"]
                            elif k["name"].lower()=="facebook":
                                my_data["face_link"] = k["link"]
                            else:
                                 wbsites.append(k["link"])
                        my_data["websites"] = wbsites
                    if i.lower()=="header_images":
                        l1 = []
                        for j in result["knowledge_graph"][i]:
                            l1.append(j["image"])
                        if len(l1)>1:
                            my_data["profile_images"] = l1[0]
                            my_data["post_images"] = l1[1:]
                        else:
                            if len(l1)>0:
                                my_data["profile_images"] = l1[0]
                            else:
                                my_data["profile_images"] = ""
                                my_data["post_images"] = ""
                # print("Loop is done")
            my_data["work"] = work
            my_data["hometown"] = hometown
            my_data["bio"] = bio
            if my_data.get("insta_link")==None:
                my_data["insta_link"] = ""
            if my_data.get("face_link")==None:
                my_data["face_link"] = ""
            if my_data.get("linkedin_link")==None:
                my_data["linkedin_link"] = ""
            if result.get("inline_images"):
                print("Getting Inline Images for Peoples Card for Famous Personality")
                l1 = []
                print(result["inline_images"][0].keys())
                for j in result["inline_images"]:
                    l1.append(j["original"])
                # print(result["search_information"]["query_displayed"])
                # print(l1)
                if my_data.get("post_images")!=None:
                    c = my_data["post_images"]
                    c.extend(l1)
                    my_data["post_images"] = c
                  
                else:
                    my_data["post_images"] = l1
                # print(my_data["post_images"])
        except:
            print("Error in Peoples Card Data")
            my_data = {}
            pass
    except Exception as e:
        print(e)
        print("******************","Serp_API Failed to retive websites data","******************")
    

    return my_links,snippet,serach_images,my_data



# serach_serp("Guido Marsch",location = "switzerland")



# from sklearn.cluster import DBSCAN
# from sklearn.feature_extraction.text import TfidfVectorizer
# import numpy as np

# # Sample data (replace with actual data from web scraping or APIs)
# profiles = [
#     {"name": "John Dwan", "platform": "LinkedIn", "profile_id": 1},
#     {"name": "John Doe", "platform": "Instagram", "profile_id": 2},
#     {"name": "John Doee", "platform": "Facebook", "profile_id": 3},
#     {"name": "Jane Doe..", "platform": "LinkedIn", "profile_id": 4},
#     {"name": "John Smith", "platform": "Instagram", "profile_id": 5},
#     # Add more profiles here...
# ]

# # Extract names from profiles
# names = [profile["name"] for profile in profiles]

# # Create TF-IDF vectors from profile names
# vectorizer = TfidfVectorizer()
# tfidf_matrix = vectorizer.fit_transform(names)

# # Convert the TF-IDF matrix to a numpy array
# tfidf_array = tfidf_matrix.toarray()

# # Create a distance matrix based on cosine similarity
# distance_matrix = 1 - np.dot(tfidf_array, tfidf_array.T)

# # Perform DBSCAN clustering
# dbscan = DBSCAN(eps=0.2, min_samples=2, metric="precomputed")
# dbscan.fit(distance_matrix)

# # Assign cluster labels to profiles
# cluster_labels = dbscan.labels_

# # Create a dictionary to store clusters
# clusters = {}
# for i, profile in enumerate(profiles):
#     cluster_label = cluster_labels[i]
#     if cluster_label not in clusters:
#         clusters[cluster_label] = []
#     clusters[cluster_label].append(profile)

# # Print the clusters
# for cluster_label, cluster_profiles in clusters.items():
#     if cluster_label != -1:  # -1 represents noise (unclustered profiles)
#         print(f"Cluster {cluster_label}:")
#         for profile in cluster_profiles:
#             print(f"- {profile['platform']} (Profile ID: {profile['profile_id']})")
#     else:
#         print("Noise (Unclustered Profiles):")
#         for profile in cluster_profiles:
#             print(f"- {profile['platform']} (Profile ID: {profile['profile_id']})")
