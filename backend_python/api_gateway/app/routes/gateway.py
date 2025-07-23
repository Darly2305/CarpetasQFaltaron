# API Gateway routing logic - Complete conversion from Express.js to FastAPI
from fastapi import APIRouter, Request, Depends, HTTPException
from datetime import datetime
import httpx
import os
from backend_python.shared.config import settings
from backend_python.shared.logger import setup_logger
from backend_python.api_gateway.app.middleware.auth import authenticate_request
from backend_python.api_gateway.app.services.mockDataGenerator import MockDataGenerator

# Initialize router and logger
router = APIRouter()
logger = setup_logger("api_gateway")
mock_data_generator = MockDataGenerator()

# Service endpoints configuration
SERVICES = {
    "SENSOR_SERVICE": os.getenv("SENSOR_SERVICE_URL", "http://localhost:8001"),
    "AI_SERVICE": os.getenv("AI_SERVICE_URL", "http://localhost:8002"),
    "NOTIFICATION_SERVICE": os.getenv("NOTIFICATION_SERVICE_URL", "http://localhost:8003"),
}

async def proxy_request(request: Request, target_url: str, path_rewrite: dict = None):
    """Generic function to proxy requests to microservices"""
    try:
        # Build target URL with path rewriting
        original_path = str(request.url.path)
        target_path = original_path
        
        if path_rewrite:
            for old_path, new_path in path_rewrite.items():
                if original_path.startswith(old_path):
                    target_path = original_path.replace(old_path, new_path, 1)
                    break
        
        full_url = f"{target_url.rstrip('/')}{target_path}"
        
        # Get request body
        body = await request.body()
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.request(
                method=request.method,
                url=full_url,
                params=request.query_params,
                content=body,
                headers={
                    key: value for key, value in request.headers.items()
                    if key.lower() not in ['host', 'content-length']
                }
            )
            
            return response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
            
    except httpx.TimeoutException:
        logger.error(f"Timeout error for {target_url}{target_path}")
        raise HTTPException(status_code=504, detail="Service timeout")
    except httpx.RequestError as e:
        logger.error(f"Request error for {target_url}: {str(e)}")
        raise HTTPException(status_code=502, detail="Service unavailable")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Dashboard ENDPOINTS
@router.get("/dashboard/metrics")
async def get_dashboard_metrics(auth: bool = Depends(authenticate_request)):
    """Get aggregated dashboard metrics from multiple services"""
    try:
        logger.info("Fetching dashboard metrics")
        
        # Mock data for now - in production, this would aggregate from multiple services
        mock_metrics = {
            "totalEquipment": 247,
            "onlineEquipment": 235,
            "activeAlerts": 23,
            "scheduledMaintenance": 18,
            "averageEfficiency": 94.2,
            "uptime": 98.5,
            "trends": {
                "efficiency": [
                    {"date": "2024-01-01T00:00:00Z", "value": 93.1},
                    {"date": "2024-01-02T00:00:00Z", "value": 94.2},
                    {"date": "2024-01-03T00:00:00Z", "value": 95.1},
                ],
                "uptime": [
                    {"date": "2024-01-01T00:00:00Z", "value": 97.8},
                    {"date": "2024-01-02T00:00:00Z", "value": 98.5},
                    {"date": "2024-01-03T00:00:00Z", "value": 98.1},
                ],
                "maintenance": [
                    {"date": "2024-01-01T00:00:00Z", "value": 15},
                    {"date": "2024-01-02T00:00:00Z", "value": 18},
                    {"date": "2024-01-03T00:00:00Z", "value": 12},
                ]
            }
        }
        
        logger.info("Dashboard metrics retrieved successfully")
        return {"success": True, "data": mock_metrics}
        
    except Exception as e:
        logger.error(f"Dashboard metrics error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch dashboard metrics")

