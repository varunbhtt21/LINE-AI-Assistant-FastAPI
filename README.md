# LINE-AI Assistant

Integration between LINE Messaging API and Makkaizou AI using FastAPI

## Implementation Progress

### ✅ Phase 1: Foundation (Completed)
- **Project Structure**
  - FastAPI application setup with modular architecture
  - PostgreSQL database integration
  - Docker containerization with networking
  - Comprehensive logging system

- **Core Components**
  - LINE webhook endpoint implementation
  - Database models and migrations
  - Basic message handling
  - Environment configuration
  - GitHub repository setup

### ✅ Phase 2: Core Implementation (Completed)
- **Message Processing**
  - LINE webhook validation
  - Message event handling
  - Mention detection in group chats
  - Error logging and monitoring

- **Integration Features**
  - Makkaizou API connection
  - Response handling and formatting
  - Database persistence
  - Docker networking configuration

### 🚧 Phase 3: Enhancement (In Progress)
- Loading indicator implementation
- Advanced error handling
- Comprehensive monitoring
- Performance optimizations
- Rich message formatting
- Caching mechanisms

### 📅 Phase 4: Testing & Deployment (Planned)
- End-to-end testing
- Load testing
- Security audits
- Production deployment
- Documentation updates

## Recent Technical Improvements
- Added explicit DNS configuration
- Implemented bridge network for containers
- Enhanced container communication
- Fixed network connectivity issues

## Setup Instructions

### Prerequisites
- Docker and Docker Compose
- Python 3.8+
- PostgreSQL (if running without Docker)
- LINE Developer Account
- Makkaizou API Access

### Environment Setup
1. Clone the repository
```bash
git clone https://github.com/varunbhtt21/LINE-AI-Assistant-FastAPI.git
cd LINE-AI-Assistant-FastAPI
```

2. Copy environment example and configure
```bash
cp .env.example .env
# Edit .env with your configurations
```

3. Start with Docker
```bash
docker-compose up -d
```

4. Check logs
```bash
docker-compose logs -f app
```

### LINE Configuration
1. Set up LINE Developer Account
2. Create LINE Official Account
3. Configure Webhook URL
4. Enable webhook setting

### Testing
1. Add the LINE bot to a group
2. Mention the bot in a message
3. Check application logs for response

## Architecture

The application follows a modular architecture:
- `/app`: Main application code
  - `/api`: API endpoints
  - `/database`: Database models and connection
  - `/services`: Business logic
  - `/utils`: Utility functions

## Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details.

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

## Acknowledgements

- [LINE Messaging API](https://developers.line.biz/en/docs/messaging-api/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Pydantic](https://pydantic-docs.helpmanual.io/)