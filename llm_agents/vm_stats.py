from pd_ai_agent_core.core_types import LlmChatAgent, LlmChatResultmChatResult


class VMStatsAgent(LlmChatAgent):
    def __init__(self):
        super().__init__(
            name="VM Statistics Agent",
            instructions="I provide detailed statistics about virtual machines.",
            functions=[self.get_vm_resources, self.get_vm_performance],
        )

    def get_vm_resources(self, vm_id: str) -> LlmChatResult:
        """Get resource usage for a VM"""
        # This is just a mock implementation
        return LlmChatResult(
            value=f"Getting resource usage for VM {vm_id}",
            context_variables={"vm_id": vm_id},
        )

    def get_vm_performance(self, vm_id: str) -> LlmChatResult:
        """Get performance metrics for a VM"""
        # This is just a mock implementation
        return LlmChatResult(
            value=f"Getting performance metrics for VM {vm_id}",
            context_variables={"vm_id": vm_id},
        )
