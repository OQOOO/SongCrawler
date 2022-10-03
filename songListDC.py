import requests
import time
from bs4 import BeautifulSoup



# . : 하나의 문자를 의미
# ^ : 문자열의 시작 (de -> desk, destination (o) | fade (x))
# $ : 문자열의 끝 (se -> case, base (o) | face (x))



def resSoup(url): # url -> html 전환 함수



    # 유저에이전트         ↓
    head = {"user-Agent":""}




    res = requests.get(url, headers= head)
    soup = BeautifulSoup(res.text, "html.parser")
    return soup

def searchSongDC(first, last):
    pageCount = first; songCount = 0
    textList = []
    musicList = []
    for i in range(first, last + 1):                                # url의 페이지 지정을 담당하는 부분을 이용해 원하는만큼의 페이지 가져오기(10 이하로)
        pageText = f"------------ {pageCount}페이지 ------------"
        print(pageText)
        textList.append(pageText)

        url = f"https://search.dcinside.com/post/p/{i}/sort/latest/q/.EC.A7.80.EB.93.A3.EB.85.B8"
        soup = resSoup(url)
        posts = soup.find_all("a", attrs={"class":"tit_txt"})       # 게시물의 url을 가지고있는 a class="tit_txt"요소를 모두 찾아 posts배열로 만들기

        for j in posts:                                             # posts 배열의 요소에서 url과 글제목 추출하고, 게시물 url은 다시한번 html로 전환
            postHref = j['href']
            postText = j.text                                  
            p_soup = resSoup(postHref)                              
            
            page = p_soup.find("embed", attrs={"scr":''})           # 게시물 html 문서 내부에 유튜브 링크 주소를 포함한 인자를 찾아 배열의 형태로 만들기
            tPage = str(page)
            tList = tPage.split()

            for k in tList:                                         # 배열에서 원하는 인자 찾아서 알맞은 형태로 가공하여 배열에 저장
                if k[:3] == "src":                                  
                    print(postText)
                    link1 = k[5:-1]
                    link2 = link1[:24]

                    songCount += 1
                    textList.append(str(songCount)+'. '+postText)
                    musicList.append(link2 + 'watch?v=' + link1[30:])
        
        pageCount += 1
        time.sleep(0.1) #dcinside ip차단 방지용 딜레이
    return textList, musicList