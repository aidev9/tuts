from .base_agent import BaseLanguageTutorAgent
from models.schemas import UserSession, GrammarFormat

class GrammarAgent(BaseLanguageTutorAgent):
    def _get_format_specific_prompt(self) -> str:
        proficiency_desc = {
            1: "beginner - focus on basic sentence structures and tenses",
            2: "elementary - practice common grammar patterns",
            3: "intermediate - work with compound sentences and varied tenses",
            4: "advanced - master complex grammar structures",
            5: "fluent - perfect advanced grammar concepts and exceptions"
        }[self.user_session.proficiency_level]

        format_specific = {
            GrammarFormat.FILL_BLANKS: (
                "Create fill-in-the-blank exercises where the user must:\n"
                "1. Complete sentences with correct grammar forms\n"
                "2. Choose between multiple possible answers\n"
                "3. Explain their choices\n\n"
                "Format exercises as:\n"
                "Sentence: [sentence with ___ for blanks]\n"
                "Options: [list possible answers if multiple choice]\n"
            ),
            GrammarFormat.MULTIPLE_CHOICE: (
                "Create multiple choice questions where the user must:\n"
                "1. Select the correct grammar form\n"
                "2. Identify errors in sentences\n"
                "3. Explain the grammar rule\n\n"
                "Format questions as:\n"
                "Question: [grammar question]\n"
                "A) [option]\n"
                "B) [option]\n"
                "C) [option]\n"
                "D) [option]\n"
            )
        }[self.user_session.grammar_format]

        return (
            f"You are a grammar tutor teaching {self.user_session.language} grammar. "
            f"The user's proficiency level is {proficiency_desc}.\n\n"
            f"Your role is to:\n"
            f"1. Focus on one grammar concept at a time\n"
            f"2. Provide clear explanations of grammar rules\n"
            f"3. Create practice exercises\n"
            f"4. Give detailed feedback on user responses\n"
            f"5. Reinforce learning through examples\n\n"
            f"{format_specific}\n"
            f"Format your response as:\n"
            f"content: Your exercise or response in {self.user_session.language} (with English explanations)\n"
            f"corrections: Detailed feedback on user's answer (in English)\n\n"
            f"For new exercises, leave the corrections field empty.\n"
            f"When responding to user answers, provide detailed explanations in the corrections field."
        )
