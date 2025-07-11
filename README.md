
# Weather Dashboard

A full stack weather dashboard application using Flask (backend) and React (frontend).

## Project Structure
- `flask_backend/`: Flask backend for weather API and search history
- `frontend/`: React app for user interface
- `docker-compose.yml`: Multi-container setup for backend and frontend

## Development

### Backend (Flask)
1. Go to `flask_backend/`
2. (Recommended) Create and activate virtual environment
3. Install dependencies: `pip install -r requirements.txt`
4. Run server: `python app.py`
   - The backend runs on port 5001 by default

### Frontend (React)
1. Go to `frontend/`
2. Install dependencies: `npm install`
3. Run dev server: `npm run dev`
   - The frontend runs on port 5173 by default

### Docker
To run both services with Docker Compose:
```sh
docker-compose up --build
```

## Notes
- All code, comments, and names are in English only.
- Backend runs on port 5001, frontend on port 5173 by default.
