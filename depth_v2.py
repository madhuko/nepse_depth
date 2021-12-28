# %%
import datetime
#%%
import pandas as pd
import requests

class TokenParser():
    def __init__(self):
        ###############################################MAGIC ARRAY###############################################
        self.data_segment_data_0 = [
                                      0x09, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 
                                      0x01, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x03, 0x00, 0x00, 0x00, 
                                      0x02, 0x00, 0x00, 0x00, 0x05, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 
                                      0x07, 0x00, 0x00, 0x00, 0x09, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 
                                      0x00, 0x00, 0x00, 0x00, 0x03, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 
                                      0x02, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 
                                      0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 
                                      0x09, 0x00, 0x00, 0x00, 0x05, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 
                                      0x06, 0x00, 0x00, 0x00, 0x03, 0x00, 0x00, 0x00, 0x07, 0x00, 0x00, 0x00, 
                                      0x02, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x06, 0x00, 0x00, 0x00, 
                                      0x09, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 
                                      0x01, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 
                                      0x03, 0x00, 0x00, 0x00, 0x03, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 
                                      0x04, 
                                    ]
        
    def rdx(self, w2c_p0, w2c_p1, w2c_p2, w2c_p3, w2c_p4):

        w2c_i0 = w2c_p1
        w2c_i1 = 100
        w2c_i0 = w2c_i0 // w2c_i1
        w2c_i1 = 10
        w2c_i0 = w2c_i0 % w2c_i1
        w2c_i1 = w2c_p1
        w2c_i2 = 10
        w2c_i1 = w2c_i1 // w2c_i2
        w2c_p0 = w2c_i1
        w2c_i2 = 10
        w2c_i1 = w2c_i1 % w2c_i2
        w2c_i0 += w2c_i1
        w2c_p2 = w2c_i0
        w2c_i1 = w2c_p2
        w2c_i2 = w2c_p1
        w2c_i3 = w2c_p0
        w2c_i4 = 10
        w2c_i3 *= w2c_i4
        w2c_i2 -= w2c_i3
        w2c_i1 += w2c_i2
        w2c_i2 = 2
        w2c_i1 <<= (w2c_i2 & 31)

        w2c_i1 = self.data_segment_data_0[w2c_i1]
        w2c_i0 += w2c_i1
        w2c_i1 = 22
        w2c_i0 += w2c_i1
        return w2c_i0


    def cdx(self, w2c_p0, w2c_p1, w2c_p2, w2c_p3, w2c_p4):
        w2c_i0 = w2c_p1
        w2c_i1 = 10
        w2c_i0 = w2c_i0 // w2c_i1
        w2c_p0 = w2c_i0
        w2c_i1 = 10
        w2c_i0 = w2c_i0 % w2c_i1
        w2c_i1 = w2c_p1
        w2c_i2 = w2c_p0
        w2c_i3 = 10
        w2c_i2 *= w2c_i3
        w2c_i1 -= w2c_i2
        w2c_i0 += w2c_i1
        w2c_i1 = w2c_p1
        w2c_i2 = 100
        w2c_i1 = w2c_i1 // w2c_i2
        w2c_i2 = 10
        w2c_i1 = w2c_i1 % w2c_i2
        w2c_i0 += w2c_i1
        w2c_i1 = 2
        w2c_i0 <<= (w2c_i1 & 31)

        w2c_i0 = self.data_segment_data_0[w2c_i0]
        w2c_i1 = 22
        w2c_i0 += w2c_i1

        return w2c_i0

    def parse_token_response(self, token_response):
        n = self.cdx(token_response['salt1'], token_response['salt2'], token_response['salt3'], token_response['salt4'], token_response['salt5']);
        l = self.rdx(token_response['salt1'], token_response['salt2'], token_response['salt4'], token_response['salt3'], token_response['salt5']);
        
        i = self.cdx(token_response['salt2'], token_response['salt1'], token_response['salt3'], token_response['salt5'], token_response['salt4']);
        r = self.rdx(token_response['salt2'], token_response['salt1'], token_response['salt3'], token_response['salt4'], token_response['salt5']);

        access_token  = token_response['accessToken']
        refresh_token = token_response['refreshToken']
        
        parsed_access_token  = access_token[0:n] + access_token[n + 1: l] + access_token[l + 1:]
        parsed_refresh_token = refresh_token[0:i] + refresh_token[i + 1: r] + refresh_token[r + 1:]
    
        #returns both access_token and refresh_token
        #Right now new access_token can be used for every new api request
        return (parsed_access_token, parsed_refresh_token)

