[English](README.md)
[简体中文](README_ZH.md)

# efcCache

efcCache is a general-purpose cache library that supports multiple storage backends, including:

- Local file
- SQLite
- MySQL
- PostgreSQL
- Redis

## Installation

Install efcCache using pip:

```bash
pip install efcCache
```

## Quick Start

Here's a simple example of using efcCache:

```python
import efcCache
from efcCache.providers.FileCache import FileCache

# Create a cache manager
cacheManager = efcCache.CacheManager(default_storage="local")

# Set up storage backend
cacheManager.set_storage("local", FileCache(storage_path="./storage/"))

# Use the cache class
print("Testing file cache:")
cacheManager.set("test", "File cache test")
print(cacheManager.get("test"))
print(cacheManager.exists("test"))
cacheManager.delete("test")
print(cacheManager.exists("test"))
```

Importing other cache providers:
```python
import efcCache
from efcCache.providers.FileCache import FileCache
from efcCache.providers.SQLiteCache import SQLiteCache
from efcCache.providers.RedisCache import RedisCache
from efcCache.providers.MySQLCache import MySQLCache
from efcCache.providers.PostgreSQLCache import PostgreSQLCache

# Create a cache manager
manager = efcCache.CacheManager(default_storage="local")

# Set up storage backends
manager.set_storage("local", FileCache(storage_path="./storage/"))
manager.set_storage("sqlite", SQLiteCache(storage_path="./storage/cache.db"))
manager.set_storage("redis", RedisCache(host="localhost", port=6379, db=0))
manager.set_storage("mysql", MySQLCache(connection_string="mysql://root:password@localhost:3306/test", table="cache"))
manager.set_storage("postgresql", PostgreSQLCache(connection_string="postgresql://postgres:password@localhost:5432/test", table="cache"))

# Test file cache
print("Testing file cache:")
manager.get_storage("local").set("test", "File cache test")
print(manager.get_storage("local").get("test"))
print(manager.get_storage("local").exists("test"))
manager.get_storage("local").delete("test")
print(manager.get_storage("local").exists("test"))

# Test SQLite cache
print("\nTesting SQLite cache:")
manager.get_storage("sqlite").set("test", "SQLite cache test")
print(manager.get_storage("sqlite").get("test"))
print(manager.get_storage("sqlite").exists("test"))
manager.get_storage("sqlite").delete("test")
print(manager.get_storage("sqlite").exists("test"))

# Test Redis cache
print("\nTesting Redis cache:")
manager.get_storage("redis").set("test", "Redis cache test")
print(manager.get_storage("redis").get("test"))
print(manager.get_storage("redis").exists("test"))
manager.get_storage("redis").delete("test")
print(manager.get_storage("redis").exists("test"))

# Test MySQL cache
print("\nTesting MySQL cache:")
manager.get_storage("mysql").set("test", "MySQL cache test")
print(manager.get_storage("mysql").get("test"))
print(manager.get_storage("mysql").exists("test"))
manager.get_storage("mysql").delete("test")
print(manager.get_storage("mysql").exists("test"))

# Test PostgreSQL cache
print("\nTesting PostgreSQL cache:")
manager.get_storage("postgresql").set("test", "PostgreSQL cache test")
print(manager.get_storage("postgresql").get("test"))
print(manager.get_storage("postgresql").exists("test"))
manager.get_storage("postgresql").delete("test")
print(manager.get_storage("postgresql").exists("test"))

# Test expiration time
print("\nTesting expiration time:")
manager.get_storage("local").set("expire_test", "Expiration test", expire=5)
print(manager.get_storage("local").get("expire_test"))
import time
print("Waiting for 6 seconds...")
time.sleep(6)
print(manager.get_storage("local").get("expire_test"))

# Test default storage
print("\nTesting default storage:")
manager.set("default_test", "Default storage test")
print(manager.get("default_test"))
print(manager.exists("default_test"))
manager.delete("default_test")
print(manager.exists("default_test"))
```

## Contributing

Contributions are welcome, whether it's code contributions, bug reports, or suggestions for improvements. Please check our [contribution guidelines](CONTRIBUTING.md) for more information.

## License

efcCache is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.