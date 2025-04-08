from bs4 import BeautifulSoup
import shutil
import pathlib
import logging
import streamlit as st


def add_analytics_tag():
    # 🔹 여기에 본인의 Google Analytics 측정 ID를 입력하세요!
    analytics_id = "G-PM1BSV6F2D"

    analytics_js = f"""
    <!-- Global site tag (gtag.js) - Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id={analytics_id}"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', '{analytics_id}');
    </script>
    <div id="{analytics_id}"></div>
    """

    # 🔹 Streamlit의 `index.html` 파일 경로 찾기
    index_path = pathlib.Path(st.__file__).parent / "static" / "index.html"
    logging.info(f'Editing {index_path}')

    # 🔹 HTML 파일을 수정하기 위해 BeautifulSoup 사용
    soup = BeautifulSoup(index_path.read_text(), features="html.parser")

    # GA 코드가 이미 삽입되어 있는지 확인 (중복 삽입 방지)
    if not soup.find(id=analytics_id):  
        bck_index = index_path.with_suffix('.bck')

        # 🔹 기존 백업이 있으면 복구, 없으면 백업 생성
        if bck_index.exists():
            shutil.copy(bck_index, index_path)  # 백업 복구
        else:
            shutil.copy(index_path, bck_index)  # 백업 저장

        # 🔹 <head> 태그 내부에 GA 코드 삽입
        html = str(soup)
        new_html = html.replace('<head>', '<head>\n' + analytics_js) 
        index_path.write_text(new_html)

# 🔹 실행 시 GA 코드 삽입
add_analytics_tag()
