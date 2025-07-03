# RedisQ Docker Testing Guide 🐳

This guide shows how to test RedisQ using Docker and Docker Compose.

## 🚀 Quick Start

### 1. Run Tests with Docker Compose

```bash
# Build and run the test suite
docker-compose up --build redisq

# Run the example usage
docker-compose up --build redisq-example

# Run both tests and example
docker-compose up --build
```

### 2. Interactive Testing

```bash
# Start Redis in the background
docker-compose up -d redis

# Run tests interactively
docker-compose run --rm redisq python test_redisq.py

# Run examples interactively
docker-compose run --rm redisq python example_usage.py

# Get a shell in the container
docker-compose run --rm redisq bash
```

### 3. Debugging with Redis CLI

```bash
# Start Redis CLI (debug profile)
docker-compose --profile debug up redis-cli

# Or run Redis CLI commands directly
docker-compose run --rm redis-cli redis-cli -h redis ping
docker-compose run --rm redis-cli redis-cli -h redis info
```

## 🔧 Available Services

| Service | Purpose | Port |
|---------|---------|------|
| `redis` | Redis server | 6379 |
| `redisq` | Test runner | - |
| `redisq-example` | Example usage | - |
| `redis-cli` | Redis CLI (debug) | - |

## 🛠️ Docker Commands

### Build and Test

```bash
# Build the Docker image
docker-compose build

# Run tests
docker-compose up redisq

# Run examples
docker-compose up redisq-example

# Clean up
docker-compose down -v
```

### Development

```bash
# Start Redis for development
docker-compose up -d redis

# Run your Python code against containerized Redis
# (Redis will be available at localhost:6379)
python test_redisq.py
```

### Monitoring

```bash
# View logs
docker-compose logs -f redisq
docker-compose logs -f redis

# Check Redis health
docker-compose exec redis redis-cli ping

# Monitor Redis commands
docker-compose exec redis redis-cli monitor
```

## 📦 Image Details

- **Base Image**: `python:3.13-slim`
- **Python Version**: 3.13
- **Redis Version**: 7-alpine
- **Size**: ~200MB (optimized)

## 🔍 Troubleshooting

### Redis Connection Issues

```bash
# Check if Redis is running
docker-compose ps

# Test Redis connectivity
docker-compose exec redis redis-cli ping

# Check Redis logs
docker-compose logs redis
```

### Application Issues

```bash
# Check application logs
docker-compose logs redisq

# Get shell access
docker-compose run --rm redisq bash

# Test Redis connection from app
docker-compose run --rm redisq python -c "import redis; r=redis.Redis(host='redis'); print(r.ping())"
```

## 🧪 Testing Different Scenarios

### Performance Testing

```bash
# Run multiple instances
docker-compose up --scale redisq=3

# Monitor Redis performance
docker-compose exec redis redis-cli --latency
```

### Different Redis Configurations

```bash
# Use different Redis image
docker-compose run --rm -e REDIS_IMAGE=redis:6-alpine redisq

# Connect to external Redis
docker-compose run --rm -e REDIS_URL=redis://your-redis-host:6379 redisq
```

## 📝 Notes

- Redis data is persisted in a Docker volume
- The application automatically waits for Redis to be healthy
- All services are connected via a dedicated network
- Use `--profile debug` for additional debugging services

## 🚀 Next Steps

1. **Local Development**: Use `docker-compose up -d redis` for local Redis
2. **CI/CD**: Use the Dockerfile for automated testing
3. **Production**: Adapt the compose file for production deployment

---

**Happy testing with Docker!** 🐳
