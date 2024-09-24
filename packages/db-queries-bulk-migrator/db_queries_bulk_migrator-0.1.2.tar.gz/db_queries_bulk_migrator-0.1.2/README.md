# Dynatrace DB Queries Extension Bulk Migrator

Tool to help with creating Extensions 2.0 declarative SQL extensions off of Extensions 1.0 Custom DB Queries extension configurations.

## API Authentication

For commands that interact with the Dynatrace API you need to provide an API URL and Access token. These can be provided on the command line but it is recommended to use environment variables:

- DT_URL (e.g. https://xxx.live.dynatrace.com)
- DT_TOKEN
  - permissions:
    - ReadConfig
    - WriteConfig
    - extensions.read
    - extensions.write

## Commands

Use `--help` with any command to view unique options.

```
 Usage: dbqm pull [OPTIONS]

 Pull EF1 db queries configurations into a spreadsheet.

╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *  --dt-url             TEXT  [env var: DT_URL] [default: None] [required]                                                                                                                                                                                         │
│ *  --dt-token           TEXT  [env var: DT_TOKEN] [default: None] [required]                                                                                                                                                                                       │
│    --output-file        TEXT  [default: custom.remote.python.dbquery-export.xlsx]                                                                                                                                                                                  │
│    --help                     Show this message and exit.  
```

### dbql pull

Used to pull all EF1 Custom DB Queries configurations and export them to an Excel sheet for manual review and as an input to later steps.

