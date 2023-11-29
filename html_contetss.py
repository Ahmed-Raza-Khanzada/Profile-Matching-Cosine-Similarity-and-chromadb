import pandas as pd

from utils import clean_text


def my_html(insta,facebook,linkedin,twitter,websites,post_images,profile_images):
 
    my_css = '''         body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f0f0f0;
        }

        .profile {
            background-color: #fff;
            max-width: 800px;
            margin: 20px auto;
            padding: 20px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }

        .profile-image {
            text-align: center;
        }

        .profile-image img {
            max-width: 170px;
            max-height: 170px;
            margin: 0 10px 0 10px;
        }

        .post-image img {
            max-width: 160px;
            max-height: 160px;
            margin: 10px;
        }

        .profile-name {
            text-align: center;
            font-size: 24px;
            margin: 10px 0;
        }

        .card {
            margin: 20px;
            padding: 1px 0 5px 0;
            background-color: #fff;
            box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
        }

        .card-flex {
            display: -webkit-box;
            display: -webkit-flex;
            display: flex;
            padding: 10px;
        }

        .card-sm {
            -webkit-box-flex: 1;
            -webkit-flex: 1;
            flex: 1;
            margin-right: 5%;
            background-color: #fff;
            box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
            max-width: 350px;
            padding: 10px;
        }

        .card-flex>div:last-child {
            margin-right: 0;
        }

        .card-heading {
            font-size: 20px;
            margin: 10px;
        }

        .card-text {
            font-size: 16px;
            margin: 10px;
        }

        .group-card {
            display: -webkit-box;
            display: -webkit-flex;
            display: flex;
            padding: 10px;
        }

        .group {
            -webkit-box-flex: 1;
            -webkit-flex: 1;
            flex: 1;
            margin-right: 5px;
            background-color: #cfcfcf;
            box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
            padding: 10px;
            width: auto;
            text-align: center;
        }

        .button-flex {
            display: -webkit-box;
            display: -webkit-flex;
            display: flex;
            padding: 10px;
        }

        .button {
            background-color: #f2f2f2;
            text-align: center;
            padding: 10px 25px 10px 25px;
            border-radius: 100px;
            color: black;
            margin-right: 10px;
            display: -webkit-box;
            display: -webkit-flex;
            display: flex;
            align-items: center;
        }

        .icon {
            margin-right: 5px;
            align-items: center;
        }

        .profile-link {
            text-align: center;
            margin-top: 20px;
        }

        .profile-link a {
            text-decoration: none;
            background-color: #0077b5;
            color: #fff;
            padding: 10px 20px;
            border-radius: 5px;
            font-weight: bold;
        }

        .social-link {
            margin-top: 10px;
            text-align: center;
        }

        .social-link a {
            text-decoration: none;
            background-color: #4267B2;
            color: #fff;
            padding: 5px 10px;
            border-radius: 5px;
            font-weight: bold;
            margin: 0 5px;
        }

        .social-link a:hover {
            background-color: #334d8c;
        }

        .instagram-link {
            text-align: center;
            margin-top: 20px;
        }

        .instagram-link a {
            text-decoration: none;
            background-color: #e4405f;
            color: #fff;
            padding: 10px 20px;
            border-radius: 5px;
            font-weight: bold;
            display: inline-block;
        }

        .instagram-link a:hover {
            background-color: #d42949;
        }'''

    html_content = f'''
    <html lang="en">

    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Profile</title>
        <style>
            {my_css}
        </style>
    </head>

    <body>
        <div class="profile">

            <div class="profile-image">
                        {profile_images}
                    
            </div>

            <div class="card-flex">
                <div class="card-sm">
                    <h2 class="card-heading">Address</h2>
                    <p class="card-text">
                        {clean_text(' '.join(facebook['hometown']) if type(facebook['hometown']) == list else facebook['hometown'])}
                    </p>
                </div>
                <div class="card-sm">
                    <h2 class="card-heading">Website</h2>
                    {websites}

                </div>
            </div>

            <div class="card">
                <h2 class="card-heading">Information</h2>
                <p class="card-text">
                    {' '.join(facebook['bio']) if type(facebook['bio']) == list else facebook['bio']}<br/>
                    {' '.join(insta['biography']) if type(insta['biography']) == list else insta['biography']}<br/>
                    {' '.join(linkedin['biography']) if type(linkedin['biography']) == list else linkedin['biography']}<br/>
                    {' '.join(linkedin['about']) if type(linkedin['about']) == list else linkedin['about']}<br/>
                    {' '.join(facebook['education']) if type(facebook['education']) == list else facebook['education']}<br/>
                    {' '.join(twitter['biography']) if type(twitter['biography']) == list else twitter['biography']}<br/>
                </p>
            </div>
            <div class="card">
                <h2 class="card-heading">Work</h2>
                <p class="card-text">
                    {clean_text(' '.join(facebook['work']) if type(facebook['work']) == list else facebook['work'])}<br/>
                    {clean_text(' '.join(insta['work']) if type(insta['work']) == list else insta['work'])}<br/>
                    {clean_text(' '.join(linkedin['work']) if type(linkedin['work']) == list else linkedin['work'])}<br/>
                    {clean_text(' '.join(twitter['work']) if type(twitter['work']) == list else twitter['work'])}<br/>
                </p>
            </div>
            <div class="card">
                <h2 class="card-heading">Social-Media-Groups</h2>
                <div class="group-card">
                    <div class="group"> Group#1 </div>
                    <div class="group"> Group#2 </div>
                    <div class="group"> Group#3 </div>
                    <div class="group"> Group#4 </div>
                    <div class="group"> Group#5 </div>
                </div>
            </div>
            <div class="card">
                <h2 class="card-heading">Social-Media-Profile</h2>
                <div class="button-flex">
                    <a href="{insta["link"]}" class="button">
                        <div class="icon">
                            <img src="https://cdn.icon-icons.com/icons2/1584/PNG/512/3721672-instagram_108066.png" width="20" />
                        </div>
                        instagram
                    </a>
                    <a href="{facebook["link"]}" class="button">
                        <div class="icon">
                            <img src="https://cdn.icon-icons.com/icons2/836/PNG/512/Facebook_icon-icons.com_66805.png" width="18"/>
                        </div>
                        facebook
                    </a>
                    <a href="{linkedin["link"]}" class="button">
                        <div class="icon">
                            <img src="https://cdn.icon-icons.com/icons2/2037/PNG/512/in_linked_linkedin_media_social_icon_124259.png" width="20"/>
                        </div>
                        linkedin
                    </a>
                </div>
                <div class="group-card">
                    <div class="post-image">
                    {post_images}
                    </div>
                </div>

            </div>
    </body>

    </html>

    '''
    
    
    return html_content
