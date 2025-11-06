🛡️ Network Guard Pro - Advanced Network Monitoring System
=========================================================

📖 Description:
Network Guard Pro is a comprehensive security system for detecting ARP Spoofing attacks and network scans in real-time. Written in Python and designed for Windows systems.

🎯 Features:
=============
✅ ARP Spoofing attack detection (arpspoof, ettercap)
✅ Network scan detection (netdiscover, nmap, masscan)
✅ Behavioral network monitoring
✅ Instant Windows desktop notifications
✅ Detailed security logging
✅ User-friendly interface

🚀 System Requirements:
=======================
- Windows 10/11
- Python 3.7 or newer
- Administrator privileges

📥 Installation:
================
1. Install Python from python.org (select "Add to PATH")
2. Open Command Prompt as Administrator
3. Install required libraries:
   pip install plyer
4. Save Network_Guard_Pro.py in a suitable folder

▶️ Running the Application:
===========================
Method 1: Double-click Start_Network_Guard.bat
Method 2: Open Command Prompt and run:
   python Network_Guard_Pro.py

📊 System Outputs:
==================
📁 Logs: NetworkGuard_Logs folder on Desktop
🔔 Notifications: Automatic Windows notifications
📝 Reports: Live reports in command window

🎯 Alert Types:
===============
🔍 SCAN DETECTED    - Network scan detected
🚨 ARP SPOOFING     - ARP spoofing attack
💀 CRITICAL ATTACK  - Critical security attack
⚠️ BEHAVIOR ALERT   - Abnormal network activity

🧪 System Testing:
==================
To test scan detection:
   netdiscover -i eth0 -r 192.168.1.0/24

To test ARP Spoofing detection:
   arpspoof -i eth0 -t 192.168.1.100 192.168.1.1

⚙️ Default Settings:
====================
- Scanning interval: 3 seconds
- History: Last 15 changes per device
- Detection threshold: 8 changes in 15 seconds

📞 Support:
===========
If you encounter issues:
1. Verify Python and library installation
2. Run as Administrator
3. Check log files in Desktop/NetworkGuard_Logs/

⚠️ Important Notes:
===================
- For educational and security purposes only
- User is responsible for legal usage
- Recommended to test in controlled environments first

🔄 Version Information:
=======================
Version: 2.0
Release Date: 2024
Developer: Network Security Team

=========================================================
🛡️ Keep Your Network Secure with Network Guard Pro!
=========================================================