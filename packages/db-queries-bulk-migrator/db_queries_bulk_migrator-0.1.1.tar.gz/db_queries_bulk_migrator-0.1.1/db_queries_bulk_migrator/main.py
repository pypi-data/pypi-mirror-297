import typer
from typing_extensions import Annotated
import pandas as pd
from dynatrace import Dynatrace
from dynatrace.environment_v2.extensions import MonitoringConfigurationDto
from dynatrace.http_client import TOO_MANY_REQUESTS_WAIT
from rich.progress import track
from rich import print

from typing import Optional, List
import logging

from .models import CustomDBQuery

logger = logging.getLogger()
logger.setLevel(logging.INFO)

EF1_EXTENSION_ID = "custom.remote.python.dbquery"
TIMEOUT = 120

app = typer.Typer()

def queries_from_ef1_config(full_config: dict):
    properties = full_config.get("properties", {})
    full_config.update({
        "database_type": properties['database_type'],
        "group_name": properties['group_name'],
        "database_host": properties['database_host'],
        "database_name": properties['database_name'],
        "database_username": properties['database_username'],
        "custom_device_name": properties['custom_device_name']
    })
    
    configured_queries: List[CustomDBQuery] = []
    query_index = 1
    while query_index < 11:
        if properties[f"query_{query_index}_value"]:
            configured_queries.append(
                CustomDBQuery(
                    properties[f"query_{query_index}_name"],
                    properties[f"query_{query_index}_schedule"],
                    properties[f"query_{query_index}_value"],
                    properties[f"query_{query_index}_value_columns"],
                    properties[f"query_{query_index}_dimension_columns"],
                    properties[f"query_{query_index}_extra_dimensions"],
                )
            )
        query_index += 1
    return configured_queries

@app.command()
def hello():
    print("hello")

@app.command(help="Pull EF1 db queries configurations into a spreadsheet.")
def pull(
    dt_url: Annotated[str, typer.Option(envvar="DT_URL")],
    dt_token: Annotated[str, typer.Option(envvar="DT_TOKEN")],
    output_file: Optional[str] = None or f"{EF1_EXTENSION_ID}-export.xlsx",
):
    dt = Dynatrace(
        dt_url,
        dt_token,
        too_many_requests_strategy=TOO_MANY_REQUESTS_WAIT,
        retries=3,
        log=logger,
        timeout=TIMEOUT,
    )
    configs = list(dt.extensions.list_instances(extension_id=EF1_EXTENSION_ID))
    all_queries: List[CustomDBQuery] = []
    full_configs = []

    for config in track(configs, description="Pulling EF1 configs"):
        config = config.get_full_configuration(EF1_EXTENSION_ID)
        full_config = config.json()
        properties = full_config.get("properties", {})

        full_config.update({
            "database_type": properties['database_type'],
            "group_name": properties['group_name'],
            "database_host": properties['database_host'],
            "database_name": properties['database_name'],
            "database_username": properties['database_username'],
            "custom_device_name": properties['custom_device_name']
        })
        
        configured_queries = queries_from_ef1_config(full_config)
        all_queries.extend(configured_queries)
        full_config.update({"queries": len(configured_queries)})
        full_configs.append(full_config)
        
    print("Finished pulling configs...")
    print("Adding data to document...")
    writer = pd.ExcelWriter(
        output_file,
        engine="xlsxwriter",
    )
    df = pd.DataFrame(full_configs)
    df.to_excel(writer, "Endpoints", index=False, header=True)

    df_queries = pd.DataFrame({"queries": [query.value for query in all_queries]})
    df_queries.to_excel(writer, "Queries", index=False, header=True)

    print("Closing document...")
    writer.close()
    print(f"Exported configurations available in '{output_file}'")

if __name__ == "__main__":
    app()
