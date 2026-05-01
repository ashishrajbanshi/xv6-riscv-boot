import json
import time


def handler(event, context):
    start_time = time.time()
    end_time = time.time()

    return {
        "statusCode": 200,
        "body": {
            "message": "noop baseline",
            "execution_time_ms": (end_time - start_time) * 1000,
        },
    }


if __name__ == "__main__":
    print(json.dumps(handler({}, None), indent=2))
