# Terminal GPT

A simple command-line interface (CLI) tool to chat with ChatGPT using OpenAI's API.

## Setup

1. Ensure you have Node.js installed on your system. You can download it from [nodejs.org](https://nodejs.org/).

2. Clone or download this project to your local machine.

3. Navigate to the project directory:
   ```
   cd terminal-gpt
   ```

4. Install the dependencies:
   ```
   npm install
   ```

5. Set up your OpenAI API key:
   - Open the `.env` file in the project directory.
   - Replace the placeholder with your actual OpenAI API key. You can get one from [OpenAI's website](https://platform.openai.com/account/api-keys).

## Usage

Run the CLI tool:
```
npm start
```

Or directly:
```
node cli_gpt_node.js
```

Type your messages and press Enter. The tool will respond with ChatGPT's replies. Type "exit" to quit the conversation.

## Features

- Interactive chat with ChatGPT in the terminal.
- Maintains conversation history for context.
- Easy to set up and use.

## Dependencies

- `openai`: For interacting with OpenAI's API.
- `dotenv`: For loading environment variables from the `.env` file.

## License

This project is licensed under the ISC License.
