# VulnLib - Docker Setup

This guide explains how to run the VulnLib application using Docker Compose.

## Prerequisites

- Docker
- Docker Compose

## Quick Start

1. **Build and start the application:**
   ```bash
   docker-compose up --build
   ```

2. **Access the application:**
   - Open your browser and go to `http://localhost`

3. **Stop the application:**
   ```bash
   docker-compose down
   ```

## Docker Commands

### Build and run in detached mode:
```bash
docker-compose up -d --build
```

### View logs:
```bash
docker-compose logs -f vulnlib-app
```

### Restart the application:
```bash
docker-compose restart vulnlib-app
```

### Stop and remove containers:
```bash
docker-compose down
```

### Remove containers and volumes:
```bash
docker-compose down -v
```

## Data Persistence

The following directories are mounted as volumes to persist data:
- `./uploads` - File uploads
- `./instance` - SQLite database
- `./static/uploads` - Static file uploads

## Environment Variables

You can customize the application by modifying the environment variables in `docker-compose.yml`:
- `FLASK_ENV` - Set to `production` for production deployment
- `SECRET_KEY` - Change this for security in production

## Production Deployment

For production use, consider:

1. **Uncomment PostgreSQL service** in `docker-compose.yml`
2. **Update Flask configuration** to use PostgreSQL instead of SQLite
3. **Add Redis service** for caching
4. **Use environment files** for sensitive configuration
5. **Add reverse proxy** (Nginx) for better performance
6. **Set `FLASK_ENV=production`**

## Troubleshooting

### Permission Issues
If you encounter permission issues with uploads:
```bash
sudo chown -R $(id -u):$(id -g) uploads instance static/uploads
```

### Database Issues
To reset the database:
```bash
docker-compose down -v
rm -rf instance/vulnlib.db
docker-compose up --build
```

## Security Note

This application is intentionally vulnerable for educational purposes. Do not use in production without addressing security issues.