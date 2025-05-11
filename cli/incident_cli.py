"""
Incident Management CLI
"""
#!/usr/bin/env python3

import click
import yaml
import json
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from pathlib import Path
import os
import sys
from typing import Optional, Dict, List

console = Console()

class IncidentManager:
    def __init__(self):
        self.config_path = Path.home() / '.incident-framework'
        self.config_path.mkdir(exist_ok=True)
        self.config_file = self.config_path / 'config.yaml'
        self.load_config()

    def load_config(self):
        if not self.config_file.exists():
            self.config = {
                'nats_url': 'nats://localhost:4222',
                'elasticsearch_url': 'http://localhost:9200',
                'oncall_rotation': {},
                'teams': {}
            }
            self.save_config()
        else:
            with open(self.config_file) as f:
                self.config = yaml.safe_load(f)

    def save_config(self):
        with open(self.config_file, 'w') as f:
            yaml.dump(self.config, f)

@click.group()
def cli():
    """Incident Management Framework CLI"""
    pass

@cli.command()
@click.argument('team_name')
@click.argument('member_name')
@click.argument('email')
def add_oncall(team_name: str, member_name: str, email: str):
    """Add a team member to the on-call rotation"""
    manager = IncidentManager()
    if team_name not in manager.config['teams']:
        manager.config['teams'][team_name] = {'members': []}
    
    manager.config['teams'][team_name]['members'].append({
        'name': member_name,
        'email': email
    })
    manager.save_config()
    console.print(f"[green]Added {member_name} to {team_name}'s on-call rotation[/green]")

@cli.command()
@click.argument('incident_id')
@click.argument('title')
@click.argument('severity', type=click.Choice(['low', 'medium', 'high', 'critical']))
def create_incident(incident_id: str, title: str, severity: str):
    """Create a new incident"""
    incident = {
        'id': incident_id,
        'title': title,
        'severity': severity,
        'status': 'active',
        'created_at': datetime.now().isoformat(),
        'updates': []
    }
    
    # Save incident to file
    incidents_dir = Path.home() / '.incident-framework' / 'incidents'
    incidents_dir.mkdir(exist_ok=True)
    
    with open(incidents_dir / f"{incident_id}.yaml", 'w') as f:
        yaml.dump(incident, f)
    
    console.print(Panel(f"[bold green]Created incident {incident_id}[/bold green]\n"
                       f"Title: {title}\n"
                       f"Severity: {severity}"))

@cli.command()
@click.argument('incident_id')
def get_incident(incident_id: str):
    """Get incident details"""
    incident_file = Path.home() / '.incident-framework' / 'incidents' / f"{incident_id}.yaml"
    if not incident_file.exists():
        console.print(f"[red]Incident {incident_id} not found[/red]")
        return
    
    with open(incident_file) as f:
        incident = yaml.safe_load(f)
    
    table = Table(title=f"Incident {incident_id}")
    table.add_column("Field", style="cyan")
    table.add_column("Value", style="green")
    
    for key, value in incident.items():
        if key != 'updates':
            table.add_row(key, str(value))
    
    console.print(table)

@cli.command()
@click.argument('incident_id')
@click.argument('update')
def update_incident(incident_id: str, update: str):
    """Add an update to an incident"""
    incident_file = Path.home() / '.incident-framework' / 'incidents' / f"{incident_id}.yaml"
    if not incident_file.exists():
        console.print(f"[red]Incident {incident_id} not found[/red]")
        return
    
    with open(incident_file) as f:
        incident = yaml.safe_load(f)
    
    incident['updates'].append({
        'timestamp': datetime.now().isoformat(),
        'message': update
    })
    
    with open(incident_file, 'w') as f:
        yaml.dump(incident, f)
    
    console.print(f"[green]Added update to incident {incident_id}[/green]")

@cli.command()
@click.argument('incident_id')
def generate_postmortem(incident_id: str):
    """Generate a post-mortem report for an incident"""
    incident_file = Path.home() / '.incident-framework' / 'incidents' / f"{incident_id}.yaml"
    if not incident_file.exists():
        console.print(f"[red]Incident {incident_id} not found[/red]")
        return
    
    with open(incident_file) as f:
        incident = yaml.safe_load(f)
    
    postmortem_dir = Path.home() / '.incident-framework' / 'postmortems'
    postmortem_dir.mkdir(exist_ok=True)
    
    postmortem = {
        'incident_id': incident_id,
        'title': incident['title'],
        'severity': incident['severity'],
        'start_time': incident['created_at'],
        'end_time': datetime.now().isoformat(),
        'timeline': incident['updates'],
        'impact': 'To be filled',
        'root_cause': 'To be filled',
        'action_items': []
    }
    
    postmortem_file = postmortem_dir / f"{incident_id}_postmortem.yaml"
    with open(postmortem_file, 'w') as f:
        yaml.dump(postmortem, f)
    
    console.print(f"[green]Generated post-mortem template for incident {incident_id}[/green]")
    console.print(f"Please edit {postmortem_file} to complete the post-mortem")

if __name__ == '__main__':
    cli() 