__author__ = 'Samuel'

import pprint
import numpy as np
import json

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.client import GoogleCredentials

NUMPY_CONVERSIONS = {int: ('i8', int),
                     float: ('f8', float),
                     str: ('U128', str),
                     'json_int': (np.dtype(object), lambda x: np.array(json.loads(x)))}


def get_service():
    """returns an initialized and authorized bigquery client"""
    credentials = GoogleCredentials.get_application_default()
    if credentials.create_scoped_required():
        credentials = credentials.create_scoped(
            'https://www.googleapis.com/auth/bigquery')
    return build('bigquery', 'v2', credentials=credentials)


def run_query(project, raw_query, columns_type=float):
    def get_rows(response, data, i):
        if response['jobComplete']:
            if 'rows' in response:
                for row in response['rows']:
                    for j, cell in enumerate(row['f']):
                        data[j][i] = NUMPY_CONVERSIONS[columns_type[j]][1](cell['v'])
                    i += 1
        else:
            raise RuntimeError('Query execution timeout.')
        return i

    job = get_service().jobs()
    body = {"timeoutMs": 1000 * 300,
            "kind": "bigquery#queryRequest",
            "dryRun": False,
            "useQueryCache": True,
            "maxResults": 10000,
            "query": raw_query
            }
    try:
        response = job.query(projectId=project, body=body).execute()
        results_args = {"projectId": project,
                        "jobId": response['jobReference']['jobId'],
                        "maxResults": 10000}
        labels = [f['name'] for f in response['schema']['fields']]
        try:
            iter(columns_type)
        except TypeError:
            columns_type = [columns_type] * len(response['schema']['fields'])
        data = []
        for column_type in columns_type:
            data.append(np.zeros(int(response['totalRows']), dtype=NUMPY_CONVERSIONS[column_type][0]))
        start_index = 0
        start_index = get_rows(response, data, start_index)
        while "pageToken" in response:
            results_args["pageToken"] = response['pageToken']
            response = job.getQueryResults(**results_args).execute()
            start_index = get_rows(response, data, start_index)
        return data, labels
    except HttpError as err:
        print('Error in querytableData: ', pprint.pprint(err.content))
