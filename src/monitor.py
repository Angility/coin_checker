def evaluate_alerts(coin_data: dict, coin_list: list[dict], triggered_alerts: set) -> list:

    list_alerts = []
    for current_coin in coin_list:
        if current_coin['id'] in coin_data:

            target = current_coin['target_usd']
            price_now = coin_data[current_coin['id']]
            condition = current_coin['condition']
            
            if  (target >= price_now and condition == 'below') or (target <= price_now and condition == 'above'):
                alert_text = f"{'BUY' if condition == 'below' else 'SELL'} SIGNAL - {current_coin['tik']} is {current_coin['condition']} target! Current: ${price_now:,.5f}, Target: ${target:,.5f}"
                alert = f"{current_coin['tik']}_{current_coin['condition']}_${target}"
                
                if alert not in triggered_alerts:
                    list_alerts.append(alert_text)
                    triggered_alerts.add(alert)
            
    return list_alerts

