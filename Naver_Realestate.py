import streamlit as st
import requests
import pandas as pd
import re

# Streamlit page setup
st.set_page_config(page_title="Real Estate Listings Viewer", layout="wide")
st.title("내집마련 프로젝트")


def convert_to_decimal_uk(input_string):
    # "억"과 "만" 단위 처리
    input_string = input_string.replace(',', '').strip()
    pattern = r'(\d+)억(?:\s*(\d+))?'
    match = re.match(pattern, input_string)

    if match:
        # 억 단위
        billion = int(match.group(1))
        # 억 뒤에 만 단위가 있는 경우 처리
        ten_thousand = int(match.group(2)) if match.group(2) else 0
        # 소수점으로 변환
        return billion + ten_thousand / 10000
    return None

# Define the cookies and headers as provided
cookies = {
    'NSCS': '1',
    'NAC': '5OXqBYAvogLS',
    '_fwb': '98xuCdOYpo9nABpd1Yr9jy.1732993793195',
    'NNB': 'TNP2OYYBMNFWO',
    'landHomeFlashUseYn': 'Y',
    '_fwb': '98xuCdOYpo9nABpd1Yr9jy.1732993793195',
    'wcs_bt': '4f99b5681ce60:1733323401',
    'NFS': '2',
    'BNB_FINANCE_HOME_TOOLTIP_MYASSET': 'true',
    '_gcl_au': '1.1.416900759.1735854858',
    '_ga_J5CZVNJNQP': 'GS1.1.1735854857.1.1.1735855227.0.0.0',
    'nhn.realestate.article.rlet_type_cd': 'A01',
    '_ga': 'GA1.1.1359129107.1735854858',
    '_ga_EFBDNNF91G': 'GS1.1.1736348968.1.1.1736349126.0.0.0',
    'nhn.realestate.article.trade_type_cd': '""',
    'NACT': '1',
    'realestate.beta.lastclick.cortar': '4146500000',
    'SRT30': '1736886971',
    'SRT5': '1736886971',
    'REALESTATE': 'Wed%20Jan%2015%202025%2005%3A36%3A19%20GMT%2B0900%20(Korean%20Standard%20Time)',
}
headers = {
    'accept': '*/*',
    'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7,zh;q=0.6,ja;q=0.5',
    'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IlJFQUxFU1RBVEUiLCJpYXQiOjE3MzY4ODY5NzksImV4cCI6MTczNjg5Nzc3OX0.QHnoJtnaHfzCJmN1kNEmbOBO_vfqlPCAHMm6K_yX6Ik',
    'priority': 'u=1, i',
    'referer': 'https://new.land.naver.com/complexes/26925?ms=37.3165058,127.0650103,17&a=APT:PRE:ABYG:JGC&e=RETAIL',
    'sec-ch-ua': '"Chromium";v="130", "Whale";v="4", "Not.A/Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Whale/4.29.282.15 Safari/537.36',
}

# Function to get data from the API for pages 1 to 10
@st.cache_data
def fetch_all_data():
    all_articles = []
    for page in range(1, 6):
        try:
            # Make the request for the specific page
            url = f'https://new.land.naver.com/api/articles/complex/26925?realEstateType=APT%3APRE%3AABYG%3AJGC&tradeType=A1&tag=%3A%3A%3A%3A%3A%3A%3A%3A&rentPriceMin=0&rentPriceMax=900000000&priceMin=0&priceMax=900000000&areaMin=0&areaMax=900000000&oldBuildYears&recentlyBuildYears&minHouseHoldCount&maxHouseHoldCount&showArticle=false&sameAddressGroup=false&minMaintenanceCost&maxMaintenanceCost&priceType=RETAIL&directions=&{page}&complexNo=26925&buildingNos=&areaNos=&type=list&order=rank'
            response = requests.get(url, cookies=cookies, headers=headers)

            # Verify response is valid JSON
            if response.status_code == 200:
                data = response.json()
                articles = data.get("articleList", [])
                all_articles.extend(articles)
            else:
                st.warning(f"Failed to retrieve data for page {page}. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}")
        except ValueError:
            st.error(f"Non-JSON response for page {page}.")

    return all_articles

# Fetch data for all pages
data = fetch_all_data()

