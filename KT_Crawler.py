import requests
from bs4 import BeautifulSoup
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",      
    user="root",           
    password="",   
    database="WebKT",  
    port=3306
)
cursor = conn.cursor()
print("Kết nối MySQL thành công")


category_url = "https://baomoi.com/kinh-te/trang162.epi"
headers = {"User-Agent": "Mozilla/5.0"}


response = requests.get(category_url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    
    articles = soup.find_all("h3", class_="font-semibold block")

    for article in articles:
        link_tag = article.find("a")
        if link_tag and "href" in link_tag.attrs:
            title = link_tag.get_text(strip=True)
            url = link_tag["href"]

            if not url.startswith("http"):  
                url = "https://baomoi.com" + url

            
            article_response = requests.get(url, headers=headers)
            if article_response.status_code == 200:
                article_soup = BeautifulSoup(article_response.text, "html.parser")
                paragraphs = article_soup.find_all("p",class_="text")
                content = "\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))

                
                sql = "INSERT INTO baiviet (title, url, content) VALUES (%s, %s, %s)"
                cursor.execute(sql, (title, url, content))
                conn.commit()

                print(f" Đã lưu: {title}")

cursor.close()
conn.close()
print("Hoàn tất!")
