import logging,requests, csv
from requests.adapters import HTTPAdapter, Retry

from bs4 import BeautifulSoup

logging.basicConfig(level=logging.DEBUG)

s = requests.Session()
retries = Retry(total=20, backoff_factor=1, status_forcelist=[ 429 ])
s.mount('https://', HTTPAdapter(max_retries=retries))

page = 0
# Initialize a list to store the results  
results = []

baseUrl = "https://notaries-directory.eu/en/"

with open("c:/Users/jakub/OneDrive/Companies/Softville/Apps/Notaries/notaries-data.csv",
          'w', newline='', encoding='utf-8') as csvfile:
    notaryWriter = csv.writer(csvfile, delimiter=';',quotechar='|', quoting=csv.QUOTE_MINIMAL)
    notaryWriter.writerow(["Name", "Address", "Website"])

    while True:
        searchPageUrl = f"{baseUrl}/search?langcode=pl&language-label=Polish&page={page}"
        response = s.get(searchPageUrl)

        if not response.status_code == 200:
            response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        list_elements = soup.findAll("li", {"class": "list-element"})

        if len(list_elements) == 0:
            print(f"{page} doesn't contain any results. Url {searchPageUrl}")
            break

        for li in list_elements:
            notary_name = li.find('div', class_='notary-name').find('h3').get_text(strip=True) if li.find('div', class_='notary-name') and li.find('div', class_='notary-name').find('h3') else None

            address_notary = li.find('p', class_='address-notary').get_text(strip=True) if li.find('p',
                                                                                                class_='address-notary') else None
            notary_detail_link = li.find('a', class_='notary-detail-link')['href'] if li.find('a',
                                                                                            class_='notary-detail-link') else None

            # If the link is relative, make it absolute
            if notary_detail_link:
                notary_detail_link = requests.compat.urljoin(baseUrl, notary_detail_link)

            address_notary = str(address_notary).replace(" ", "").replace("\n", " ")
            
            notaryWriter.writerow([notary_name, address_notary, notary_detail_link])
            # Append the extracted data as a dictionary
            results.append({
                'notary_name': notary_name,
                'address_notary': address_notary,
                'notary_detail_link': notary_detail_link
            })

        page += 1

# Print the results
for result in results:
    print(result)
