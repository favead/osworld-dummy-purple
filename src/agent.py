import base64

from a2a.server.tasks import TaskUpdater
from a2a.types import (DataPart, FilePart, FileWithBytes, Message, Part,
                       TaskState, TextPart)
from a2a.utils import new_agent_text_message

from messenger import Messenger


class Agent:
    def __init__(self):
        self.messenger = Messenger()
        # Initialize other state here

    async def run(self, message: Message, updater: TaskUpdater) -> None:
        """Implement your agent logic here.

        Args:
            message: The incoming message
            updater: Report progress (update_status) and results (add_artifact)

        Use self.messenger.talk_to_agent(message, url) to call other agents.
        """
        # Replace this example code with your agent logic

        await updater.update_status(
            TaskState.working, new_agent_text_message("Thinking...")
        )
        # Unpack parts sent by A2AClientAgent
        instruction = ""
        obs: dict = {}
        env_config: dict = {}

        for part in message.parts:
            root = part.root
            if isinstance(root, TextPart):
                instruction = root.text
                print(f"instruction: {instruction}")
            elif isinstance(root, FilePart):
                if isinstance(root.file, FileWithBytes):
                    obs["screenshot"] = base64.b64decode(root.file.bytes)
                    print(f"  obs[screenshot]: {len(obs['screenshot'])} bytes")
            elif isinstance(root, DataPart):
                if "env_config" in root.data:
                    env_config = root.data["env_config"]
                    print(f"env_config: {env_config!r}")
                else:
                    obs.update(root.data)
                    for key, val in root.data.items():
                        print(f"  obs[{key}]: {val!r}")

        response = "dummy agent doing nothing"
        actions = ["DONE"]

        await updater.add_artifact(
            parts=[
                Part(root=TextPart(text=response)),
                Part(root=DataPart(data={"actions": actions})),
            ],
            name="prediction",
        )
