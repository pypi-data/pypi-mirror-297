# paperqa-api

Python client for interacting with paperqa app

# Usage

Make sure to set the environment variable `PQA_API_TOKEN` or `PQA_API_KEY` to your API token.

```sh
export PQA_API_TOKEN=pqa-...
```

To query agent:

```py
import pqapi
response = pqapi.agent_query(
    "Are COVID-19 vaccines effective?"
)
```

to query with a specific bibliography (collection of papers)

```py
import pqapi
response = pqapi.agent_query(
    "Are COVID-19 vaccines effective?",
    "covid"
)
```

## Templates

You can use templates to batch multiple queries together. A minimal example would be:

```jinja
The effectiveness of COVID-19 is given below:
{{ "Are COVID-19 vaccines effective?" | pqa}}
```

Or, more complex examples can use shared bibliographies set by variables names:

```jinja
{% with bib = "covid" %}
## Info
{{ "Are COVID-19 vaccines effective?" | pqa(bib)}}

## Modality
{{ "Has there been an AAV COVID-19 vaccine?" | pqa(bib)}}
{% endwith %}
```

You render it via:

```sh
pqa-render template.jinja > output.md
```

## Managing bibliographies

To get information about a specific bibliography

```py
import pqapi
response = pqapi.get_bibliography(
    "default"
)
print(response)
```

You do not need to explicitly create a bibliography, just adding files will create one. To upload files:

```py
import pqapi
files = open("paper.pdf", "rb")
metadata =
    pqapi.UploadMetadata(filename="paper.pdf", citation="Test Citation")

response = pqapi.upload_file(
    "default",
    file
    metadata
)
```

To delete a bibliography:

```py
import pqapi
response = pqapi.delete_bibliography(
    "default"
)
```

# Development

You can change the server URL endpoint to a local PQA server with

```sh
export PQA_URL="http://localhost:8080"
```
