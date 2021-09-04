from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

USER_AGENT = {"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'}
SEARCH_INPUT = str(input("Type here Bol product search tab?: "))

search_name = SEARCH_INPUT

def data_manipulation():
    first_url, soup = get_url(search_name, 1)  #1 = page
    last_page = get_last_pagination(soup)

    get_product_data(last_page, first_url)
    


## BOL Main Page
def get_url(search_name, page):

    # Goal: Get Bol Search Product URL
    # Return Search_URL & soup for other function

    search_url = 'https://www.bol.com/nl/nl/s/?page=' + str(page) + '&searchtext=' + search_name
    headers = USER_AGENT
    page = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    return search_url, soup


def get_last_pagination(soup):

    # Gets the last page of the pagination
    last_page = soup.find(class_="pagination").get_text().split()[-1]
    return last_page


# get all Product Data
def get_product_data(last_page, first_url):     #GOOD #TODO Some of the saved Data are dubble

    product_row = []
    url = int(last_page) + 1

    for urls in range(1, url, 1):
        # Url = pagination number link
        pagination_url = re.sub("\d", str(urls), str(first_url))  # "\d" == find Digit, urls == Loop pagenumbers, first_url == get first productpage
        print(f'page {urls} of {url - int(1)}')

        # Get every individual Link of product
        product_link = get_individual_productlink(pagination_url)

        # Use all individual product links and give me the product Details
        link_count = 0
        for product_page in product_link:
            link_count += 1
            product_details = get_product_information(product_page)
            print(f'Product {link_count} of {len(product_link)}')

            product_detail = {
                'title': product_details['title'],
                'subtitle': product_details['subtitle'],
                'brand': product_details['brand'],
                'serie': product_details['serie'],
                'rating': product_details['rating'],
                'rated': product_details['rated'],
                'price': product_details['price'],
                'stock': product_details['stock'],
                'link': product_page,
                'count_images': product_details['count_images'],
                'warning_text': product_details['warning_text'],
                'description': product_details['description'],
            }

            product_row.append(product_detail)


    product_detail = pd.DataFrame(product_row)
    product_detail.to_csv('products.csv', index=True, header=[
        'title', 'subtitle', 'brand', 'serie', 'rating', 'rated', 'price', 
        'stock', 'link', 'count_images', 'warning_text', 'description'])



# Get all individual product links on page
def get_individual_productlink(pagination_url):      #GOOD

    headers = USER_AGENT
    page = requests.get(pagination_url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    product_list = soup.find_all('li', class_='product-item--row')

    # Get all Individual ProductLink on a page
    links = []
    for lists in product_list:
        for item in lists.find_all('div', class_='h-o-hidden'):
            for link in item.find_all('a', href=True):
                links.append("https://www.bol.com" + link['href'])

    return links


# Get app product details of product page
def get_product_information(link):      #GOOD
    headers = USER_AGENT
    page = requests.get(link, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Scraping 1Page Data
    title = soup.select('span[data-test="title"]')[0].get_text()
    price = soup.select('span[data-test="price"]')[0].get_text().strip().replace('\n', ',').replace(' ', '')
    count_images= soup.select('div.filmstrip-viewport ol > li')
    description = soup.select('div[data-test="description"]')[0].get_text()

    # Getting Data From a Chrome Extention is not possable
    #OLD PRICE AFTER DISCOUNT NOT GETTING

    # OFF Couse it to long to print
    #spec = soup.select('div.js_specifications_content > div.specs')
    #spec_list = soup.select('dl.specs__list > div.specs__row')
    
    try:
        brand = soup.select('a[data-role="BRAND"]')[0].get_text().strip()
    except:
        brand = ''
        print('Brand Value Missing!')

    try:
        subtitle = soup.select('span[data-test="subtitle"]')[0].get_text()
    except:
        subtitle = ''
        print('Subtitle Value Missing!')

    try:
        serie = soup.select('a[data-analytics-tag="series"]')[0].get_text().strip()
    except:
        serie = ''
        print('Serie Value Missing!')

    try:
        rating = soup.select('div[data-test="rating-suffix"]')[0].get_text().split('/')[0]
    except:
        rating = ''
        print('Rating Value Missing!')

    try:
        rated = soup.select('div[data-test="rating-suffix"]')[0].get_text().split('/')[1].split(' ')[1].split('(')[1]
    except:
        rated = ''
        print('Rated Value Missing!')

    try:
        stock = soup.select('div[data-test="delivery-highlight"]')[0].get_text().strip()
    except:
        stock = ''
        print('Stock Value Missing!')

    try:
        warning_text = soup.select('span[data-test="product-warning-text-0"]')[0].get_text().strip()
    except:
        warning_text = ''
        print('Warning_text Value Missing!')


    product = {
        'title': title,
        'subtitle': subtitle,
        'brand': brand,
        'serie': serie,
        'rating': rating,
        'rated': rated,
        'price': price,
        'stock': stock,
        'count_images': len(count_images),
        'warning_text': warning_text,
        'description': description,
        #'spec': spec,  # Scrap whole div -> Later Fix
        #'spec_list': spec_list,  # Scrap whole div -> Later Fix
    }

    return product




