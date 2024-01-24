from bs4 import BeautifulSoup
import requests

def is_valid_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException:
        return False

def generate_page_urls(base_url, max_page=22):
    all_urls = []
    for page_num in range(1, max_page + 1):
        current_url = base_url if page_num == 1 else f"{base_url}{page_num}/"
        if is_valid_url(current_url):
            all_urls.append(current_url)
    return all_urls         

def extract_mockup_href(page):
    all_hrefs = []
    html_text = requests.get(page).text
    soup = BeautifulSoup(html_text, 'html.parser')
    link_elements = soup.find_all('a', class_ = 'category-post-module--overlay--48cdf')
    for link_element in link_elements:
        href = link_element['href']
        all_hrefs.append(href)
    return all_hrefs

def generate_all_mockup_links():
    all_page_urls = generate_page_urls('https://www.anthonyboyd.graphics/mockups-collection/')
    total_mockups = 0
    urls = []
    for page_url in all_page_urls:
        mockup_links = extract_mockup_href(page_url) 
        for link in mockup_links:
            download_url_base = 'https://www.anthonyboyd.graphics'
            download_url = f"{download_url_base}{link}"
            urls.append(download_url)
            total_mockups += 1
    return urls, total_mockups

def download_files(url):
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'html.parser')
    download_links = soup.find_all('a', class_ = 'download-button-module--btn--904bd')
    for link in download_links:
        dl_url = link['href']
        filename = f"add path here{link['href'][77:]}"
        response = requests.get(dl_url, stream=True)
        with open(filename, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)

def main():
    print(f"Fetching {generate_all_mockup_links()[1]} mockups...")
    urls = generate_all_mockup_links()[0]
    dl_count = 0
    for url in urls:
        print(url)
        download_files(url)
        dl_count += 1
        print(f"\033[32mDownloaded ({dl_count}/{generate_all_mockup_links()[1]}) Mockup(s)\033[0m")
if __name__ == "__main__":
    main()
