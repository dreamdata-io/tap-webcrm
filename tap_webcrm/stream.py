import os
import pkg_resources
import json


def load_schema(stream_name):
    filename = f"tap_webcrm/schemas/{stream_name}.json"
    filepath = os.path.join(
        pkg_resources.get_distribution("tap_webcrm").location, filename
    )
    with open(filepath, "r") as fp:
        return json.load(fp)


def discover(stream_names):
    streams = [
        {
            "tap_stream_id": stream_name,
            "stream": stream_name,
            "schema": load_schema(stream_name),
        }
        for stream_name in stream_names
    ]
    return {"streams": streams}