def my_peoplecard(my_data,websites,post_images,profile_images):
 
    my_css = '''         body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f0f0f0;
        }

        .profile {
            background-color: #fff;
            max-width: 800px;
            margin: 20px auto;
            padding: 20px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }

        .profile-image {
            text-align: center;
        }

        .profile-image img {
            max-width: 170px;
            max-height: 170px;
            margin: 0 10px 0 10px;
        }

        .post-image img {
            max-width: 160px;
            max-height: 160px;
            margin: 10px;
        }

        .profile-name {
            text-align: center;
            font-size: 24px;
            margin: 10px 0;
        }

        .card {
            margin: 20px;
            padding: 1px 0 5px 0;
            background-color: #fff;
            box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
        }

        .card-flex {
            display: -webkit-box;
            display: -webkit-flex;
            display: flex;
            padding: 10px;
        }

        .card-sm {
            -webkit-box-flex: 1;
            -webkit-flex: 1;
            flex: 1;
            margin-right: 5%;
            background-color: #fff;
            box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
            max-width: 350px;
            padding: 10px;
        }

        .card-flex>div:last-child {
            margin-right: 0;
        }

        .card-heading {
            font-size: 20px;
            margin: 10px;
        }

        .card-text {
            font-size: 16px;
            margin: 10px;
        }

        .group-card {
            display: -webkit-box;
            display: -webkit-flex;
            display: flex;
            padding: 10px;
        }

        .group {
            -webkit-box-flex: 1;
            -webkit-flex: 1;
            flex: 1;
            margin-right: 5px;
            background-color: #cfcfcf;
            box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
            padding: 10px;
            width: auto;
            text-align: center;
        }

        .button-flex {
            display: -webkit-box;
            display: -webkit-flex;
            display: flex;
            padding: 10px;
        }

        .button {
            background-color: #f2f2f2;
            text-align: center;
            padding: 10px 25px 10px 25px;
            border-radius: 100px;
            color: black;
            margin-right: 10px;
            display: -webkit-box;
            display: -webkit-flex;
            display: flex;
            align-items: center;
        }

        .icon {
            margin-right: 5px;
            align-items: center;
        }

        .profile-link {
            text-align: center;
            margin-top: 20px;
        }

        .profile-link a {
            text-decoration: none;
            background-color: #0077b5;
            color: #fff;
            padding: 10px 20px;
            border-radius: 5px;
            font-weight: bold;
        }

        .social-link {
            margin-top: 10px;
            text-align: center;
        }

        .social-link a {
            text-decoration: none;
            background-color: #4267B2;
            color: #fff;
            padding: 5px 10px;
            border-radius: 5px;
            font-weight: bold;
            margin: 0 5px;
        }

        .social-link a:hover {
            background-color: #334d8c;
        }

        .instagram-link {
            text-align: center;
            margin-top: 20px;
        }

        .instagram-link a {
            text-decoration: none;
            background-color: #e4405f;
            color: #fff;
            padding: 10px 20px;
            border-radius: 5px;
            font-weight: bold;
            display: inline-block;
        }

        .instagram-link a:hover {
            background-color: #d42949;
        }'''

    html_content = f'''
    <html lang="en">

    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Profile</title>
        <style>
            {my_css}
        </style>
    </head>

    <body>
        <div class="profile">

            <div class="profile-image">
                        {profile_images}
                    
            </div>

            <div class="card-flex">
                <div class="card-sm">
                    <h2 class="card-heading">Address</h2>
                    <p class="card-text">
                        {clean_text(' '.join(my_data['hometown']) if type(my_data['hometown']) == list else my_data['hometown'])}
                    </p>
                </div>
                <div class="card-sm">
                    <h2 class="card-heading">Website</h2>
                    {websites}

                </div>
            </div>

            <div class="card">
                <h2 class="card-heading">Information</h2>
                <p class="card-text">
                    {my_data["bio"]}<br/>
                   
                </p>
            </div>
            <div class="card">
                <h2 class="card-heading">Work</h2>
                <p class="card-text">
                    {clean_text(' '.join(my_data['work']) if type(my_data['work']) == list else my_data['work'])}<br/>
                   
                </p>
            </div>
            <div class="card">
                <h2 class="card-heading">Social-Media-Groups</h2>
                <div class="group-card">
                    <div class="group"> Group#1 </div>
                    <div class="group"> Group#2 </div>
                    <div class="group"> Group#3 </div>
                    <div class="group"> Group#4 </div>
                    <div class="group"> Group#5 </div>
                </div>
            </div>
            <div class="card">
                <h2 class="card-heading">Social-Media-Profile</h2>
                <div class="button-flex">
                    <a href="{my_data["insta_link"]}" class="button">
                        <div class="icon">
                            <img src="https://cdn.icon-icons.com/icons2/1584/PNG/512/3721672-instagram_108066.png" width="20" />
                        </div>
                        instagram
                    </a>
                    <a href="{my_data["face_link"]}" class="button">
                        <div class="icon">
                            <img src="https://cdn.icon-icons.com/icons2/836/PNG/512/Facebook_icon-icons.com_66805.png" width="18"/>
                        </div>
                        facebook
                    </a>
                    <a href="{my_data["linkedin_link"]}" class="button">
                        <div class="icon">
                            <img src="https://cdn.icon-icons.com/icons2/2037/PNG/512/in_linked_linkedin_media_social_icon_124259.png" width="20"/>
                        </div>
                        linkedin
                    </a>
                </div>
                <div class="group-card">
                    <div class="post-image">
                    {post_images}
                    </div>
                </div>

            </div>
    </body>

    </html>

    '''
    
    
    return html_content

