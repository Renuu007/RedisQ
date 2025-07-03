# RedisQ Development Guide 🛠️

This guide covers development setup, contributing guidelines, and the project roadmap for RedisQ.

## 🛠️ Development & Contributing

### Roadmap

#### Core Features
- [ ] **Graceful shutdown** - Clean worker thread termination
- [ ] **Enhanced error handling** - Retry mechanisms and failure recovery
- [ ] **Task TTL** - Automatic cleanup of stale tasks
- [ ] **Custom serialization** - Support for complex data types
- [ ] **Connection pooling** - Efficient Redis connection management
- [ ] **Async support** - `@fifo` decorator for async functions

#### Reliability & Monitoring
- [ ] **Comprehensive tests** - Unit tests for all components
- [ ] **Performance benchmarks** - Throughput and latency metrics
- [ ] **Health checks** - Worker and queue monitoring
- [ ] **Metrics export** - Prometheus/StatsD integration

#### DevOps
- [ ] **CI/CD pipeline** - GitHub Actions for testing and publishing
- [ ] **Documentation** - API docs and advanced guides
- [ ] **Docker support** - Official Docker images

### Contributing

We welcome contributions! Here's how to help:

1. **🐛 Report bugs** - Open an issue with details
2. **💡 Suggest features** - Share your ideas
3. **🧪 Add tests** - Help improve reliability
4. **📝 Improve docs** - Make it easier for others
5. **🔧 Submit PRs** - Fix bugs or add features

### Development Setup

```bash
# Clone the repo
git clone https://github.com/Renuu007/RedisQ.git
cd RedisQ

# Set up development environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .
pip install -r requirements-dev.txt

# Run tests
pytest
```

## 📜 License

MIT License - feel free to use in your projects!

## 🙏 Acknowledgments

- Built with ❤️ for the Python community
- Inspired by the need for simple, reliable task queues
- Thanks to Redis for the robust foundation

---

**Ready to contribute? [Get started with development setup!](#development-setup)** 🚀
