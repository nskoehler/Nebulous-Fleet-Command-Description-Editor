#Typograph Module: Handles Italics and Bold text formatting.

#Function: analyzes text, inserts &lt;i&gt; and &lt;/i&gt; tags for italics, and &lt;b&gt; and &lt;/b&gt; tags for bold text based on grouped strings of inputs.

# Retrieve user input from main editor
# Analyze user input
# Insert &lt;i&gt; and &lt;/i&gt; tags around strings of text that should be italicized
# Insert &lt;b&gt; and &lt;/b&gt; tags around strings of text that should be bold
# Send modified text to NDE Export

def apply_typograph_tags(text, style_info):
    """
    text: the string to process
    style_info: a list of tuples (start_idx, end_idx, is_bold, is_italic)
    Returns: string with <b>...</b> and <i>...</i> tags applied
    """
    result = ""
    last_idx = 0
    for start, end, bold, italic in style_info:
        # Add any text before this segment
        if start > last_idx:
            result += text[last_idx:start]
        segment = text[start:end]
        if bold and italic:
            result += f"&lt;b&gt;&lt;i&gt;{segment}&lt;/i&gt;&lt;/b&gt;"
        elif bold:
            result += f"&lt;b&gt;{segment}&lt;/b&gt;"
        elif italic:
            result += f"&lt;i&gt;{segment}&lt;/i&gt;"
        else:
            result += segment
        last_idx = end
    # Add any remaining text
    if last_idx < len(text):
        result += text[last_idx:]
    return result