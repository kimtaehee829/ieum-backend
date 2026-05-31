#  이음 (Ieum) - Backend

<div align="center">
  <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white">
  <img src="https://img.shields.io/badge/django%20rest-ff1709?style=for-the-badge&logo=django&logoColor=white">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white">
  <br>
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white">
  <img src="https://img.shields.io/badge/Google_Cloud_Run-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white">
  <img src="https://img.shields.io/badge/Google_Cloud_Storage-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white">
  <img src="https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white">
</div>

##  프로젝트 소개
'이음'은 스쳐 지나간 인연을 다시 찾을 수 있도록 돕는 서비스입니다. 
본 레포지토리는 '이음' 서비스의 백엔드(API 서버)를 담당하며, 다중 미디어 파일(단서) 처리와 유연한 해시태그 검색 기능을 안정적으로 제공하는 데 집중했습니다.

## 🔗 링크
- API 명세서: https://www.notion.so/v2-2-3706e3032ec880f2811ee2f33c75514b?source=copy_link
- **배포 서버 URL:** https://ieum-backend-api-35900716842.asia-northeast3.run.app/api/

---

## ⚙️ 핵심 아키텍처 및 기능

### 1. ☁️ 인프라 및 배포 (DevOps)
- **Docker & Cloud Run:** Docker 컨테이너 기반으로 서버를 패키징하여 Google Cloud Run에 배포, 트래픽에 따른 유연한 Auto-scaling 환경 구축.
- **CI/CD 파이프라인:** GitHub Actions를 활용하여 `main` 브랜치 PR 머지 시 Django 테스트 및 자동 빌드/배포 수행.

### 2. 🔐 유저 및 인증 (Auth)
- **JWT 기반 인증:** `rest_framework_simplejwt`를 활용한 Access/Refresh Token 발급 및 인증.
- **안전한 로그아웃 & 탈퇴:** Refresh Token Blacklist 처리 및 회원 탈퇴 시 작성한 게시글/GCS 미디어 파일의 완벽한 연쇄 삭제(Cascade) 구현.

### 3. 📝 게시글 및 단서 파일 처리 (Posts & Clues)
- **다중 미디어 일괄 업로드:** 텍스트(게시글)와 다중 파일(이미지/영상/음성)을 `multipart/form-data`로 한 번에 수신하여 GCS 버킷에 동시 저장.
- **보안 및 용량 제한:** 확장자에 따른 동적 파일 사이즈 제한(이미지 10MB, 영상 50MB, 음성 20MB) 및 유효성 검사 적용.
- **다대다(M:N) 태그 시스템:** 게시글과 태그 간의 다대다 관계를 설정하여 다중 태그 교집합 필터링 기능 구현.

---

##  트러블슈팅 및 기술적 도전

### 1. GCS 파일 다운로드 시 CORS 및 파일명 깨짐 이슈 해결
- **문제:** 프론트엔드에서 GCS 파일 다운로드 시 브라우저 CORS 정책으로 인해 다운로드가 차단되거나 새 탭으로 열리는 문제 발생.
- **해결:** 외부 HTTP 통신(`requests.get`) 대신 장고의 `FileResponse`를 활용하여 GCS 스토리지를 직접 스트리밍 방식으로 읽어 메모리 과부하(OOM)를 방지함. 또한, `Content-Disposition` 헤더와 `urllib.parse.quote`를 적용해 한글 파일명 깨짐 현상을 완벽히 해결하고 즉시 다운로드가 가능하도록 커스텀 API를 구축함.

### 2. FormData 배열 파싱 및 M:N 관계 업데이트 충돌 해결
- **문제:** 게시글 수정(`PATCH`) 시 프론트엔드의 `FormData` 특성상 배열 데이터가 문자열(`"A,B"`) 또는 배열(`["A", "B"]`)로 혼재되어 서버로 전달되어 파싱 에러 발생.
- **해결:** `views.py` 내부에 데이터 타입(`isinstance`)을 엄격히 검사하는 정제 로직을 추가하여, 어떤 형태로 데이터가 인입되든 파이썬 리스트로 안전하게 변환하도록 방어 로직 구축. 기존 태그를 `clear()`로 초기화 후 재할당하는 방식으로 다대다 관계의 무결성을 유지함.



---

## 👨‍💻 Backend Developer
- **김태희:** API 설계 및 개발, DB 모델링
- **유윤민:** GCP 인프라 구축