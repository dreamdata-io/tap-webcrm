import os
import pkg_resources
import json
import sys

from typing import Dict, Any, List

import singer
from singer import utils

logger = singer.get_logger()


def process_streams(client, streams, state):
    implemented_streams = {
        "opportunity": {
            "bookmark_property": "OpportunityUpdatedAt",
            "generator": client.query_opportunity,
            "key_properties": ["OpportunityId"],
            "exclude_fields": ["op_multiTerritory", "op_lastUpdatedById", "RowNumber"],
        },
        "organisation": {
            "bookmark_property": "OrganisationUpdatedAt",
            "generator": client.query_organisation,
            "key_properties": ["OrganisationId"],
            "exclude_fields": ["o_lastUpdatedById", "RowNumber"],
        },
        "person": {
            "bookmark_property": "PersonUpdatedAt",
            "generator": client.query_person,
            "key_properties": ["PersonId"],
            "exclude_fields": [
                "p_lastUpdatedById",
                "p_reportFilterMatch",
                "p_marketDataProviderId",
                "p_lastLogin",
                "p_memDate",
                "RowNumber",
            ],
        },
    }

    if not streams:
        streams = implemented_streams
    else:
        for stream_name in streams:
            if stream_name not in implemented_streams:
                raise ValueError(
                    f"'streams.{stream_name}' is not in list of valid streams: {implemented_streams.keys()}"
                )

    for stream_name, stream_custom in streams.items():
        stream_config = implemented_streams[stream_name]

        bookmark_property = stream_config["bookmark_property"]
        generator = stream_config["generator"]
        key_properties = stream_config["key_properties"]
        exclude_fields = stream_config.get("exclude_fields") + stream_custom.get(
            "exclude_fields", []
        )
        sample_size = stream_custom.get("sample_size")

        logger.info(f"[{stream_name}] streaming..")

        checkpoint = singer.get_bookmark(state, stream_name, bookmark_property)
        if checkpoint:
            logger.info(f"[{stream_name}] previous state: {checkpoint}")

        new_checkpoint = emit_stream(
            stream_name,
            generator,
            bookmark_property,
            key_properties,
            checkpoint,
            exclude_fields=exclude_fields,
            sample_size=sample_size,
        )

        singer.write_bookmark(state, stream_name, bookmark_property, new_checkpoint)

        logger.info(f"[{stream_name}] emitting state: {state}")

        singer.write_state(state)

        logger.info(f"[{stream_name}] done")


def emit_stream(
    stream_name,
    stream_generator,
    bookmark_property,
    key_properties,
    checkpoint,
    exclude_fields=None,
    sample_size=None,
):
    # load schema from disk
    schema = load_schema(stream_name)

    # write schema
    singer.write_schema(stream_name, schema, key_properties)

    # keep this backup in case the pull dies
    checkpoint_backup = checkpoint

    # set the most recent update to the dawn of time
    # which is also a valid checkpoint since every
    # new record will be newer than that
    most_recent_update = "0001-01-01T00:00:00+00:00"

    i = 0
    try:
        with singer.metrics.record_counter(stream_name) as counter:
            for record in stream_generator():
                # retrieve updatedAt field for each record
                updated_time = record[bookmark_property]

                # skip records if there was a previous checkpoint
                if checkpoint and checkpoint >= updated_time:
                    continue

                # remove fields that are in the exclude_fields argument
                if exclude_fields:
                    for field in exclude_fields:
                        record.pop(field, None)

                # write record with extracted timestamp
                singer.write_record(stream_name, record, time_extracted=utils.now())

                # keep track of the most recent record
                if most_recent_update < updated_time:
                    most_recent_update = updated_time

                i += 1
                counter.increment(1)

                if sample_size and sample_size < i:
                    break

                # instrument with metrics to allow targets to receive progress
        return most_recent_update

    # because the documents are orderes by createdAt time
    # and not updated at, we should only save the state when
    # a complete successful run was achieved.
    # If an error occured mid-run, thereit is almost guaranteed that
    # records that have not been processed contain an UpdatedTime that is older
    # than the
    except Exception as err:
        logger.error(f"{str(err)}")
        return checkpoint_backup


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
