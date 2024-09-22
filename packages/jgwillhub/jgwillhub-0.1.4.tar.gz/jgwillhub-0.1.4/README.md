# jgwillhub

This project is a Python module called `jgwillhub` that wraps the functionality of pulling prompts from the 'langchainhub' using the 'langchain' module.

## Project Structure

The project has the following files:

- `jgwillhub/jgwillhub/__init__.py`: This file is the initialization file for the `jgwillhub` module.

- `jgwillhub/jgwillhub/prompts.py`: This file contains the implementation of the `hub` module, which wraps the functionality of pulling prompts from the 'langchainhub'. It includes a function `pull` that takes a `tool_hub_tag` as input and returns the corresponding prompt template.

- `jgwillhub/jgwillhub/cli.py`: This file contains the implementation of the `jhub` command-line interface (CLI). It provides a way to get a list of prompts from user 'jgwill' in the 'langchainhub'.

- `tests/__init__.py`: This file is the initialization file for the tests directory.

- `tests/test_prompts.py`: This file contains the unit tests for the `prompts.py` module.

- `jgwill-hub.yml`: This file is a YAML setting file that defines the supported prompts with their descriptions and variables.

- `requirements.txt`: This file lists the dependencies required for the project.

## `prompts.py` Module

The `prompts.py` module exports the following functions and classes:

- `pull(tool_hub_tag: str) -> str`: A function that takes a `tool_hub_tag` as input and returns the corresponding prompt template.

## `cli.py` Module

The `cli.py` module exports the following functions and classes:

- No specific exports mentioned.

## `jgwill-hub.yml` File

The `jgwill-hub.yml` file contains the following structure:

```yaml
prompts:
  - tag: "jgwill/cmpenghelperbeta"
    description: "Create a ChatMusician Musical Inference Request"
    variables:
      - creation_name
      - seq_name
      - musical_notes
  - tag: "jgwill/json2yaml"
    description: "Simple Tool to convert input JSON into YAML"
  - tag: "jgwill/sfcp"
    description: "Shift focus from technical-aspect to creative practitionner perspective"
    variables:
      - content
  - tag: "jgwill/stcgoalsfcp"
    description: "Shift focus from technical-aspect to creative practitionner perspective with a structured user goal in the inputs"
    variables:
      - content
      - stcgoal
```

Please refer to the individual files for more details on their implementation.
```

Let me know if there's anything else I can help you with!