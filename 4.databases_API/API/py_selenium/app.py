import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import EdgeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import tabulate
import streamlit as sl


options = EdgeOptions()
options.add_argument('--headless')

def get_youtube_channel_data():
    channel = input('What is the channel name? ')
    max_scrolls = int(input('How many pages you want to scrap? ')) - 1
    with webdriver.Edge(options=options) as driver:
        driver.get('https://www.youtube.com/@' + channel + '/videos')

        # Wait until the main contents container is present
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.ID, "contents")))
        time.sleep(2)

        scroll_count = 0
        last_height = driver.execute_script("return document.documentElement.scrollHeight")

        while scroll_count <= max_scrolls:
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            time.sleep(3)
            new_height = driver.execute_script("return document.documentElement.scrollHeight")

            # If no new content is loaded, break early
            if new_height == last_height:
                break

            last_height = new_height
            scroll_count += 1

        try:
            # Get all contents container
            contents = driver.find_element(By.ID, 'contents')

            # Extract video titles and URLs
            videos_titles = contents.find_elements(By.ID, 'video-title-link')
            titles = []
            urls = []
            for video in videos_titles:
                title_text = video.text  # Just the title text
                url_text = video.get_property('href')
                titles.append(title_text)
                urls.append(url_text)

            # Extract video metadata: views and publish dates
            views = []
            dates = []
            video_metadata = contents.find_elements(By.ID, 'metadata-line')
            for metadata in video_metadata:
                span_tags = metadata.find_elements(By.TAG_NAME, 'span')
                if len(span_tags) >= 2:
                    views.append(span_tags[0].text)
                    dates.append(span_tags[1].text)
                else:
                    views.append("N/A")
                    dates.append("N/A")

            # Combine extracted data into lists for tabulation and JSON output
            results = []
            results_json = []
            for title, url, view, date in zip(titles, urls, views, dates):
                results.append([title, url, view, date])
                results_json.append({
                    "title": title,
                    "url": url,
                    "views": view,
                    "date": date
                })

            data_table = tabulate.tabulate(results, headers=['Title', 'URL', 'Views', 'Date of Publish'],
                                           tablefmt='pretty', stralign='left', numalign='left')

            # Save table to a text file
            with open(f'{channel}_data.txt', 'w', encoding='utf-8') as file:
                file.write(data_table)

            # Save results in JSON format
            with open(f'{channel}_data.json', 'w', encoding='utf-8') as json_file:
                json.dump(results_json, json_file, indent=4, ensure_ascii=False)
        except Exception as e:
            print('The page was not found or an error occurred:', e)


if __name__ == '__main__':
    get_youtube_channel_data()
