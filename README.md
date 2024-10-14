# Curiosity

Curiosity is a Python program inspired by the Mars Curiosity rover, designed to explore and extract personal channels of users in public groups on Telegram. This tool helps you discover the personal chat details of members in a specified public group, allowing for deeper engagement and connection.

## Features

- **User Discovery**: Automatically retrieves usernames and their corresponding personal chat usernames from a specified public group.
- **SQLite Database**: Stores the extracted data in a SQLite database for easy access and management.
- **Asynchronous Processing**: Efficiently processes group members using asynchronous programming, ensuring quick and responsive operations.

## Why Use Curiosity?

Curiosity can be beneficial for various use cases, including:

- **Community Engagement**: Connect with members of a public group more personally by accessing their personal chat details.
- **Data Analysis**: Analyze user interactions and engagement within a group setting.
- **Research**: Gather insights about group dynamics and member participation.

## Getting Started

### Prerequisites

- Python 3.7 or higher
- Required Python packages: `pyrogram`, `python-dotenv`, `sqlite3`
- A Telegram account and API credentials (API ID and API Hash)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd curiosity
   ```

2. Install the required packages:
   ```bash
   pip install pyrogram python-dotenv
   ```

3. Create a `.env` file in the root directory and add your Telegram API credentials:
   ```
   API_ID=your_api_id
   API_HASH=your_api_hash
   GROUP_USERNAME=your_group_username
   ```

### Usage

Run the program using the following command:
