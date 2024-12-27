def get_db():
    from app import engine
    from sqlalchemy.orm import sessionmaker


    Session = sessionmaker(autoflush=False, autocommit=False, bind=engine)
    db = Session()
    try:
        yield db
    finally:
        db.close()