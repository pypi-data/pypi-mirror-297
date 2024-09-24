from uuid import UUID

import yaml
from dotenv import load_dotenv
from fastapi import BackgroundTasks, FastAPI, HTTPException
from fastapi.responses import JSONResponse

# If the next line raises parse errors it means that you have to fix the import path
from {{folder_name}}.crew import {{class_name}}Crew as Crew


from agenticos.server.models import NodeDescription, Task, TaskStatus

load_dotenv()

config_path = "src/agentic/agentic_config.yml"
app = FastAPI()

tasks : dict[UUID, Task] = {}


def run_task(crewaiApp: any, task : Task) -> None:
    try:
        crewaiApp.crew().kickoff(inputs=task.inputs)
        task.output = crewaiApp.reporting_task().output.raw
        task.status = TaskStatus.COMPLETED
    except Exception as e:
        task.output = str(e)
        task.status = TaskStatus.FAILED

@app.get(
    "/node/description",
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


@app.post("/task")
async def run(inputs: dict[str, str], background_tasks: BackgroundTasks) -> str:
    task = Task(inputs=inputs, status=TaskStatus.RUNNING, output="")
    tasks[task.id] = task
    background_tasks.add_task(run_task, Crew(), task)
    return str(task.id)

@app.get("/task/{task_id}") 
def get_task(task_id: str) -> Task:
    if UUID(task_id) not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks[UUID(task_id)]

@app.get("/tasks")
def get_tasks() -> list[str]:
    return [str(tk) for tk in tasks.keys()]


@app.get("/health")
def health() -> JSONResponse:
    return JSONResponse({"status": "ok"})