class Nepse:
    def __init__(self):
        self.token_parser     = TokenParser()
        
        self.token_url            = "https://newweb.nepalstock.com/api/authenticate/prove"
        
        self.price_volume_url     = "https://www.nepalstock.com.np/api/nots/securityDailyTradeStat/58"
        self.summary_url          = "https://newweb.nepalstock.com.np/api/nots/market-summary/"
        self.top_ten_scrips_url   = "https://newweb.nepalstock.com.np/api/nots/top-ten/trade-qty"
        self.supply_demand_url    = "https://newweb.nepalstock.com.np/api/nots/nepse-data/supplydemand"
        self.turnover_url         = "https://newweb.nepalstock.com.np/api/nots/top-ten/turnover"
        self.top_gainers_url      = "https://newweb.nepalstock.com.np/api/nots/top-ten/top-gainer"
        self.top_losers_url       = "https://newweb.nepalstock.com.np/api/nots/top-ten/top-loser"
        self.nepse_open_url       = "https://newweb.nepalstock.com.np/api/nots/nepse-data/market-open"
        self.nepse_index_url      = "https://newweb.nepalstock.com.np/api/nots/nepse-index"
        self.nepse_subindices_url = "https://newweb.nepalstock.com/api/nots"
        self.getStockDepth_url    ="https://newweb.nepalstock.com.np/api/nots/nepse-data/marketdepth/{}"
        self.getListedStock_url="https://newweb.nepalstock.com.np/api/nots/securityDailyTradeStat/{}"
        self.get_all_listed_url="https://newweb.nepalstock.com.np/api/nots/company/list"
        self.get_market_depth_url="https://newweb.nepalstock.com.np/api/nots/nepse-data/marketdepth/{}"

        self.headers= {
                            'Host': 'newweb.nepalstock.com',
                            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',
                            'Accept': 'application/json, text/plain, */*',
                            'Accept-Language': 'en-US,en;q=0.5',
                            'Accept-Encoding': 'gzip, deflate, br',
                            'Connection': 'keep-alive',
                            'Referer': 'https://newweb.nepalstock.com/',
                            'Pragma': 'no-cache',
                            'Cache-Control': 'no-cache',
                            'TE': 'Trailers',
                        }
    ###############################################PRIVATE METHODS###############################################
    
    def requestAPI(self, url, access_token=None):
        if access_token is not None:
            headers = {'Authorization': f'Salter {access_token}', **self.headers}
        else:
            headers = self.headers
            
        return requests.get(url, headers=headers,verify=False).json()
        
        
    def getValidToken(self):
        token_response = self.requestAPI(url=self.token_url)
        
        
        # for salt_index in range(1, 6):
        #     token_response[f'salt{salt_index}'] = int([f'salt{salt_index}'])
        token_response
        #returns access_token only, refresh token is not used right now
        return self.token_parser.parse_token_response(token_response)[0]
    
    ###############################################PUBLIC METHODS###############################################
        
    def getPriceVolume(self):
        access_token = self.getValidToken()
        return self.requestAPI(url=self.price_volume_url, access_token=access_token)
    
    def getSummary(self):
        access_token = self.getValidToken()
        return self.requestAPI(url=self.summary_url, access_token=access_token)
    
    def getTopTenScrips(self):
        access_token = self.getValidToken()
        return self.requestAPI(url=self.top_ten_scrips_url, access_token=access_token)
    
    def getSupplyDemand(self):
        access_token = self.getValidToken()
        return self.requestAPI(url=self.supply_demand_url, access_token=access_token)
    
    def getTopGainers(self):
        access_token = self.getValidToken()
        return self.requestAPI(url=self.top_gainers_url, access_token=access_token)
    
    def getTopLosers(self):
        access_token = self.getValidToken()
        return self.requestAPI(url=self.top_losers_url, access_token=access_token)
    
    def isNepseOpen(self):
        access_token = self.getValidToken()
        return self.requestAPI(url=self.nepse_open_url, access_token=access_token)
    
    def getNepseIndex(self):
        access_token = self.getValidToken()
        return self.requestAPI(url=self.nepse_index_url, access_token=access_token)
    
    def getNepseSubIndices(self):
        access_token = self.getValidToken()
        return self.requestAPI(url=self.nepse_subindices_url, access_token=access_token)
    
    def getStockDepth(self,sid):
        access_token = self.getValidToken()
        print(self.getStockDepth_url.format(sid))
        return self.requestAPI(url=self.getStockDepth_url.format(sid),access_token=access_token)
    
    def getListedStock(self,sect_id):
      access_token=self.getValidToken()
      return self.requestAPI(url=self.getListedStock_url.format(sect_id),access_token=access_token)
    
    def get_all_listed(self):
      access_token=self.getValidToken()
      return self.requestAPI(url=self.get_all_listed_url,access_token=access_token)

    def get_market_depth(self,id):
        access_token=self.getValidToken()
        return self.requestAPI(url=self.get_market_depth_url.format(id),access_token=access_token)
####################################Usage####################################
nepse = Nepse()
# %%
basic_list=nepse.get_all_listed()


filtered_list=[]
for i in basic_list:
  if i['instrumentType'] in ['Equity','Mutual Funds']:
    filtered_list.append(i)
basic_list=[]
for i in filtered_list:
  if i['status']=="A":
    basic_list.append(i)
# %%
filename=str(datetime.datetime.now())[:16].replace(":","").replace("-","")
f= open("files/"+ filename,"a")
delimiter="|"

for i in basic_list[:]:
  print(nepse.get_market_depth_url.format(i["id"]))
  f.write(str(datetime.datetime.now()))
  f.write(delimiter+i["symbol"]+delimiter)
  try:
    resp=nepse.get_market_depth(i["id"])
    f.write(resp.text)
  except:
    f.write("NULL")
  
  f.write("\n")
f.close()


# %%
