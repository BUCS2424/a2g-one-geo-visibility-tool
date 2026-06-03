# A2G ONE - AI-Powered GEO Visibility Tool

An intelligent platform that audits business digital footprints and generates actionable AI visibility scores using the 2026 GEO (Generative Engine Optimization) standards.

## Project Structure

```
.
├── server/              # Node.js Backend + Express API
├── client/              # Vite + React Frontend
├── engine/              # Python GEO Scoring Engine
├── docs/                # Documentation
└── README.md
```

## Features

- **AI Visibility Scoring**: 29-signal audit engine based on 2026 standards
- **Structural Analysis**: Schema markup detection, mobile optimization, crawlability
- **Sentiment Analysis**: Reputation scoring from Google Maps, Yelp, Reddit
- **Semantic Optimization**: Voice search & conversational readiness
- **Automated Reports**: Beautiful PDF audit reports
- **User Authentication**: JWT-based authentication
- **Multi-tenant Support**: Serve multiple businesses

## Tech Stack

### Backend
- Node.js + Express.js
- MongoDB (Atlas)
- JWT Authentication
- Python Integration (GEO Engine)

### Frontend
- Vite
- React 18+
- Tailwind CSS
- Axios for API calls

### Engine
- Python 3.10+
- BeautifulSoup4 (web scraping)
- OpenAI/Google Generative AI APIs
- Requests library

## Getting Started

### Prerequisites
- Node.js 18+
- Python 3.10+
- MongoDB Atlas account
- OpenAI API key

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/BUCS2424/a2g-one-geo-visibility-tool.git
   cd a2g-one-geo-visibility-tool
   ```

2. **Backend Setup**
   ```bash
   cd server
   npm install
   cp ../.env.example .env
   npm run dev
   ```

3. **Frontend Setup** (in new terminal)
   ```bash
   cd client
   npm install
   npm run dev
   ```

4. **Python Engine Setup** (in new terminal)
   ```bash
   cd engine
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python main.py
   ```

## API Endpoints

- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/audits` - Create new audit
- `GET /api/audits/:id` - Get audit report
- `GET /api/audits` - List user audits
- `PATCH /api/audits/:id` - Update audit

## Documentation

- [Setup Guide](./docs/SETUP.md)
- [API Documentation](./docs/API.md)

## License

MIT
