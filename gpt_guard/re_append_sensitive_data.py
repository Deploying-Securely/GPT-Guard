def replace_placeholders_with_items(sentence, items, tag):
    for i, item in enumerate(items):
        placeholder = f"{tag}_{i+1}"
        sentence = sentence.replace(placeholder, item)
    return sentence

# Takes the output of the response and a list of the removed items and returns the unredacted response
def re_append_sensitive_data(gpt_output, removed_sanitized_data):
    result = gpt_output
    for tag, items in removed_sanitized_data:
        result = replace_placeholders_with_items(result, items, tag)
    return result
