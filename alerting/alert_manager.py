#!/usr/bin/env python3

import asyncio
import json
import nats
from datetime import datetime
from typing import Dict, List, Optional
import logging
from pathlib import Path
import yaml

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AlertManager:
    def __init__(self, nats_url: str = "nats://localhost:4222"):
        self.nats_url = nats_url
        self.nc = None
        self.subscriptions = {}
        self.alert_rules = self._load_alert_rules()

    def _load_alert_rules(self) -> Dict:
        rules_file = Path(__file__).parent / 'alert_rules.yaml'
        if not rules_file.exists():
            return {}
        with open(rules_file) as f:
            return yaml.safe_load(f)

    async def connect(self):
        """Connect to NATS server"""
        try:
            self.nc = await nats.connect(self.nats_url)
            logger.info(f"Connected to NATS server at {self.nats_url}")
        except Exception as e:
            logger.error(f"Failed to connect to NATS server: {e}")
            raise

    async def subscribe_to_alerts(self, subject: str, callback):
        """Subscribe to alerts on a specific subject"""
        if not self.nc:
            await self.connect()
        
        sub = await self.nc.subscribe(subject, cb=callback)
        self.subscriptions[subject] = sub
        logger.info(f"Subscribed to alerts on subject: {subject}")

    async def publish_alert(self, subject: str, alert_data: Dict):
        """Publish an alert to a specific subject"""
        if not self.nc:
            await self.connect()
        
        alert_data['timestamp'] = datetime.now().isoformat()
        await self.nc.publish(subject, json.dumps(alert_data).encode())
        logger.info(f"Published alert to {subject}: {alert_data}")

    async def process_alert(self, msg):
        """Process incoming alerts"""
        try:
            alert_data = json.loads(msg.data.decode())
            logger.info(f"Received alert: {alert_data}")
            
            # Apply alert rules
            for rule in self.alert_rules.get('rules', []):
                if self._matches_rule(alert_data, rule):
                    await self._execute_rule_actions(rule, alert_data)
        
        except json.JSONDecodeError:
            logger.error(f"Failed to decode alert message: {msg.data}")
        except Exception as e:
            logger.error(f"Error processing alert: {e}")

    def _matches_rule(self, alert_data: Dict, rule: Dict) -> bool:
        """Check if an alert matches a rule"""
        for condition in rule.get('conditions', []):
            field = condition.get('field')
            operator = condition.get('operator')
            value = condition.get('value')
            
            if field not in alert_data:
                return False
            
            alert_value = alert_data[field]
            
            if operator == 'equals' and alert_value != value:
                return False
            elif operator == 'contains' and value not in alert_value:
                return False
            elif operator == 'greater_than' and alert_value <= value:
                return False
            elif operator == 'less_than' and alert_value >= value:
                return False
        
        return True

    async def _execute_rule_actions(self, rule: Dict, alert_data: Dict):
        """Execute actions for a matched rule"""
        for action in rule.get('actions', []):
            action_type = action.get('type')
            
            if action_type == 'notify':
                await self._send_notification(action, alert_data)
            elif action_type == 'escalate':
                await self._escalate_alert(action, alert_data)
            elif action_type == 'create_incident':
                await self._create_incident(action, alert_data)

    async def _send_notification(self, action: Dict, alert_data: Dict):
        """Send notification for an alert"""
        channel = action.get('channel', 'slack')
        message = action.get('message', f"Alert: {alert_data}")
        # For demo, just log. In real use, integrate with Slack API.
        logger.info(f"[NOTIFY] Channel: {channel} | Message: {message}")

    async def _escalate_alert(self, action: Dict, alert_data: Dict):
        """Escalate an alert"""
        # Implement escalation logic
        logger.info(f"Escalating alert: {alert_data}")

    async def _create_incident(self, action: Dict, alert_data: Dict):
        """Create an incident from an alert"""
        # Write incident to a shared YAML file (for demo purposes)
        incident_id = f"auto-{int(datetime.now().timestamp())}"
        incident = {
            'id': incident_id,
            'title': action.get('title', 'Auto-generated Incident'),
            'severity': action.get('severity', 'high'),
            'status': 'active',
            'created_at': datetime.now().isoformat(),
            'updates': [
                {'timestamp': datetime.now().isoformat(), 'message': f"Incident created from alert: {alert_data}"}
            ]
        }
        incidents_dir = Path.home() / '.incident-framework' / 'incidents'
        incidents_dir.mkdir(exist_ok=True)
        with open(incidents_dir / f"{incident_id}.yaml", 'w') as f:
            yaml.dump(incident, f)
        logger.info(f"Created incident {incident_id} from alert: {alert_data}")

    async def close(self):
        """Close NATS connection"""
        if self.nc:
            await self.nc.close()
            logger.info("Closed NATS connection")

async def main():
    alert_manager = AlertManager()
    await alert_manager.connect()
    
    # Subscribe to alerts
    await alert_manager.subscribe_to_alerts("alerts.>", alert_manager.process_alert)
    
    try:
        # Keep the connection alive
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        await alert_manager.close()

if __name__ == "__main__":
    asyncio.run(main()) 