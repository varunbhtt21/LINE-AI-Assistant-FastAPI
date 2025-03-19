# Makkaizou-LINE Integration

This project integrates a custom "Makkaizou" system (a ChatGPT-based chatbot solution) with a LINE Official Account. The system receives messages from a LINE group, processes them via the Makkaizou API, and responds with the output of the Makkaizou system.

## Features

- Receives webhook events from LINE
- Processes messages that mention the LINE Official Account
- Maps LINE group IDs to Makkaizou talk_ids
- Calls the Makkaizou API to process prompts
- Sends responses back to LINE groups
- Logs all interactions for monitoring and debugging

## Technology Stack

- **Backend**: Python FastAPI
- **Database**: PostgreSQL
- **External APIs**: LINE Messaging API, Makkaizou API

## Prerequisites

- Python 3.8+
- PostgreSQL
- LINE Developer Account
- LINE Official Account
- Makkaizou API access

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/makkaizou-line-integration.git
cd makkaizou-line-integration
```

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

5. Edit the `.env` file with your configuration.

## Configuration

The following environment variables need to be set:

- `DATABASE_URL`: PostgreSQL connection string
- `LINE_CHANNEL_SECRET`: LINE channel secret
- `LINE_CHANNEL_ACCESS_TOKEN`: LINE channel access token
- `MAKKAIZOU_API_KEY`: Makkaizou API key
- `MAKKAIZOU_API_URL`: Makkaizou API URL

## Running the Application

### Development

```bash
uvicorn app.main:app --reload
```

### Production

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Setting up LINE Webhook

1. Go to the [LINE Developers Console](https://developers.line.biz/)
2. Create a new provider if you don't have one
3. Create a new channel of type "Messaging API"
4. Set the webhook URL to your server's URL + `/webhook/line`
5. Enable webhooks
6. Generate a channel access token

## Testing

You can test the application using Postman:

1. Send a POST request to `/webhook/line`
2. Set the `X-Line-Signature` header with a valid signature
3. Use a sample webhook event in the request body

## Project Structure

```
makkaizou-line-integration/
├── app/
│   ├── api/
│   │   ├── webhook.py
│   │   └── ...
│   ├── database/
│   │   ├── models.py
│   │   └── ...
│   ├── services/
│   │   ├── line_service.py
│   │   ├── makkaizou_service.py
│   │   └── ...
│   ├── utils/
│   │   ├── auth.py
│   │   ├── logging.py
│   │   └── ...
│   ├── config.py
│   └── main.py
├── tests/
│   └── ...
├── .env
├── .env.example
├── requirements.txt
└── README.md
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [LINE Messaging API](https://developers.line.biz/en/docs/messaging-api/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Pydantic](https://pydantic-docs.helpmanual.io/)