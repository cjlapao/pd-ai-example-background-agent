from pd_ai_agent_core.core_types import LlmChatAgent, LlmChatResulthatResult


class VMToolsAgent(LlmChatAgent):
    def __init__(self):
        super().__init__(
            name="VM Tools Agent",
            instructions="I help manage virtual machines with basic operations.",
            functions=[self.get_vm_info, self.check_vm_status],
        )

    def get_vm_info(self, vm_id: str) -> LlmChatResult:
        """Get basic information about a VM"""
        # This is just a mock implementation
        return LlmChatResult(
            value=f"Getting info for VM {vm_id}", context_variables={"vm_id": vm_id}
        )

    def check_vm_status(self, vm_id: str) -> LlmChatResult:
        """Check if a VM is running"""
        # This is just a mock implementation
        return LlmChatResult(
            value=f"Checking status for VM {vm_id}", context_variables={"vm_id": vm_id}
        )
