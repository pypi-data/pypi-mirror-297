import os
try:
    import requests
    import random,user_agent
    import uuid,instaloader,time
except:
        os.system("pip install requests random user_agent uuid instaloader time")
        import requests
        import random,user_agent
        import uuid,instaloader,time
uuidd = str(uuid.uuid4())
device_id = uuidd.replace("-", "")
class Instagram:
    def Check(email):
                    url = "https://i.instagram.com/api/v1/users/lookup/"
                    lookup_headers = {
                                    "Accept-Encoding": "gzip",
                                    "User-Agent": "Instagram 328.0.0.42.92 Android (33/13; 450dpi; 1080x2208; samsung/xiaomi; M2012K11C; a13ve; mt6768; ar_AE; 591192831)",
                                    "X-IG-Android-ID": f"android-{device_id}",
                                    "X-IG-Device-ID": uuidd,
                                }
                    data = {
                                    "signed_body": "SIGNATURE.{\"country_codes\":\"[{\\\"country_code\\\":\\\"971\\\",\\\"source\\\":[\\\"default\\\"]}]\",\"phone_id\":\"{uuid}\",\"q\":\"{email}\",\"guid\":\"{uuid}\",\"device_id\":\"android-{device_id}\",\"android_build_type\":\"release\",\"waterfall_id\":\"{uuid}\",\"directly_sign_in\":\"true\",\"is_wa_installed\":\"true\"}".replace("{email}", email).replace("{uuid}", uuidd).replace("{device_id}", device_id)
                                }

                    lookup_response = requests.post(url, headers=lookup_headers, data=data)
                    if "multiple_users_found" in lookup_response.text:
                        return {'status': 'Good', 'result': 'Account Found', 'Mode': '@KKKKKQ9'}
                    else:
                            return {'status': 'Good', 'result': 'Account Not Found', 'Mode': '@KKKKKQ9'}
    def Info(user):
                headers = {
  'authority': 'i.instagram.com',
  'accept': '*/*',
  'accept-language': 'ar-AE,ar;q=0.9,en-US;q=0.8,en;q=0.7',
  'origin': 'https://www.instagram.com',
  'referer': 'https://www.instagram.com/',
  'sec-ch-ua': '"Chromium";v="105", "Not)A;Brand";v="8"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Linux"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-site',
  'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
  'x-asbd-id': '198387',
  'x-csrftoken': 'bXKL9GTAtK2cYn2IoXBtmQT9J1kEHmQv',
  'x-ig-app-id': '936619743392459',
  'x-ig-www-claim': 'hmac.AR0qFm_PDZfOSVRxZVwKIcwP0xOOG29DNOU5Ec98eOYiANXY',
  'x-instagram-ajax': '1006477071',
  }
                params = {
                'username': f'{user}',
                }
                requests_info1 = requests.get('https://i.instagram.com/api/v1/users/web_profile_info/', params=params, headers=headers)
                requests_info = requests_info1.json()
                name = requests_info['data']['user']['full_name']
                username =  requests_info['data']['user']['username']
                id = requests_info['data']['user']['id']
                following = requests_info['data']['user']["edge_follow"]["count"]
                followers = requests_info['data']['user']["edge_followed_by"]["count"]
                post = requests_info['data']['user']["edge_owner_to_timeline_media"]["count"]
                bio = requests_info['data']['user']['biography']
                id_req = requests.get(f"https://o7aa.pythonanywhere.com/?id={id}").json()
                data = id_req['date']
                link = (f"https://www.instagram.com/{username}/")
                return {'Username':username,'Name':name,'data':data,'Id':id,'Following':following,'Followers':followers,"Post":post,'Bio':bio,'Account_Link':link,'Mode': '@KKKKKQ9'}
    def getoldusers():
        try:
            lsd=''.join(random.choice('2ULwtVInskNgB5QAG8IdQQfY1jVdyRSkg02fn5DXJR4Uuge4db2od8j6BFl0') for _ in range(16))
            id=str(random.randrange(10000,739988755))

            headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://www.instagram.com',
            'referer': 'https://www.instagram.com/0s9s/',
            'user-agent': str(user_agent.generate_user_agent()),
            'x-fb-lsd': 'insta'+lsd,
        }
            data = {
            'lsd': 'insta'+lsd,
            'variables': '{"id":"'+id+'","relay_header":false,"render_surface":"PROFILE"}',
            'doc_id': '7397388303713986',
        }
            user= requests.post('https://www.instagram.com/api/graphql', headers=headers, data=data).json()['data']['user']['username']
            return {'Username':user,'Mode': '@KKKKKQ9'}

        except Exception as e:
            return None
    def sessionid(username,password):
            headers = {"accept": "*/*",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "ar,en;q=0.9",
                "content-length": "317",
                "content-type": "application/x-www-form-urlencoded",
                "cookie": "mid=Yemn3AAEAAGx56yZBU5-oiVvPQ4e; ig_did=B8C62C92-A3F7-418B-8F2D-7552C1467C20; ig_nrcb=1; fbm_124024574287414=base_domain=.instagram.com;",
                "origin": "https://www.instagram.com",
                "referer": "https://www.instagram.com/accounts/login/",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "user-agent": user_agent.generate_user_agent(),
                "x-csrftoken": "dlVqZxJJmbq22SfBTTC3pPlEcsDkptlj",
                "x-ig-app-id": "936619743392459",
                "x-ig-www-claim": "hmac.AR1cXkJeUEqtcGbsTBzJrMSHrjfv-gbYYkqfI4FZCDO_-3mb",
                "x-instagram-ajax": "1c61e9255248",
                "x-requested-with": "XMLHttpRequest"}
            data={'username': username,'enc_password': "#PWD_INSTAGRAM_BROWSER:0:&:"+password,}

            response = requests.post('https://www.instagram.com/api/v1/web/accounts/login/ajax/', headers=headers, data=data)
            try:
                ses = response.cookies.get_dict()['sessionid']
                return {'sessionid':{ses},'Mode': '@KKKKKQ9'}
            except:
                return 'ERROR : Username Or Password Wrong'
    def following(target,sessionid):
        info=requests.get('https://anonyig.com/api/ig/userInfoByUsername/'+target,headers={'user-agent': user_agent.generate_user_agent()}).json()['result']
        id=info['user']['pk']
        count = info['user']['following_count']
        cookies = {
                    'ig_did': '9669EE3D-9AA8-4A7D-84B9-2738EFE07C31',
                    'ig_nrcb': '1',
                    'mid': 'ZuydJgALAAHgHrsiGEXlJTLU8ZBg',
                    'datr': 'Jp3sZu-JWHb3PPSORdl09M0f',
                    'csrftoken': 'BSTqYpml9ApETJCc7SJXCeJUnVQSkKJ3',
                    'ds_user_id': '61133585536',
                    'sessionid': sessionid,
                    'shbid': '"2476\\05461133585536\\0541758318862:01f7b68aa989e19c1d450206cf928099068ab69a3655a60bae81d706b0f0a14eb0d3719a"',
                    'shbts': '"1726782862\\05461133585536\\0541758318862:01f7589e936c303fd72c884e0d071569c031b18b6b56bc6dd0973129f42f56c86570904e"',
                    'wd': '1365x945',
                    'rur': '"RVA\\05461133585536\\0541758318911:01f7085bff8a402a2e6f6e8ab8036052f1cc56e83bd2fca92ea06db3482b5e1af1ddbcbb"',
                }

        headers = {
                    'accept': '*/*',
                    'accept-language': 'en-US,en;q=0.9',
                    # 'cookie': 'ig_did=9669EE3D-9AA8-4A7D-84B9-2738EFE07C31; ig_nrcb=1; mid=ZuydJgALAAHgHrsiGEXlJTLU8ZBg; datr=Jp3sZu-JWHb3PPSORdl09M0f; csrftoken=BSTqYpml9ApETJCc7SJXCeJUnVQSkKJ3; ds_user_id=61133585536; sessionid=61133585536%3AHw3xTTAs2kNoTf%3A24%3AAYfiMml6NV2u7puMNfqKlVJl58xFXkLhErVCUATuZw; shbid="2476\\05461133585536\\0541758318862:01f7b68aa989e19c1d450206cf928099068ab69a3655a60bae81d706b0f0a14eb0d3719a"; shbts="1726782862\\05461133585536\\0541758318862:01f7589e936c303fd72c884e0d071569c031b18b6b56bc6dd0973129f42f56c86570904e"; wd=1365x945; rur="RVA\\05461133585536\\0541758318911:01f7085bff8a402a2e6f6e8ab8036052f1cc56e83bd2fca92ea06db3482b5e1af1ddbcbb"',
                    'priority': 'u=1, i',
                    'referer': 'https://www.instagram.com/d_r_n/following/',
                    'sec-ch-prefers-color-scheme': 'dark',
                    'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
                    'sec-ch-ua-full-version-list': '"Google Chrome";v="129.0.6668.59", "Not=A?Brand";v="8.0.0.0", "Chromium";v="129.0.6668.59"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-model': '""',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-ch-ua-platform-version': '"15.0.0"',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-origin',
                    'user-agent': user_agent.generate_user_agent(),
                    'x-asbd-id': '129477',
                    'x-csrftoken': 'BSTqYpml9ApETJCc7SJXCeJUnVQSkKJ3',
                    'x-ig-app-id': '936619743392459',
                    'x-ig-www-claim': 'hmac.AR09bdfDA0NvG62iAuVQekRHtbPWBf_SQkZdzBIbvmg_JDTd',
                    'x-requested-with': 'XMLHttpRequest',
                }

        params = {
                    'count': count,
                }

        response = requests.get(
                    f'https://www.instagram.com/api/v1/friendships/{id}/following/',
                    params=params,
                    cookies=cookies,
                    headers=headers,
                ).json()
        for i in range(count):
            try:
                username = response['users'][i]['username']
                print({'username':username,'Mode':'@KKKKKQ9'})
            except Exception as e:
                        return 'Your sessionid Got Banned Try Again Later'
    def followers(username,password,target):
        L = instaloader.Instaloader()
        L.login(username, password)
        profile = instaloader.Profile.from_username(L.context, target)
        for followee in profile.get_followers():
                try:
                    name1 = str(followee)
                    name2 = name1.split('Profile ')[1]
                    name3 = name2.split(' (')[0]
                    time.sleep(60)
                    print({'username':name3,'Mode':'@KKKKKQ9'})
                except:
                    return 'Your sessionid Got Banned Try Again Later'
    def login(username,password):
        random_uuid = uuid.uuid4()
        device_id = str(random_uuid).replace("-", "")
        url = "https://i.instagram.com/api/v1/accounts/login/"

        headers = {
                            "Accept-Encoding": "gzip",
                            "Accept-Language": "en-US",
                            "Connection": "Keep-Alive",
                            "Content-Length": "330",
                            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                            "Cookie": "mid=Zq_SxQABAAFwUCIa9KHIn1rlOIiN; csrftoken=SuzlAHVsab8fEuBhnK51ksCUjZLKCkyV",
                            "Cookie2": "$Version=1",
                            "Host": "i.instagram.com",
                            "User-Agent": "Instagram 6.12.1 Android (33/13; 450dpi; 1080x2009; samsung/xiaomi; M2012K11C; a13ve; mt6768; en_US)",
                            "X-IG-Capabilities": "AQ==",
                            "X-IG-Connection-Type": "WIFI",
                        }

        data = {
                            "ig_sig_key_version": "4",
                            "signed_body": "f4ef46b2c12815ec0c5b7866b08fa96ea392fe9b233add6a058a6236b8ca515b.{\"username\":\"{1}\",\"password\":\"{2}\",\"device_id\":\"android-{id}\",\"guid\":\"{guid}\",\"_csrftoken\":\"SuzlAHVsab8fEuBhnK51ksCUjZLKCkyV\"}".replace("{1}",username).replace("{2}",password).replace("{id}",device_id[:16]).replace("{guid}",str(uuid.uuid4())
            )
                        }

        response = requests.post(url, headers=headers, data=data).text
        if "logged_in_user" in response:
            return {'status':'ok','logged_in_user':True,'Mode':'@KKKKKQ9'}
        elif "checkpoint_required" in response:
            return {'status':'ok','logged_in_user':'checkpoint','Mode':'@KKKKKQ9'}
        else:
            return {'status':'ok','logged_in_user':False,'Mode':'@KKKKKQ9'}
    def getrandomuser(word):
        headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded',
            # 'cookie': 'ig_did=9669EE3D-9AA8-4A7D-84B9-2738EFE07C31; ig_nrcb=1; mid=ZuydJgALAAHgHrsiGEXlJTLU8ZBg; datr=Jp3sZu-JWHb3PPSORdl09M0f; shbid="2476\\05461133585536\\0541758318862:01f7b68aa989e19c1d450206cf928099068ab69a3655a60bae81d706b0f0a14eb0d3719a"; shbts="1726782862\\05461133585536\\0541758318862:01f7589e936c303fd72c884e0d071569c031b18b6b56bc6dd0973129f42f56c86570904e"; csrftoken=c3K96JBD7YHr5oYZveanDWW1YWpOx12m; ds_user_id=64540361093; sessionid=64540361093%3AMIHM28oD3SQWj6%3A3%3AAYcSpICOayKuw4mlqCNdXCe7GQrsHqsaAXPAdWS4QQ; wd=1172x945; rur="CLN\\05464540361093\\0541758325017:01f7187a749c954124ea0e896dbc33a93b69f6de91de98509ba2653e16dcda3664f3d925"',
            'origin': 'https://www.instagram.com',
            'priority': 'u=1, i',
            'referer': 'https://www.instagram.com/z.yyz3/',
            'sec-ch-prefers-color-scheme': 'dark',
            'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
            'sec-ch-ua-full-version-list': '"Google Chrome";v="129.0.6668.59", "Not=A?Brand";v="8.0.0.0", "Chromium";v="129.0.6668.59"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua-platform-version': '"15.0.0"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
            'x-asbd-id': '129477',
            'x-bloks-version-id': '45949a58ec060709d5054d638e57729a553188c614b175e79022df638c465743',
            'x-csrftoken': 'c3K96JBD7YHr5oYZveanDWW1YWpOx12m',
            'x-fb-friendly-name': 'PolarisSearchBoxRefetchableQuery',
            'x-fb-lsd': 'Jz_QNPAPuDFR5P9okyB4bV',
            'x-ig-app-id': '936619743392459',
        }

        data = {
            'av': '17841464352817545',
            '__d': 'www',
            '__user': '0',
            '__a': '1',
            '__req': '15',
            '__hs': '19985.HYP:instagram_web_pkg.2.1..0.1',
            'dpr': '1',
            '__ccg': 'UNKNOWN',
            '__rev': '1016645849',
            '__s': 'as7rpz:2gmi86:rm8nyd',
            '__hsi': '7416502291445634002',
            '__dyn': '7xeUjG1mxu1syUbFp41twpUnwgU7SbzEdF8aUco2qwJxS0k24o0B-q1ew65xO0FE2awgo9oO0n24oaEnxO1ywOwv89k2C1Fwc60D87u3ifK0EUjwGzEaE2iwNwmE7G4-5o4q3y1Sx-0lKq2-azqwt8d-2u2J0bS1LwTwKG1pg2fwxyo6O1FwlEcUed6goK2OubxKi2K7E5yqcxK2K1ew',
            '__csr': 'gigqYp2AYoxvf4lFbTjj8AQGOJkGL-lQn9HF9ruFRihJk9P6LAuGiCDAZpdx2-GKBpGmufGiKAEzKqQgwFfV-qWByUOi8K2mA4utrmaGWyGGVtoCFHDxdAKuVogAhe4Fp9E88kw04SCw3HEujxSKawAwWOwsE5yqu3q0FVEC3AE0bbV4ea6EZbgggjS0J4l3U8Q2CdyFEpwhUk8VRCYOw4MIAWj8mA4N8G2Twe63F8weax1hY9wlWwyg6505sIC0zES1Nx-0bdhpQ9EE5O3Z3po07Be0dUw1KK',
            '__comet_req': '7',
            'fb_dtsg': 'NAcNHbQHE80tz7psai4UxdmKO_ZiBeUGnFvioBxfOSNad9sIVdTlycA:17864789131057511:1726786920',
            'jazoest': '26452',
            'lsd': 'Jz_QNPAPuDFR5P9okyB4bV',
            '__spin_r': '1016645849',
            '__spin_b': 'trunk',
            '__spin_t': '1726789002',
            'qpl_active_flow_ids': '1056839232',
            'fb_api_caller_class': 'RelayModern',
            'fb_api_req_friendly_name': 'PolarisSearchBoxRefetchableQuery',
            'variables': '{"data":{"context":"blended","include_reel":"true","query":"{1}","rank_token":"1726789012137|acf5baaa3e8bd63b19c2aaf21b458a92f6719c73d09cee164d9bdebbf7545d37","search_surface":"web_top_search"},"hasQuery":true}'.replace("{1}",word),
            'server_timestamps': 'true',
            'doc_id': '7935512656557707',
        }

        response = requests.post('https://www.instagram.com/graphql/query', headers=headers, data=data).json()
        usr = response['data']['xdt_api__v1__fbsearch__topsearch_connection']['users'][1]['user']['username']
        return {'username':usr,'Mode':'@KKKKKQ9'}