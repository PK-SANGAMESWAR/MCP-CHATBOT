# Expense Tracker MCP Server

A Model Context Protocol (MCP) server for tracking expenses, built with `fastmcp`.

## Features

This server provides tools to manage expenses in a local SQLite database (`expenses.db`) and exposes categories via a resource.

### Tools

- **`add_expense`**: Add a new expense.
  - Arguments: `date` (YYYY-MM-DD), `amount`, `category`, `subcategory` (optional), `note` (optional).
- **`list_expenses`**: List expenses within a date range.
  - Arguments: `start_date`, `end_date`.
- **`summarize`**: Summarize expenses by category.
  - Arguments: `start_date`, `end_date`, `category` (optional filter).
- **`edit_expense`**: Edit an existing expense.
  - Arguments: `id`, `date`, `amount`, `category`, `subcategory`, `note`.
- **`delete_expense`**: Delete an expense by ID.
  - Arguments: `id`.
- **`add_credit`**: Add credit to a user account (default user).
  - Arguments: `amount`, `user_name` (optional, default="default").

### Resources

- **`expense://categories`**: Returns the content of `categories.json`.

## Prerequisites

- Python >= 3.12
- `uv` (recommended for dependency management)

## Installation & Usage

### Using `uv` (Recommended)

You can run the server directly using `uv`:

```bash
uv run main.py
```

### Manual Installation

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install fastmcp
   ```

3. Run the server:
   ```bash
   python main.py
   ```

## Configuration for Claude Desktop

Add the following to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "expense-tracker": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "fastmcp",
        "c:\\Users\\LOQ\\Downloads\\ExpenseTracker_MCP_Server\\main.py"
      ]
    }
  }
}
```

*Note: Update the path to `main.py` to match your local path.*
