import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import sys
import os
import logging
import pdb

def set_log_file(log_file_name):
    path = os.getcwd()
    logging.basicConfig(filename=log_file_name,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        filemode='a')

    logger=logging.getLogger()
    # The following line sets the root logger level as well:
    logger.setLevel(logging.INFO)

    return logger


def extract_url(soup,player,formated_name,current_url, output_file_name):
    response = requests.get(current_url)
    
    soup = BeautifulSoup(response.content, 'html.parser')

    try:
        if filter == "marketcap":
            search_tag_list = soup.find("tbody").find_all("tr")
            for a in range(len(search_tag_list)):
                try:
                    scraped_name = soup.find(class_ = "company-code").text
                except:
                    scraped_name = ""
                try:
                    country = soup.find_all(class_= "info-box")[2].find(class_ = "responsive-hidden").text
                except:
                    country = ""
                try:
                    year_market_cap = search_tag_list[a].find_all("td")[0].text
                except:
                    year_market_cap =  ""
                try:
                    market_cap = search_tag_list[a].find_all("td")[1].text
                except:
                    market_cap =  ""
                try:
                    market_cap_change = search_tag_list[a].find_all("td")[2].text
                except:
                    market_cap_change =  ""
                try:
                    market_cap_raw = search_tag_list[a].text
                except:
                    market_cap_raw =  ""
                
                market_cap_dict = {"player" : player, "formated_name" : formated_name, "scraped_name" : scraped_name,"country":country, "year_market_cap" : year_market_cap,"market_cap":market_cap,  "market_cap_change":market_cap_change, "market_cap_raw":market_cap_raw, "Current_url" : current_url}
                market_cap_df = pd.DataFrame(market_cap_dict, index=[0])#,columns=["players", "formated_name", "scraped_name","country", "year_market_cap","market_cap", "market_cap_change", "market_cap_raw",])
                with open(output_file_name,'a',newline='',encoding='utf-8') as f:
                    market_cap_df.to_csv(f,mode='a',header=f.tell()==0)

        elif filter == "revenue":
            search_tag_list = soup.find("tbody").find_all("tr")
            for a in range(len(search_tag_list)):
                
                try:
                    scraped_name = soup.find(class_ = "company-code").text
                except:
                    scraped_name = ""
                try:
                    country = soup.find_all(class_= "info-box")[2].find(class_ = "responsive-hidden").text
                except:
                    country = ""
                try:
                    year_revenue = search_tag_list[a].find_all("td")[0].text
                except:
                    year_revenue =  ""
                try:
                    revenue = search_tag_list[a].find_all("td")[1].text
                except:
                    revenue =  ""
                try:
                    revenue_change = search_tag_list[a].find_all("td")[2].text
                except:
                    revenue_change =  ""
                try:
                    revenue_raw = search_tag_list[a].text
                except:
                    revenue_raw =  ""

                revenue_dict = {"player" : player, "formated_name" : formated_name, "scraped_name" : scraped_name,"country":country, "year_revenue" : year_revenue,"revenue":revenue,  "revenue_change":revenue_change, "revenue_raw":revenue_raw, "Current_url" : current_url}
                revenue_df = pd.DataFrame(revenue_dict, index=[0])#,columns=["players", "formated_name", "scraped_name","country", "year_revenue","revenue", "revenue_change", "revenue_raw"])
                with open(output_file_name,'a',newline='',encoding='utf-8') as f:
                    revenue_df.to_csv(f,mode='a',header=f.tell()==0)

        elif filter == "pe-ratio":
            search_tag_list = soup.find("tbody").find_all("tr")
            for a in range(len(search_tag_list)):
                
                try:
                    scraped_name = soup.find(class_ = "company-code").text
                except:
                    scraped_name = ""
                try:
                    country = soup.find_all(class_= "info-box")[2].find(class_ = "responsive-hidden").text
                except:
                    country = ""
                try:
                    year_pe_ratio = search_tag_list[a].find_all("td")[0].text
                except:
                    year_pe_ratio =  ""
                try:
                    pe_ratio = search_tag_list[a].find_all("td")[1].text
                except:
                    pe_ratio =  ""
                try:
                    pe_ratio_change = search_tag_list[a].find_all("td")[2].text
                except:
                    pe_ratio_change =  ""
                try:
                    pe_ratio_raw = search_tag_list[a].text
                except:
                    pe_ratio_raw =  ""    

                pe_ratio_dict = {"player" : player, "formated_name" : formated_name, "scraped_name" : scraped_name,"country":country, "year_pe_ratio" : year_pe_ratio,"pe_ratio":pe_ratio,  "pe_ratio_change":pe_ratio_change, "pe_ratio_raw":pe_ratio_raw, "Current_url" : current_url}
                pe_ratio_df = pd.DataFrame(pe_ratio_dict, index=[0])#,columns=["players", "formated_name", "scraped_name","country", "year_pe_ratio","pe_ratio", "pe_ratio_change", "pe_ratio_raw"])
                with open(output_file_name,'a',newline='',encoding='utf-8') as f:
                    pe_ratio_df.to_csv(f,mode='a',header=f.tell()==0)   
    
    except Exception as e:
        print(e)

def main(start_count, end_count, filter, source_file_name, output_file_name):
    try:
        url_df = pd.read_csv(source_file_name, encoding = "latin" )
        url_df.fillna("", inplace = True) #,encoding='latin'
        c = start_count
        for row in url_df[start_count:end_count].iterrows():
            try:
                row = row[1]
                player = row["player"]
                formated_name = row["formatted_player"]
                base_url = row["url"]

                print(f"{str(c)} ---- {player} ---- {formated_name}")
                logger.info(f"{str(c)} ---- {player} ----- {formated_name}")

                if base_url =="":
                    name = formated_name.lower()
                    name = name.replace(" ", "-")
                    base_url = f"https://companiesmarketcap.com/{name}"
                
                    print(f"Base url  --- {str(base_url)}")
                    logger.info(f"Base url  --- {str(base_url)}")
                    base_url = str(base_url).strip()
                    current_url = f"{base_url}/{filter}/"
                else:
                    base_url = base_url.replace("/marketcap/", "").strip()

                    # url = base_url.strip()
                    # filter_list = ["marketcap","revenue","pe-ratio"]s
                    # pdb.set_trace()
                    # for filter in filter_list:
                    current_url = f"{base_url}/{filter}/"

                print(f"current url   :   {str(current_url)}")
                logger.info(f"current url   :   {str(current_url)}")
        
                response = requests.get(current_url)  
                soup = BeautifulSoup(response.content, 'html.parser')
                time.sleep(2)
                
                extract_url(soup,player,formated_name,current_url, output_file_name)
                time.sleep(1)
                

            except Exception as e:
                print("Main Loop Exception " + str(e))
                logger.info("Main Loop Exception " + str(e))
                continue


    except Exception as e:
        print("Main Exception ", e)
        logger.info("Main Exception " + str(e))

if __name__ == '__main__':

    file_no = sys.argv[1]
    start_count = int(sys.argv[2])
    end_count = int(sys.argv[3])
    source_file_name = 'market_analysis_1.2.csv'

    filter_list = ["marketcap","revenue","pe-ratio"]

    for filter in filter_list:
        output_file_name = f"companies_{filter}" + str(file_no) + ".csv"
        log_file_name = f"companies_{filter}" +  str(file_no) + ".log"
        logger = set_log_file(log_file_name)

        main(start_count, end_count, filter, source_file_name, output_file_name)