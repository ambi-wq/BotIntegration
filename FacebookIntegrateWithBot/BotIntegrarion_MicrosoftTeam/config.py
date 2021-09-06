import os

class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "2164624a-3247-4519-9ae4-c1b1dd837d68")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "5104577f-ca6c-4d19-aa34-9d799ec39f05")