import os
import json
import pkg_resources

import singer
from singer import utils, catalog

from tap_webcrm import metadata

implemented_streams = {
    "opportunity": {
        "bookmark_property": "OpportunityUpdatedAt",
        "key_properties": ["OpportunityId"],
        "include_prefix": "Opportunity",
        "generator_attr": "query_opportunity",
    },
    "organisation": {
        "bookmark_property": "OrganisationUpdatedAt",
        "key_properties": ["OrganisationId"],
        "include_prefix": "Organisation",
        "generator_attr": "query_organisation",
    },
    "person": {
        "bookmark_property": "PersonUpdatedAt",
        "key_properties": ["PersonId"],
        "include_prefix": "Person",
        "generator_attr": "query_person",
    },
    "delivery": {
        "bookmark_property": "DeliveryUpdatedAt",
        "key_properties": ["DeliveryId"],
        "include_prefix": "Delivery",
        "generator_attr": "query_delivery",
    },
    "activity": {
        "bookmark_property": "ActivityUpdatedAt",
        "key_properties": ["ActivityId"],
        "include_prefix": "Activity",
        "generator_attr": "query_activity",
    },
}


def discover() -> catalog.Catalog:
    stream_catalog = catalog.Catalog([])

    for stream_name, stream_metadata in implemented_streams.items():
        schema_dict = load_schema(stream_name)

        key_properties = stream_metadata["key_properties"]
        include_prefix = stream_metadata["include_prefix"]
        generator_attr = stream_metadata["generator_attr"]
        bookmark_property = stream_metadata["bookmark_property"]

        mdata = metadata.get_standard_metadata(
            schema=schema_dict,
            schema_name=stream_name,
            key_properties=key_properties,
            include_prefix=include_prefix,
            generator_attr=generator_attr,
            bookmark_property=bookmark_property,
        )

        schema = catalog.Schema.from_dict(schema_dict)

        catalog_entry = catalog.CatalogEntry(
            stream=stream_name,
            tap_stream_id=stream_name,
            key_properties=key_properties,
            schema=schema,
            metadata=mdata,
            replication_method="FULL_TABLE",
        )

        stream_catalog.streams.append(catalog_entry)

    return stream_catalog


def do_discover():
    stream_catalog = discover()
    catalog.write_catalog(stream_catalog)


def load_schema(stream_name) -> dict:
    filename = f"tap_webcrm/schemas/{stream_name}.json"
    filepath = os.path.join(
        pkg_resources.get_distribution("tap_webcrm").location, filename
    )
    with open(filepath, "r") as fp:
        return json.load(fp)
