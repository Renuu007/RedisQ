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

| Service | Purpose | Container Name | Port |
|---------|---------|----------------|------|
| `redis` | Redis server | `redisq-redis` | 6379 |
| `redisq` | Test runner | `redisq-app` | - |
| `redisq-example` | Example usage | `redisq-example` | - |
| `redis-cli` | Redis CLI (debug) | `redisq-cli` | - |

## 🛠️ Docker Commands

### Build and Test

```bash
# Build the Docker image
docker-compose build

# Run tests only
docker-compose up --build redisq

# Run examples only
docker-compose up --build redisq-example

# Run both tests and examples
docker-compose up --build

# Clean up containers and volumes
docker-compose down -v
```

### Development

```bash
# Start Redis for development
docker-compose up -d redis

# Run your Python code against containerized Redis
# (Redis will be available at localhost:6379)
python test_redisq.py
python example_usage.py
```

### Monitoring and Debugging

```bash
# View logs for all services
docker-compose logs -f

# View logs for specific service
docker-compose logs -f redisq
docker-compose logs -f redis
docker-compose logs -f redisq-example

# Check Redis health
docker-compose exec redis redis-cli ping

# Monitor Redis commands in real-time
docker-compose exec redis redis-cli monitor

# Start Redis CLI for debugging (uses debug profile)
docker-compose --profile debug up redis-cli
```

## 📦 Image Details

- **Base Image**: `python:3.13-slim`
- **Python Version**: 3.13
- **Redis Version**: 7-alpine
- **Container Names**: 
  - `redisq-redis` (Redis server)
  - `redisq-app` (Test runner)
  - `redisq-example` (Example usage)
  - `redisq-cli` (Redis CLI for debugging)
- **Network**: `redisq-network` (bridge driver)
- **Volumes**: `redis_data` (persistent Redis data)
- **Size**: ~200MB (optimized)

## 🔍 Troubleshooting

### Redis Connection Issues

```bash
# Check if Redis is running and healthy
docker-compose ps

# Test Redis connectivity
docker-compose exec redis redis-cli ping

# Check Redis logs
docker-compose logs redis

# Verify Redis is listening on correct port
docker-compose exec redis redis-cli -h redis -p 6379 ping
```

### Application Issues

```bash
# Check application logs
docker-compose logs redisq

docker-compose logs redisq-example

# Get shell access to debug
docker-compose run --rm redisq bash

docker-compose run --rm redisq-example bash

# Test Redis connection from app containers
docker-compose run --rm redisq python -c "import redis; r=redis.Redis(host='redis'); print(r.ping())"

docker-compose run --rm redisq-example python -c "import redis; r=redis.Redis(host='redis'); print(r.ping())"

# Check environment variables
docker-compose run --rm redisq env | grep REDIS
```

## 🔧 Advanced Usage

### Custom Commands

```bash
# Run custom Python commands
docker-compose run --rm redisq python -c "from redisq import RedisQ; print('RedisQ imported successfully')"

# Execute shell commands in containers
docker-compose run --rm redisq ls -la /app

docker-compose run --rm redisq pip list

# Connect to Redis CLI interactively
docker-compose run --rm redis-cli redis-cli -h redis

# Monitor Redis in real-time
docker-compose run --rm redis-cli redis-cli -h redis monitor
```

### PowerShell Users

```powershell
# Use semicolon instead of && for command chaining
cd "d:\NEXT '25\GitHub\RedisQ"; docker-compose up --build

# View logs with filtering
docker-compose logs --tail=50 redisq

docker-compose logs --follow --tail=10 redis
```

## 🚨 Troubleshooting

Having issues? Check our common solutions:

- **Port 6379 already in use**: Stop local Redis or change port mapping
- **PowerShell command issues**: Use semicolon (`;`) instead of `&&`
- **Container connection refused**: Ensure Redis health check passes
- **Build failures**: Clear Docker cache with `docker system prune`
- **Permission errors**: Ensure Docker daemon is running and accessible

## 🚀 Next Steps

1. **Local Development**: Use `docker-compose up -d redis` for local Redis server
2. **CI/CD Integration**: Use the services in your GitHub Actions or CI pipeline
3. **Production Deployment**: Adapt the compose file for production environments
4. **Monitoring**: Add Redis monitoring tools like RedisInsight
5. **Scaling**: Use Docker Swarm or Kubernetes for production scaling

---

**Happy testing with Docker!** 🐳
