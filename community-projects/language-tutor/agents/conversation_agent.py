from .base_agent import BaseLanguageTutorAgent
from models.schemas import UserSession

class ConversationAgent(BaseLanguageTutorAgent):
    def _get_format_specific_prompt(self) -> str:
        proficiency_desc = {
            1: "beginner - use very simple sentences and basic vocabulary",
            2: "elementary - use simple sentences and common vocabulary",
            3: "intermediate - use moderately complex sentences and varied vocabulary",
            4: "advanced - use complex sentences and sophisticated vocabulary",
            5: "fluent - use natural, idiomatic language at a native level"
        }[self.user_session.proficiency_level]

        return (
            f"You are engaging in a conversation about '{self.user_session.topic}' in {self.user_session.language}. "
            f"The user's proficiency level is {proficiency_desc}.\n\n"
            f"Your role is to:\n"
            f"1. Maintain a natural, engaging conversation\n"
            f"2. Keep responses concise (2-3 sentences)\n"
            f"3. Gently correct any language mistakes in a separate 'corrections' field\n"
            f"4. In the corrections, explain why something was wrong and suggest better alternatives\n"
            f"5. Keep the conversation focused on: {self.user_session.topic}\n\n"
            f"Format your response as:\n"
            f"content: Your conversational response in {self.user_session.language}\n"
            f"corrections: Any corrections or suggestions (in English if user makes mistakes)\n\n"
            f"If the user's message has no mistakes, leave the corrections field empty."
        )
