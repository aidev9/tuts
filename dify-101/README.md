# Dify 101: Designing Visual AI Workflows for Smarter Agents

Welcome to the official repository for **Dify 101: Designing Visual AI Workflows for Smarter Agents**! This repo is the future home of the video tutorial designed to help developers understand how to build a visual AI app using the **Dify** platform. Whether you're a beginner or an experienced developer, your contributions are what make this project a success.

> [!IMPORTANT]  
> This repo is looking for contributors. Please check out the [guidelines](#guidelines), [benefits](#benefits) and [how to get in touch](#getintouch).

## 💎 What We Are Looking For

We are aiming to build a video tutorial explaining how to build agentic flows using Defi as a visual workflow platform.

We would like to provide several examples, starting from elementary to more advanced workflows, offering the audience a chance to see the capabilities of the platform, while keeping it fairly concise to fit within 60 minutes of watch time.

## 📗 Tutorial Modules

### Sign up and Configuration

- Introduction - walk through the Dify website and plans
- Sign up with GitHub account
- Explore the UI - click on Explore, Studio, Knowledge and Tools
- Configure models - OpenAI keys
- Explore templates - Explore Apps by Dify

### Create a Chatbot: From Template

- Studio > Create from template > Filter to Chatbot > Website Generator
  - Generate a website - Model 01-mini
  - Prompt: `Create a website for signing up members to a community of AI Software Developers`
  - Review the code

### Create a Chatbot: Medical Assistant

- Studio > Create from blank > Chatbot (Quickly build an LLM-based chatbot with simple configuration. You can switch to Chatflow later)
  - App name: Medical Assistant
  - Description: Provide MDs fresh medical knowledge
  - Prompt: You are a helpful medical research assistant. Help Medical Doctors with fresh medical facts
  - Chat: What are the home remedies for tonsillitis
  - Review the answer
  - Explore the Publish button:
    - Publish > Run App
    - Publish > Embed into Site
    - Publish > Open in Explore
    - Publish > Access API Reference

### Create an Agent: Medical Web Scraper

- Studio > Create from blank > Agent (An intelligent agent capable of iterative reasoning and autonomous tool use to achieve tasks)
  - App name: Medical Agent
  - Description: Provide MDs fresh medical knowledge
  - Prompt: You are a helpful medical research assistant who knows how to scrape websites and process data. When asked, use the tools available to scrape a website and output JSON.
  - Tools:
    - webscraper
    - json_process parse
  - Chat: Visit https://www.piedmont.org/living-real-change/9-natural-cold-and-flu-remedies and extract the flu remedies in a JSON format with remedy title and description
  - Review the answer

### Create a Chatflow: Medical RAG System

- Studio > Create from blank > Chatflow (Workflow orchestration for multi-round complex dialogue tasks with memory capabilities)
  - App name: Medical Chatflow
  - Description: Provide MDs fresh medical knowledge
  - Blocks
    - Add START
    - Add LLM
    - Add Answer
    - Add Knowledge
      - Add Knowledge - flu-remedies.pdf
    - Optional: Add Parameter Extractor
      - remedy_name: string
      - remedy_description: string
  - Prompt: You are a helpful medical research assistant who knows how to use knowledge to provide useful information medical doctors. When asked, use the tools available to provide information
  - Chat: What are the 9 home remedies for flu?
  - Review the answer

### Create a Workflow: Medical Search System with Tools (Brave Search)

- Studio > Create from blank > Chatflow (Workflow orchestration for single-round tasks like automation and batch processing)
  - App name: Medical Workflow
  - Description: Provide MDs fresh medical knowledge
  - Blocks
    - Add START block
    - Add Tools > BraveSearch
      - Enter Brave API Key: xxxxx
      - Enter Brave API Endpoint: https://api.search.brave.com/res/v1/web/search
      - Confgiure BraveSearch Block:
        - Query string: Top 10 flu home remedies
        - Result count: 5
    - Add LLM block
      - Context:
        - BraveSearch text
      - System prompt: `Use the search results from BraveSearch {{#1736341367672.text#}} and summarize the 10 best home remedies for flu`
      - User prompt: `What are the best home remedies for flu?`
    - Add End block
  - Run the workflow
  - Review the answer

## 🤝 How You Can Contribute

We welcome contributions of all kinds, no matter your skill level or area of expertise. Here are some ways you can get involved:

1. **Share an Idea**: Have a suggestion for improving this project? Open an issue and share your thoughts.
2. **Report a Bug**: Encountered an issue? Let us know by submitting a detailed bug report.
3. **Write an Article**: Help others learn by writing blog posts, tutorials, or case studies about this project.
4. **Design Visuals**: Contribute by creating engaging designs, like a cover image for our YouTube video.
5. **Write Code**: Submit code samples, fixes, or improvements to our guides and resources.
6. **Review Pull Requests**: Share your feedback on code submissions to ensure quality and accuracy.
7. **Create a Video**: Produce educational or promotional videos for our YouTube channel.
8. **Enhance Documentation**: Improve clarity and accessibility in our README, guides, and comments.
9. **Build New Features**: Help extend the functionality of the project with innovative ideas.
10. **Test the App**: Perform quality assurance by testing features and reporting issues.

## 🚀 <a name="guidelines">Guidelines for Contributors</a>

To contribute as efficiently as possible, please follow these guidelines:

1. **[Read the Code of Conduct](../CODE_OF_CONDUCT.md)**: Be respectful and constructive in your communications.
2. **Use Issues and Pull Requests**: Create an issue to discuss changes before submitting a pull request.
3. **Follow the Style Guide**: Adhere to the project’s coding and design standards.
4. **Provide Detailed Descriptions**: Include clear explanations and steps to reproduce for issues or changes.
5. **Test Your Work**: Make sure your contributions are bug-free and functional.
6. **[Read the Contribution Guide](../CONTRIBUTING.md)**: Find out the best ways to contribute.

## 📬 <a name="getintouch">How to Get in Touch</a>

- **Discord Server**: [Join our community server](https://discord.gg/eQXBaCvTA9)
- **GitHub Issues**: Use the [Issues tab](https://github.com/aidev9/tuts/issues) to share ideas or report bugs
- **Social Media**: Connect with us on X [@AISoftwareDev9](https://-com/AISoftwareDev9)
- **Social Media**: Connect with us on Bluesky [@aidev9.bsky.social](https://bsky.app/profile/aidev9.bsky.social)

## 🌟 <a name="benefits">Why Contribute? The Benefits</a>

By contributing to this project, you’ll:

1. **Boost Your Portfolio**: Show off your contributions on GitHub, LinkedIn, or resumes.
2. **Learn and Grow**: Improve your skills by collaborating with a vibrant community of developers.
3. **Network with Peers**: Build relationships with contributors, maintainers, and industry professionals.
4. **Shape the Project**: Play a key role in the direction and success of the initiative.
5. **Gain Recognition**: Get credited in the README and shoutouts on social media.
6. **Learn AI Tools**: Deepen your understanding of AI tools by working hands-on with the latest and greatest platforms
7. **Improve Communication**: Enhance your technical writing and collaboration skills.
8. **Enjoy Creative Freedom**: Express your creativity through content, design, and code.
9. **Contribute to Open Source**: Be part of the open-source community, making resources free for all.
10. **Give Back**: Help others on their journey to mastering AI development.

## 🛠 Getting Started

1. Fork this repository.
2. Clone the fork to your local machine.
3. Create a new branch for your contribution.
4. Make your changes and test them thoroughly.
5. Push your branch and open a pull request.

Thank you for contributing.
