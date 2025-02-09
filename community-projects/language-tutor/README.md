# Language Tutor App

An interactive language learning application powered by AI that helps users practice vocabulary and grammar through personalized exercises.

## Features

### 1. Personalized Learning Experience

- **Language Selection**: Support for multiple languages
- **Proficiency Levels**: Adapts content difficulty based on user level (1-5)
- **Topic-Based Learning**: Focus on specific topics or general language skills

### 2. Exercise Types

#### Grammar Exercises

- **Fill in the Blanks**: Practice grammar by completing sentences
- **Multiple Choice**: Select the correct grammatical form
- **Smart Answer Checking**: Handles accents and special characters intelligently
- **Detailed Explanations**: Learn from comprehensive grammar rule explanations

#### Vocabulary Exercises

- **Flashcards**: Learn new words with translation and context
- **Word Usage Examples**: See how words are used in sentences
- **Progress Tracking**: Review words you've learned

#### Conversation Practice

- **Interactive Dialogues**: Practice real-world conversations
- **Contextual Responses**: AI adapts responses to your input
- **Cultural Context**: Learn appropriate language use in different situations
- **Natural Flow**: Experience natural language progression in conversations

### 3. AI-Powered Features

- **Dynamic Exercise Generation**: Exercises are generated in real-time using LLM
- **Adaptive Difficulty**: Content matches your proficiency level
- **Contextual Feedback**: Get helpful explanations for your answers
- **Natural Language Understanding**: Handles variations in user responses

## Technical Details

### Prerequisites

- Python 3.11 or higher
- Groq API key for LLM integration

### Installation

- Clone the repository:

```bash
git clone <repository-url>
cd language-tutor
```

- Create and activate a virtual environment:

```bash
python -m venv ltutenv
source ltutenv/bin/activate  # On Windows: ltutenv\Scripts\activate
```

- Install dependencies:

```bash
pip install -r requirements.txt
```

- Set up environment variables:

```bash
# Create .env file
echo "GROQ_API_KEY=your_api_key_here" > .env
```

### Running the App

- Start the Streamlit app:

```bash
streamlit run app.py
```

- Open your browser and navigate to:

- Local: <http://localhost:8501>
- Network: <http://your-network-ip:8501>

## Project Structure

```sh
language-tutor/
├── agents/
│   ├── base_agent.py         # Base class for language agents
│   ├── grammar_agent.py      # Grammar exercise generation
│   ├── vocabulary_agent.py   # Vocabulary exercise generation
│   └── conversation_agent.py # Interactive conversation practice
├── components/
│   ├── exercise_card.py    # Grammar exercise UI component
│   └── flashcard.py        # Vocabulary flashcard UI component
├── models/
│   └── schemas.py          # Data models and enums
├── utils/
│   └── exercise_generator.py # Exercise generation utilities
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Key Components

### Exercise Generator

- Manages the generation of both grammar and vocabulary exercises
- Integrates with LLM for dynamic content creation
- Handles exercise type selection and difficulty adjustment

### Grammar Agent

- Generates contextually appropriate grammar exercises
- Provides multiple exercise formats (fill-in-blanks, multiple choice)
- Creates detailed explanations for grammar rules

### Exercise Card Component

- Displays grammar exercises with various input methods
- Handles answer validation and feedback
- Supports accent-aware answer checking
- Manages exercise state and transitions

### Conversation Agent

- Facilitates natural language conversations
- Adapts responses based on user proficiency
- Provides cultural context and explanations
- Corrects language mistakes while maintaining conversation flow

## Future Enhancements

1. **User Progress Tracking**
   - Save learning history
   - Track commonly made mistakes
   - Provide progress analytics

2. **Enhanced Exercise Types**
   - Sentence construction
   - Word order exercises
   - Listening comprehension

3. **Social Features**
   - User communities
   - Progress sharing
   - Competitive elements

4. **Content Management**
   - Save favorite exercises
   - Create custom exercise sets
   - Export learning materials

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
