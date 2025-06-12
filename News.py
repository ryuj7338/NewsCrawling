from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

#  크롬 옵션 설정
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(options=options)

query = "경호"
num_pages = 3
news_data = []

driver = webdriver.Chrome()

for page in range(1, num_pages + 1):
    start = (page - 1) * 10 + 1
    url = f"https://search.naver.com/search.naver?where=news&query={query}&start={start}"
    driver.get(url)

    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[href^="http"]')))

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # 기사 블록 기준으로 전체 선택
    article_blocks = soup.select('div.sds-comps-base-layout')

    for block in article_blocks:
        # 제목 및 링크 추출
        title_tag = block.select_one('span.sds-comps-text-type-headline1')
        link_tag = title_tag.find_parent('a') if title_tag else None

        # 요약
        summary_tag = block.select_one('span.sds-comps-text-type-body1')

        # 썸네일 이미지
        img_tag = block.find('img')

        title = title_tag.get_text(strip=True) if title_tag else ''
        link = link_tag['href'] if link_tag and link_tag.has_attr('href') else ''
        summary = summary_tag.get_text(strip=True) if summary_tag else ''
        image = img_tag['src'] if img_tag and img_tag.has_attr('src') else ''

        # 제목 있는 경우만 추가
        if title:
            news_data.append((title, link, summary, image))

    time.sleep(1)

driver.quit()

# 결과 출력
print("===== 뉴스 정보 모음 =====")
for idx, (title, link, summary, image) in enumerate(news_data, 1):
    print(f"{idx}. {title}")
    print(f" 링크: {link}")
    print(f" 요약: {summary}")
    print(f" 썸네일: {image}")
    print("-" * 80)