def my_blur_html(insta,facebook,linkedin,twitter,websites,post_images,profile_images):
 
    my_css = '''         body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f0f0f0;
        }

        .profile {
            background-color: #fff;
            max-width: 800px;
            margin: 20px auto;
            padding: 20px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }

        .profile-image {
            text-align: center;
        }

        .profile-image img {
            max-width: 170px;
            max-height: 170px;
            margin: 0 10px 0 10px;
        }

        .post-image img {
            max-width: 160px;
            max-height: 160px;
            margin: 10px;
            filter: blur(5px);
        }

        .profile-name {
            text-align: center;
            font-size: 24px;
            margin: 10px 0;
        }

        .card {
            margin: 20px;
            padding: 1px 0 5px 0;
            background-color: #fff;
            box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
        }

        .card-flex {
            display: -webkit-box;
            display: -webkit-flex;
            display: flex;
            padding: 10px;
        }

        .card-sm {
            -webkit-box-flex: 1;
            -webkit-flex: 1;
            flex: 1;
            margin-right: 5%;
            background-color: #fff;
            box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
            max-width: 350px;
            padding: 10px;
        }

        .card-flex>div:last-child {
            margin-right: 0;
        }

        .card-heading {
            font-size: 20px;
            margin: 10px;
            
        }

        .card-text {
            font-size: 16px;
            margin: 10px;
        }

        .group-card {
            display: -webkit-box;
            display: -webkit-flex;
            display: flex;
            padding: 10px;
            filter: blur(5px);
        }

        .group {
            -webkit-box-flex: 1;
            -webkit-flex: 1;
            flex: 1;
            margin-right: 5px;
            background-color: #cfcfcf;
            box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
            padding: 10px;
            width: auto;
            text-align: center;
        }

        .button-flex {
            display: -webkit-box;
            display: -webkit-flex;
            display: flex;
            padding: 10px;
        }

        .button {
            background-color: #f2f2f2;
            text-align: center;
            padding: 10px 25px 10px 25px;
            border-radius: 100px;
            color: black;
            margin-right: 10px;
            display: -webkit-box;
            display: -webkit-flex;
            display: flex;
            align-items: center;
        }

        .icon {
            margin-right: 5px;
            align-items: center;
        }

        .profile-link {
            text-align: center;
            margin-top: 20px;
        }

        .profile-link a {
            text-decoration: none;
            background-color: #0077b5;
            color: #fff;
            padding: 10px 20px;
            border-radius: 5px;
            font-weight: bold;
        }

        .social-link {
            margin-top: 10px;
            text-align: center;
        }

        .social-link a {
            text-decoration: none;
            background-color: #4267B2;
            color: #fff;
            padding: 5px 10px;
            border-radius: 5px;
            font-weight: bold;
            margin: 0 5px;
        }

        .social-link a:hover {
            background-color: #334d8c;
        }

        .instagram-link {
            text-align: center;
            margin-top: 20px;
        }

        .instagram-link a {
            text-decoration: none;
            background-color: #e4405f;
            color: #fff;
            padding: 10px 20px;
            border-radius: 5px;
            font-weight: bold;
            display: inline-block;
        }

        .instagram-link a:hover {
            background-color: #d42949;

        
        }'''

    html_content = f'''
    <html lang="en">

    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Profile</title>
        <style>
            {my_css}
        </style>
    </head>

    <body>
        <div class="profile">

            <div class="profile-image">
                        {profile_images}
                    
            </div>

            <div class="card-flex">
                <div class="card-sm">
                    <h2 class="card-heading">Address</h2>
                    <p class="card-text">
                        {clean_text(' '.join(facebook['hometown']) if type(facebook['hometown']) == list else facebook['hometown'])}
                    </p>
                </div>
                <div class="card-sm">
                    <h2 class="card-heading">Website</h2>
                    {websites}

                </div>
            </div>

            <div class="card">
                <h2 class="card-heading">Information</h2>
                <p class="card-text">
                    {' '.join(facebook['bio']) if type(facebook['bio']) == list else facebook['bio']}<br/>
                    {' '.join(insta['biography']) if type(insta['biography']) == list else insta['biography']}<br/>
                    {' '.join(linkedin['biography']) if type(linkedin['biography']) == list else linkedin['biography']}<br/>
                    {' '.join(linkedin['about']) if type(linkedin['about']) == list else linkedin['about']}<br/>
                    {' '.join(facebook['education']) if type(facebook['education']) == list else facebook['education']}<br/>
                    {' '.join(twitter['biography']) if type(twitter['biography']) == list else twitter['biography']}<br/>
                </p>
            </div>
            <div class="card">
                <h2 class="card-heading">Work</h2>
                <p class="card-text">
                    {clean_text(' '.join(facebook['work']) if type(facebook['work']) == list else facebook['work'])}<br/>
                    {clean_text(' '.join(insta['work']) if type(insta['work']) == list else insta['work'])}<br/>
                    {clean_text(' '.join(linkedin['work']) if type(linkedin['work']) == list else linkedin['work'])}<br/>
                    {clean_text(' '.join(twitter['work']) if type(twitter['work']) == list else twitter['work'])}<br/>
                </p>
            </div>
            <div class="card">
                <h2 class="card-heading">Social-Media-Groups</h2>
                <div class="group-card">
                    <div class="group"> Group#1 </div>
                    <div class="group"> Group#2 </div>
                    <div class="group"> Group#3 </div>
                    <div class="group"> Group#4 </div>
                    <div class="group"> Group#5 </div>
                </div>
            </div>
            <div class="card">
                <h2 class="card-heading">Social-Media-Profile</h2>
                <div class="button-flex">
                    <a href="{insta["link"]}" class="button">
                        <div class="icon">
                            <img src="https://cdn.icon-icons.com/icons2/1584/PNG/512/3721672-instagram_108066.png" width="20" />
                        </div>
                        instagram
                    </a>
                    <a href="{facebook["link"]}" class="button">
                        <div class="icon">
                            <img src="https://cdn.icon-icons.com/icons2/836/PNG/512/Facebook_icon-icons.com_66805.png" width="18"/>
                        </div>
                        facebook
                    </a>
                    <a href="{linkedin["link"]}" class="button">
                        <div class="icon">
                            <img src="https://cdn.icon-icons.com/icons2/2037/PNG/512/in_linked_linkedin_media_social_icon_124259.png" width="20"/>
                        </div>
                        linkedin
                    </a>
                </div>
                <div class="group-card">
                    <div class="post-image">
                    {post_images}
                    </div>
                </div>

            </div>
    </body>

    </html>

    '''
    
    
    return html_content



    # html_content = f"""<html lang="en">
    #         <head>
    #             <meta charset="UTF-8">
    #             <meta name="viewport" content="width=device-width, initial-scale=1.0">
    #             <title>Profile</title>
    #                 <style>
    #                 {my_css}
    #                 </style>
    #         </head>
    #         <body>
    #             <div class="profile">
            
    #                 <!-- Main(Instagram) Section -->
    #                 <div class="profile-image">
    #                     <img src="{insta['image']}" alt="Profile Image">
    #                 </div>
    #                 <div class="profile-name">{clean_text(insta["fullName"])}</div>
                    

    #                 <!-- Facebook Section -->
    #                 <div class="section">
    #                     <h2>Facebook Profile</h2>
    #                     <p>
    #                         Bio: {clean_text(' '.join( facebook['bio']) if type(facebook['bio']) == list else facebook['bio'])}
    #                     </p>
    #                     <p>
    #                         Home Town: {clean_text(' '.join( facebook['hometown']) if type(facebook['hometown']) == list else facebook['hometown'])}
    #                     </p>
    #                     <p>
    #                         Education: {clean_text(' '.join( facebook['education']) if type(facebook['education']) == list else facebook['education'])}
    #                     </p>
    #                     <p>
    #                     Work: {clean_text(' '.join( facebook['work']) if type(facebook['work']) == list else facebook['work'])}
    #                     </p>
    #                     <p>
    #                         Gender: {clean_text(' '.join( facebook['Gender']) if type(facebook['Gender']) == list else facebook['Gender'])}
    #                     </p>
    #                     <p>
    #                         Email: {clean_text(' '.join( facebook['Email']) if type(facebook['Email']) == list else facebook['Email'])}
    #                     </p>
    #                     <p>
    #                         Birth: {clean_text(' '.join( facebook['Birth_year']) if type(facebook['Birth_year']) == list else facebook['Birth_year']) }
    #                     </p>
    #                     <p>
    #                         Address: {clean_text(' '.join( facebook['Address']) if type(facebook['Address']) == list else facebook['Address'])}
    #                     </p>
    #                     <div class="social-link">
    #                         <a href="{facebook['link']}">Click here to see Facebook profile</a>
    #                     </div>
    #                 </div>

    #                 <!-- Instagram Section -->
    #                 <div class="section">
    #                     <h2>Instagram Profile</h2>
    #                     <p>
    #                         Description: {clean_text(insta['biography'])}
    #                     </p>

    #                     <p>
    #                         Posts: {insta['posts']}
    #                     </p>
    #                     <p>
    #                         Following: {insta['following']}
    #                     </p>
    #                     <p>
    #                         Followers:{insta['followers']}
    #                     </p>

    #                     <div class="instagram-link">
    #                         <a href="{insta['link']}">Click here to see Instagram profile</a>
    #                     </div>
    #                 </div>
    #             </div>
    #         </body>
    #         </html>"""