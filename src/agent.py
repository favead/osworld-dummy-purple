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

        instruction = ""
        for part in message.parts:
            if isinstance(part.root, TextPart):
                instruction = part.root.text
                print(f"instruction: {instruction}")
            elif isinstance(part.root, FilePart):
                file = part.root.file
                if isinstance(file, FileWithBytes):
                    raw = base64.b64decode(file.bytes)
                    print(f"  obs[screenshot]: {len(raw)} bytes")
            elif isinstance(part.root, DataPart):
                for key, val in part.root.data.items():
                    print(f"  obs[{key}]: {val!r}")

        llm_response = "dummy agent doing nothing"
        actions = ["DONE"]

        await updater.add_artifact(
            parts=[
                Part(root=TextPart(text=llm_response)),
                Part(root=DataPart(data={"actions": actions})),
            ],
            name="Response",
        )
