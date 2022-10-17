import requests
import lxml.html

from parameter_store.ssm import Ssm
from notification_service.pushover import Pushover


def lambda_handler(event, context):
    store = Ssm()

    try:
        pushover_api_key = store.get("/jtweets/pushover/api_key", with_decryption=True)
        pushover_app_id = store.get("/jtweets/pushover/app_id")
        pushover = Pushover(pushover_api_key, pushover_app_id)

    except Exception as e:
        print(f"Failed to set up Pushover.  Error: {str(e)}")
        raise e

    programs = dict()
    program_list = store.get("/holiday_program/programs").split(sep=",")
    for p in program_list:
        programs[p] = dict()
        programs[p]["old"] = store.get(f"/holiday_program/{p}/old")
        programs[p]["xpath"] = store.get(f"/holiday_program/{p}/xpath")
        programs[p]["url"] = store.get(f"/holiday_program/{p}/url")

    for p_name, this_program in programs.items():
        webpage = requests.get(this_program["url"])
        try:
            lxml_webpage = lxml.html.fromstring(webpage.text)
            this_program["new"] = lxml_webpage.xpath(this_program["xpath"])[0].text
        except Exception as e:
            message = f"Program {p_name} - failed to find xpath to old string - has xpath changed?  Error: {str(e)}"
            print(message)
            pushover.send(
                message,
                title="School Holiday Program error",
            )
            continue

        if this_program["new"] != this_program["old"]:
            print(f"{p_name}: Found a change:")
            pushover.send(
                f"Marker changed from {this_program['new']} to {this_program['new']}",
                subject="School Holiday Program notification",
            )
            print("  - Successfully sent Pushover notification")
            store.put(f"/holiday_program/{p_name}/old", this_program["new"])
            print("  - Successfully updated store")
        else:
            print(f"{p_name}: No change")

    print("Comparison completed successfully")


lambda_handler(None, None)
