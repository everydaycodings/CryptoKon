import requests
from bs4 import BeautifulSoup
import json
import streamlit as st
import http.client
import json


def update_list():
    conn = http.client.HTTPSConnection("api.coingecko.com")

    headersList = {
    "Accept": "*/*",
    "User-Agent": "Thunder Client (https://www.thunderclient.com)" 
    }

    payload = ""

    conn.request("GET", "/api/v3/coins/list?include_platform=false", payload, headersList)
    response = conn.getresponse()
    result = response.read()
    data = result.decode("utf-8")

    file_opened = open("files/crypto_list.json", "w")
    file_opened.write(data)



def get_asset_list():

    asset_list = []
    f = open("files/crypto_list.json", "r")
    asset_dist = json.load(f)

    for asset in asset_dist:
        name = "{} | ({})".format(asset["name"], asset["symbol"])
        asset_list.append(name)

    return asset_list


def get_asset_id(asset_name):

    f = open("files/crypto_list.json", "r")
    asset_dist = json.load(f)

    for asset in asset_dist:
        if asset['name'] == str(asset_name).split(" | ")[0]:
            res = asset["id"]
            return res


def text_added(asset):

    if str(asset).find('-') != -1:
        return "danger"
    else:
        return "success"




def asset_signals(slug):
    
    data_list = []

    try:
        reqUrl = "https://services.intotheblock.com/api/{}/signals".format(slug)

        headersList = {
        "Accept": "*/*",
        "User-Agent": "Thunder Client (https://www.thunderclient.com)" 
        }

        payload = ""

        response = requests.request("GET", reqUrl, data=payload,  headers=headersList).text

        response = json.loads(response)

        bearish = response["summary"]["bearish"]
        neutral = response["summary"]["neutral"]
        bullish = response["summary"]["bullish"]

        data_summary = {
            "bearish": bearish,
            "neutral": neutral,
            "bullish": bullish
        }
        

        for i in range(len(response["signals"])):

            single_response = response["signals"][i]

            name = single_response["name"]

            if name == "futures_market_momentum":
                futures_market_momentum = single_response["sentiment"]
                
                data = {
                    "name": single_response["title"],
                    "data": futures_market_momentum
                }

                data_list.append(data)
            
            elif name == "addresses_net_growth":
                addresses_net_growth = "{}% {}".format(float(single_response["value"]) * 100,  single_response["sentiment"])

                data = {
                    "name": single_response["title"],
                    "data": addresses_net_growth
                }
                
                data_list.append(data)

            elif name == "in_out_var":
                in_out_var = "{}% {}".format(float(single_response["value"]) * 100,  single_response["sentiment"])

                data = {
                    "name": single_response["title"],
                    "data": in_out_var
                }
                
                data_list.append(data)

            elif name == "concentration_var":
                in_out_var = "{}% {}".format(float(single_response["value"]) * 100,  single_response["sentiment"])

                data = {
                    "name": single_response["title"],
                    "data": in_out_var
                }
                
                data_list.append(data)

            elif name == "largetxs_var":
                in_out_var = "{}% {}".format(float(single_response["value"]) * 100,  single_response["sentiment"])

                data = {
                    "name": single_response["title"],
                    "data": in_out_var
                }
                
                data_list.append(data)

            elif name == "smart_price":
                in_out_var = "{}% {}".format(float(single_response["value"]) * 100,  single_response["sentiment"])

                data = {
                    "name": single_response["title"],
                    "data": in_out_var
                }
                
                data_list.append(data)

            elif name == "bid_ask_imbalance":
                in_out_var = "{}% {}".format(float(single_response["value"]) * 100,  single_response["sentiment"])

                data = {
                    "name": single_response["title"],
                    "data": in_out_var
                }
                
                data_list.append(data)
    
    except:
        data_summary = {}
    

    
    return data_summary, data_list



