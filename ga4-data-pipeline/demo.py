import os
from ga4 import GA4RunReport
from google.cloud import pubsub_v1
import json

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'docker-kubernetes-370811-f49003f1ee92.json'

property_id = '347364731'

lst_dimension = ['pageTitle']
lst_metrics = ['sessions']

ga4_report = GA4RunReport(property_id)
response = ga4_report.query_report(
    lst_dimension, lst_metrics, 10, True
)

publisher = pubsub_v1.PublisherClient()
topic_name = 'projects/{project_id}/topics/{topic}'.format(
    project_id='docker-kubernetes-370811',
    topic='ga4',  # Set this to something appropriate.
)

for i in range(10):
    ga4_json = json.dumps({'title': response['rows'][i][0], 'count': response['rows'][i][1]}, ensure_ascii=False)
    print(ga4_json)
    future = publisher.publish(topic_name, data=ga4_json.encode('utf-8'))
    future.result()
