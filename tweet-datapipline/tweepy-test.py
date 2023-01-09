import tweepy
import json
import os
from google.cloud import pubsub_v1

# access credentials 지정
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'docker-kubernetes-370811-f49003f1ee92.json'

bearer_token = 'Put your bearer_token here'

# pub/sub publisherClient 생성
publisher = pubsub_v1.PublisherClient()
topic_name = 'projects/{project_id}/topics/{topic}'.format(
    project_id='docker-kubernetes-370811',
    topic='tweets',  # pub/sub 주제(topic) 지정
)

# tweepy.StreamClient 클래스를 상속받는 클래스
class TwitterStream(tweepy.StreamingClient):
    def on_data(self, raw_data):
        raw_data = json.loads(raw_data.decode('utf-8'))
        raw_data = raw_data['data']
        #print(raw_data)
        # 영어 트윗만 가져오기
        if raw_data['lang'] == 'en':
            tweet = json.dumps({'id': raw_data['id'], 'created_at': raw_data['created_at'], 'text': raw_data['text']}, default=str)
            # topic으로 publish
            future = publisher.publish(topic_name, data=tweet.encode('utf-8'))
            future.result()
            print(tweet)

    def on_error(self, status_code):
        print(status_code)
        if status_code == 420:
            return False

# 규칙 제거 함수
def delete_all_rules(rules):
    # 규칙 값이 없는 경우 None 으로 들어온다.
    if rules is None or rules.data is None:
        return None
    stream_rules = rules.data
    ids = list(map(lambda rule: rule.id, stream_rules))
    client.delete_rules(ids=ids)

# 스트림 클라이언트 인스턴스 생성
client = TwitterStream(bearer_token)

# 모든 규칙 불러오기 - id값을 지정하지 않으면 모든 규칙을 불러옴
rules = client.get_rules()

# 모든 규칙 제거
delete_all_rules(rules)

# 스트림 규칙 추가
client.add_rules(tweepy.StreamRule(value="netflix"))

# 스트림 시작(expension 사용)
client.filter(tweet_fields=["lang", "created_at"])
