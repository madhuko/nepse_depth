import requests,datetime

header={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 Edg/90.0.818.66',
    'Accept': '*/*',
    'content-type': 'application/json',
    'Accept-Encoding': 'gzip, deflate, br',
}

payload_id=requests.get("http://nepse-payload-id.samrid.me",headers=header)

b_url="https://newweb.nepalstock.com.np/api/nots/security?nonDelisted=true"
m_url="https://newweb.nepalstock.com.np/api/nots/nepse-data/marketdepth/{}"
t_url="https://newweb.nepalstock.com.np/api/nots/security-detail/{}"

basic_list=requests.get(b_url,headers=header).json()

f= open("files/depth.txt","a")
delimiter="|"
for i in basic_list[:3]:
  print(t_url.format(i["id"]))
  f.write(str(datetime.datetime.now()))
  f.write(delimiter+i["symbol"]+delimiter)
  try:
    resp=requests.get(m_url.format(i["id"]),headers=header)
    f.write(resp.text())
  except:
    f.write("NULL")
  
  f.write("\n")
f.close()
