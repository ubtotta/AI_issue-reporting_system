def get_suggestion(label):
    suggestions = {
        'fan': ("Fan not working or making noise", "Please check the wiring or motor issue"),
        'ac': ("Air conditioner issue", "Clean the filters or check gas level"),
        'wall_leakage': ("Wall leakage detected", "Seal cracks and check for broken pipes")
    }
    return suggestions.get(label, ("Unknown issue", "Please inspect manually"))
