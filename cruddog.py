import click
import datadog
import json
import re
import select
import sys

from dateutil import parser
from tabulate import tabulate


fmap = {'time':
        {'api_namespace': 'Timeboard', 'resp_container': 'dashes'},
        'screen':
        {'api_namespace': 'Screenboard', 'resp_container': 'screenboards'}}


@click.command()
@click.option('--app_key', '-app', required=True, help='app-key to auth with')
@click.option('--api_key', '-api', required=True, help='api-key to auth with')
@click.option('--timeboard', '-t', 'rtype', flag_value='time', default=True,
              help='whether to operate on timeboards  [default]')
@click.option('--screenboard', '-s', 'rtype', flag_value='screen',
              help='whether to operate on screenboards')
@click.option('--query', '-q', 'mode', flag_value='query_resource',
              default=True, help='query an existing resource(s)  [default]')
@click.option('--backup', '-b', 'mode', flag_value='backup_resource',
              help='backup an existing resource')
@click.option('--update', '-u', 'mode', flag_value='update_resource',
              help='update an existing resource')
@click.option('--create', '-c', 'mode', flag_value='create_resource',
              help='create a new resource')
@click.option('--filter', '-f', default=".",
              help='regex filter to apply when querying')
@click.option('--id', '-i', help='the id of the resource to interact with')
def main(app_key, api_key, filter, id, rtype, mode):
    """
    Simple tool for interacting with Datadog Timeboards and Screenboards.

    Options can also be optionally set via an environment variable, of the form:
        CRUDDOG_{{LONG_OPTION_NAME_HERE}}
    """
    # TODO : add debugging option to dump params

    # initialise the datadog client
    datadog.initialize(api_key=api_key,
                       app_key=app_key)

    if mode:
        method_name = mode  # set by the command line options
        possibles = globals().copy()
        possibles.update(locals())
        method = possibles.get(method_name)
        if not method:
            raise NotImplementedError("Method %s not implemented" % method_name)
        method(filter, id, rtype)


def query_resource(filter, id, rtype):
    boardspace = get_api_namespace(rtype)
    # resp = datadog.api.Timeboard.get_all()
    resp = boardspace.get_all()

    if filter:
        # TODO : add debug option to dump filter
        pattern = re.compile(filter, re.IGNORECASE)

    items = []
    for item in resp['dashes']:
        match = pattern.search(item['title'])
        if match:
            items.append([item['id'],
                         item['title'],
                         parser.parse(item['created']).
                          strftime('%Y-%m-%d %H:%M:%S'),
                         parser.parse(item['modified']).
                          strftime('%Y-%m-%d %H:%M:%S')])

    print(tabulate(items, headers=["Id", "Title", "Created", "Modified"]))


def backup_resource(filter, id, rtype):
    boardspace = get_api_namespace(rtype)

    # TODO : check there was a valid response
    resp = boardspace.get(id)

    print(json.dumps(resp['dash'],
                     sort_keys=True,
                     indent=2,
                     separators=(',', ': ')))


def update_resource(filter, id, rtype):
    create_update_resource("update", id, rtype)


def create_resource(filter, id, rtype):
    create_update_resource("create", id, rtype)


def create_update_resource(action, id, rtype):
    boardspace = get_api_namespace(rtype)

    si = ""

    for line in sys.stdin:
        si += str(line)

    # TODO : make sure this is a safe operation
    jsonData = json.loads(si)

    reqParams = req_params_json(jsonData)

    if action == "update":
        resp = boardspace.update(id, **reqParams)
    elif action == "create":
        resp = boardspace.create(**reqParams)

    print(resp)


def req_params_json(jsonData):
    reqParams = {}

    for key in [
            "description",
            "graphs",
            "height",
            "read_only",
            "template_variables",
            "title",
            "widgets",
            "width"
    ]:
        if key in jsonData:
            reqParams[key] = jsonData[key]

    return reqParams


def get_api_namespace(rtype):
    api = datadog.api

    # TODO : wrap this in a try statement
    boardspace = getattr(api, fmap[rtype]['api_namespace'])

    return boardspace


def read_stdin():
    si = ""
    if select.select([sys.stdin, ], [], [], 0.0)[0]:
        for line in sys.stdin:
            si += str(line)
        return si
    else:
        print("No data")
        return None


if __name__ == '__main__':
    main(auto_envvar_prefix='CRUDDOG')
