"""Main FastAPI application"""
from fastapi import FastAPI
from infrastructure.controllers import cv_controller, csv_controller, health_controller

app = FastAPI(title="File Upload Processor", version="1.0.0")

# Include routers
app.include_router(health_controller.router)
app.include_router(cv_controller.router)
app.include_router(csv_controller.router)