def asset_overview(slug):


    try:
        reqUrl = "https://services.intotheblock.com/api/{}/overview".format(slug)

        headersList = {
        "Accept": "*/*",
        "User-Agent": "Thunder Client (https://www.thunderclient.com)" 
        }

        payload = ""

        response = requests.request("GET", reqUrl, data=payload,  headers=headersList).text

        response = json.loads(response)


        large_trx = response["largeTxs"]
        whale_holdings = float(response["concentration"]) * 100
        btc_correlation = float(response["btcCorrelation"]) * 100
        money_in = response["inOutOfTheMoney"]["in"]
        money_between = response["inOutOfTheMoney"]["between"]
        money_out = response["inOutOfTheMoney"]["out"]
        holder = response["byTimeHeldComposition"]["hodler"]
        trader = response["byTimeHeldComposition"]["trader"]
        cruiser = response["byTimeHeldComposition"]["cruiser"]

        data = {

            "large_trx_num": len(large_trx),
            "whale_holdings": "%.2f"%whale_holdings,
            "btc_correlation": "%.2f"%btc_correlation,
            "money_in": money_in,
            "money_out": money_out,
            "money_between": money_between,
            "holder": holder,
            "cruiser": cruiser,
            "trader": trader
        }

    
    except:

        data = {}

    return data



def crypto_desc(slug):

    data_list = []

    try:
        reqUrl = "https://research.binance.com/en/projects/{}".format(slug)

        headersList = {
        "Accept": "*/*",
        "User-Agent": "Thunder Client (https://www.thunderclient.com)" 
        }

        payload = ""

        response = requests.request("GET", reqUrl, data=payload,  headers=headersList).text
        soup = BeautifulSoup(response, 'html.parser')

        for s in  soup.find( class_ = "jsx-341700367" ):
            desc = list(s.text.split("."))
            data_list = desc
    
    except:
        pass
    
    return data_list



