import requests


def kakaoGetUserInfo(access_token):
    """
    카카오 사용자 정보 가져오는 함수입니다.
    """
    kakao_url = "https://kapi.kakao.com"
    getKakaoUserInfoPath = "/v2/user/me"

    headers = {"Authorization": f"Bearer ${access_token}",
               "Content-type": "application/x-www-form-urlencoded;charset=utf-8"}

    response = requests.get(kakao_url + getKakaoUserInfoPath, headers=headers)

    try:
        kakaoInfo = response.json()
        kakaoId = kakaoInfo['id']
        nickname = kakaoInfo.get('kakao_account', {}).get('profile', {}).get('nickname', None)
        import random
        nickname = nickname if nickname else 'jerny' + ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=3))

        kakaoInfo = {"id": kakaoId, "nickname": nickname}
        return kakaoInfo
    except Exception:
        return None


