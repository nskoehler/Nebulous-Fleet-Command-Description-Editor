#Export Module: Adds miscellaneous features to the final export to ensure compatibility with the game.

#Function: Add <description> and </description> to the beginning and end of exported text.

# Retrieve user input from main editor
# Analyze user input
# Modify text to string "<description>UserInput</description>"
# Return modified text directly to output

def export_description(text):
    """
    Wraps the text in <description> tags, each on its own line.
    """
    return f"<Description>\n{text}\n</Description>"