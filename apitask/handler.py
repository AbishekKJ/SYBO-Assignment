"""
Project: NinjaSpoilers
Author: Abishek KJ
Date: 09-Jul-2021
"""

from services.ninjaspoilersmanager import NinjaSpoilersManager


def get_ninja_spoilers_user_services(event, context):
    """
    Lambda handler for ninja spoilers
    """
    manager_obj = NinjaSpoilersManager(event, context)
    response = manager_obj.run()
    return response

