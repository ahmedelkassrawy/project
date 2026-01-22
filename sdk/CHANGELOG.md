# Changelog

All notable changes to the SWCPY SDK will be documented in this file.

## [0.0.1] - 2026-01-21

### Added
- Initial release of SWCPY SDK
- Complete implementation of all SWC Fantasy Sports API endpoints
- SWCClient class with all API methods
- SWCConfig class for client configuration
- Pydantic data models for type safety:
  - Player, PlayerBase
  - Performance
  - Team, TeamBase
  - League
  - Counts
- Exponential backoff retry mechanism
- Comprehensive documentation:
  - README.md with full API reference
  - QUICKSTART.md for getting started
  - SDK_SUMMARY.md for overview
  - ARCHITECTURE.md for design details
- Example script (example.py) demonstrating all features
- Test suite (test_swcpy.py) with unit and integration tests
- Pytest configuration
- Package configuration (pyproject.toml)

### Features
- List and get individual players
- List and get individual performances
- List and get individual leagues
- List and get individual teams
- Get entity counts
- Health check endpoint
- Filtering by date, name, and other parameters
- Pagination support (skip/limit)
- Automatic retry with exponential backoff
- Type-safe responses with Pydantic validation
- Support for CSV and Parquet bulk file formats

### Dependencies
- httpx>=0.27.0 - HTTP client
- pydantic>=2.0 - Data validation
- backoff>=2.2.1 - Retry mechanism
- python-dotenv>=1.0.0 - Environment variables
- pytest>=8.1 - Testing framework

### Documentation
- Complete API reference with examples
- Quick start guide
- Architecture documentation
- Working example script
- Test examples

## Future Enhancements (Planned)

### [0.1.0] - Planned
- [ ] Async support with asyncio
- [ ] Bulk file download functionality
- [ ] Caching layer for frequently accessed data
- [ ] Rate limiting support
- [ ] Request/response logging
- [ ] Custom retry strategies

### [0.2.0] - Planned
- [ ] CLI tool for quick data queries
- [ ] Export utilities (to CSV, JSON, etc.)
- [ ] Data transformation utilities
- [ ] Batch operations support

### [0.3.0] - Planned
- [ ] WebSocket support (if API adds it)
- [ ] Streaming data support
- [ ] Real-time updates
- [ ] Event subscriptions

---

## Version Format

This project follows [Semantic Versioning](https://semver.org/):
- MAJOR version for incompatible API changes
- MINOR version for added functionality (backwards compatible)
- PATCH version for backwards compatible bug fixes
