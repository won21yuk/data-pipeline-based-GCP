import os
import datetime
from typing import List
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (Dimension, Metric, DateRange, Metric, OrderBy,
                                                FilterExpression, MetricAggregation, CohortSpec)
from google.analytics.data_v1beta.types import RunReportRequest, RunRealtimeReportRequest

class GA4Exception(Exception):
    '''base class for GA4 exceptions'''

# core report
class GA4RunReport:
    """class to query GA4 core report
    More information: https://developers.google.com/analytics/devguides/reporting/data/v1/basics
    """

    def __init__(self, property_id):
        self.property_id = property_id
        self.client = BetaAnalyticsDataClient()

    def query_report(self, dimensions: List[str], metrics: List[Metric], row_limit: int = 10000,
                     quota_usage: bool = False):
        """
        :param dimensions: categorical attributes (age, country, city, etc)
        :type dimensions: [dimension type]
                :param dimensions: categorical attributes (age, country, city, etc)

        :param metrics: numeric attributes (views, user count, active users)
        :type metrics: [metric type]

        """
        try:
            dimension_list = [Dimension(name=dim) for dim in dimensions]
            metrics_list = [Metric(name=m) for m in metrics]

            report_request = RunReportRequest(
                property=f'properties/{self.property_id}',
                dimensions=dimension_list,
                metrics=metrics_list,
                limit=row_limit,
                return_property_quota=quota_usage,
                date_ranges=[DateRange(start_date='2022-09-28', end_date="today")],
            )
            response = self.client.run_report(report_request)

            output = {}
            if 'property_quota' in response:
                output['quota'] = response.property_quota

            # construct the dataset
            headers = [header.name for header in response.dimension_headers] + [header.name for header in
                                                                                response.metric_headers]
            rows = []
            for row in response.rows:
                rows.append(
                    [dimension_value.value for dimension_value in row.dimension_values] + \
                    [metric_value.value for metric_value in row.metric_values])
            output['headers'] = headers
            output['rows'] = rows
            return output
        except Exception as e:
            raise GA4Exception(e)

# realtime report
class GA4RealTimeReport:
    """class to query GA4 real time report
    More information: https://developers.google.com/analytics/devguides/reporting/data/v1/realtime-basics
    """

    def __init__(self, property_id):
        self.property_id = property_id
        self.client = BetaAnalyticsDataClient()

    def query_report(self, dimensions: List[str], metrics: List[Metric], row_limit: int = 10000,
                     quota_usage: bool = False):
        """
        :param dimensions: categorical attributes (age, country, city, etc)
        :type dimensions: [dimension type]
                :param dimensions: categorical attributes (age, country, city, etc)

        :param metrics: numeric attributes (views, user count, active users)
        :type metrics: [metric type]

        """
        try:
            dimension_list = [Dimension(name=dim) for dim in dimensions]
            metrics_list = [Metric(name=m) for m in metrics]

            report_request = RunRealtimeReportRequest(
                property=f'properties/{self.property_id}',
                dimensions=dimension_list,
                metrics=metrics_list,
                limit=row_limit,
                return_property_quota=quota_usage
            )
            response = self.client.run_realtime_report(report_request)

            output = {}
            if 'property_quota' in response:
                output['quota'] = response.property_quota

            # construct the dataset
            headers = [header.name for header in response.dimension_headers] + [header.name for header in
                                                                                response.metric_headers]
            rows = []
            for row in response.rows:
                rows.append(
                    [dimension_value.value for dimension_value in row.dimension_values] + \
                    [metric_value.value for metric_value in row.metric_values])
            output['headers'] = headers
            output['rows'] = rows
            return output
        except Exception as e:
            raise GA4Exception(e)