def asset_details_v2(asset_id):

    green_score = []
    yellow_score = []
    red_score = []

    data_list = []
    try:
        reqUrl = "https://api.coingecko.com/api/v3/coins/{}?localization=false&tickers=true&market_data=true&community_data=true&developer_data=true&sparkline=true".format(asset_id)

        headersList = {
        "Accept": "*/*",
        "User-Agent": "Thunder Client (https://www.thunderclient.com)" 
        }

        payload = ""

        response = requests.request("GET", reqUrl, data=payload,  headers=headersList).text
        response = json.loads(response)

        slug = response["id"]
        name = "{}({})".format(response["name"], response["symbol"])
        hashing_algorithm = response["hashing_algorithm"]

        try:
            homepage = response["links"]["homepage"]
        except:
            homepage = ["--"]
        
        
        try:
            blockchain_link = response["links"]["blockchain_site"]
        except:
            blockchain_link = ["--"]
        
        try:
            facebook_name = response["links"]["facebook_username"]
        except:
            facebook_name = ["--"]
        
        try:
            subreddit_url = response["links"]["subreddit_url"]
            subreddit_name = str(subreddit_url).replace("https://www.reddit.com/r/", "")

        except:
            subreddit_url = "--"
        
        try:
            github_link = response["links"]["repos_url"]["github"]
        except:
            github_link = ["--"]
        
        try:
            asset_img = response["image"]["large"]
        except:
            asset_img = ["--"]
        
        try:
            country_origin = response["country_origin"]
        except:
            country_origin = ["--"]
        
        try:
            market_cap_Rank = response["market_cap_rank"]
        except:
            market_cap_Rank = "--"
        
        try:
            current_price = response["market_data"]["current_price"]["usd"]
        except:
            current_price = 0.001
        
        try:
            roi = "%.2f"%float(response["market_data"]["roi"]["percentage"])
        except:
            roi = "--"
        
        try:
            ath = response["market_data"]["ath"]["usd"]
        except:
            ath = 0.00
        
        try:
            atl = response["market_data"]["atl"]["usd"]
        except:
            atl = 0.0
        
        try:
            ath_per = response["market_data"]["ath_change_percentage"]["usd"]
        except:
            ath_per = "--"
        
        try:
            atl_per = response["market_data"]["atl_change_percentage"]["usd"]
        except:
            atl_per = "--"
        
        try:
            dilution_cap = response["market_data"]["fully_diluted_valuation"]["usd"]
        except:
            dilution_cap = 0.0

        try:
            market_cap = response["market_data"]["market_cap"]["usd"]
        except:
            market_cap = 0.00
        
        try:
            volume = response["market_data"]["total_volume"]["usd"]
        except:
            volume = 0.0

        try:
            facebook_likes = response["community_data"]["facebook_likes"]
        except:
            facebook_likes = "--"
        
        try:
            reddit_average_posts_48h = response["community_data"]["reddit_average_posts_48h"]
        except:
            reddit_average_posts_48h = "--"
        
        try:
            reddit_average_comments_48h = response["community_data"]["reddit_average_comments_48h"]
        except:
            reddit_average_comments_48h = "--"
        
        try:
            reddit_subscribers = response["community_data"]["reddit_subscribers"]
        except:
            reddit_subscribers = "--"
        
        try:
            reddit_accounts_active_48h = response["community_data"]["reddit_accounts_active_48h"]
        except:
            reddit_accounts_active_48h = "--"
        
        try:
            telegram_channel_user_count = response["community_data"]["telegram_channel_user_count"]
        except:
            telegram_channel_user_count = "--"

        try:
            github_subscribers = response["developer_data"]["subscribers"]
        except:
            github_subscribers = "--"
        
        try:
            pull_request_contributors = response["developer_data"]["pull_request_contributors"]
        except:
            pull_request_contributors = "--"

        try:
            twitter = "https://twitter.com/{}".format(response["links"]["twitter_screen_name"])
            twitter_name = response["links"]["twitter_screen_name"]
        except:
            twitter = "--"
            twitter_name = "--"
        
        try:
            twitter_followers = response["community_data"]["twitter_followers"]
        except:
            twitter_followers = "--"
        
        try:
            alexa_rank = response["public_interest_stats"]["alexa_rank"]
        except:
            alexa_rank = "--"
        
        try:
            up_vote = response["sentiment_votes_up_percentage"]
        except:
            up_vote = "--"
        
        try:
            coingecko_rank = response["coingecko_rank"]
        except:
            coingecko_rank = "--"
        
        try:
            developer_score = response["developer_score"]
        except:
            developer_score = "--"
        
        try:
            community_score = response["community_score"]
        except:
            community_score = "--"
        
        try:
            liquidity_score = response["liquidity_score"]
        except:
            liquidity_score = "--"
        
        try:
            price_change_24h = response["market_data"]["price_change_percentage_24h"]
            marketcap_change_24h = response["market_data"]["market_cap_change_percentage_24h"]
        except:
            price_change_24h = 0.0
            marketcap_change_24h = 0.0
        
        try:
            max_supply = response["market_data"]["max_supply"]
        except:
            max_supply = "--"
        
        try:
            total_supply = response["market_data"]["total_supply"]
        except:
            total_supply = "--"
        
        try:
            circulating_supply = response["market_data"]["circulating_supply"]
        except:
            circulating_supply = "--"
        
        try:
            forks = response["developer_data"]["forks"]
        except:
            forks = "--"
        
        try:
            stars = response["developer_data"]["stars"]
        except:
            stars = "--"
        
        try:
            total_issues = response["developer_data"]["total_issues"]
        except:
            total_issues = "--"
        
        try:
            closed_issues = response["developer_data"]["closed_issues"]
        except:
            closed_issues = "--"
        
        try:
            pull_requests_merged = response["developer_data"]["pull_requests_merged"]
        except:
            pull_requests_merged = "--"
        
        try:
            commit_count_4_weeks = response["developer_data"]["commit_count_4_weeks"]
        except:
            commit_count_4_weeks = "--"
        
        try:
            categories = str(response["categories"]).replace("[", "").replace("]", "").replace("'", "")
        except:
            categories = "--"

        try:
            market_turover_rate = "%.2f"%((volume / market_cap) * 100)
        except:
            market_turover_rate = "--"
        
        try:
            investors_link = "https://dropstab.com/{}".format(asset_id)
        except:
            investors_link = ""
        
        try:
            investors_link_fund = "https://dropstab.com/{}/fundraising".format(asset_id)
        except:
            investors_link_fund = ""
        
        try:
            binance_research = "https://research.binance.com/en/projects/{}".format(asset_id)
        except:
            binance_research = ""
        
        other_links = [investors_link, binance_research, investors_link_fund]

        for i in range(len(response["tickers"])):
            single_scores = response["tickers"][i]

            score = single_scores["trust_score"]

            if score == "green":
                green_score.append(score)
            
            elif score == "yellow":
                yellow_score.append(score)

            elif score == "red":
                red_score.append(score)
        
        data = {
            "slug": slug,
            "name": name,
            "asset_img": asset_img,
            "country_origin": country_origin,
            "market_cap_Rank": market_cap_Rank,
            "current_price": current_price,
            "current_price_per": price_change_24h,
            "current_price_text": text_added(price_change_24h),
            "roi": roi,
            "ath": ath,
            "atl": atl,
            "ath_per": ath_per,
            "ath_text": text_added(ath_per),
            "atl_per": atl_per,
            "atl_text": text_added(atl_per),
            "market_cap": market_cap,
            "market_cap_per": marketcap_change_24h,
            "market_cap_text":text_added(marketcap_change_24h),
            "dilution_cap": dilution_cap,
            "volume": volume,
            "hashing_algorithm": hashing_algorithm,
            "homepage": homepage,
            "blockchain_link": blockchain_link,
            "facebook_name": facebook_name,
            "subreddit_url": subreddit_url,
            "subreddit_name": subreddit_name,
            "twitter_url": twitter,
            "twitter_name":twitter_name,
            "twitter_followers": twitter_followers,
            "facebook_likes": facebook_likes,
            "reddit_average_posts_48h": reddit_average_posts_48h,
            "reddit_average_comments_48h": reddit_average_comments_48h,
            "reddit_subscribers": reddit_subscribers,
            "reddit_accounts_active_48h": reddit_accounts_active_48h,
            "telegram_channel_user_count": telegram_channel_user_count,
            "github_link": github_link,
            "github_subscribers": github_subscribers,
            "forks": forks,
            "stars": stars,
            "total_issues": total_issues,
            "closed_issues": closed_issues,
            "pull_requests_merged": pull_requests_merged,
            "commit_count_4_weeks": commit_count_4_weeks,
            "pull_request_contributors": pull_request_contributors,
            "alexa_rank": alexa_rank,
            "up_vote": up_vote,
            "coingecko_rank": coingecko_rank,
            "developer_score": developer_score,
            "community_score": community_score,
            "liquidity_score": liquidity_score,
            "max_supply": max_supply,
            "total_supply": total_supply,
            "circulating_supply": circulating_supply,
            "categories": categories,
            "market_turnover_rate": market_turover_rate,
            "green_score": len(green_score),
            "yellow_score": len(yellow_score),
            "red_score": len(red_score),
            "other_links": other_links
        }

        data_list.append(data)
    
    except:
        pass

    return data



