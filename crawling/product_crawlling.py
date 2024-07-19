import requests
from bs4 import BeautifulSoup
import pandas as pd

data = []
for i in range(1, 11):
    # 요청할 웹 페이지 URL
    url = f'https://www.oliveyoung.co.kr/store/display/getMCategoryList.do?dispCatNo=100000100010016&fltDispCatNo=&prdSort=01&pageIdx={i}&rowsPerPage=24&searchTypeSort=btn_thumb&plusButtonFlag=N&isLoginCnt=0&aShowCnt=0&bShowCnt=0&cShowCnt=0&trackingCd=Cat100000100010016_Small&amplitudePageGubun=&t_page=&t_click=&midCategory=%EB%A1%9C%EC%85%98&smallCategory=%EC%A0%84%EC%B2%B4&checkBrnds=&lastChkBrnd='

    # 웹 페이지 요청
    response = requests.get(url)
    html_content = response.content

    # HTML 파싱
    soup = BeautifulSoup(html_content, 'html.parser')

    # 특정 클래스 'prd_info'를 가진 모든 요소 선택
    elements = soup.find_all(class_='prd_info')
    
    # 데이터 저장을 위한 리스트
    
    # 선택한 요소들로부터 데이터 추출
    for element in elements:
        # 제품명 추출
        product_name = element.find(class_='tx_name').get_text(strip=True) if element.find(class_='tx_name') else ""
        
        # 가격 추출 (여러 클래스 중 첫 번째 가격만 사용)
        prices = element.find_all(class_='tx_num')
        if prices:
            original_price = prices[0].get_text(strip=True) if len(prices) > 0 else ""
            current_price = prices[1].get_text(strip=True) if len(prices) > 1 else ""
        else:
            original_price = ""
            current_price = ""
        
        # 이미지 URL 추출
        img_tag = element.find('img')
        img_url = img_tag['src'] if img_tag else ""
        
        # 추출한 데이터를 리스트에 추가
        data.append([product_name, original_price, img_url])



# 데이터프레임 생성
df = pd.DataFrame(data, columns=['Product Name', 'Original Price', 'Image URL'])

# CSV 파일로 저장
output_path = 'extracted_data.csv'
df.to_csv(output_path, index=False, encoding='utf-8-sig')

print(f"Data saved to {output_path}")
