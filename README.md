# 💼 잡코리아 채용 기술 분석 프로젝트 (Web Crawling & Visualization)

크롤링을 활용해 **잡코리아 채용 공고**를 수집하고, 기업이 요구하는 **핵심 기술 스택**을 분석하는 프로젝트입니다.  
정적 크롤링(BeautifulSoup)과 동적 크롤링(Selenium)을 이용하며, **스킬 빈도 시각화 + 워드클라우드**를 자동 생성합니다.

---

## 📅 프로젝트 기간
- 2025.02.18 ~ 2025.02.24

## 🛠️ 사용 기술
- Python, Selenium, BeautifulSoup, WordCloud, Pandas, Matplotlib

---

## 📁 폴더 구조

```
jobkorea_skill_project/
├── data/                             # 데이터 및 마스크 이미지
│   ├── cloud.png                     # 워드클라우드 마스크 이미지
│   └── jobkorea_skill_frequency.csv  # 스킬 빈도 데이터
├── images/                           # 시각화 결과 이미지
│   ├── skill_graph_.png              # 키워드별 스킬 빈도 그래프
│   └── wordcloud_.png                # 키워드별 워드클라우드 이미지
├── jobkorea_메모.txt                  # HTML 구조 분석 참고 메모
├── jobkorea.py                       # 크롤링 + 시각화 전체 코드
└── README.md                         # 프로젝트 설명 문서
```

---

## ▶️ 실행 방법

```bash
pip install pandas matplotlib selenium beautifulsoup4 wordcloud koreanize-matplotlib
```

이후 아래 Python 스크립트를 실행합니다.

```bash
python jobkorea.py
```

---

## ⚙️ 실행 시 자동으로 수행되는 작업

- 키워드별 채용공고 크롤링
- HTML 구조 분석을 통한 스킬 태그 추출
- 상위 기술 스택 추출 → 바 차트 및 워드클라우드 시각화

### 🔑 기본 크롤링 키워드
> 빅데이터, 인공지능, Python, SQL, 머신러닝, 딥러닝, 자연어처리

---

## 💬 프로젝트 회고
- ✅ 직접 URL 패턴을 분석하고, 스크래핑 구조를 잡아나가며 크롤링의 전체 흐름을 체득함
- ✅ HTML 구조가 예외적인 경우에도 대응 가능한 다중 선택자 처리 학습
- ✅ 단어 빈도 기반의 워드클라우드 시각화를 통해 기업이 진짜 원하는 기술 인사이트를 시각화
- ✅ 크롤링뿐 아니라 분석, 시각화까지 자동화하며 파이썬 기반 크롤링 파이프라인 구현

---

## 👩‍💻 제작자

- **이름:** Emily  
- **역할:** 전체 프로젝트 구현 (크롤링, 전처리, 시각화, 메모 분석 포함)

---

## 🔗 프로젝트 링크

🧾 [프로젝트 상세 노션 페이지](https://yeonghyekim.notion.site/1a4e2859370c80b19aecc73ec02be810?pvs=4)  