def ico_details(asset_id):

    date_list = []

    try:

        reqUrl = "https://dropstab.com/{}".format(asset_id)

        headersList = {
        "Accept": "*/*",
        "User-Agent": "Thunder Client (https://www.thunderclient.com)" 
        }

        payload = ""

        response = requests.request("GET", reqUrl)
        soup_raw = BeautifulSoup(response.content, features="html.parser")
        soup = BeautifulSoup(soup_raw.prettify(), features="html.parser")

        ico_price_raw = soup.find_all("div", {"class": "flex w-full items-center text-sm font-medium border-b border-solid border-gray-200 py-3 dark:border-zinc-700"})

        for i in ico_price_raw:
            ico_price = i.find("dd", {"class": "ml-auto min-w-0 text-right"}).getText().strip(" ").strip("\n").strip(" ")

        ico_date_raw = soup.find_all("div", {"class": "flex w-full items-center text-sm font-medium pt-3"})
        data_list_raw = ico_date_raw[0].find_all("time", {"class": "whitespace-nowrap"})

        for i in data_list_raw:
            ico_date = i.getText().strip(" ").strip("\n").strip(" ")

            date_list.append(ico_date)

        data = {
            "ico_price": ico_price,
            "ico_date": "{} - {}".format(date_list[0], date_list[1])
        }

    except:

        data = {
            "ico_price": "--",
            "ico_date": "--"
        }

    return data



