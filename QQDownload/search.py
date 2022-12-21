import requests

def search_music(req):
    # obj = {...req.query, ...req.body}
    # uin = globalCookie.userCookie()['uin']
    # if obj.get('ownCookie'):
    #     uin = req.cookies.get('uin') or uin

    page_no =  1
    page_size =  20
    key = "周杰伦"
    search_type = 0
    raw = 0

    # if not key:
    #     return {
    #         'result': 500,
    #         'errMsg': '关键词不能为空'
    #     }

    # cache_key = f'search_{key}_{page_no}_{page_size}_{search_type}'
    # cache_data = cache.get(cache_key)
    # if cache_data:
    #     return cache_data

    type_map = {
        0: 'song',
        2: 'album',
        1: 'singer',
        3: 'songlist',
        7: 'lyric',
        12: 'mv'
    }
    if search_type not in type_map:
        return {
            'result': 500,
            'errMsg': '搜索类型错误，检查一下参数 t'
        }

    params = {
        'req_1': {
            'method': 'DoSearchForQQMusicDesktop',
            'module': 'music.search.SearchCgiService',
            'param': {
                'num_per_page': page_size,
                'page_num': page_no,
                'query': key,
                'search_type': search_type
            }
        }
    }
    result = {}

    try:
        result = requests.post(
            url='https://u.y.qq.com/cgi-bin/musicu.fcg',
            data=params,
            headers={
                'Referer': 'https://y.qq.com'
            }
        ).json()
    except requests.exceptions.RequestException as error:
        return {
            'result': 400,
            'error': str(error)
        }

    if raw:
        return result

    print(1)

    response = {
        'result': 100,
        'data': {
            'list': result['req_1']['data']['body'][type_map[search_type]]['list'],
            'pageNo': page_no,
            'pageSize': page_size,
            'total': result['req_1']['data']['meta']['sum'],
            'key': result['req_1']['data']['meta']['query'] or key,
            't': search_type,
            'type': type_map[search_type]
        }
    }
    print(response)


def search():
    req= requests.get(
        url="http://127.0.0.1:3300/search?key=周杰伦"
    )
    res =req.json()
    print(1)
    
    
if __name__ == '__main__':
    search()
    