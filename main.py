# -*- coding: <utf-8> -*-

import bs4
from urllib.request import urlopen
from json import dumps
from time import localtime, strftime

# check the URL pattern constantly for update
URL_TEMPLATE_USER = r"http://www.zhihu.com/people/{0:s}"


def getUserInfoById(id):

    '''
    :param id: the user id searched for
    :return: json-string contains the information about the user
    '''

    if len(str(id).strip()) == 0:
        return dumps({})

    userURL = URL_TEMPLATE_USER.format(str(id))

    # read the html
    s = urlopen(userURL).read()
    return __processUserString(s)

def __parseZhihuTime(sec):
    return strftime("%Y-%m-%d %H:%M:%S",localtime(int(sec)))

def __processUserString(s):
    d = dict()
    soup = bs4.BeautifulSoup(s, "lxml")

    d['name'] = str(soup.select_one("div.title-section > span.name").string)

    if soup.select_one("div.title-section > span.bio"):
        d['remark'] = str(soup.select_one("div.title-section > span.bio").string)

    #weibo if exists
    if soup.select_one(".zm-profile-header-user-weibo"):
        d['weibo'] =soup.select_one(".zm-profile-header-user-weibo")['href']

    if soup.select_one("span.business.item"):
        d['business'] = str(soup.select_one("span.business.item")['title'])

    # icon-profile-male
    if soup.select_one("span.info-wrap > span.gender > i"):
        d['gender'] = [i for i in soup.select_one("span.info-wrap > span.gender > i")['class'] if "profile" in i][0].split("-")[2]

    # info about zhihu involvement
    d['agrees_recieved'] = int(soup.select_one(".zm-profile-header-user-agree > strong").string)
    d['thanks_recieved'] = int(soup.select_one(".zm-profile-header-user-thanks > strong").string)

    # answers

    answer_agree = [int(i.string) for i in soup.select("#zh-profile-answers-inner-list  .zm-profile-vote-num")]
    answer_question = [i.string for i in soup.select("#zh-profile-answers-inner-list .zm-profile-question .question_link")]
    answer_text = [i.string for i in soup.select("#zh-profile-answers-inner-list .zm-profile-item-text")]
    d['answer'] = list(zip(answer_question, answer_text, answer_agree))


    # last active
    last_active_time = [__parseZhihuTime(i["data-time"]) for i in soup.select("#zh-profile-activity-wrap .zm-profile-section-item.zm-item.clearfix")]
    last_active_question = [str(i.string) for i in soup.select("#zh-profile-activity-wrap a.question_link")]
    last_active_question_url = [i['href'] for i in soup.select("#zh-profile-activity-wrap a.question_link")]

    d['activity'] = list(zip(last_active_time, last_active_question, last_active_question_url))

    return dumps(d, ensure_ascii=False)

if __name__ == "__main__":
    print(getUserInfoById("sgfxq"))