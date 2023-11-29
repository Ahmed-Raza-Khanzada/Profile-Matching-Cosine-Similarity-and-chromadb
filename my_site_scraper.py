import requests
from bs4 import BeautifulSoup
import re
import time

def scrape_first_paragraph_and_linkedin(url):
    # Send an HTTP GET request to the website with a timeout of 5 seconds
    try:
        response = requests.get(url, timeout=60)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find the first paragraph tag (e.g., <p>) with text content
            first_paragraph = soup.find('p', text=True)

            if first_paragraph:
                # Extract and print the text from the first paragraph
                print("First Paragraph Text:")
                # print(first_paragraph.text)
            else:
                print("No paragraph with text found on the page.")

            lis = "\n"
            print("***************Getting data from Scraper*****************")
            my_li = soup.find_all('li')
            for li in my_li:
                lis = lis+"\n"+ li.text.strip()
                # print(li.text.strip())
                # print("LIsss")
      
            # Find LinkedIn URL if available using a regular expression
            linkedin_url = None
            pattern = re.compile(r'https?://www.linkedin.com/.*')
            for link in soup.find_all('a', href=True):
                if pattern.match(link['href']):
                    linkedin_url = link['href']
                    break

            if linkedin_url:
                print("LinkedIn Profile URL:")
                print(linkedin_url)
            else:
                print("LinkedIn URL not found on the page.")
            return first_paragraph, lis, linkedin_url
        else:
            print(f"Failed to retrieve the page. Status code: {response.status_code}")
    except requests.exceptions.Timeout:
        print(f"Request to {url} timed out after 5 seconds.")
    except Exception as e:
        print(e)
    return None, None, None

if __name__ == "__main__":
    # Provide the URL of the website you want to scrape
    website_url = "https://www.michaelkors.com/"
    scrape_first_paragraph_and_linkedin(website_url)
