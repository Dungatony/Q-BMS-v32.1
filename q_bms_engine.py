import yaml
import logging

# Cấu hình logging để AI/Nhà nghiên cứu dễ trace log
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("QBMS_Engine")

class QBMSController:
    def __init__(self, config_path="config.yaml"):
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)
        logger.info(f"System {self.config['system_name']} initialized.")

    def system_state_vote(self, s1, s2, s3):
        """
        Triple Modular Redundancy (TMR) Logic.
        Đảm bảo hệ thống vẫn an toàn ngay cả khi 1 cảm biến bị lỗi.
        """
        if s1 == s2 == s3: return s1
        elif s1 == s2: return s1
        elif s1 == s3: return s1
        elif s2 == s3: return s2
        else:
            logger.critical("TMR Voting Failure: Inconsistent sensor data.")
            return "CRITICAL_ERROR"

    def safety_check(self, current_temp, current_activity):
        """
        Kiểm tra trạng thái an toàn dựa trên file config.
        """
        thresholds = self.config['safety_thresholds']
        reactor = self.config['reactor_settings']

        if current_temp > reactor['operating_temp_celsius']['critical_threshold']:
            return "EMERGENCY_QUENCH"
        
        if current_activity > thresholds['max_effluent_activity_bq_l']:
            return "CONTAINMENT_BREACH"
            
        return "OPERATIONAL"

# --- MÔ PHỎNG VẬN HÀNH ---
if __name__ == "__main__":
    # Khởi tạo hệ thống
    engine = QBMSController()
    
    # Giả lập dữ liệu từ 3 cảm biến
    sensor_data = [1120, 1120, 1121] 
    
    # Thực hiện bỏ phiếu
    result = engine.system_state_vote(*sensor_data)
    
    # Kiểm tra an toàn
    status = engine.safety_check(current_temp=result, current_activity=0.02)
    
    print(f"System Status: {status} | Voted Temp: {result}°C")
