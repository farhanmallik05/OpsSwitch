# OpsSwitch Task Runner recipes

default:
    @just --list

# Run automated end-to-end incident simulation
simulate:
    python scripts/simulate_incident.py --auto-approve

# Run the 7-pillar pytest integration suite
test:
    pytest tests/test_incident_flow.py -v

# Run the mock Cart & Checkout service standalone server
serve:
    python scripts/simulate_incident.py --mode serve --port 8000

# Run the simulation in interactive mode with human sign-off prompt
interactive:
    python scripts/simulate_incident.py --mode interactive
