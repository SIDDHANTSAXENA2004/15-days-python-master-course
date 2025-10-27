# #requests and beautifulsoup

# #requests.get(URL)

# #response.text ->raw html

# #BeautifulSoup(response.text,"html.parser")

# #soup.find(),soup.find_all()


# import requests
# from bs4 import BeautifulSoup

# URL="https://en.wikipedia.org/wiki/Web_scraping"

# headers={
#     "User-Agent":"Mozilla/5.0"
# }

# response=requests.get(URL,headers=headers)

# if response.status_code==200:
#     raw_html=response.text
#     soup=BeautifulSoup(raw_html,"html.parser")
#     # print(soup.prettify())
#     # print(soup.title)
#     # page_title=soup.title.text
#     # print(page_title)
#     # page_title=soup.title.string
#     # print(page_title)
#     # all_paragraphs=soup.find_all("p")
#     # print(len(all_paragraphs))
#     # # print(all_paragraphs[:3])
#     # for paragraph in all_paragraphs[:3]:
#     #     # print(paragraph.text.strip())
#     #     print(paragraph.get_text(strip=True))

    
#     # frist_paragraph=soup.find("p")
#     # if frist_paragraph:
#     #     print(frist_paragraph.text.strip())
#     main_content=soup.find(id="mw-content-text")
#     if main_content:
#         content_paras=main_content.find_all("p")
#         print(len(content_paras))

#         references=main_content.find(class_="references")
#         if references:
#             # lis=references.find_all("li")
#             # print(len(lis))
#             # for i,li in enumerate(lis):
#             #     print(i,li.text.strip()+"\n")
#             links=references.find_all("a")
#             print(len(links))

#             for i,link in enumerate(references.find_all("a")):
#                 print(i,link.text.strip(),link.get("href"),link["href"],"\n")
#         else:
#             print("references not found")
        
#     else:
#         print("main content not found")
# else:
#     print("error")

import requests
from bs4 import BeautifulSoup

URL="https://en.wikipedia.org/wiki/Web_scraping"

headers={
    "User-Agent":"Mozilla/5.0"
}

response=requests.get(URL,headers=headers)

final_text=""

if response.status_code==200:
    soup=BeautifulSoup(response.text,"html.parser")

    page_title=soup.title.text
    final_text+=page_title+"\n"

    main_content=soup.find(id="mw-content-text")
    if main_content:
       all_text=main_content.get_text(separator="\n",strip=True)
       final_text+=all_text

       with open("scrped_knowledge.txt","w",encoding="utf-8") as file:
           file.write(final_text)
    else:
        print("main content not found")

else:
    print("error failes to get a response from website")