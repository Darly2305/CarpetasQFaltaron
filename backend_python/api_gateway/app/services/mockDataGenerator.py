from datetime import datetime
import random

class MockDataGenerator:
    def __init__(self):
        self.equipment_list = [
            {
                "id": "KONE-ELV-001",
                "type": "elevator",
                "model": "MonoSpace 500",
                "location": "Building A - Tower 1",
                "status": "active",
                "installDate": datetime(2020, 1, 15),
                "sensors": [
                    {"type": "position", "parameter": "car_position", "model": "AS5600", "samplingRate": 100},
                    {"type": "temperature", "parameter": "motor_temperature", "model": "DS18B20", "samplingRate": 10},
                    {"type": "vibration", "parameter": "bearing_vibration", "model": "MPU6050", "samplingRate": 50}
                ]
            }
        ]

    def generate_sensor_data(self, equipment_id: str):
        equipment = next((eq for eq in self.equipment_list if eq["id"] == equipment_id), None)
        if not equipment:
            return []
        return [
            {
                "id": f"{equipment_id}-{sensor['parameter']}-{int(datetime.utcnow().timestamp() * 1000)}",
                "equipmentId": equipment_id,
                "sensorType": sensor["type"],
                "parameter": sensor["parameter"],
                "value": self.generate_sensor_value(sensor["parameter"]),
                "unit": self.get_sensor_unit(sensor["parameter"]),
                "timestamp": datetime.utcnow().isoformat(),
                "status": "active",
                "threshold": self.get_sensor_threshold(sensor["parameter"]),
                "location": equipment["location"]
            }
            for sensor in equipment["sensors"]
        ]

    def generate_alerts(self, equipment_id: str):
        if random.random() > 0.7:
            return [{
                "id": f"alert-{equipment_id}-{int(datetime.utcnow().timestamp() * 1000)}",
                "equipmentId": equipment_id,
                "type": "warning",
                "title": "Motor Temperature High",
                "message": "Motor temperature exceeds normal range",
                "parameter": "motor_temperature",
                "value": 58,
                "threshold": 55,
                "timestamp": datetime.utcnow().isoformat(),
                "status": "active",
                "priority": "medium"
            }]
        return []

    def generate_predictions(self, equipment_id: str):
        return [{
            "equipmentId": equipment_id,
            "parameter": "motor_temperature",
            "prediction": "normal",
            "confidence": 0.85,
            "timestamp": datetime.utcnow().isoformat(),
            "modelVersion": "1.0.0"
        }]

    def generate_dashboard_stats(self):
        return {
            "totalElevators": 247,
            "activeAlerts": 23,
            "averageEfficiency": 94.2,
            "dailyTasks": 18,
            "trends": {
                "elevators": 12,
                "alerts": 5,
                "efficiency": 2.3,
                "tasks": 15
            }
        }

    def get_equipment_list(self):
        return self.equipment_list

    def generate_sensor_value(self, parameter: str):
        values = {
            "car_position": 50,
            "motor_temperature": 45 + random.random() * 15,
            "bearing_vibration": 2.5 + random.random() * 1.5
        }
        return values.get(parameter, 50)

    def get_sensor_unit(self, parameter: str):
        units = {
            "car_position": "m",
            "motor_temperature": "°C",
            "bearing_vibration": "mm/s"
        }
        return units.get(parameter, "unit")

    def get_sensor_threshold(self, parameter: str):
        thresholds = {
            "motor_temperature": {"warning": 55, "critical": 70},
            "bearing_vibration": {"warning": 4.0, "critical": 6.0}
        }
        return thresholds.get(parameter)

# Usage example:
# mock_data_generator = MockDataGenerator()
# equipment = mock_data_generator.get_equipment_list()