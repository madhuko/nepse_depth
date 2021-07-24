import requests,datetime,concurrent
from requests.adapters import HTTPAdapter
header={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 Edg/90.0.818.66',
    'Accept': '*/*',
    'content-type': 'application/json',
    'Accept-Encoding': 'gzip, deflate, br',
}
s = requests.Session()
s.mount(m_url, HTTPAdapter(max_retries=5))

# payload_id=requests.get("http://nepse-payload-id.samrid.me",headers=header)

b_url="https://newweb.nepalstock.com.np/api/nots/company/list"
m_url="https://newweb.nepalstock.com.np/api/nots/nepse-data/marketdepth/{}"
t_url="https://newweb.nepalstock.com.np/api/nots/security-detail/{}"
basic_list=requests.get(b_url,headers=header).json()

filtered_list=[]
for i in basic_list:
  if i['instrumentType'] in ['Equity','Mutual Funds']:
    filtered_list.append(i)
basic_list=[]
for i in filtered_list:
  if i['status']=="A":
    basic_list.append(i)

filename=str(datetime.datetime.now())[:16].replace(":","").replace("-","")
f= open("files/"+ filename,"a")
delimiter="|"

for i in basic_list[:]:
#   print(t_url.format(i["id"]))
  f.write(str(datetime.datetime.now()))
  f.write(delimiter+i["symbol"]+delimiter)
  try:
    resp=requests.get(m_url.format(i["id"]),headers=header)
    f.write(resp.text)
  except:
    f.write("NULL")
  
  f.write("\n")
f.close()
