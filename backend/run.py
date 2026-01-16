import uvicorn;
import os

if __name__ == "__main__": 
    try:
        port = int(os.environ.get("CORS_ORIGINS", 8000))
    except ValueError:
        port = 8000
        
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=port,
        reload=True  
    )