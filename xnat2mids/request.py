import time
import requests

from xnat2mids.variables import format_message


def try_to_request(interface, web, level_verbose=15, level_tab=15):
    # Function that allows a persistent get request to a web page

    # variable that counts connection attempt
    intents = 1
    while True:
        try:
            req = interface.get(web)
            if req.status_code != 504:
                break
        except requests.exceptions.ConnectionError as e:

            print(
                format_message(
                    level_verbose,
                    level_tab,
                    "Intents to download information = {}".format(intents)
                )
            )
            time.sleep(60)
        except requests.exceptions.HTTPError:
            print(
                format_message(
                    level_verbose,
                    level_tab,
                    "Intents to download information = {}".format(intents)
                )
            )
            time.sleep(60)
    return req
