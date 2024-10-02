## Setup instructions

Curl command to test your local Ollama instance:

`curl --location 'http://localhost:11434/api/chat' \
--header 'Content-Type: application/json' \
--data '{
  "model": "llama3.1", 
  "messages": [
    {
      "role": "system", 
      "content": "you are a salty pirate" 
    },
    {
      "role": "user", 
      "content": "why is the sky blue" 
    }
  ],
  "stream": false 
}'`
