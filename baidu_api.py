import time
import requests
import pandas as pd
from tqdm import tqdm

URL = "https://opendata.baidu.com/api.php?" \
      "resource_id=6899&" \
      "query=失信人名单&" \
      "cardNum={card_id}&" \
      "iname={name}&" \
      "areaName={area}&" \
      "pn={page}&" \
      "rn={row_number}&" \
      "from_mid=1&" \
      "format=json&" \
      "t={time}&" \
      "ie=utf-8&" \
      "oe=utf-8"


def format_url(name, card_id="", area="", page=0, row_number=50) -> str:
    """获取URL."""
    current_time = int(time.time())
    return URL.format(card_id=card_id,
                      name=name,
                      area=area,
                      page=page * row_number,
                      row_number=row_number,
                      time=current_time)


def request_baidu_data(name, card_id="", area="", page=0) -> dict:
    """基本的请求函数，可以加入sleep等进行改进.

    Notes
      这个函数如果请求成功，会返回一个dict

    """
    response = requests.get(format_url(name, card_id, area, page))
    if response.ok:
        return response.json()
    else:
        raise Exception("request failure")


def get_baidu_data(name, card_id="", area="", page=0, sleep=0.0) -> list:
    """这是一个简单的request函数例子，如果有必要可以加入sleep等等改进."""
    data = request_baidu_data(name=name, card_id=card_id, area=area, page=page)
    time.sleep(sleep)
    if data["data"]:
        list_of_people = data["data"][0]["disp_data"]
        return list_of_people
    return []


def get(name, card_id="", area="", max_page=1000) -> pd.DataFrame:
    """
    该函数会一页一页（每页50个）地下载数据并显示进度，最大默认1000页.

    Notes:
        可能会有少部分重复数据，注意检查.

    """
    list_of_people = []
    last_case_code = []
    page = 0
    with tqdm() as bar:
        while page < max_page:
            # download data
            data = get_baidu_data(name,
                                  card_id=card_id,
                                  area=area,
                                  page=page,
                                  sleep=0.1)
            # terminate if data is empty or is the same as the last result
            data_case_code = [i["caseCode"] for i in data]
            if (last_case_code and last_case_code == data_case_code) or not data:
                return pd.DataFrame(list_of_people).drop_duplicates()
            # append data
            list_of_people += data
            page += 1
            last_case_code = data_case_code
            bar.update(1)
        return pd.DataFrame(list_of_people).drop_duplicates()


# test
if __name__ == '__main__':
    print(get(name="杨文豪"))
    print(get(name="杨文豪", area="北京"))
