# MCP Chatbot Project

This project contains a collection of MCP (Model Context Protocol) servers and a client, designed to demonstrate various capabilities like expense tracking, math operations, remote database access, and video generation using Manim.

## Project Structure

The project is divided into several separate sub-directories, each containing its own specific implementation:

- **MCP_CLIENT**: A client application that interacts with the MCP servers using LangChain and Ollama.
- **ExpenseTracker_MCP_Server**: An MCP server for tracking expenses, using a local database.
- **MCP_MATH_SERVER**: An MCP server for performing mathematical operations.
- **MCP_REMOTE**: An MCP server for remote operations (using SQLite).
- **PROXY_SERVER**: A proxy server implementation.
- **manim-mcp-server**: An MCP server for generating math animations using Manim.

> [!IMPORTANT]
> **ALL FILES WERE SEPERATE AND THE LINKS IN THE CODE ARE BASED ON THAT FILE FOLDER PATH.**
> Please ensure you are running the code from the correct directory context or adjust paths as necessary.

## Model Performance Note

> [!NOTE]
> **O/P MAY BE LITTLE CHNGING OR NOT SATISFYING BECAUSE OF LLAMA 3B MODEL SMALL MODEL.**
> The project is configured to use a smaller language model (Llama 3B). As a result, the output quality and consistency may vary compared to larger models.

## Installation

1.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2.  Ensure you have the necessary environment variables set up for each server as described in their respective directories (if applicable).

## Usage

Navigate to the specific sub-directory of the component you wish to run and follow the instructions in that directory (if available) or run the main entry point (usually `main.py` or `app.py`).
