# 📝 Lessons Learned & Patterns

## 1. 🤖 GitHub Actions Node.js Deprecation
- **상황**: GitHub 액션 중 `actions/checkout@v3` 등이 Node 20의 차기 EOL(End of Life) 문제로 경고/에러 발생.
- **해결 패턴**: 
  1. 액션 버전을 최신(`v4`, `v5` 등)으로 올림.
  2. `env: FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: true`를 추가하여 선제적으로 인프라 버전 강제 적용.

## 2. 📉 yfinance 429 에러 해결 및 스크래핑 전략
- **상황**: `yfinance` 환율 조회가 잦은 빈도로 `429 Too Many Requests`로 막히고 Session User-Agent 우회도 실패함. 최근 야후의 보안 정책.
- **해결 패턴**: 불안정한 라이브러리 우회만 고집하지 않고, `requests`와 `BeautifulSoup`을 사용해 구글 파이낸스 등을 직접 크롤링하는 쪽으로 변경하는 것이 훨씬 직관적이고 지속 가능한 해결책임.
