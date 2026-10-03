import yaml
import os
import sys
import api_client
import monitor
import time
import notifier
from datetime import datetime

# Загрузка настроек из файла конфигурации
def load_config(config_path: str) -> dict:

    if not os.path.exists(config_path):
        print(f"❌ ERROR: Config file not found at {config_path}")
        sys.exit(1)

    with open(config_path, 'r', encoding='utf-8') as file:
        try:
           config = yaml.safe_load(file)
           return config
        except yaml.YAMLError as exc:
            print(f"❌ ERROR: Error occured while parsing YAML file: {exc}")
            sys.exit(1)

if __name__ == "__main__":
    base_dir =  os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_file = os.path.join(base_dir, 'config', 'conf.yaml')
    triggered_alerts = set()
    print(f"Loading configuration from: {config_file}")
    app_config = load_config(config_file)
    
    # Проверяем загрузку конфига
    """
    print(f"/n --- Loaded Config ---")
    print(f"Coins to monitor: {len(app_config['monitoring']['coins'])}")
    for coin in app_config['monitoring']['coins']:
        print(f" - {coin['id']}: Target ${coin['target_usd']} - {coin['condition']}")
    print(f"Ntfy topic: {app_config['ntfy']['topic']}")
    print("---------------------")
    """
    interval = app_config['settings']['check_interval_seconds']
    server_url = app_config['ntfy']['server_url']
    topic = app_config['ntfy']['topic']
    token = app_config['ntfy']['token']
    unsended_alerts = []
    print(f"[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] 🚩 SUCCESSFUL START")
    
    while True:
        coin_data = api_client.fetch_prices([item["id"] for item in app_config['monitoring']['coins']])
        list_alerts = monitor.evaluate_alerts(coin_data, app_config['monitoring']['coins'], triggered_alerts)
        list_alerts.extend(unsended_alerts)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if list_alerts:  
            print(f"[{timestamp}] 🚨 ALERTS TRIGGERED:")
            for alert in list_alerts:
                
                print(f"-> {alert}")
                response = notifier.send_ntfy_notification(server_url,topic,token,alert)
                
                if response:
                    print(f"[{timestamp}] 🚀 SUCCESS: [{alert}] was sended to ntfy!")
                    
                    if alert in unsended_alerts:
                        unsended_alerts.remove[alert]
                
                else:
                    print(f"[{timestamp}] ⚠️ WARNING: [{alert}] was not sended to ntfy!")
                    unsended_alerts.append(alert)
        #else:
            #print(f"[{timestamp}] 🛈 No alerts. Nothing to send.")

        time.sleep(interval)

