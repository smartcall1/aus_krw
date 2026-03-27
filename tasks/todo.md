# 호주 달러 환율 알림 봇 수정 작업

## 1. 개요
* GitHub Actions Node.js 20 지원 중단(Deprecation) 에러 수정
* 환율 API (yfinance) 429 Too Many Requests 발생 에러 수정

## 2. 체크리스트
- [x] `.github/workflows/main.yml` 수정
  - `actions/checkout` 버전을 `v4`로, `actions/setup-python` 버전을 `v5`로 업데이트
  - Node 24 환경 변수 `FORCE_JAVASCRIPT_ACTIONS_TO_NODE24` 명시적 설정
- [x] `main.py` 및 `requirements.txt` 수정
  - `yfinance` 모듈 제거 (`Too Many Requests`의 근본적인 차단 이슈)
  - `requests`와 `BeautifulSoup`을 사용하여 구글 파이낸스를 직접 크롤링하는 방식으로 교체
- [x] 변경 사항 적용 및 스크립트 실행 테스트 완료
- [x] 작업 완료 후 리뷰 기록

## 3. 리뷰
- **문제 원인**: 
  - Github Actions: Node.js 20 EOL 대응 정책으로 구버전 액션들(checkout@v3, setup-python@v4) 실행 시 강제 경고 발생.
  - 환율 봇 차단: 야후 파이낸스가 보안 강화를 이유로 파이썬 스크립트 등 비정상적인 접근에 대해 429 Too Many Requests 에러를 던지며 접근을 차단함.
- **해결 방법**:
  - `main.yml`에서 Action들의 최신 버전을 적용하고, 명시적으로 Node 24 환경 지원 변수(`FORCE_JAVASCRIPT_ACTIONS_TO_NODE24`)를 설정하여 워크플로우를 최신화했습니다.
  - 파이썬 크롤링 로직에서 `yfinance` 라이브러리를 제거하고, 구글 파이낸스(`https://www.google.com/finance/quote/AUD-KRW`)의 환율 정보를 직접 스크래핑하도록 구조를 개편했습니다. 우회 차단 위험이 없어지면서 현재 정상적으로 호주 환율이 출력됨을 확인했습니다 (예: 1039.06).
