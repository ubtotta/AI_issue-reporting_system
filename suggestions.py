# suggestions.py
def get_suggestion(issue_type):
    if issue_type == 'fan':
        return "Fan not working", "Check power supply or replace capacitor"
    elif issue_type == 'ac':
        return "AC issue", "Check compressor or coolant level"
    elif issue_type == 'wall_leakage':
        return "Wall leakage", "Inspect plumbing and seal cracks"
    else:
        return "Unknown", "No suggestion available"
