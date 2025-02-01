import streamlit as st
from bs4 import BeautifulSoup
import requests
import pandas as pd
from tqdm.contrib.concurrent import thread_map
import time


st.header('Travel With AI :racing_motorcycle:', divider='rainbow') #project title

def get_pagination_links():
    pagination_link = []
    for i in range(1,96+1):
        link = f'https://www.eventbrite.sg/d/singapore/all-events/?page={i}'
        pagination_link.append(link)
    return pagination_link

pagination_urls = get_pagination_links()
st.markdown(
    f"<h4 style='text-align: center; color: #FF0000; background: linear-gradient(to right, #FF0000, #FF7F00, #FFFF00, #00FF00, #0000FF, #4B0082, #8B00FF); -webkit-background-clip: text; color: transparent;'>🚀 Scraping the Data for the Up-Coming Events 🔍</h4>"
    ,
    unsafe_allow_html=True
)

def get_all_event_urls(pass_links):
    cookies = {
        'django_timezone': 'Asia/Calcutta',
        'csrftoken': '288442825735449ea13333e8f307edd4',
        'django_timezone': 'Asia/Calcutta',
        'eblang': 'lo%3Den_SG%26la%3Den-gb',
        'guest': 'identifier%3D5ffacde7-c49a-473d-b9d2-d436c5368715%26a%3D13a0%26s%3D1fdc6a6ef03364ebcf7e577ebb8320c811c3629fba48f399cb1c69f7b747b83d',
        'G': 'v%3D2%26i%3D5ffacde7-c49a-473d-b9d2-d436c5368715%26a%3D13a0%26s%3Dbde8aa9196d32183f85ed2b257ab16ceb1207ffc',
        'SS': 'AE3DLHSi6x8OlInF-axHYENI5Nc2FqBERQ',
        'AS': '8528a7c9-b074-47c8-8429-cb8657422665',
        'location': '%7B%22current_place_parent%22%3A%20%22India%22%2C%20%22place_type%22%3A%20%22locality%22%2C%20%22current_place%22%3A%20%22Coimbatore%22%2C%20%22latitude%22%3A%2011.0142%2C%20%22country%22%3A%20%22India%22%2C%20%22place_id%22%3A%20%22102030495%22%2C%20%22slug%22%3A%20%22india--coimbatore%22%2C%20%22longitude%22%3A%2076.9941%7D',
        'tcm': '{"purposes":{"SaleOfInfo":false,"Functional":false,"Analytics":false,"Advertising":false},"timestamp":"2025-01-31T13:03:12.535Z","confirmed":true,"prompted":false,"updated":true}',
        'location': '{%22current_place%22:%22Singapore%22%2C%22country%22:%22Singapore%22%2C%22latitude%22:1.357685%2C%22longitude%22:103.80938%2C%22slug%22:%22singapore%22%2C%22place_type%22:%22country%22%2C%22place_id%22:%2285632605%22%2C%22is_online%22:false}',
        'mgrefby': '',
        'mgref': 'typeins',
        'session': 'identifier%3D47f3e78cf430460f8fb74da31f2a8908%26issuedTs%3D1738329556%26originalTs%3D1738328579%26s%3Daf9eedaea7808b1a9eb947a8a7f8cf6f200c695759ddeb65ddcc9600d842115b',
        'stableId': 'afb5124c-260c-4bc7-beba-08c8d3be761d',
        'SP': 'AGQgbbk8Fis1dSZY4qPJwRqX4y2OmUu98deUyLJ4eMbOcJFlbPf7DQItfotvvbGoq5jEq3Vlm2c8QETeGGarvecooZFosonSR4knJxid7Tlr72RMh17ConF1cwGBLKeQmAqMzgfMa6dVOet4zZ8bAKsUAFlBSn1B1tpD-cDcRzQWOng-JMBpNDxN6PklaM9_YGAe4QIWkhKTeHCTO3RHiaC68VskjBKStt7dR_UsQYTtOfwBnlHNd4g',
        '_dd_s': 'rum=0&expire=1738330469746',
    }

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.5',
        # 'cookie': 'django_timezone=Asia/Calcutta; csrftoken=288442825735449ea13333e8f307edd4; django_timezone=Asia/Calcutta; eblang=lo%3Den_SG%26la%3Den-gb; guest=identifier%3D5ffacde7-c49a-473d-b9d2-d436c5368715%26a%3D13a0%26s%3D1fdc6a6ef03364ebcf7e577ebb8320c811c3629fba48f399cb1c69f7b747b83d; G=v%3D2%26i%3D5ffacde7-c49a-473d-b9d2-d436c5368715%26a%3D13a0%26s%3Dbde8aa9196d32183f85ed2b257ab16ceb1207ffc; SS=AE3DLHSi6x8OlInF-axHYENI5Nc2FqBERQ; AS=8528a7c9-b074-47c8-8429-cb8657422665; location=%7B%22current_place_parent%22%3A%20%22India%22%2C%20%22place_type%22%3A%20%22locality%22%2C%20%22current_place%22%3A%20%22Coimbatore%22%2C%20%22latitude%22%3A%2011.0142%2C%20%22country%22%3A%20%22India%22%2C%20%22place_id%22%3A%20%22102030495%22%2C%20%22slug%22%3A%20%22india--coimbatore%22%2C%20%22longitude%22%3A%2076.9941%7D; tcm={"purposes":{"SaleOfInfo":false,"Functional":false,"Analytics":false,"Advertising":false},"timestamp":"2025-01-31T13:03:12.535Z","confirmed":true,"prompted":false,"updated":true}; location={%22current_place%22:%22Singapore%22%2C%22country%22:%22Singapore%22%2C%22latitude%22:1.357685%2C%22longitude%22:103.80938%2C%22slug%22:%22singapore%22%2C%22place_type%22:%22country%22%2C%22place_id%22:%2285632605%22%2C%22is_online%22:false}; mgrefby=; mgref=typeins; session=identifier%3D47f3e78cf430460f8fb74da31f2a8908%26issuedTs%3D1738329556%26originalTs%3D1738328579%26s%3Daf9eedaea7808b1a9eb947a8a7f8cf6f200c695759ddeb65ddcc9600d842115b; stableId=afb5124c-260c-4bc7-beba-08c8d3be761d; SP=AGQgbbk8Fis1dSZY4qPJwRqX4y2OmUu98deUyLJ4eMbOcJFlbPf7DQItfotvvbGoq5jEq3Vlm2c8QETeGGarvecooZFosonSR4knJxid7Tlr72RMh17ConF1cwGBLKeQmAqMzgfMa6dVOet4zZ8bAKsUAFlBSn1B1tpD-cDcRzQWOng-JMBpNDxN6PklaM9_YGAe4QIWkhKTeHCTO3RHiaC68VskjBKStt7dR_UsQYTtOfwBnlHNd4g; _dd_s=rum=0&expire=1738330469746',
        'priority': 'u=0, i',

        'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Brave";v="132"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'sec-gpc': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
    }
    event_response = requests.get(pass_links, cookies=cookies, headers=headers)
    code = BeautifulSoup(event_response.text, 'html.parser')
    event_link = [x.find('a')['href'] for x in code.findAll('section',{'class':'event-card-details'})]
    return event_link

