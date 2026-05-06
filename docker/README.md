# Docker build and deployment info

## Build Docker Image
```bash
docker build -t contractiq:latest .
```

## Run with Docker Compose
```bash
# Development
docker-compose up

# Production
docker-compose -f docker-compose.yml up -d

# View logs
docker-compose logs -f api

# Stop services
docker-compose down
```

## Database

The docker-compose includes PostgreSQL. Connect with:
- Host: localhost
- Port: 5432
- User: contractiq
- Password: contractiq
- Database: contractiq_db

pgAdmin is available at http://localhost:5050

## Environment Variables

Create .env file in project root:
```
GEMINI_API_KEY=your_key_here
SECRET_KEY=your_secret_key
DATABASE_URL=postgresql://contractiq:contractiq@db:5432/contractiq_db
ENVIRONMENT=production
```
