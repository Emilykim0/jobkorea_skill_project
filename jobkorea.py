import time                      # 차단방지를 위해 크롤링 중간중간 sleep()을 이용해 요청을 쉬게하기
import pandas as pd              # Dataframe 형태로 저장 및 분석
from selenium import webdriver   # 크롬을 자동으로 실행하여 웹사이트에 접속
from selenium.webdriver.common.by import By                      # Selenium에서 HTML 요소를 찾을 때 사용하는 방식(Selector Type)을 지정하는 클래스
from selenium.webdriver.support.ui import WebDriverWait          # 페이지가 완전히 로딩될 때까지 대기하는 기능
from selenium.webdriver.support import expected_conditions as EC # Selenium에서 특정 요소가 로딩될 때까지 기다리는 기능
from bs4 import BeautifulSoup    # HTML을 파싱하여 원하는 정보 추출
from collections import Counter  # 단어 빈도수를 계산하는 라이브러리
from wordcloud import WordCloud  # 단어 빈도수를 기반으로 워드 클라우드 생성
import matplotlib.pyplot as plt  # 데이터 시각화(그래프 그리기)
import numpy as np               # 워드클라우드용 마스크 이미지를 처리할 때 사용
from PIL import Image            # 이미지파일(clound.png)을 불러와서 워드 클라우드 마스크로 사용
import koreanize_matplotlib      # 한글 폰트 문제 해결


