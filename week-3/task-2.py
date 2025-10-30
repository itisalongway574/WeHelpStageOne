import urllib.request as request
from bs4 import BeautifulSoup
# 加入爬蟲的時間延遲
import time
import csv

# 首頁連結
url_latest = "https://www.ptt.cc/bbs/Steam/index.html"
base_url = 'https://www.ptt.cc'

# 儲存所有要爬取的頁面連結
url_list = []

# 儲存所有頁數的post_data
result = []


def get_url_previous(url, page_num):  # 遞迴爬取所需頁數的連結
    global url_list
    # 每次執行時都先清空
    url_list = []

    current_url = url
    # 儲存跑了幾頁
    count = 0

    while count < page_num:
        url_list.append(current_url)
        count += 1
        if count >= page_num:
            break

        # 根據current_url去獲取下一頁的連結
        req = request.Request(current_url, headers={
                              'User-Agent': 'Mozilla/5.0'})
        with request.urlopen(req) as response:
            html_content = response.read().decode('utf-8')
            # 當前頁面的HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        # 找出current_url對應的上一頁連結
        btn_group = soup.find(
            'div', class_='btn-group btn-group-paging').find_all('a')
        for btn in btn_group:
            if btn.text == '‹ 上頁':
                # 將獲取的url取代原本的current_url，然後跑下一個迴圈
                current_url = base_url + btn['href']
                break
        time.sleep(1)  # 延遲1秒才會進行下一頁的爬蟲


get_url_previous(url_latest, 3)


def get_post_data(url):  # 爬取當前頁數的post_data

    req = request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with request.urlopen(req) as response:
        html_content = response.read().decode('utf-8')
    soup = BeautifulSoup(html_content, 'html.parser')

    posts = soup.find_all('div', class_='r-ent')
    for post in posts:
        global result
        post_data = {}

        # 先判斷該文章是否是被刪除的狀態
        # 如果是刪除的狀態會找不到href
        post_a_tag = post.find('div', class_='title').find('a')
        if post_a_tag:
            # 取得文章連結
            post_url = post.find('div', class_='title').find('a')['href']
            # post_data['url'] = 'https://www.ptt.cc' + post_url

            post_title = post.find('div', class_='title').find('a').text
            post_data['title'] = post_title

            # 進到對應的頁面
            post_req = request.Request(
                'https://www.ptt.cc' + post_url, headers={'User-Agent': 'Mozilla/5.0'})
            with request.urlopen(post_req) as response:
                html_content = response.read().decode('utf-8')
            post_soup = BeautifulSoup(html_content, 'html.parser')

            # 找出日期對應的article-metaline
            article_metaline = post_soup.find_all(
                'div', class_='article-metaline')

            # 遞迴找出裡面有「時間」」的article-metaline
            post_date = None
            for metaline in article_metaline:
                if metaline.find('span', class_='article-meta-tag').text == '時間':
                    # print('找到時間')
                    post_date = metaline.find(
                        'span', class_='article-meta-value').text
                    if post_date:
                        post_data['date'] = post_date
                    # 處理沒有找到時間資料的情況
                    else:
                        post_data['date'] = ''
                    break

            # 取得讚數
            like_span = post.find('div', class_='nrec').find('span')
            like_count = None
            # 判斷有無like
            if like_span:
                like_count = like_span.text
            else:
                like_count = '0'
            post_data['like'] = like_count

            result.append(post_data)
        else:
            # 如果找不到a-tag，那就代表該文章是被刪除的狀態
            pass


for url in url_list:
    get_post_data(url)

# print(result)


# 定義CSV欄位名稱
articles_csv_field = ['title', 'like', 'date']
articles_csv_name = 'articles.csv'

# 產生CSV檔案
with open(articles_csv_name, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=articles_csv_field)
    writer.writerows(result)
