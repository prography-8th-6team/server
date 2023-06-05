import requests

from applications.base.jwt_utils import decode_jwt, generate_access_jwt, generate_refresh_jwt


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


def token_equality_check(access_token, refresh_token):
    access_token_payload = decode_jwt(access_token)
    refresh_token_payload = decode_jwt(refresh_token)

    if access_token_payload and refresh_token_payload:
        access_token_user_id = access_token_payload.get("user_id", None)
        refresh_token_user_id = refresh_token_payload.get("user_id", None)

        if access_token_user_id == refresh_token_user_id:
            new_access_token = generate_access_jwt(access_token_user_id)
            new_refresh_token = generate_refresh_jwt(refresh_token_user_id)

            results = {"token": new_access_token, "refresh_token": new_refresh_token}
            return results
        else:
            return None
    else:
        return None
