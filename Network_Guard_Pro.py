#!/usr/bin/env python3
# Network Guard Pro v2.0 - Final Clean Version
import os
import time
import subprocess
import logging
import collections
import re
from datetime import datetime

class ARPSpoofingDetector:
    def __init__(self):
        self.router_mac = None
        self.gateway_ip = self.detect_gateway()
        print(f"[SYSTEM] Gateway detected: {self.gateway_ip} - Network_Guard_Pro.py:15")
    
    def detect_gateway(self):
        """Detect default gateway"""
        try:
            result = subprocess.run(['route', 'print', '0.0.0.0'], 
                                 capture_output=True, text=True, encoding='cp866')
            for line in result.stdout.split('\n'):
                if '0.0.0.0' in line and '255.255.255.255' not in line:
                    parts = line.split()
                    if len(parts) > 2:
                        return parts[2]
        except Exception as e:
            print(f"[ERROR] Gateway detection failed: {e} - Network_Guard_Pro.py:28")
        return '192.168.1.1'
    
    def detect_spoofing(self, current_arp):
        """Detect ARP spoofing attacks"""
        alerts = []
        
        # Check for MAC duplication
        ip_per_mac = {}
        for ip, mac in current_arp.items():
            if mac in ip_per_mac:
                ip_per_mac[mac].append(ip)
            else:
                ip_per_mac[mac] = [ip]
        
        for mac, ips in ip_per_mac.items():
            if len(ips) > 1:
                alerts.append(("spoof", f"Duplicate MAC {mac} for {len(ips)} IPs"))
        
        # Monitor gateway changes
        if self.gateway_ip in current_arp:
            current_mac = current_arp[self.gateway_ip]
            if self.router_mac and self.router_mac != current_mac:
                alerts.append(("critical", "Gateway MAC changed - ARP Spoofing detected!"))
            self.router_mac = current_mac
        
        return alerts

class NetworkScanDetector:
    def detect_scans(self, arp_history):
        """Detect network scans"""
        alerts = []
        current_time = datetime.now()
        
        for ip, history in arp_history.items():
            recent = [h for h in history if (current_time - h[0]).total_seconds() <= 15]
            if len(recent) >= 8:
                alerts.append(("scan", f"Network scan from {ip}"))
        
        return alerts

class BehavioralMonitor:
    def __init__(self):
        self.device_history = []
    
    def detect_anomalies(self, current_arp):
        """Detect behavioral anomalies"""
        anomalies = []
        device_count = len(current_arp)
        
        self.device_history.append(device_count)
        if len(self.device_history) > 10:
            self.device_history = self.device_history[-10:]
        
        if len(self.device_history) > 1:
            avg_devices = sum(self.device_history) / len(self.device_history)
            if device_count > avg_devices * 1.5:
                anomalies.append(f"Device spike: {device_count} (average: {avg_devices:.1f})")
        
        return anomalies

