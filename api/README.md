## Folder Structure

```
chimney_farms/
├── api/
│   ├── main.py                  # FastAPI app entrypoint

│   ├── routes/                  # All routers
│   │   ├── __init__.py
│   │   └── customer_route.py    # Customer-related routes

│   ├── core/                    # Core utilities & settings
│   │   └── lifespan.py          # App startup/shutdown logic

│   ├── db/                      # Database-related modules
│   │   ├── __init__.py
│   │   ├── engine.py            # create_async_engine + retry logic
│   │   ├── session.py           # AsyncSession + get_session
│   │   └── init.py              # DB table creation logic

│   ├── dtos/                    # SQLAlchemy DTOs
│   │   ├── __init__.py
│   │   ├── base_dto.py          # Base DTO class
│   │   ├── customer_dto.py      # Customer DTO
│   │   ├── crop_dto.py          # Crop DTO
│   │   ├── extent_range_dto.py  # Extent Range DTO
│   │   ├── layout_dto.py        # Layout DTO
│   │   ├── payment_mode_dto.py  # Payment Mode DTO
│   │   ├── plot_dto.py          # Plot DTO

│   ├── schemas/                 # Pydantic models
│   │   ├── __init__.py
│   │   ├── customer_schema.py   # Customer schema

│   ├── daos/                    # Data Access Objects
│   │   ├── __init__.py
│   │   ├── customer_dao.py      # Customer DAO

├── .env                         # Environment variables
├── pyproject.toml               # Project configuration
└── Dockerfile (optional)        # Docker container setup
```

## Command to Run

```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8080
```
