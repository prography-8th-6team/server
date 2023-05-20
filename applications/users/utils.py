import requests


def kakaoGetUserInfo(access_token):
    """
    카카오 사용자 정보 가져오는 함수입니다.
    """
    kakaoURL = "https://kapi.kakao.com"
    getKakaoUserInfoPath = "/v2/user/me"

    headers = {"Authorization": f"Bearer ${access_token}",
               "Content-type": "application/x-www-form-urlencoded;charset=utf-8"}

    response = requests.get(kakaoURL + getKakaoUserInfoPath, headers=headers)

    try:
        kakaoInfo = response.json()

        kakaoId = kakaoInfo['id']
        nickname = kakaoInfo['kakao_account']['profile']['nickname']

        kakaoInfo = {"id": kakaoId, "nickname": nickname}
        return kakaoInfo
    except Exception:
        return None


