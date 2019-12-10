# tap-webcrm

# installation

install via `pip` using the following command:

```bash
pip install tap-webcrm
```

below is an example of a valid `config.json` for this tap.

# Note

### singer.io compliance

The tap supports `--discover` and `--catalog` as of release v0.1. To simplify your life when working with this, use the pip package `singer-discover`:

```bash
pip install https://github.com/chrisgoddard/singer-discover/archive/master.zip
```

### Tables supported

As of right now, Dreamdata only has use for the `Opportunity`, `Organisation` and `Person` tables - but it would be trivial to add support for other ones and PRs are welcome.

# config

the API_TOKEN can be provided as the environment variables `WEBCRM_API_TOKEN` or directly in the configuration as seen below:

```json
{
  "api_token": "<API_TOKEN>"
}
```
