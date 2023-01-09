import os
from ga4 import GA4RunReport, GA4RealTimeReport
from google.cloud import pubsub_v1
import json

def RealTimeReport():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'docker-kubernetes-370811-f49003f1ee92.json'

    property_id = '347364731'

    lst_dimension = ['city']
    lst_metrics = ['activeUsers']

    ga4_report = GA4RealTimeReport(property_id)
    response = ga4_report.query_report(
        lst_dimension, lst_metrics, 10, True
    )

    return response

if __name__ == '__main__':
    while True:
        response = RealTimeReport()
        print('데이터 들어 올때까지 대기중..')
        if not response['rows']:
            pass
        else:
            print(response['rows'])
            publisher = pubsub_v1.PublisherClient()
            topic_name = 'projects/{project_id}/topics/{topic}'.format(
                project_id='docker-kubernetes-370811',
                topic='ga4',  # Set this to something appropriate.
            )
            k = len(response)
            for i in range(k):
                try:
                    ga4_json = json.dumps({'title': response['rows']},
                                          ensure_ascii=False)
                    future = publisher.publish(topic_name, data=response['rows'].encode('utf-8'))
                    future.result()
                    print(ga4_json)

                except Exception as e:
                    print(e)