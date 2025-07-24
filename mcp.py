# mcp.py
import queue
from dataclasses import dataclass
from typing import Any, List, Optional

@dataclass
class MCPMessage:
    sender: str
    receiver: str
    type: str        
    trace_id: str    
    payload: dict    

class MCPQueue:
    def __init__(self):
        self.queue = queue.Queue()

    def send(self, message: MCPMessage):
        self.queue.put(message)

    def receive(self, receiver: Optional[str] = None) -> List[MCPMessage]:
        messages = []
        temp_queue = queue.Queue()
        while not self.queue.empty():
            msg = self.queue.get()
            if receiver is None or msg.receiver == receiver:
                messages.append(msg)
            else:
                temp_queue.put(msg)
        self.queue = temp_queue
        return messages

# Shared queue instance
mcp_queue = MCPQueue()
