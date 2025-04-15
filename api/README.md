## Folder Structure

```
chimney_farms/
├── api/
│   ├── main.py                  # FastAPI app entrypoint
│   ├── routes/                  # All routers
│   │   ├── __init__.py
│   │   └── customer_route.py
│   ├── core/                    # Core utilities & settings
│   │   └── lifespan.py          # App startup/shutdown logic
│   ├── db/                      # Database-related modules
│   │   ├── __init__.py
│   │   ├── engine.py            # create_async_engine + retry logic
│   │   ├── session.py           # AsyncSession + get_session
│   │   └── init.py              # DB table creation logic
│   ├── dtos/                    # SQLAlchemy DTOs
│   │   ├── __init__.py
│   │   ├── base_dto.py          
│   │   ├── customer_dto.py          
│   ├── schemas/                 # Pydantic models
│   │   ├── customer_schema.py  
│   ├── daos/                    # Data Access Objects
│   │   ├── __init__.py
│   │   ├── customer_dao.py     
├── .env                         # Environment variables
├── pyproject.toml               # Project configuration
└── Dockerfile (optional)        # Docker container setup
```

## Command to Run

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8080
```
