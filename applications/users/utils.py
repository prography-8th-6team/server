import requests


def kakao_get_user_info(access_token):
    """
    카카오 사용자 정보 가져오는 함수입니다.
    """
    kakao_url = "https://kapi.kakao.com"
    get_kakao_user_info_path = "/v2/user/me"

    headers = {"Authorization": f"Bearer ${access_token}",
               "Content-type": "application/x-www-form-urlencoded;charset=utf-8"}

    response = requests.get(kakao_url + get_kakao_user_info_path, headers=headers)

    try:
        kakao_data = response.json()
        kakao_id = kakao_data['id']
        nickname = kakao_data['kakao_account']['profile']['nickname']

        kakao_info = {"id": kakao_id, "nickname": nickname}
        return kakao_info
    except:
        return None
