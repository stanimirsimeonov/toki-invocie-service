from toki.app import app
from toki.agents.topics import new_files_topic


@app.agent(new_files_topic)
async def greet(csv_files):
    async for greeting in csv_files:
        print(greeting)
        yield
