"""
I.R.I.S Backend - Main Application
Insight Reporting & Identification System
FastAPI server with AI agents for data analysis
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv

# Import database
from database.connection import init_db

# Import routes
from routes.auth_routes import router as auth_router
from routes.file_routes import router as file_router
from routes.analysis_routes import router as analysis_router
from routes.query_routes import router as query_router
from routes.utility_routes import router as utility_router
from routes.workspace_routes import router as workspace_router
from routes.feedback_routes import router as feedback_router
from routes.realtime_routes import router as realtime_router

# Import role-based routes
from routes.employee_routes import router as employee_router
from routes.hr_routes import router as hr_router
from routes.finance_routes import router as finance_router

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="I.R.I.S API",
    description="Insight Reporting & Identification System - Agentic Analytics Platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration
# Allow frontend to connect
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:8080",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:8080",
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle uncaught exceptions"""
    return JSONResponse(
        status_code=500,
        content={
            "detail": str(exc),
            "type": type(exc).__name__
        }
    )


# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize database, services, and agents on startup"""
    print("🚀 Starting I.R.I.S Backend...")
    
    # Initialize database
    db = init_db()
    
    # Create upload directory
    upload_dir = os.getenv("UPLOAD_DIR", "./uploads")
    os.makedirs(upload_dir, exist_ok=True)
    
    # Initialize agent manager asynchronously
    try:
        from app.agents.agent_manager import init_agent_manager
        agent_manager = await init_agent_manager(db)
        print("✅ AI agents initialized")
    except Exception as e:
        print(f"❌ Failed to initialize agents: {str(e)}")
        import traceback
        traceback.print_exc()
        # Don't raise to allow the server to start with limited functionality
    
    print("✅ Database initialized")
    print("✅ Upload directory ready")
    print("✅ I.R.I.S Backend is running!")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("👋 Shutting down I.R.I.S Backend...")
    from database.connection import close_db
    close_db()


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "service": "I.R.I.S API",
        "version": "1.0.0",
        "description": "Insight Reporting & Identification System - Agentic Analytics Platform",
        "status": "running",
        "endpoints": {
            "authentication": "/auth",
            "file_management": "/files",
            "analysis": "/analysis",
            "conversational_query": "/query",
            "workspace": "/workspace",
            "feedback": "/feedback",
            "realtime": "/realtime",
            "utilities": "/utility"
        },
        "features": [
            "Multi-agent AI Analysis",
            "Anomaly Detection (IsolationForest)",
            "Trend Forecasting (XGBoost)",
            "Root Cause Analysis",
            "AI-powered Insights",
            "Prescriptive Recommendations",
            "Conversational Q&A",
            "Real-time Data Simulation"
        ],
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc"
        }
    }


# Include routers
app.include_router(auth_router)
app.include_router(employee_router)
app.include_router(hr_router)
app.include_router(finance_router)
app.include_router(file_router)
app.include_router(analysis_router)
app.include_router(query_router)
app.include_router(utility_router)
app.include_router(workspace_router)
app.include_router(feedback_router)
app.include_router(realtime_router)

# Include agent router if exists
try:
    from app.routers import agent_router
    app.include_router(agent_router)
except ImportError:
    pass

app.include_router(auth_router)
app.include_router(file_router)
app.include_router(analysis_router)
app.include_router(query_router)
app.include_router(utility_router)
app.include_router(workspace_router)
app.include_router(feedback_router)
app.include_router(realtime_router)
app.include_router(agent_router.router)


# Run with uvicorn
if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True,  # Enable auto-reload during development
        log_level="info"
    )
