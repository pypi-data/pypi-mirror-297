# calisum - A caliap activity scraper and summarizer

This is a simple Python script that scraps Caliap and allow to you tu summarize your activity using the LLM of your choice.

## Installation

```bash
pip install calisum
```

## Usage

```
usage: calisum [-h] [--version] [-v] [-O OUTPUT] [-o] [-j] [-e EMAIL] [-p PASSWORD] [-c COOKIE] [-l LLM_URL] [-t LLM_TOKEN] [-n] [-m MODEL_ID] [-g] [url_to_scrape]

Summarize Caliap activity data.

options:
  -h, --help            show this help message and exit
  --version             Display the version of the package.
  -v, --verbose         Increase the verbosity of the output.
  -O OUTPUT, --output OUTPUT
                        Output file to save the summary to. default to stdout
  -o, --original-output
                        Output the original data instead of the summary.
  -j, --json            Output the result as json

Scraper options:
  url_to_scrape         URL to scrape the data from.
  -e EMAIL, --email EMAIL
                        Email address to use for authentication. Must be used together with --password.
  -p PASSWORD, --password PASSWORD
                        Password to use for authentication. Must be used together with --email.
  -c COOKIE, --cookie COOKIE
                        Cookie to use for authentication (PHPSESSID). Mutually exclusive with --email and --password.

LLM options:
  -l LLM_URL, --llm-url LLM_URL
                        URL to the LLM page open api endpoint (compatible with openai api standard).
  -t LLM_TOKEN, --llm-token LLM_TOKEN
                        LLM token (usefull with openai)
  -n, --jan-ai          Use localhost default jan-ai config.
  -m MODEL_ID, --model-id MODEL_ID
                        OpenAI form model id (eg: mistral-ins-7b-q4)
  -g, --global-summary  Do a global summary of individual activity (works only if original output is not selected)
```

## License
[GPL-3.0](LICENSE.md)
```