def token_statics(asset_id):

    text_data = []
    text_data_result = []

    try:
        reqUrl = "https://dropstab.com/{}/fundraising".format(asset_id)

        headersList = {
        "Accept": "*/*",
        "User-Agent": "Thunder Client (https://www.thunderclient.com)" 
        }

        payload = ""

        response = requests.request("GET", reqUrl, data=payload,  headers=headersList)
        soup_raw = BeautifulSoup(response.content, features="html.parser")
        soup = BeautifulSoup(soup_raw.prettify(), features="html.parser")

        first_layer = soup.find_all("div", attrs={"class": "space-y-4 md:space-y-6 lg:ml-5 lg:flex lg:w-1/3 lg:min-w-0 lg:max-w-xs lg:flex-col lg:self-start xl:ml-6"})[0]
        second_layer = first_layer.find_all("section")[1]
        third_layer = second_layer.find_all("div", attrs={"class": "my-3 flex items-center justify-between space-x-2 font-medium first:mt-0 last:mb-0"})
        
        for final_layer in third_layer:
            
            text = final_layer.find("dt", attrs={"aria-describedby": "ico-drops-score"}).text.strip()
            result = final_layer.find("dd", attrs={"class": "truncate text-base text-gray-800 dark:text-white"}).text.strip().replace("\xa0", " ")
            
            text_data.append(text)
            text_data_result.append(result)

        data = {
            "Total_Tokens_Sold": text_data_result[0],
            "Total_Sale": text_data_result[1],
            "Total_Raised": text_data_result[2],
        }
    
    except:
        data = {
            "Total_Tokens_Sold": "--",
            "Total_Sale": "--",
            "Total_Raised": "--",
        }

    return data




def fetch_token_allocation(asset_id):

    data_list = []

    try:
        reqUrl = "https://research.binance.com/en/projects/{}".format(asset_id)

        headersList = {
        "Accept": "*/*",
        "User-Agent": "Thunder Client (https://www.thunderclient.com)" 
        }

        payload = ""

        response = requests.request("GET", reqUrl, data=payload,  headers=headersList)
        soup_raw = BeautifulSoup(response.content, features="html.parser")
        soup = BeautifulSoup(soup_raw.prettify(), features="html.parser")

        first_layer = soup.find_all("div", attrs={"class": "jsx-540937487"})[2]
        second_layer = first_layer.find("table")
        third_layer = first_layer.find("tbody")
        fourth_layers = third_layer.find_all("tr")
        for fourth_layer in fourth_layers:
            text = fourth_layer.find_all("td", attrs={"class": "jsx-1887592274"})[0].text.strip()
            result = fourth_layer.find_all("td", attrs={"class": "jsx-1887592274"})[1].text.strip().replace(" of the total token supply", "")
            
            data = {
                "text": text,
                "result": result
            }
            data_list.append(data)
    
    except:

        data = {
            "text": "Status",
            "result": "No Data"
        }
        data_list.append(data)

    return data_list