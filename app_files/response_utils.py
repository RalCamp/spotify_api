class Response():
    def request_successful(response_object):
        if response_object.status_code == 200 or response_object.status_code == 201:
            return True
        else:
            return False
        
    def error_message(response_object):
        print("##################################################")
        print("This request has resulted in a unexpected response\nThe response status code was: " + str(response_object.status_code))
        print(response_object.json()["error"]["message"])
        if response_object.status_code == 429:
            print(response_object.headers)
        print("##################################################")