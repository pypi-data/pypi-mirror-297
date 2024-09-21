import json

import yaml
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import JSONResponse

# If the next line raises parse errors it means that you have to fix the import path
from {{folder_name}}.crew import {{class_name}}Crew as Crew

from agenticos.server.models import NodeDescription

load_dotenv()

config_path = "src/agentic/agentic_config.yml"
app = FastAPI()


@app.get(
    "/description",
    summary="Get the description of the node",
    response_model=NodeDescription,
)
def description() -> NodeDescription:
    with open(config_path, "r") as file:
        parsedContent = yaml.safe_load(file)

        node_name = next(iter(parsedContent))

        return NodeDescription(
            name=node_name,
            description=parsedContent[node_name]["description"],
            inputs=parsedContent[node_name]["inputs"],
        )


@app.post("/run")
def run(inputs: dict[str, str]) -> str:
    crewaiApp = Crew()
    crewaiApp.crew().kickoff(inputs=inputs)
    return crewaiApp.reporting_task().output.raw


@app.get("/health")
def health() -> JSONResponse:
    return JSONResponse({"status": "ok"})