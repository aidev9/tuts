# Create Your First LLM App in Minutes with Dify.ai | Agents, Workflows, Chatbots | No Code Tutorial

Welcome to the official repository for **[Create Your First LLM App in Minutes with Dify.ai | Agents, Workflows, Chatbots | No Code Tutorial](https://www.youtube.com/watch?v=-RdhQcD5lQw)**! This video tutorial is designed to help developers understand how to build a visual AI app using the **Dify** platform. Whether you're a beginner or an experienced developer, your contributions are what make this project a success.

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/RdhQcD5lQw/0.jpg)](https://www.youtube.com/watch?v=RdhQcD5lQw)

## Overview

Discover the power of Dify.ai, a low-code platform that makes building AI applications easier and faster than ever before! In this tutorial, we’ll walk you through everything you need to know to get started, from setting up your first project to creating fully functional applications powered by advanced language models. Whether you're a developer looking to streamline your workflow or a non-technical user curious about AI, Dify.ai offers a user-friendly interface and powerful features like visual workflows, RAG (Retrieval Augmented Generation), and Backend-as-a-Service architecture. By the end of this video, you'll have the tools and confidence to start building AI-powered solutions for your own projects in no time!

## Why Dify?

Dify.ai's most important differentiator is its user-friendly, low-code platform that enables both technical and non-technical users to rapidly develop and deploy large language model (LLM) applications. Its visual workflow interface simplifies the creation of complex AI applications without extensive technical skills, making AI development more accessible and efficient.

Unlike other platforms that may require significant coding and debugging, Dify.ai allows users to build powerful LLM applications quickly, reducing development time and complexity. This approach empowers organizations to integrate AI into their operations seamlessly, bridging the gap between technical and non-technical teams.

Additionally, Dify.ai offers features like Backend-as-a-Service (BaaS) architecture, Retrieval Augmented Generation (RAG), and extensive APIs, providing flexibility for users who require more customization in their AI solutions.

Overall, Dify.ai's combination of ease of use, rapid development capabilities, and advanced features positions it as a leading platform for generative AI application development.

## 📗 Tutorial Modules

### Sign up and Configuration

- Introduction - walk through the Dify website and plans
- Sign up with GitHub account
- Explore the UI - click on Explore, Studio, Knowledge and Tools
- Configure models - OpenAI keys
- Explore templates - Explore Apps by Dify

### Create a Chatbot: From Template

- Studio > Create from template > Filter to Chatbot > Website Generator
  - Name: Medical Website Generator
  - Generate a website - Model 01-mini
  - Prompt: `Create a website that provides information about home remedies for flu`
  - Review the code

### Create a Chatbot: Medical Assistant

- Studio > Create from blank > Chatbot (Quickly build an LLM-based chatbot with simple configuration. You can switch to Chatflow later)
  - App name: Medical Assistant
  - Description: Provide MDs fresh medical knowledge
  - Prompt: You are a helpful medical research assistant. Help Medical Doctors with fresh medical facts. Research {{topic}} and help the doctor.
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

## Looking for Collaborators

Have an idea for an article, video tutorial, a learning project or anything related to AI? Consider collaborating with our growing community of collaborators. Get started today by [posting your idea on our Discord sever](https://discord.gg/eQXBaCvTA9). Together, we are building a strong community of AI Software Developers.

## How to Contribute to This Repository

This repository is maintained by the team at **[AI Software Developers](https://www.youtube.com/@AISoftwareDevelopers)** channel. Contributions are welcome! If you'd like to contribute, please check out the contribution guidelines and submit a PR.

## Getting Started

### Accessibility and Ease of Use

Dify offers a visual, intuitive interface that empowers non-developers to create LLM applications. This ease of use contrasts with code-heavy frameworks like LangGraph or Autogen, making application deployment simpler. "The web-based UI is easy to get started with and allows non-developers to quickly design and deploy LLM applications."

### Visual LLM Development

The platform provides visual tools for designing prompts, enhancing context, observing LLM behavior, and training models. This visual approach makes the development process more accessible and transparent.

### Diverse Applications

Dify supports various application types, including chatbots, agents, text generators, chatflows, and workflows. This flexibility caters to diverse use cases.

### LLM Support

The platform supports popular LLMs like OpenAI models, Anthropic, and locally installed Ollama models (like Llama 3.3), providing flexibility in model selection.

## Key Features

- Visual Prompt Editor and Debugging: These features facilitate quick onboarding and enable developers to get their first agent running in under 10 minutes.
- Templates: Dify provides templates for common LLM applications, simplifying the development process.
- Integrations: Integrations with other platforms through references to a GitHub repository with code examples
- Community Support: A Discord server offers support and networking opportunities for Dify users.

## Tutorial Focus

The video tutorial aims to provide an overview of Dify's capabilities and demonstrate how to build basic LLM apps using the platform's visual flow editor. The tutorial uses a "Medical Assistant" use case and covers creating five different application types:

- Chatbot from Template
- Chatbot from Blank
- Agent with Tools
- RAG Chatflow from Blank
- Workflow with Tools
- Main Takeaways

Dify democratizes LLM development by providing an accessible, visual platform for building applications. This lowered barrier of entry opens up new possibilities for LLM applications by allowing individuals with limited coding experience to bring their ideas to life.
Dify is a promising tool for both beginners and experienced developers looking to build and deploy LLM applications quickly and efficiently.
Call to Action

## Call to Action

- Explore the Dify website and available plans
- Visit the provided GitHub repository for helpful resources and code examples
- Join the Discord server for support and networking
- Explore Dify's user-friendly and powerful platform features that empower anyone to build sophisticated LLM applications

## Thank you

Thank you for contributing to this repository! Your efforts help create a valuable resource for the AI community. If you have any questions, feel free to reach out via [our Discord sever](https://discord.gg/eQXBaCvTA9) or open an issue in this repository. Let’s build a strong AI community together!

## Video Summary

Dify is a visual LLM platform that **enables the easy and intuitive building of GPT-based applications.** The platform offers a web-based user interface (UI) that **simplifies the design and deployment of LLM applications,** particularly for individuals without coding experience. Dify stands out for its visual design, context enhancement, observation, and training features. It also supports various LLMs including OpenAI models, Anthropic, and Ollama models like Llama 3.3 when installed locally. Dify's emphasis on visual prompt editing and debugging helps users quickly grasp the platform, allowing them to create their first agent in under 10 minutes.

**Dify supports five distinct application types:**

- **Chatbot:** This application type likely focuses on creating conversational AI experiences.
- **Agent:** This application may involve building agents capable of performing specific tasks or actions.
- **Text Generator:** This application likely centers around generating text for various purposes.
- **Chatflow:** This type probably involves designing conversational flows or sequences.
- **Workflow:** This application may focus on creating automated workflows involving different steps and actions.

Dify facilitates LLM development through **chatflows, agents, and workflows**, lowering the barriers to entry for those interested in creating LLM applications. The platform's visual editors **open up possibilities for implementing creative ideas, as more individuals can engage in LLM development.**

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
