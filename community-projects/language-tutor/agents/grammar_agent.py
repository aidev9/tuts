import random
from .base_agent import BaseLanguageTutorAgent
from models.schemas import UserSession, GrammarFormat
from pydantic import BaseModel
from typing import List, Optional
from pydantic_ai import Agent

class GrammarExercise(BaseModel):
    prompt: str
    exercise_type: str
    content: str
    correct_answer: str
    options: Optional[List[str]] = None
    explanation: str

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
            f"{format_specific}"
        )
        
    async def generate_exercise(self, exercise_type: str) -> GrammarExercise:
        """Generate a grammar exercise using the LLM"""
        # Create a new agent specifically for exercise generation
        exercise_agent = Agent(
            model=self.agent.model,
            result_type=GrammarExercise,
            system_prompt=(
                f"You are a grammar exercise generator for {self.user_session.language} learners. "
                f"Create {exercise_type} exercises appropriate for proficiency level {self.user_session.proficiency_level}.\n\n"
                f"Return the exercise in this format:\n"
                f"- prompt: Brief instruction for the exercise\n"
                f"- exercise_type: '{exercise_type}'\n"
                f"- content: The exercise content (use ___ for blanks)\n"
                f"- correct_answer: The correct answer\n"
                f"- options: [List of 4 options] (REQUIRED for multiple choice, must include the correct answer)\n"
                f"- explanation: Clear explanation of the grammar rule and why this is the correct answer\n\n"
                f"Rules for multiple choice:\n"
                f"1. ALWAYS provide exactly 4 options\n"
                f"2. Include the correct answer as one of the options\n"
                f"3. Make distractors plausible but clearly incorrect\n"
                f"4. Order options randomly\n\n"
                f"Make sure:\n"
                f"1. Content is appropriate for level {self.user_session.proficiency_level}\n"
                f"2. Exercises focus on common grammar patterns\n"
                f"3. Explanations are clear and helpful\n"
                f"4. For multiple choice, all options are properly formatted and make sense"
            )
        )
        
        # Generate the exercise
        result = await exercise_agent.run(
            "Generate a grammar exercise. " +
            ("Include exactly 4 multiple choice options." if exercise_type == "multiple_choice" else "")
        )
        
        # Handle multiple choice options
        if exercise_type == "multiple_choice":
            # Create default options if none provided or wrong length
            if not result.data.options or len(result.data.options) != 4:
                result.data.options = [
                    result.data.correct_answer,
                    f"{result.data.correct_answer} (incorrect form 1)",
                    f"{result.data.correct_answer} (incorrect form 2)",
                    f"{result.data.correct_answer} (incorrect form 3)"
                ]
            
            # Ensure correct answer is in options
            if result.data.correct_answer not in result.data.options:
                # Replace a random option with the correct answer
                result.data.options[random.randint(0, 3)] = result.data.correct_answer
            
            # Shuffle the options
            random.shuffle(result.data.options)
        
        return result.data
