from app import create_app, create_db_and_table
import uvicorn

if __name__ == "__main__":
    app = create_app()
    create_db_and_table()
    uvicorn.run(app=app, host='0.0.0.0', port=8000)