@router.get("/dashboard/stats")
async def get_dashboard_stats(auth: bool = Depends(authenticate_request)):
    """Get dashboard stats (mock data)"""
    try:
        # Replace this with your actual data generator if available
        stats = {
            "totalEquipment": 247,
            "onlineEquipment": 235,
            "activeAlerts": 23,
            "scheduledMaintenance": 18,
            "averageEfficiency": 94.2,
            "uptime": 98.5
        }
        return {
            "success": True,
            "data": stats,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Dashboard stats error: {str(e)}")
        return {
            "success": False,
            "error": "Failed to fetch dashboard stats",
            "timestamp": datetime.utcnow().isoformat()
        }
        
        
#EQUIPEMENT ENDPOINTS

@router.get("/equipment")
async def get_equipment_list(auth: bool = Depends(authenticate_request)):
    """Get equipment list (mock data)"""
    try:
        equipment = mock_data_generator.get_equipment_list()
        return {
            "success": True,
            "data": equipment,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Equipment list error: {str(e)}")
        return {
            "success": False,
            "error": "Failed to fetch equipment list",
            "timestamp": datetime.utcnow().isoformat()
        }

@router.get("/sensors/{equipment_id}/data")
async def get_sensor_data(equipment_id: str, auth: bool = Depends(authenticate_request)):
    """Get sensor data for a specific equipment (mock data)"""
    try:
        sensor_data = mock_data_generator.generate_sensor_data(equipment_id)
        return {
            "success": True,
            "data": sensor_data,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Sensor data error for {equipment_id}: {str(e)}")
        return {
            "success": False,
            "error": "Failed to fetch sensor data",
            "timestamp": datetime.utcnow().isoformat()
        }
        
        
@router.get("/alerts/{equipment_id}")
async def get_alerts(equipment_id: str, auth: bool = Depends(authenticate_request)):
    """Get alerts for a specific equipment (mock data)"""
    try:
        alerts = mock_data_generator.generate_alerts(equipment_id)
        return {
            "success": True,
            "data": alerts,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Alerts error for {equipment_id}: {str(e)}")
        return {
            "success": False,
            "error": "Failed to fetch alerts",
            "timestamp": datetime.utcnow().isoformat()
        }

@router.get("/predictions/{equipment_id}")
async def get_predictions(equipment_id: str, auth: bool = Depends(authenticate_request)):
    """Get predictions for a specific equipment (mock data)"""
    try:
        predictions = mock_data_generator.generate_predictions(equipment_id)
        return {
            "success": True,
            "data": predictions,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Predictions error for {equipment_id}: {str(e)}")
        return {
            "success": False,
            "error": "Failed to fetch predictions",
            "timestamp": datetime.utcnow().isoformat()
        }

# Configuration endpoint
@router.get("/config")
async def get_system_config(auth: bool = Depends(authenticate_request)):
    """Get system configuration settings"""
    try:
        logger.info("Retrieving system configuration")
        
        config = {
            "aiProvider": os.getenv("AI_PROVIDER", "openai"),
            "sensorUpdateInterval": int(os.getenv("SENSOR_UPDATE_INTERVAL", "1000")),
            "alertThresholds": {
                "temperature": {"warning": 70, "critical": 85, "unit": "°C"},
                "vibration": {"warning": 5, "critical": 10, "unit": "mm/s"},
                "current": {"warning": 80, "critical": 95, "unit": "A"}
            },
            "maintenanceSchedule": {
                "preventiveInterval": 30,
                "inspectionInterval": 7,
                "emergencyResponseTime": 2
            },
            "notifications": {
                "email": True,
                "sms": False,
                "push": True
            }
        }
        
        logger.info("System configuration retrieved successfully")
        return {"success": True, "data": config}
        
    except Exception as e:
        logger.error(f"Configuration retrieval error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve configuration")

# Health check for gateway itself
@router.get("/health")
async def gateway_health():
    """Health check endpoint for the API gateway"""
    try:
        # Check connectivity to all services
        service_status = {}
        
        async with httpx.AsyncClient(timeout=5.0) as client:
            for service_name, service_url in SERVICES.items():
                try:
                    response = await client.get(f"{service_url}/health")
                    service_status[service_name.lower()] = {
                        "status": "healthy" if response.status_code == 200 else "unhealthy",
                        "response_time": response.elapsed.total_seconds()
                    }
                except:
                    service_status[service_name.lower()] = {
                        "status": "unreachable",
                        "response_time": None
                    }
        
        overall_status = "healthy" if all(
            s["status"] == "healthy" for s in service_status.values()
        ) else "degraded"
        
        logger.info(f"Gateway health check completed - Status: {overall_status}")
        
        return {
            "status": overall_status,
            "service": "api_gateway",
            "timestamp": datetime.utcnow().isoformat(),
            "services": service_status
        }
        
    except Exception as e:
        logger.error(f"Health check error: {str(e)}")
        return {
            "status": "unhealthy",
            "service": "api_gateway",
            "timestamp": datetime.utcnow().isoformat(),
            "error": str(e)
        }

logger.info("Gateway routes configured successfully")