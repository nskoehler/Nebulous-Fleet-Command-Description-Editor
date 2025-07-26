#Size Module: Manages text size translation.

#Function: analyzes text, inserts &lt;size=___%&gt; and &lt;/size&gt; tags around text based on grouped strings of inputs.

# Retrieve user input from main editor
# Analyze user input
# Run calculation: Divide user font size by default font size to get percentage. (Default can be set by the user)
# if the percentage is exactly 100%, do not apply size tags.
# elif the user manually overrides to include a uniform forced percentage, set size tags regardless of actual font size.
# else, Modify text to include &lt;size=___%&gt; and &lt;/size&gt; tags around text
# Send modified text to NDE Export

def apply_size_tags(text, font_info, default_size=12, force_percentage=None):
    """
    text: the string to process
    font_info: a list of tuples (start_idx, end_idx, font_size)
    default_size: the default font size to compare against
    force_percentage: if set, applies this percentage to all text regardless of actual size
    Returns: string with <size=XX%>...</size> tags applied where needed
    """
    result = ""
    last_idx = 0
    for start, end, size in font_info:
        # Add any text before this segment
        if start > last_idx:
            result += text[last_idx:start]
        segment = text[start:end]
        if force_percentage is not None:
            percent = force_percentage
        else:
            percent = int(round(size / default_size * 100))
        if percent == 100:
            result += segment
        else:
            result += f"&lt;size={percent}%&gt;{segment}&lt;/size&gt;"
        last_idx = end
    # Add any remaining text
    if last_idx < len(text):
        result += text[last_idx:]
    return result