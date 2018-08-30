# 导入相关库
import requests
import pandas as pd
from bs4 import BeautifulSoup

# 第一步：请求数据
def get_data():
    url = 'https://book.douban.com/latest'
    # headers 里面大小写均可，用来伪装浏览器
    headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/68.0.3440.106 Safari/537.36"}

    data = requests.get(url, headers=headers)

    # print(data.text)

    return data


# 第二步：解析数据
def parse_data(data):
    soup = BeautifulSoup(data.text, 'lxml')
    # print(soup)

    # 观察到网页上书籍按照左右两边分布，按照标签分别提取
    books_left = soup.find('ul', {'class': 'cover-col-4 clearfix'})
    books_left = books_left.find_all('li')

    books_right = soup.find('ul', {'class': 'cover-col-4 pl20 clearfix'})
    books_right = books_right.find_all('li')

    books = list(books_left) + list(books_right)

    # 创建不同信息列表
    img_urls = []
    titles = []
    ratings = []
    authors = []
    details = []

    # 对每一个图书区块进行相同的操作，获取图书信息
    for book in books:
        # 图书封面图片 URL 地址
        img_url = book.find_all('a')[0].find('img').get('src')
        img_urls.append(img_url)

        # 图书标题
        title = book.find_all('a')[1].get_text()
        titles.append(title)

        # 评价星级
        rating = book.find('p', {'class': 'rating'}).get_text()
        rating = rating.replace('\n', '').replace(' ', '')
        ratings.append(rating)

        # 作者及出版信息
        author = book.find('p', {'class': 'color-gray'}).get_text()
        author = author.replace('\n', '').replace(' ', '')
        authors.append(author)

        # 图书简介
        detail = book.find_all('p')[2].get_text()
        detail = detail.replace('\n', '').replace(' ', '')
        details.append(detail)

    print('img_urls: ', img_urls)
    print('titles: ', titles)
    print('ratings: ', ratings)
    print('authors: ', authors)
    print('details: ', details)

    return img_urls, titles, ratings, authors, details


# 第三步：存储数据
def save_data(img_urls, titles, ratings, authors, details):

    latest_books = pd.DataFrame()

    latest_books['img_urls'] = img_urls

    latest_books['titles'] = titles

    latest_books['ratings'] = ratings

    latest_books['authors'] = authors

    latest_books['details'] = details

    latest_books.to_csv('latest_books.csv', index=None)


# 开始爬取信息
def run():
    print('开始爬取信息... ...\n')

    data = get_data()

    img_urls, titles, ratings, authors, details = parse_data(data)

    save_data(img_urls, titles, ratings, authors, details)

    print('\n爬取信息结束')

if __name__ == '__main__':
    run()
