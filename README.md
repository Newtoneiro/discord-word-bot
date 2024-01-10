# Translation Bot for Discord

A simple Discord bot that translates words and helps you learn new vocabulary.

## Features

- Translate words from english language to Polish.
- Add words to your personal dictionary.
- Learn new words with interactive quizzes.

## Getting Started

Follow these steps to get the bot up and running in your Discord server.

### Prerequisites

- Python 3.7 or higher
- Discord.py library
- python-dotenv
- googletrans

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Newtoneiro/discord-word-bot
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root with the following content:

   ```env
   CHANNEL_ID=your_channel_id
   BOT_TOKEN=your_bot_token
   ```

4. Run the bot:

   ```bash
   python run.py
   ```

## Usage

- Use the `>t` command to translate words. Example: `>t hello world`
- Add words to your dictionary with the `>a` command. Example: `>a cat dog`
- Learn new words with the `>l` command. Example: `>l 5` (to learn 5 words)
