import json
import requests
from botocore.exceptions import ClientError

def gettwitter(brand):
    try:
        bearer_token = 'AAAAAAAAAAAAAAAAAAAAAM%2BJhgEAAAAA78%2BfDj64ysNy%2BSH9kceIY6f9flk%3D67lVBv8oJFGteq01ZkOkBz9SyZh5V9PGbdzEM3e8w3jhRGYRFA'
        headers = {"Authorization": "Bearer {}".format(bearer_token)}
        url = "https://api.twitter.com/2/tweets/search/recent"
        query_params = {'query': brand,
                        # 'start_time': start_date,
                        # 'end_time': end_date,
                        'max_results': 10,
                        'tweet.fields': 'id,text,author_id,conversation_id,created_at,geo,lang,public_metrics,referenced_tweets',
                        'user.fields': 'id,name,username,created_at,description,location,public_metrics,verified',
                        'place.fields': 'full_name,id,country,country_code,geo,name,place_type'}
        tweets = requests.get(url, headers=headers, params=query_params)
        if tweets:
                print(tweets)
                for tweet in tweets:
                    try:
                        print(tweet)
                        print("=====")
                    except AttributeError:
                        print(tweet)
                        print("=====")
        else:
            print("Response does not have the news hence not sorting but sending fail email.")
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("News is retrieved as expected , hence returning now"),
        return tweets

TittsResults = gettwitter("Elon")
print(TittsResults)