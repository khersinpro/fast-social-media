docker build -t fast_api_app -f dockerfile.dev .  
docker run -d -p 8000:8000 fast_api_app
docker-compose -f docker-compose.dev.yml up -d
