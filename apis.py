import twitter



def twitter_connect(API_key, API_secret_key,
                    access_token, access_token_secret,
                    sleep_on_rate_limit=True):
    """Connect to Twitter API, and return a handle"""

    api = twitter.Api(consumer_key=API_key,
                      consumer_secret=API_secret_key,
                      access_token_key=access_token,
                      access_token_secret=access_token_secret,
                      sleep_on_rate_limit=sleep_on_rate_limit)

    api.VerifyCredentials()

    return api


def facebook_connect():
    raise NotImplementedError

def google_docs_connect():
    raise NotImplementedError

def google_sheets_connect():
    raise NotImplementedError
