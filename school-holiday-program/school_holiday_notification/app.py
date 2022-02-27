import requests
import lxml.html
from pushover import init, Client
import boto3


def lambda_handler(event, context):

    ssm = boto3.client("ssm")

    try:
        pushover_api_key = (
            ssm.get_parameter(Name="/jtweets/pushover/api_key", WithDecryption=True)
            .get("Parameter")
            .get("Value")
        )

        pushover_app_id = (
            ssm.get_parameter(Name="/jtweets/pushover/app_id", WithDecryption=False)
            .get("Parameter")
            .get("Value")
        )

    except Exception as e:
        print(f"Failed to retrieve Pushover config.  Error: {str(e)}")
        raise e

    try:
        last_seen_holiday_program = (
            ssm.get_parameter(
                Name="/holidayprogram/last_seen_holiday_program", WithDecryption=False
            )
            .get("Parameter")
            .get("Value")
        )
    except ssm.exceptions.ParameterNotFound:
        print(
            f"No parameter set for /holidayprogram/last_seen_holiday_program - assuming this is the first run"
        )
        last_seen_holiday_program = ""
    except Exception as e:
        print(f"Failed to retrieve last holiday program string key.  Error: {str(e)}")
        raise e

    try:
        webpage = requests.get(
            "https://leapkids.com.au/index.php/programs/school-holiday-program"
        )

        lxml_webpage = lxml.html.fromstring(webpage.text)
        new_holiday_program = lxml_webpage.xpath(
            '//*[@id="jsn-mainbody"]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/h1'
        )[1].text

    except Exception as e:
        # Send some context about this error to Lambda Logs
        print(
            f"Could not find current holiday program string - has xpath changed?  Error: {str(e)}"
        )
        raise e

    if new_holiday_program == last_seen_holiday_program:
        # no change, do nothing
        print("Comparison found no change.")

    else:
        # something has changed
        print("Comparison found a change.  Now taking actions.")

        # tell me about it
        # push the result to my phone
        init(pushover_api_key)
        Client(pushover_app_id).send_message(
            f"Heading has changed from {last_seen_holiday_program} to {new_holiday_program}!",
            title="School Holiday Program notification",
        )
        print("  - Successfully sent Pushover notification")

        # then write it to SSM
        ssm.put_parameter(
            Name="/holidayprogram/last_seen_holiday_program",
            Value=new_holiday_program,
            Type="String",
            Overwrite=True,
        )
        print(
            "  - Successfully updated SSM parameter at /holidayprogram/last_seen_holiday_program"
        )

    print("Comparison completed successfully")


#lambda_handler(None, None)
