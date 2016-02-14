from urllib.request import urlopen, Request

if __name__ == '__main__':
    header = dict();
    header['User-Agent'] = r"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:44.0) Gecko/20100101 Firefox/44.0"
    header['X-Requested-With'] = r"XMLHttpRequest"
    header['Accept-Language'] = r"en-US,en;q=0.5"
    header['Content-Type'] = r"application/x-www-form-urlencoded; charset=UTF-8"

    # TODO add your own cookie here in the header

    data = "offset=180&start=1453458896&_xsrf=a1bf5b6350d9bdbd63401b9ebd05cb2d".encode("ascii")


    url = Request(
            url=r"https://www.zhihu.com/topic/20026905/followers",
            data=data,
            headers=header
    )

    s = urlopen(url).read().decode("utf-8")