class JobKoreaSkillScraper:
    def __init__(self, keywords, max_pages=2, max_jobs=10):
        self.base_url = "https://www.jobkorea.co.kr/Search/?stext="
        self.keywords = keywords
        self.max_pages = max_pages
        self.max_jobs = max_jobs
        self.driver = webdriver.Chrome()
        self.all_skills = {keyword: [] for keyword in keywords}
        self.skill_data = []


    def get_job_links(self, keyword):
        """
        키워드 검색 후 잡코리아 채용공고 링크 수집하기
        """
        job_links = [] # 각 공고 링크를 담을 리스트
        for page in range(1, self.max_pages + 1): # 1페이지 ~ max_pages까지 반복
            search_url = f"{self.base_url}{keyword}&tabType=recruit&Page_No={page}"
            self.driver.get(search_url) # 잡코리아 해당페이지를 크롬에서 실행하기
            time.sleep(3)

            soup = BeautifulSoup(self.driver.page_source, 'html.parser') # HTML 분석하기 위해
            job_elements = soup.select("a.information-title-link.dev-view") # a 태그에 class가 information-title-link.dev-view인 부분의 href에 공고 링크가 있음

            # 중간점검(디버깅용)
            print(f"[{keyword}] 페이지 {page} - {len(job_elements)}개 공고 검색됨")

            for job in job_elements[:self.max_jobs]: # 각 <a> 태그에 있는 href에서 공고링크 부분 가져와서 리스트에 url 저장하기
                link = "https://www.jobkorea.co.kr" + job["href"]
                job_links.append(link)
        
        # 중간 점검(디버깅용)
        print(f"[{keyword}] 총 {len(job_links)}개 공고 링크 수집 완료")
        return job_links # 각 키워드의 공고 링크 리스트를 반환!


    def scrape_skill_tags(self, job_link):
        """
        개별 채용공고에서 '스킬' 항목 크롤링하기
        """
        self.driver.get(job_link) # 공고 상세페이지에 접속하기

        try: # 페이지가 완전히 로딩될 때까지 기다리도록 하는 코드...
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        except:
            print(f"[WARNING] {job_link} 로딩 실패")
            return []

        time.sleep(2)
        soup = BeautifulSoup(self.driver.page_source, 'html.parser') # HTML 분석하기 위해

        skills = []

        # 디버깅용: 해당 페이지 HTML 확인 (문제가 발생하는 경우)
        if not soup:
            print(f"⚠️ [ERROR] {job_link} HTML 파싱 실패")
            return []

        # 1. `dl.tbList` 기반으로 크롤링
        skill_section = soup.find("dl", class_="tbList")
        if skill_section:
            dt_tags = skill_section.find_all("dt") # <dt>에 '스킬'이라고 적힌 부분을 찾아야해
            dd_tags = skill_section.find_all("dd") # '<dt> 스킬' 부분에있는 dd의 text가 필요해

            for dt, dd in zip(dt_tags, dd_tags): # zip(): 같은 인덱스 원소들끼리 짝지어줌
                if "스킬" in dt.text.strip():
                    skills = [s.strip() for s in dd.text.split(",")]
                    break

        # 2. `dl.tbList`가 없을 경우, `div.tbList`를 찾기
        if not skills:
            alt_skill_section = soup.find("div", class_="tbList")
            if alt_skill_section:
                skill_text = alt_skill_section.text.strip()
                skills = [s.strip() for s in skill_text.split(",")]

        return skills # 각 공고사이트에 있는 스킬들이 담긴 리스트를 반환


    def collect_skills(self):
        """
        모든 키워드에 대해 채용공고에서 '스킬' 항목 수집
        """
        for keyword in self.keywords:
            # 특정 키워드 크롤링 시작을 알리기-지금 어느 부분 진행 중인지 알기 위해서..(디버깅?)
            print(f"\n키워드 [{keyword}] 스킬 크롤링 시작...") 
            job_links = self.get_job_links(keyword) # 채용공고링크가 담겨있는 리스트 가져오기

            skills_list = []
            for idx, job_link in enumerate(job_links): # job_links에 있는 공고 사이트 하나씩 - 반복문
                # 지금 몇번째 공고의 크롤링을 시작했는지 알기 위해서..(디버깅?)
                print(f"[{keyword}] {idx+1}/{len(job_links)}번째 공고 크롤링 중... ({job_link})") 
                skills = self.scrape_skill_tags(job_link) # 각 공고 사이트에 있는 스킬 항목이 저장된 리스트 가져오기

                if skills: # skills가 하나라도 있는 경우
                    # 대충 어떤 키워드들이 저장되고 있는지 확인하기 위해
                    print(f"[{keyword}] 스킬 {len(skills)}개 추출됨 → {skills[:5]} (일부 미리보기)")
                    # append는 리스트 그 자체를 하나의 요소로 추가됨. 리스트 각 요소들을 하나씩 다른 리스트의 원소로 넣기 위해서는 extend() 사용해야함.
                    # all_skills[keyword] -> values 즉 빈 리스트에 해당함 -> 마찬가지로 extend()로 리스트에 원소 넣기!
                    self.all_skills[keyword].extend(skills) 
                    skills_list.extend(skills) 
                else: 
                    print(f"[{keyword}] 스킬 정보 없음") # skilss가 하나도 없어서 False가 되는 경우

            # value_counts(): 내림차순으로 정렬됨.
            skill_counts = pd.Series(skills_list).value_counts()  # 모든 단어의 빈도수 계산, value_counts(): 내림차순으로 정렬됨
            filtered_counts = skill_counts[~skill_counts.index.isin(self.keywords)]  # 검색 키워드 제외, '~'은 not의 의미를 가짐.
            filtered_counts = filtered_counts.head(10)  # 검색 키워드 제외 후 상위 10개 선택

            df = pd.DataFrame({"단어": filtered_counts.index, "빈도수": filtered_counts.values})
            df["키워드"] = keyword  
            self.skill_data.append(df)
            # print(df) # 컬럼이 단어, 빈도수, 키워드 인 데이터프레임 생성됨

        self.driver.quit()
        print("\n모든 키워드 크롤링 완료!")


    def plot_top_skills(self):
        """
        키워드별 상위 10개 스킬 빈도수 그래프 생성 (검색 키워드는 제외)
        """
        for keyword in self.all_skills.keys():
            df = pd.DataFrame({"단어": [], "빈도수": []})  # 빈 DataFrame 기본값 설정
            for data in self.skill_data:
                if not data.empty and "키워드" in data.columns and data["키워드"].iloc[0] == keyword:
                    df = data # 조건에 맞으면 그 DataFrame을 df로 저장하기
                    break

            if df.empty or df["단어"].empty:
                print(f"{keyword} 키워드에 대한 스킬 데이터가 부족하여 그래프 생략")
                continue

            # 그래프 그리기
            plt.figure(figsize=(12, 6))
            plt.bar(df["단어"], df["빈도수"], color="skyblue")
            plt.xticks(rotation=45)
            plt.title(f"{keyword} 관련 채용공고의 스킬 요구 빈도수")
            plt.xlabel("스킬")
            plt.ylabel("빈도수")

            filename = f"skill_graph_{keyword}.png"
            plt.savefig(filename, dpi=300)
            print(f"스킬 그래프 저장 완료: {filename}")


    def generate_wordclouds(self):
        """
        키워드별 WordCloud 생성 및 저장 (cloud.png 마스크 적용, 상위 20개 단어만 사용)
        """
        try:
            img_mask = np.array(Image.open("cloud.png"))  # 마스크 이미지 불러오기
        except FileNotFoundError:
            print("[ERROR] cloud.png 파일을 찾을 수 없습니다. 기본 형태로 WordCloud를 생성합니다.")
            img_mask = None  # 마스크 없이 기본 형태로 생성

        for keyword, skills in self.all_skills.items():
            if not skills:
                print(f"{keyword} 키워드에 대한 스킬 데이터가 부족하여 WordCloud 생략")
                continue

            # 키워드 리스트에서 검색어(키워드) 삭제
            filtered_skills = [skill for skill in skills if skill not in self.keywords]

            # 단어 빈도수 계산 (상위 20개 단어만 사용)
            word_freq = dict(Counter(filtered_skills).most_common(20))

            # wordcloud 만드는 코드!
            wordcloud = WordCloud(
                font_path="malgun.ttf",
                width=800, height=600,
                background_color="white",
                max_font_size=200,
                colormap='inferno',
                repeat=True,
                mask=img_mask
            ).generate_from_frequencies(word_freq) # word_freq: 상위 20개 단어

            # WordCloud 시각화 및 저장
            plt.figure(figsize=(10, 5))
            plt.imshow(wordcloud, interpolation="bilinear")
            plt.axis("off")
            filename = f"wordcloud_{keyword}.png"
            plt.savefig(filename, dpi=300)
            print(f"WordCloud 저장 완료: {filename}")


if __name__ == "__main__":
    keywords = ["빅데이터", "인공지능", "Python", "SQL", "머신러닝", "딥러닝", "자연어처리"]
    max_pages = 3
    max_jobs = 20

    scraper = JobKoreaSkillScraper(keywords, max_pages, max_jobs)
    scraper.collect_skills()
    scraper.plot_top_skills()
    scraper.generate_wordclouds()  # 워드클라우드 생성

# keywords = ["빅데이터", "인공지능", "Python", "SQL", "머신러닝", "딥러닝", "자연어처리"]