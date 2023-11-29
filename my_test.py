from my_call_serp import serach_serp
from html_contetss import my_peoplecard
from pdf_converter import make_html_pdf
websites_links,snippets,search_images,my_people_data = serach_serp("Ajey Nagar","United States")
if my_people_data!={}:
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

    html_people_card = my_peoplecard(my_people_data,websites=websites1,post_images=post_images1,profile_images=prof_images1)
    make_html_pdf("Ajey Nagar",html_content=html_people_card,main_path="pdfs")


    