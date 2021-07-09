"""
Project: NinjaSpoilers
Author: Abishek KJ
Date: 09-Jul-2021
"""

import json


def get_ninja_user_services(event, context):
    resource_path = event.get("resource", "")
    resource_map = {}
    response = {"headers": {
        'Access-Control-Allow-Origin': '*'
    }}
    if resource_path:
        pass
    response["statusCode"] = 404
    response["body"] = "Data not found"
    return response
