import urllib.request
import urllib.parse
import json

api_url = "http://openapi.tuling123.com/openapi/api/v2"
class airoot(object):
    def getword(self, word=''):
        text_input = word

        req = {
            "perception":
                {
                    "inputText":
                        {
                            "text": text_input
                        },

                    "selfInfo":
                        {
                            "location":
                                {
                                    "city": "昆明",
                                    "province": "云南",
                                    "street": "呈贡区"
                                }
                        }
                },

            "userInfo":
                {
                    "apiKey": "7f4eef0684a44a2390d30144fbdf2831",
                    "userId": "OnlyUseAlphabet"
                }
        }
        req = json.dumps(req).encode('utf8')

        http_post = urllib.request.Request(api_url, data=req, headers={'content-type': 'application/json'})
        response = urllib.request.urlopen(http_post)
        response_str = response.read().decode('utf8')
        response_dic = json.loads(response_str)

        intent_code = response_dic['intent']['code']
        results_text = response_dic['results'][0]['values']['text']
        print(results_text)
        return results_text