all_event_pages_links = thread_map(get_all_event_urls, pagination_urls[:4] )

loading_message = st.empty()
loading_message.markdown("<h4 style='text-align: center; color: #3498db;'>🔄 Loading events...</h4>", unsafe_allow_html=True)

# Simulating a time-consuming operation (replace this with your actual code)
time.sleep(4)  # Simulate a delay (3 seconds)

one_d_event_links = list(set(j for i in all_event_pages_links for j in i))
st.markdown(
    f"<h3 style='text-align: center; font-weight: bold; color: #FF5733; font-size: 28px;'>"
    f"🔥 Wow! Found {len(one_d_event_links)} Events 🔥</h3>",
    unsafe_allow_html=True
)
loading_message.empty()


def get_inner_page_data(pass_links):
    headers_2 = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "DNT": "1",
        "Upgrade-Insecure-Requests": "1"
    }
    inner_page_link = requests.get(pass_links, headers=headers_2)
    inner_page_code = BeautifulSoup(inner_page_link.text, 'html.parser')

    # get the data from inner pages
    data_dict = {}
    try:
        name_event = inner_page_code.find('h1', {'class': 'event-title css-0'}).get_text(strip=True).capitalize()
        data_dict['Event Name'] = name_event
    except:
        data_dict['Event Name'] = ''

    try:
        event_date_time = inner_page_code.find('span', {'class': 'date-info__full-datetime'}).get_text(strip=True)
        data_dict['Event Date'] = event_date_time

    except:
        data_dict['Event Date'] = ''

    try:
        event_location = inner_page_code.find('div', {'class': 'location-info__address'}).get_text(strip=True).replace(
            'Show map', '')
        data_dict['Event Location'] = event_location
    except:
        data_dict['Event Location'] = ''

    try:
        event_duration = inner_page_code.find('ul', {'data-testid': 'highlights'}).get_text(strip=True)
        data_dict['Event Duration'] = event_duration
    except:
        data_dict['Event Duration'] = ''

    try:
        event_description = inner_page_code.find('ul', {'data-testid': 'highlights'}).find_next('p').get_text(
            strip=True)
        data_dict['Event Description'] = event_description
    except:
        data_dict['Event Description'] = ''

    try:
        event_tags = ' | '.join([x.get_text(strip=True) for x in inner_page_code.findAll('li', {'class': 'tags-item'})])
        data_dict['Event Tags'] = event_tags
    except:
        data_dict['Event Tags'] = ''

    data_dict['Event Url'] = pass_links
    data_dict['Country'] = 'Singapore'

    return data_dict

all_page_data = thread_map(get_inner_page_data, one_d_event_links)
df = pd.DataFrame(all_page_data)

# Display the DataFrame with some custom styling

loading_message = st.empty()
loading_message.markdown(
    f"<h4 style='text-align: center; color: #3498db;'>🔄 Getting data from {len(one_d_event_links)} links </h4>"
    , unsafe_allow_html=True
)
st.markdown(
    "<h2 style='text-align: center; font-weight: bold; color: #FF5733;'>"
    "⏳ When data keeps you waiting, it's fun 😄"
    "</h2>",
    unsafe_allow_html=True
)

st.markdown(
    "<h2 style='text-align: center; color: #2ecc71;'>📊 Data Overview</h2>",
    unsafe_allow_html=True
)
st.dataframe(df)

csv = df.to_csv(index=False)
st.write(f"This is the shape of are data set {df.shape}")

# Create a download button
st.download_button(
    label="Download CSV",
    data=csv,
    file_name="data.csv",
    mime="text/csv"
)


