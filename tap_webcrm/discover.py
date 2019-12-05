import os
import json
import pkg_resources

import singer
from singer import utils, catalog, metadata

implemented_streams = {
    "opportunity": {
        "bookmark_property": "OpportunityUpdatedAt",
        "key_properties": ["OpportunityId"],
        "include_prefix": "Opportunity",
    },
    "organisation": {
        "bookmark_property": "OrganisationUpdatedAt",
        "key_properties": ["OrganisationId"],
        "include_prefix": "Organisation",
    },
    "person": {
        "bookmark_property": "PersonUpdatedAt",
        "key_properties": ["PersonId"],
        "include_prefix": "Person",
    },
    "delivery": {
        "bookmark_property": "DeliveryUpdatedAt",
        "key_properties": ["DeliveryId"],
        "include_prefix": "Delivery",
    },
    "activity": {
        "bookmark_property": "ActivityUpdatedAt",
        "key_properties": ["ActivityId"],
        "include_prefix": "Activity",
    },
}


def discover():
    stream_catalog = catalog.Catalog([])

    for stream_name, stream_metadata in implemented_streams.items():
        schema_dict = load_schema(stream_name)

        key_properties = stream_metadata["key_properties"]

        mdata = metadata.get_standard_metadata(
            schema=schema_dict, schema_name=stream_name, key_properties=key_properties,
        )

        schema = catalog.Schema.from_dict(schema_dict)

        catalog_entry = catalog.CatalogEntry(
            stream=stream_name,
            tap_stream_id=stream_name,
            key_properties=key_properties,
            schema=schema,
            metadata=mdata,
        )

        stream_catalog.streams.append(catalog_entry)

    return stream_catalog


def do_discover():
    stream_catalog = discover()
    catalog.write_catalog(stream_catalog)


def load_schema(stream_name):
    filename = f"tap_webcrm/schemas/{stream_name}.json"
    filepath = os.path.join(
        pkg_resources.get_distribution("tap_webcrm").location, filename
    )
    with open(filepath, "r") as fp:
        return json.load(fp)
