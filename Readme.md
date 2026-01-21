# 🦘 KRW/AUD 환율 알림 봇 (Exchange Rate Bot)

1시간마다 호주 달러(AUD) 대비 한국 원화(KRW) 환율을 체크하여 텔레그램으로 알려주는 봇입니다. GitHub Actions를 활용하여 서버 비용 없이 24시간 무료로 운영됩니다.

## ✨ 기능 (Features)
- **2시간 간격 자동 실행**: 별도의 서버 없이 GitHub Actions Cron 기능을 사용합니다.
- **실시간 환율 조회**: `yfinance` 라이브러리를 통해 최신 환율 정보를 가져옵니다.
- **텔레그램 알림**: 간편하게 텔레그램 메시지로 환율을 받아볼 수 있습니다.

## 🛠️ 준비물 (Prerequisites)
1. **GitHub 계정**: 이 코드를 저장하고 실행할 공간.
2. **Telegram Bot Token**: 
   - 텔레그램에서 [@BotFather](https://t.me/BotFather) 검색 -> `/newbot` -> 봇 이름 설정 -> Token 획득.
3. **Telegram Chat ID**:
   - 내 봇에게 아무 메시지나 보낸 후, `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates` 접속하여 `id` 확인 (또는 ID 확인용 봇 사용).

## 🚀 설치 및 설정 방법 (Setup Guide)

### 1. 리포지토리 설정
1. 이 프로젝트를 자신의 GitHub 리포지토리로 Fork 하거나 코드를 복사합니다.
2. 리포지토리 상단 메뉴의 **Settings** -> **Secrets and variables** -> **Actions** 로 이동합니다.
3. **New repository secret** 버튼을 눌러 다음 두 가지 변수를 추가합니다.
   - `TELEGRAM_TOKEN`: (BotFather에게 받은 토큰)
   - `CHAT_ID`: (본인의 챗 ID)

### 2. 동작 확인
- 코드를 Push하면 설정된 스케줄(2시간 간격)에 따라 자동으로 작동합니다.
- **Actions** 탭에서 실행 로그를 확인할 수 있습니다.
- 테스트를 원하면 Actions 탭에서 해당 워크플로우를 선택하고 **Run workflow** 버튼을 눌러 수동으로 즉시 실행해볼 수 있습니다.

## 📂 파일 구조
- `.github/workflows/main.yml`: 2시간마다 실행되도록 설정된 GitHub Actions 설정 파일.
- `main.py`: 환율을 조회하고 텔레그램 메시지를 보내는 파이썬 스크립트.
- `requirements.txt`: 필요한 라이브러리 목록 (`yfinance`, `requests` 등).

## ⚠️ 주의사항
- **실행 시간 오차**: GitHub Actions의 Cron 스케줄은 서버 부하에 따라 몇 분 정도 지연 실행될 수 있습니다. (정확히 정각에 오지 않을 수 있음)
- **GitHub 무료 정책**: Public 리포지토리는 무제한 무료, Private 리포지토리는 월 2,000분 무료입니다. (2시간 간격 실행 시 월 약 360분 소요되므로 Private에서도 아~주 여유롭게 무료 사용 가능)

---
Developed for efficient AUD/KRW monitoring.
