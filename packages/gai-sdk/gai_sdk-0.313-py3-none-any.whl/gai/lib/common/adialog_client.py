from abc import ABC, abstractmethod
class ADialogClient(ABC):

    @abstractmethod
    def register(self, persona):
        pass

    @abstractmethod
    def list_dialogue_messages(self):
        pass

    @abstractmethod
    def update_dialogue(self, user_message_id:str, user_id:str, user_message:str, agent_name:str, monologue:str):
        pass