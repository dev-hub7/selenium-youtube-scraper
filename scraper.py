from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd

# to install chromium & chromedriver
# https://jovian.ai/birajde9/replit-add-chromdriver-chromium

YOUTUBE_TRENDING_URL = 'https://www.youtube.com/feed/trending'

def init_driver():
  options = Options()
  options.add_argument('--no-sandbox')
  options.add_argument('--disable-dev-shm-usage')
  options.add_argument('--headless')

  driver = webdriver.Chrome(options=options)
  return driver

def get_videos(driver):
  driver.get(YOUTUBE_TRENDING_URL)
  # print(driver.title)
  videos = driver.find_elements(By.TAG_NAME, 'ytd-video-renderer')
  # print(f"{len(videos)} videos were found inside func")
  return videos

def parse_vidoe(video):
      title_el = video.find_element(By.ID, 'video-title')
      desc = video.find_element(By.ID, 'description-text').text
      img = video.find_element(By.TAG_NAME, 'img').get_attribute('src')
      channel = video.find_element(By.CLASS_NAME, 'ytd-channel-name').text
      # print(channel)
      
      return {
              "title": title_el.text,
              "url": title_el.get_attribute('href'), 
              'thumbnail_url': img,
              "description": desc,
              "channel name": channel
      }

if __name__ == "__main__":
  driver = init_driver()

  print('Start Scraping...')
  try:
    # fetch trending videos
    videos = get_videos(driver)
    print(f"{len(videos)} videos were found")
  
    # parsing first video [title, url, thumbnail_url, desc, views, uploaded, channel]
    vid_list = [parse_vidoe(video) for video in videos[:10]]
    # for video in videos:
    #   vid_list.append(parse_vidoe(video))

    # print(vid_list)
    
    print('session finished')
    driver.quit()

    # save data into a csv file
    vids_df = pd.DataFrame(vid_list)
    vids_df.to_csv('trending.csv', index=False)
    print(vids_df)
    
  except Exception as e:
    print('error occured ', e)
    driver.quit()
      