"""
weather = [
    ['9월 1일', '경기', '맑음', 27.2, 0.4, 0.1],
    ['9월 1일', '강원', '맑음', 27.2, 0.4, 0.1],
    ['9월 1일', '인천', '맑음', 27.2, 0.4, 0.1],
    ['9월 1일', '서울', "맑음", 27.2, 0.4, 0.1]
]



print(weather[0][1])
"""
"""
weather = [
    {'날짜':'9월 1일', '지역':'경기', '날씨':'맑음', '기온':27.2, '습도':0.4, '강수확률':0.1},
    {'날짜':'9월 1일', '지역': '인천', '날씨': '맑음', '기온': 27.2, '습도': 0.4, '강수확률': 0.1},
    {'날짜':'9월 1일', '지역':'서울', '날씨':'맑음', '기온':27.2, '습도':0.4, '강수확률':0.1},
    {'날짜':'9월 1일', '지역': '부', '날씨': '맑음', '기온': 27.2, '습도': 0.4, '강수확률': 0.1}
]
"""

import pprint
weather = [
    {
        '날짜':'9월 1일',
        '지역':'경기',
        '날씨':'맑음',
        '기온':27.2,
        '습도':0.4,
        '강수확률':0.1
    },
    {
        '날짜':'9월 1일',
        '지역': '인천',
        '날씨': '맑음',
        '기온': 27.2,
        '습도': 0.4,
        '강수확률': 0.1
    },
    {
        '날짜':'9월 1일',
        '지역':'서울',
        '날씨':'맑음',
        '기온':27.2,
        '습도':0.4,
        '강수확률':0.1
    },
    {
        '날짜':'9월 1일',
        '지역': '부',
        '날씨': '맑음',
        '기온': 27.2,
        '습도': 0.4,
        '강수확률': 0.1
    }
]

pprint.pprint(weather)