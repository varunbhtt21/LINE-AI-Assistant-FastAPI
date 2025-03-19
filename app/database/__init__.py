from app.database.database import Base, engine, get_db
from app.database.models import LineAccount, MakkaizouConfig, LineAccountMakkaizouMapping, LineGroup, MessageLog, ErrorLog

# Create all tables in the database
def init_db():
    Base.metadata.create_all(bind=engine) 