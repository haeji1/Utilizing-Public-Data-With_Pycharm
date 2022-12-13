from bs4 import BeautifulSoup
from urllib.request import urlopen

# lawd_cd = 28200 인천 광역시 구월동
# date = 202212
# 법정동 코드 검색 : https://www.code.go.kr/stdcode/regCodeL.do
print('검색 하고자 하는 법정동 코드 앞 다섯 글자와 날짜(년도,월) 여섯 글자를 입력해 주세요 (줄바꿈)')
lawd_cd = int(input())
date = int(input())

print('검색 하고자 하는 아파트 이름이 있다면 아파트 이름을 정확히 입력 해 주세요. 없다면 x나 X를 입력 해 주세요.')
apart_name = input()

endpoint = "http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptRent"
url = f"{endpoint}?LAWD_CD={lawd_cd}&DEAL_YMD={date}&serviceKey={'cRyybv7k/CIvARR5cQnSRQxZxWoQZ0VoEjF9m3tyfnRAOkTQ0ih2PvsFa2zwjbLzZms23fjH0dOnsDBNiCSssg=='}"

res = urlopen(url)
res_parse = BeautifulSoup(res, 'lxml-xml') # xml 파싱
rental_fee = res_parse.find_all('item')

no_input_apt_dats = []
input_apt_data = []

# 알고자 하는 아파트 이름을 입력 한 경우
if apart_name != 'x' or apart_name != 'X':
    cnt = 0
    for i in range(len(rental_fee)):
        apt = rental_fee[i].아파트.string.strip()
        if apt == apart_name:
            dep = rental_fee[i].보증금액.string.strip()
            month = rental_fee[i].월세금액.string.strip()
            y_input_data = [dep, month]
            input_apt_data.append(y_input_data)
            cnt += 1
    if cnt >= 1:
        for apt_rent in range(len(input_apt_data)):
            apt_r, apt_m = input_apt_data[apt_rent][0], input_apt_data[apt_rent][1]
            print(apt_rent + 1, ':')
            print('보증금 :', apt_r, '월세 :', apt_m)

    if cnt <= 0 and len(apart_name) >= 2:
        print('검색 한 아파트에 관한 정보가 없습니다. 이름을 다시 한 번 확인 해 주세요')


# 알고자 하는 아파트 이름을 입력 하지 않은 경우 모든 정보 출력
if apart_name == 'x' or apart_name == 'X':
    for i in range(len(rental_fee)):
        deposit = rental_fee[i].보증금액.string.strip()
        monthly_fee = rental_fee[i].월세금액.string.strip()
        year = rental_fee[i].건축년도.string.strip()
        name = rental_fee[i].법정동.string.strip()
        apart = rental_fee[i].아파트.string.strip()
        size = rental_fee[i].전용면적.string.strip()

        n_input_data = [deposit, monthly_fee, year, name, apart, size]
        no_input_apt_dats.append(n_input_data)

    print('전체결과 :')
    print(no_input_apt_dats)

    for i in range(len(no_input_apt_dats)):
        x,y = no_input_apt_dats[i][0],no_input_apt_dats[i][1]
        apart = no_input_apt_dats[i][4]
        print(i + 1,':')
        print(apart,'보증금 :',x,'월세 :',y)

