# 최성진 교수 홈페이지 사용 안내

홈페이지 파일은 완성되어 있으며, **아직 GitHub 저장소를 만들거나 인터넷에 공개하지 않았습니다.**

**내 컴퓨터에서 보기**

[홈페이지 열기](index.html)를 누르거나, `sungjin-choi-site` 폴더 안의 `index.html`을 더블클릭하세요. 압축본을 받았다면 먼저 압축을 풀고 폴더 구성을 유지해 주세요.

별도 서버 설치 없이 메뉴 이동, 논문 검색·연도/종류 필터, 인용문 저장, BibTeX·CSV 내려받기를 사용할 수 있습니다. `Cite`는 인용문을 복사하며, 브라우저가 복사를 허용하지 않으면 텍스트 파일로 저장합니다. 외부 논문·기사·Google Scholar 링크를 열 때는 인터넷이 필요합니다.

| 메뉴 | 내용 |
|---|---|
| Home | 연구 그림, Scholar 인용 지표, 대표 논문 5편 |
| Research | 주요 연구 분야 |
| Publications | 학술지 239건, 학회 218건, 책 챕터 1건: 총 458건 |
| Patents & Awards | 국내·미국 특허 문서 25건, 공동논문상·학생상·논문 인정 15건 |
| Team | 연구팀 구성원 8명 |
| Media | 기사·연구 소식 12건 |
| About | 이력과 연락처 |

수상 목록의 15건은 모두 교수 개인상이라는 뜻이 아닙니다. 공동논문상 13건, 학생경진대회상 1건, IEDM 하이라이트 1건을 구분했습니다. 국내 특허 21건과 미국 문서 4건을 수록했습니다. 국가별 같은 특허군의 기록이 포함되며, 25개의 서로 다른 발명이라는 뜻은 아닙니다. 특허의 상태와 번호는 출처에 기록된 내용을 표시했습니다.

**내용 업데이트**

논문·특허·수상·기사·팀 정보의 관리 원본은 [content.json](content.json)입니다. 이 파일을 수정한 다음, 홈페이지 폴더에서 Python 3으로 아래 명령을 실행하면 화면 파일을 다시 만듭니다.

```text
python build.py
```

Python은 업데이트할 때만 필요하며, 홈페이지를 보는 사람에게는 필요하지 않습니다. 생성된 HTML만 직접 수정하면 다음 재생성 때 덮어씌워질 수 있습니다. 변경할 자료를 주고 홈페이지 업데이트를 요청해도 됩니다.

**다른 사람도 접속할 수 있게 공개하기**

처음 공개할 때는 본인의 [GitHub 계정](https://github.com/signup)이 필요합니다. 무료 계정에서는 **Public 저장소**로 GitHub Pages를 이용할 수 있습니다. 기본 주소는 `https://USERNAME.github.io/`이며, `USERNAME`은 실제 GitHub 사용자 이름으로 바꿉니다. [GitHub 공식 시작 안내](https://docs.github.com/en/pages/quickstart)

1. GitHub에 가입하고 이메일 인증을 마칩니다.
2. **New repository**에서 이름을 `USERNAME.github.io`로 지정합니다. 사용자 이름은 소문자로 쓰고, **Public**을 선택합니다. **Add README**를 켠 뒤 저장소를 만듭니다.
3. **Add file → Upload files**에서 홈페이지 폴더 **안의 파일과 `assets` 폴더**를 올립니다. `index.html`이 저장소 첫 화면에 보여야 합니다. `sungjin-choi-site`라는 상위 폴더나 ZIP 파일째 올리지 않습니다. `.nojekyll`도 함께 올립니다. 업로드 내용을 `main`에 저장합니다. [공식 파일 업로드 안내](https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository)
4. **Settings → Pages → Build and deployment**에서 **Source: Deploy from a branch**, **Branch: main**, **Folder: /(root)**를 선택하고 **Save**를 누릅니다. [공식 게시 설정 안내](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)
5. 게시가 끝나면 같은 화면의 **Visit site**로 열어 확인합니다. 반영에는 최대 약 10분이 걸릴 수 있습니다. 공개 주소는 다른 사람에게 공유할 수 있습니다. [공식 게시 확인 안내](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site)

이후에는 내용을 수정하고 `python build.py`로 다시 만든 파일을 같은 저장소에 업데이트하면 됩니다. GitHub에서 Python을 실행하는 과정은 필요하지 않습니다.

**내 이름의 도메인 사용하기**

기본 `github.io` 주소로 먼저 공개한 뒤, 원한다면 별도로 도메인을 구매해 연결할 수 있습니다. 원하는 이름의 등록 가능 여부와 가격을 먼저 확인해야 하며, **현재 확보하거나 연결한 개인 도메인은 없습니다.** 구매 후 GitHub Pages의 **Custom domain**과 도메인 판매사의 주소 연결 설정(DNS)을 맞추면 됩니다. [GitHub 공식 맞춤 도메인 안내](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site)

공개 절차는 2026년 9월 23일 GitHub 공식 문서를 기준으로 확인했습니다.

**첫 화면의 Scholar 지표**

Citations, h-index, i10-index는 교수님의 공개 Scholar 프로필에서 확인한 값입니다. 숫자와 Google Scholar 링크를 누르면 해당 프로필로 이동합니다. 확인일을 함께 표시하며, 현재 확인된 수치를 유지합니다. 자동 갱신은 사용하지 않고, 교수님이 요청하실 때 최신 수치를 확인해 수정합니다.
