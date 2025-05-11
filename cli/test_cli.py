import subprocess

def test_create_incident():
    result = subprocess.run([
        'python', 'incident_cli.py', 'create-incident', 'test-1', 'Test Incident', 'low'
    ], cwd='.', capture_output=True, text=True)
    assert 'Created incident test-1' in result.stdout 