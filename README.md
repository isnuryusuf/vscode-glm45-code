# FastAPI Vue Boilerplate

A complete boilerplate for building web applications with FastAPI backend, Vue.js frontend, and SQLite database.

## Features

- **FastAPI Backend**: Modern, fast web framework for building APIs with Python
- **Vue.js Frontend**: Progressive JavaScript framework for building user interfaces
- **SQLite Database**: Lightweight, serverless SQL database engine
- **RESTful API**: Complete CRUD operations for items and users
- **CORS Configuration**: Properly configured for frontend-backend communication
- **Responsive Design**: Mobile-friendly interface
- **Environment Configuration**: Flexible configuration with environment variables
- **Database Relationships**: Proper SQLAlchemy relationships between models
- **Error Handling**: Comprehensive error handling with proper HTTP status codes

## Project Structure

```
├── backend/
│   ├── main.py              # FastAPI application entry point
│   ├── run.py               # Startup script for development
│   ├── config.py            # Configuration management
│   ├── database.py          # Database configuration
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── .env.example         # Environment variables template
│   ├── requirements.txt     # Python dependencies
│   └── routers/
│       ├── __init__.py
│       ├── items.py         # Items API endpoints
│       └── users.py         # Users API endpoints
├── frontend/
│   ├── package.json         # Node.js dependencies
│   ├── public/
│   │   └── index.html       # HTML template
│   └── src/
│       ├── main.js          # Vue application entry point
│       ├── App.vue          # Root component
│       ├── router/
│       │   └── index.js     # Vue router configuration
│       ├── services/
│       │   └── api.js       # API service
│       └── views/
│           ├── Home.vue     # Home page
│           ├── Items.vue    # Items management
│           └── Users.vue    # Users management
└── README.md                # This file
```

## Setup Instructions

### Prerequisites

- Python 3.8+
- Node.js 14+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables (optional):
   ```bash
   cp .env.example .env
   # Edit .env file with your configuration
   ```

5. Run the FastAPI server (choose one method):

   **Method 1: Using the startup script (recommended for development)**
   ```bash
   python run.py
   ```

   **Method 2: Direct execution**
   ```bash
   python main.py
   ```

   **Method 3: Using uvicorn directly**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

   The backend will be available at `http://localhost:8000`
   - API documentation: `http://localhost:8000/docs`
   - Alternative docs: `http://localhost:8000/redoc`
   - Health check: `http://localhost:8000/api/health`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

3. Run the Vue development server:
   ```bash
   npm run serve
   ```

   The frontend will be available at `http://localhost:8080`

## API Endpoints

### Health Check
- `GET /api/health` - Check backend health

### Items
- `GET /api/items/` - Get all items
- `POST /api/items/` - Create a new item
- `GET /api/items/{id}` - Get a specific item
- `PUT /api/items/{id}` - Update an item
- `DELETE /api/items/{id}` - Delete an item

### Users
- `GET /api/users/` - Get all users
- `POST /api/users/` - Create a new user
- `GET /api/users/{id}` - Get a specific user

## Development

### Backend Development

The FastAPI backend includes:
- Automatic API documentation with Swagger UI
- SQLAlchemy ORM for database operations
- Pydantic for data validation
- CORS middleware for frontend communication

### Frontend Development

The Vue.js frontend includes:
- Vue Router for navigation
- Axios for HTTP requests
- Responsive design with CSS Grid and Flexbox
- Component-based architecture

## Database

The application uses SQLite as the database. The database file (`app.db`) will be created automatically in the backend directory when the application first runs.

## Environment Variables

You can configure the application using environment variables:

### Backend
- `DATABASE_URL`: SQLite database connection string (default: `sqlite:///./app.db`)

### Frontend
- `VUE_APP_API_BASE_URL`: Backend API base URL (default: `http://localhost:8000`)

## Building for Production

### Backend
```bash
cd backend
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Frontend
```bash
cd frontend
npm run build
```

The built frontend files will be in the `frontend/dist` directory.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the MIT License.