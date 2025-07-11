# Weather Dashboard

A full stack weather dashboard application using Django (backend) and React (frontend).

## Project Structure
- `backend/`: Django project and app for weather API and history
- `frontend/`: React app for user interface
- `docker-compose.yml`: Multi-container setup for backend and frontend

## Development

### Backend (Django)
1. Go to `backend/`
2. Create and activate virtual environment
3. Install dependencies: `pip install -r requirements.txt`
4. Run server: `python manage.py runserver`

### Frontend (React)
1. Go to `frontend/`
2. Install dependencies: `npm install`
3. Run dev server: `npm run dev`

### Docker
To run both services with Docker Compose:
```sh
docker-compose up --build
```

## Notes
- All code, comments, and names are in English only.
- Backend runs on port 8000, frontend on port 5173 by default.
