from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange
from google.analytics.data_v1beta.types import Dimension
from google.analytics.data_v1beta.types import Metric
from google.analytics.data_v1beta.types import RunReportRequest
from run_report import print_run_report_response

import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'docker-kubernetes-370811-f49003f1ee92.json'

def sample_run_report(property_id):
    """Runs a simple report on a Google Analytics 4 property."""
    # Using a default constructor instructs the client to use the credentials
    # specified in GOOGLE_APPLICATION_CREDENTIALS environment variable.
    client = BetaAnalyticsDataClient()

    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name="pageTitle"), Dimension(name="city")],
        metrics=[Metric(name="sessions")],
        date_ranges=[DateRange(start_date="2020-03-31", end_date="today")],
    )
    response = client.run_report(request)
    print_run_report_response(response)
    # print("Report result:")
    # for row in response.rows:
    #     print(row.dimension_values[0].value, row.metric_values[0].value)


sample_run_report(347364731)
