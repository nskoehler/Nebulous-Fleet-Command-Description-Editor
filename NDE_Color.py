#Color Module: Handles color selection and conversion for the editor.

#Function: analyzes text, inserts &lt;color=#____&gt; and &lt;/color&gt; tags around text based on grouped strings of inputs.

# Retrieve user input from main editor
# Analyze user input
# if the user specifies a default color, apply it in terms of the name of the color instead of the hex code
# else, Insert &lt;color=#____&gt; and &lt;/color&gt; tags around strings of text that should be colored
# Send modified text to NDE Export

def apply_color_tags(text, color_info, default_color="#000000"):
    """
    text: the string to process
    color_info: a list of tuples (start_idx, end_idx, color_hex)
    default_color: the default color (do not output color tags for this)
    Returns: string with <color=#XXXXXX>...</color> tags applied only for non-default colors
    """
    result = ""
    last_idx = 0
    for start, end, color in color_info:
        # Add any text before this segment
        if start > last_idx:
            result += text[last_idx:start]
        segment = text[start:end]
        if color.lower() == default_color.lower():
            result += segment
        else:
            result += f"&lt;color={color}&gt;{segment}&lt;/color&gt;"
        last_idx = end
    # Add any remaining text
    if last_idx < len(text):
        result += text[last_idx:]
    return result