# Transform data into a DataFrame if data is available
if data:
    df = pd.DataFrame(data)
    # Select columns to display
    df_display = df[["floorInfo","dealOrWarrantPrc", "areaName", "direction", "articleConfirmYmd", "articleFeatureDesc",
                     "tagList", "buildingName","realtorName"]]
    df_display.columns = ["층수","호가","면적","향","등록일","설명","TAG","동","부동산"]
    df_display["면적"] = (df_display["면적"].astype(int) // 3.3).astype(int)
    df_display["호가"] = df_display["호가"].apply(convert_to_decimal_uk)
    # Display the table in Streamlit with a clean, readable layout
    st.write("### 버들치마을성복자이1차 리스트")
    st.dataframe(df_display, height = 500)
else:
    st.write("No data available.")


cookies = {
    'NSCS': '1',
    'NAC': '5OXqBYAvogLS',
    '_fwb': '98xuCdOYpo9nABpd1Yr9jy.1732993793195',
    'NNB': 'TNP2OYYBMNFWO',
    'landHomeFlashUseYn': 'Y',
    '_fwb': '98xuCdOYpo9nABpd1Yr9jy.1732993793195',
    'wcs_bt': '4f99b5681ce60:1733323401',
    'NFS': '2',
    'BNB_FINANCE_HOME_TOOLTIP_MYASSET': 'true',
    '_gcl_au': '1.1.416900759.1735854858',
    '_ga_J5CZVNJNQP': 'GS1.1.1735854857.1.1.1735855227.0.0.0',
    'nhn.realestate.article.rlet_type_cd': 'A01',
    '_ga': 'GA1.1.1359129107.1735854858',
    '_ga_EFBDNNF91G': 'GS1.1.1736348968.1.1.1736349126.0.0.0',
    'nhn.realestate.article.trade_type_cd': '""',
    'NACT': '1',
    'realestate.beta.lastclick.cortar': '4146500000',
    'SRT30': '1736886971',
    'REALESTATE': 'Wed%20Jan%2015%202025%2006%3A03%3A12%20GMT%2B0900%20(Korean%20Standard%20Time)',
}
headers = {
    'accept': '*/*',
    'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7,zh;q=0.6,ja;q=0.5',
    'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IlJFQUxFU1RBVEUiLCJpYXQiOjE3MzY4ODU3OTEsImV4cCI6MTczNjg5NjU5MX0.cJIRVY_gNPgSCWDL6VLeRcd_0--_fNH3ikilmNni9C8',
    # 'cookie': 'NSCS=1; NAC=5OXqBYAvogLS; _fwb=98xuCdOYpo9nABpd1Yr9jy.1732993793195; NNB=TNP2OYYBMNFWO; landHomeFlashUseYn=Y; _fwb=98xuCdOYpo9nABpd1Yr9jy.1732993793195; wcs_bt=4f99b5681ce60:1733323401; NFS=2; BNB_FINANCE_HOME_TOOLTIP_MYASSET=true; _gcl_au=1.1.416900759.1735854858; _ga_J5CZVNJNQP=GS1.1.1735854857.1.1.1735855227.0.0.0; nhn.realestate.article.rlet_type_cd=A01; _ga=GA1.1.1359129107.1735854858; _ga_EFBDNNF91G=GS1.1.1736348968.1.1.1736349126.0.0.0; nhn.realestate.article.trade_type_cd=""; NACT=1; realestate.beta.lastclick.cortar=4146500000; SRT30=1736886971; REALESTATE=Wed%20Jan%2015%202025%2006%3A03%3A12%20GMT%2B0900%20(Korean%20Standard%20Time)',
    'priority': 'u=1, i',
    'referer': 'https://new.land.naver.com/complexes/3715?ms=37.3165187,127.0728102,17&a=APT:PRE:ABYG:JGC&e=RETAIL',
    'sec-ch-ua': '"Chromium";v="130", "Whale";v="4", "Not.A/Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Whale/4.29.282.15 Safari/537.36',
}

# Function to get data from the API for pages 1 to 10
@st.cache_data
def fetch_all_data():
    all_articles = []
    for page in range(1, 6):
        try:
            # Make the request for the specific page
            url = f'https://new.land.naver.com/api/articles/complex/3715?realEstateType=APT%3APRE%3AABYG%3AJGC&tradeType=A1&tag=%3A%3A%3A%3A%3A%3A%3A%3A&rentPriceMin=0&rentPriceMax=900000000&priceMin=0&priceMax=900000000&areaMin=0&areaMax=900000000&oldBuildYears&recentlyBuildYears&minHouseHoldCount&maxHouseHoldCount&showArticle=false&sameAddressGroup=false&minMaintenanceCost&maxMaintenanceCost&priceType=RETAIL&directions=&{page}&complexNo=3715&buildingNos=&areaNos=&type=list&order=rank'
            response = requests.get(url, cookies=cookies, headers=headers)

            # Verify response is valid JSON
            if response.status_code == 200:
                data = response.json()
                articles = data.get("articleList", [])
                all_articles.extend(articles)
            else:
                st.warning(f"Failed to retrieve data for page {page}. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}")
        except ValueError:
            st.error(f"Non-JSON response for page {page}.")

    return all_articles

# Fetch data for all pages
data = fetch_all_data()

# Transform data into a DataFrame if data is available
if data:
    df = pd.DataFrame(data)
    # Select columns to display
    df_display = df[["floorInfo","dealOrWarrantPrc", "areaName", "direction", "articleConfirmYmd", "articleFeatureDesc",
                     "tagList", "buildingName","realtorName"]]
    df_display.columns = ["층수","호가","면적","향","등록일","설명","TAG","동","부동산"]
    df_display["면적"] = (df_display["면적"].astype(int) // 3.3).astype(int)
    df_display["호가"] = df_display["호가"].apply(convert_to_decimal_uk)
    # Display the table in Streamlit with a clean, readable layout
    st.write("### 성동마을LG빌리지3차 리스트")
    st.dataframe(df_display, height = 500)
else:
    st.write("No data available.")