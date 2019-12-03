# tap-webcrm

# how to execute

run the following command in the root of the folder:

```bash
pipenv install . && pipenv run tap-webcrm -c config.json > opp.ndjson
```

below is an example of a valid `config.json` for this tap.

# Note

### singer.io compliance

As of right now, the tap does not support `--discovery` or the `--catalog` argument. This was build in a rush before completely understanding those concepts. They are on the roadmap however, but right now, what would normally be achieved through the `--catalog` argument, ie. filtering fields etc. is achieved in the `--config` argument in the `streams` field. See the below example of how to exclude fields for instance.

### Tables supported

As of right now, Dreamdata only has use for the `Opportunity`, `Organisation` and `Person` tables - but it would be trivial to add support for other ones and PRs are welcome.

# config

the API_TOKEN can be provided as the environment variables `WEBCRM_API_TOKEN` or directly in the configuration as seen below:

```json
{
  "api_token": "<API_TOKEN>",
  "streams": {
    "opportunity": {
      "exclude_fields": [
        "OpportunityPlus1",
        "OpportunityPlus2",
        "OpportunityPlus3",
        "OpportunityPlus4",
        "OpportunityPlus5",
        "OpportunityPlus6",
        "OpportunityPlus7",
        "OpportunityPlus8",
        "OpportunityPlus9",
        "Opportunitylus10",
        "Opportunitylus11",
        "Opportunitylus12",
        "Opportunitylus13",
        "Opportunitylus14",
        "Opportunitylus15",
        "Opportunitylus16",
        "Opportunitylus17",
        "Opportunitylus18",
        "Opportunitylus19",
        "Opportunitylus20",
        "OpportunityCustom1",
        "OpportunityCustom2",
        "OpportunityCustom3",
        "OpportunityCustom4",
        "OpportunityCustom5",
        "OpportunityCustom6",
        "OpportunityCustom7",
        "OpportunityCustom8",
        "OpportunityCustom9",
        "OpportunityCustom10",
        "OpportunityCustom11",
        "OpportunityCustom12",
        "OpportunityCustom13",
        "OpportunityCustom14",
        "OpportunityCustom15"
      ]
    },
    "organisation": {
      "exclude_fields": [
        "OrganisationPlus1",
        "OrganisationPlus2",
        "OrganisationPlus3",
        "OrganisationPlus4",
        "OrganisationPlus5",
        "OrganisationPlus6",
        "OrganisationPlus7",
        "OrganisationPlus8",
        "OrganisationPlus9",
        "OrganisationPlus10",
        "OrganisationPlus11",
        "OrganisationPlus12",
        "OrganisationPlus13",
        "OrganisationPlus14",
        "OrganisationPlus15",
        "OrganisationPlus16",
        "OrganisationPlus17",
        "OrganisationPlus18",
        "OrganisationPlus19",
        "OrganisationPlus20",
        "OrganisationCustom1",
        "OrganisationCustom2",
        "OrganisationCustom3",
        "OrganisationCustom4",
        "OrganisationCustom5",
        "OrganisationCustom6",
        "OrganisationCustom7",
        "OrganisationCustom8",
        "OrganisationCustom9",
        "OrganisationCustom10",
        "OrganisationCustom11",
        "OrganisationCustom12",
        "OrganisationCustom13",
        "OrganisationCustom14",
        "OrganisationCustom15"
      ]
    },
    "person": {
      "exclude_fields": [
        "PersonPlus1",
        "PersonPlus2",
        "PersonPlus3",
        "PersonPlus4",
        "PersonPlus5",
        "PersonPlus6",
        "PersonPlus7",
        "PersonPlus8",
        "PersonPlus9",
        "PersonPlus10",
        "PersonPlus11",
        "PersonPlus12",
        "PersonPlus13",
        "PersonPlus14",
        "PersonPlus15",
        "PersonPlus16",
        "PersonPlus17",
        "PersonPlus18",
        "PersonPlus19",
        "PersonPlus20",
        "PersonCustom1",
        "PersonCustom2",
        "PersonCustom3",
        "PersonCustom4",
        "PersonCustom5",
        "PersonCustom6",
        "PersonCustom7",
        "PersonCustom8",
        "PersonCustom9",
        "PersonCustom10",
        "PersonCustom11",
        "PersonCustom12",
        "PersonCustom13",
        "PersonCustom14",
        "PersonCustom15",
        "PersonCheckMark1",
        "PersonCheckMark2",
        "PersonCheckMark3",
        "PersonCheckMark4",
        "PersonCheckMark5",
        "PersonCheckMark6",
        "PersonCheckMark7",
        "PersonCheckMark8",
        "PersonCheckMark9",
        "PersonCheckMark10",
        "PersonMemo"
      ]
    }
  }
}
```
