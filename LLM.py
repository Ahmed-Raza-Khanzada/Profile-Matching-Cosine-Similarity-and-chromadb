from sentence_transformers import SentenceTransformer, util
import torch
import pandas as pd
embedder = SentenceTransformer('all-MiniLM-L6-v2')
def LLM_MAtching(linkedin_prof_data=None,facebook_prof_data = None,insta_prof_data = None):
  
  if linkedin_prof_data and facebook_prof_data and insta_prof_data:
    corpus_embeddings = embedder.encode(linkedin_prof_data, convert_to_tensor=True)
    corpus_embeddings2 = embedder.encode(facebook_prof_data, convert_to_tensor=True)
    df = {"Positions":[],"Scores":[]}
    top_link = len(linkedin_prof_data)
    top_face = len(facebook_prof_data)
    top_insta = len(insta_prof_data)
    # print(top_k,top_k2,top_k3)
    for pos, face in enumerate(facebook_prof_data):
        for pos2, insta in enumerate(insta_prof_data):
            for pos3, linkedin in enumerate(linkedin_prof_data):
                query1 = face
                query2 = insta
                query3 = linkedin
                query_embedding1 = embedder.encode(query1, convert_to_tensor=True)
                query_embedding2 = embedder.encode(query2, convert_to_tensor=True)
                # query_embedding3 = embedder.encode(query3, convert_to_tensor=True)

                cos_scores1 = util.cos_sim(query_embedding1, corpus_embeddings)[0]
                cos_scores2 = util.cos_sim(query_embedding2, corpus_embeddings)[0]
                cos_scores3 = util.cos_sim(query_embedding2, corpus_embeddings2)[0]
               
                top_results1 = torch.topk(cos_scores1, k=top_link)
                top_results2 = torch.topk(cos_scores2, k=top_link)
                top_results3 = torch.topk(cos_scores3, k=top_face)

                for score1, idx1 in zip(top_results1[0], top_results1[1]):
                    for score2, idx2 in zip(top_results2[0], top_results2[1]):
                        for score3, idx3 in zip(top_results3[0], top_results3[1]):
                            combined_score = (
                                round(float(score1), 4) +
                                round(float(score2), 4) +
                                round(float(score3), 4)
                            )

                            if query1 == "None":
                                combined_score = combined_score - 0.3
                            if query2 == "None":
                                combined_score = combined_score - (0.3 * 2)
                            if query3 == "None":
                                combined_score = combined_score - (0.3 * 3)
                            if "Guido Marsman" in query1:
                                combined_score = combined_score - 0.3
                            
                            df["Positions"].append(("facebook"+str(pos), "insta"+str(pos2), "linkedin"+str(int(idx1))   ))
                            df["Scores"].append(combined_score)

    name = "facebook-insta-linkedin"
    df["Match Columns"] = [name] * len(df["Positions"])
    df = pd.DataFrame(df)

    return df
  elif linkedin_prof_data and insta_prof_data:
    corpus_embeddings = embedder.encode(linkedin_prof_data, convert_to_tensor=True)
    df = {"Positions":[],"Scores":[]}
    top_k =len(linkedin_prof_data)
    
    for pos2,insta in enumerate(insta_prof_data):
     
      query2  = insta
    
      query_embedding2 = embedder.encode(query2, convert_to_tensor=True)

     
      cos_scores2 = util.cos_sim(query_embedding2, corpus_embeddings)[0]
     
      top_results2 = torch.topk(cos_scores2, k=top_k)

      for score2, idx2 in zip(top_results2[0], top_results2[1]):#facebook
          # print(int(idx),round(float(score),4))
          # print(corpus[idx], "(Score: {:.4f})".format(score))
            
            combined_score = round(float(score2),4)
            if query2=="None":
              combined_score = combined_score-0.3
            if "Guido Marsman" in query2:
               combined_score = combined_score-0.3
            df["Positions"].append(("insta"+str(pos2),"linkedin"+str(int(idx2))))
            df["Scores"].append(combined_score)
    name = "insta-"+"linkedin"
    df["Match Columns"] = [name]*len(df["Positions"])
    df = pd.DataFrame(df)
    return df
  elif linkedin_prof_data and facebook_prof_data:
    corpus_embeddings = embedder.encode(linkedin_prof_data, convert_to_tensor=True)
    df = {"Positions":[],"Scores":[]}
    top_k =len(linkedin_prof_data)
    
    for pos2,facebook in enumerate(facebook_prof_data):
     
      query2  = facebook
    
      query_embedding2 = embedder.encode(query2, convert_to_tensor=True)

     
      cos_scores2 = util.cos_sim(query_embedding2, corpus_embeddings)[0]
     
      top_results2 = torch.topk(cos_scores2, k=top_k)

      for score2, idx2 in zip(top_results2[0], top_results2[1]):#facebook
          # print(int(idx),round(float(score),4))
          # print(corpus[idx], "(Score: {:.4f})".format(score))
            
            combined_score = round(float(score2),4)
            if query2=="None":
              combined_score = combined_score-0.3
            df["Positions"].append(("facebook"+str(pos2),"linkedin"+str(int(idx2))))
            df["Scores"].append(combined_score)
    name = "facebook-"+"linkedin"
    df["Match Columns"] = [name]*len(df["Positions"])
    df = pd.DataFrame(df)
    return df
  elif insta_prof_data and facebook_prof_data:
    corpus_embeddings = embedder.encode(insta_prof_data, convert_to_tensor=True)
    df = {"Positions":[],"Scores":[]}
    top_k =len(insta_prof_data)
    
    for pos2,facebook in enumerate(facebook_prof_data):
     
      query2  = facebook
    
      query_embedding2 = embedder.encode(query2, convert_to_tensor=True)

     
      cos_scores2 = util.cos_sim(query_embedding2, corpus_embeddings)[0]
     
      top_results2 = torch.topk(cos_scores2, k=top_k)

      for score2, idx2 in zip(top_results2[0], top_results2[1]):#facebook
          # print(int(idx),round(float(score),4))
          # print(corpus[idx], "(Score: {:.4f})".format(score))
            
            combined_score = round(float(score2),4)
            if query2=="None":
              combined_score = combined_score-0.3
            df["Positions"].append(("facebook"+str(pos2),"insta"+str(int(idx2))))
            df["Scores"].append(combined_score)
    name = "facebook-"+"insta"
    df["Match Columns"] = [name]*len(df["Positions"])
    df = pd.DataFrame(df)
    
    return df