class NetworkGuardPro:
    def __init__(self):
        self.known_devices = {}
        self.arp_history = collections.defaultdict(list)
        self.scan_count = 0
        self.spoof_count = 0
        self.alert_count = 0
        
        self.spoof_detector = ARPSpoofingDetector()
        self.scan_detector = NetworkScanDetector()
        self.behavior_monitor = BehavioralMonitor()
        
        self.setup_logging()
        self.show_welcome()
    
    def show_welcome(self):
        """Show welcome message without encoding issues"""
        print("\nNETWORK GUARD PRO v2.0 - Network_Guard_Pro.py:106")
        print("")
        print("Protection System: ACTIVE - Network_Guard_Pro.py:108")
        print("")
    
    def setup_logging(self):
        """Setup logging system"""
        log_dir = os.path.expanduser("~\\Desktop\\NetworkGuard_Logs")
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        logging.basicConfig(
            filename=os.path.join(log_dir, 'security.log'),
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        print(f"[INFO] Logs directory: {log_dir} - Network_Guard_Pro.py:122")
    
    def get_arp_table(self):
        """Get current ARP table"""
        arp_table = {}
        try:
            result = subprocess.run(['arp', '-a'], capture_output=True, text=True, encoding='cp866')
            for line in result.stdout.split('\n'):
                if 'dynamic' in line.lower():
                    parts = line.split()
                    if len(parts) >= 2:
                        ip, mac = parts[0], parts[1].upper()
                        if ip and mac and mac != 'FF-FF-FF-FF-FF-FF':
                            arp_table[ip] = mac
            return arp_table
        except Exception as e:
            print(f"[ERROR] Cannot read ARP table: {e} - Network_Guard_Pro.py:138")
            return {}
    
    def show_alert(self, message, alert_type="ALERT"):
        """Show alert with notification"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"[{timestamp}] {alert_type}: {message} - Network_Guard_Pro.py:144")
        
        # Try desktop notification
        try:
            from plyer import notification
            notification.notify(
                title=f"Network Guard - {alert_type}",
                message=message,
                timeout=8,
                app_name="Network Guard Pro"
            )
        except:
            pass
    
    def show_stats(self, current_arp):
        """Show current statistics"""
        print(f"[STATUS] Devices: {len(current_arp)} | Scans: {self.scan_count} | Attacks: {self.spoof_count} | Alerts: {self.alert_count} - Network_Guard_Pro.py:160")
    
    def start_protection(self):
        """Start network protection"""
        # Initial scan
        initial_devices = self.get_arp_table()
        print(f"[SCAN] Monitoring {len(initial_devices)} network devices - Network_Guard_Pro.py:166")
        print("[SYSTEM] Realtime protection activated - Network_Guard_Pro.py:167")
        print("Press CTRL+C to stop\n - Network_Guard_Pro.py:168")
        
        cycle = 0
        try:
            while True:
                cycle += 1
                current_arp = self.get_arp_table()
                
                # Update device history
                for ip, mac in current_arp.items():
                    self.arp_history[ip].append((datetime.now(), mac))
                    if len(self.arp_history[ip]) > 15:
                        self.arp_history[ip] = self.arp_history[ip][-15:]
                
                # Run security checks
                scan_alerts = self.scan_detector.detect_scans(self.arp_history)
                spoof_alerts = self.spoof_detector.detect_spoofing(current_arp)
                behavior_alerts = self.behavior_monitor.detect_anomalies(current_arp)
                
                # Process all alerts
                all_alerts = scan_alerts + spoof_alerts
                
                for alert_type, alert_msg in all_alerts:
                    self.alert_count += 1
                    if alert_type == "scan":
                        self.scan_count += 1
                        self.show_alert(alert_msg, "SCAN DETECTED")
                    elif alert_type == "spoof":
                        self.spoof_count += 1
                        self.show_alert(alert_msg, "ARP SPOOFING")
                    elif alert_type == "critical":
                        self.spoof_count += 1
                        self.show_alert(alert_msg, "CRITICAL ATTACK")
                
                # Show behavior anomalies
                for behavior_alert in behavior_alerts:
                    self.show_alert(behavior_alert, "BEHAVIOR ALERT")
                
                # Show stats every 10 cycles
                if cycle % 10 == 0:
                    self.show_stats(current_arp)
                
                time.sleep(3)  # Check every 3 seconds
                
        except KeyboardInterrupt:
            self.show_final_report()
    
    def show_final_report(self):
        """Show final protection report"""
        print("\n - Network_Guard_Pro.py:217" + "PROTECTION REPORT")
        print("======================== - Network_Guard_Pro.py:218")
        print(f"Scan Detections: {self.scan_count} - Network_Guard_Pro.py:219")
        print(f"ARP Attack Detections: {self.spoof_count} - Network_Guard_Pro.py:220")
        print(f"Total Security Alerts: {self.alert_count} - Network_Guard_Pro.py:221")
        print("======================== - Network_Guard_Pro.py:222")
        print("Network Guard Pro stopped - Network_Guard_Pro.py:223")

# Main execution
if __name__ == "__main__":
    try:
        print("[SYSTEM] Starting Network Guard Pro... - Network_Guard_Pro.py:228")
        guard = NetworkGuardPro()
        guard.start_protection()
    except Exception as e:
        print(f"[FATAL] System error: {e} - Network_Guard_Pro.py:232")