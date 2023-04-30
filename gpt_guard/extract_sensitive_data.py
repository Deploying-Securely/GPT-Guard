import re
import spacy

nlp = spacy.load("en_core_web_sm")

def extract(text, pattern):
    return re.findall(pattern, text)

def replace(text, words_to_replace, replacement):
    pattern = re.compile(r"\b(" + "|".join(words_to_replace) + r")\b")
    return pattern.sub(replacement, text)

# Using spacy NLP library to identify potential sensitive items.
# Defaults to using the PERSON and PRODUCT entities, but this can be 
# modified using the sanitize_query function
def extract_names(text, spacy_entities):
    doc = nlp(text)
    entities = [(entity.text, entity.label_) for entity in doc.ents]
    names = [entity[0] for entity in entities if (entity[1] in spacy_entities)]
    return names

# Using regex to identify IPv4 and IPv6 addresses
def extract_ipv4_addresses(text):
    ipv4_pattern = r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"
    return extract(text, ipv4_pattern)

def extract_ipv6_addresses(text):
    ipv6_pattern = r"\b(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\b"
    return extract(text, ipv6_pattern)

# Using regex to find probable credentials
def find_credentials(text):
    words = text.split()
    result = [word for word in words if len(word) >= 8 and re.search(r'\d', word) and re.search(r'[a-zA-Z]', word) and re.search(r'\W', word)]
    return result

def replace_with_placeholders(sentence, items, tag):
    for i, item in enumerate(items):
        placeholder = f"{tag}_{i+1}"
        sentence = sentence.replace(item, placeholder)
    return sentence, items

# Allows for redaction of user-defined terms
def replace_custom_strings(sentence, custom_strings, tag):
    for i, custom_string in enumerate(custom_strings):
        placeholder = f"{tag}_{i+1}"
        sentence = sentence.replace(custom_string, placeholder)
    return sentence, custom_strings

def find_and_replace_sensitive_data(text, spacy_entities, custom_strings=[]):
    replacements = [
        ("NAME", extract_names(text, spacy_entities)),
        ("IPV4", extract_ipv4_addresses(text)),
        ("IPV6", extract_ipv6_addresses(text)),
        ("CREDENTIAL", find_credentials(text)),
    ]

    if custom_strings:
        replacements.append(("CUSTOM", custom_strings))

    sanitized_data = text
    for tag, items in replacements:
        sanitized_data, _ = replace_with_placeholders(sanitized_data, items, tag)
    return sanitized_data, replacements

def sanitize_query(query, custom_identifiers=[], spacy_entities=["PERSON", "PRODUCT"], preamble="In the following prompt, I am going remove certain information and replace each instance with sequentially-numbered placeholders in ALL CAPS (e.g. NAME_1). Ignore these placeholders and respond as if you were receiving a normal prompt. Prompt: "):
    sanitized_data_with_identifiers = find_and_replace_sensitive_data(query, custom_identifiers)
    sanitized_input = sanitized_data_with_identifiers[0]
    identifiers = sanitized_data_with_identifiers[1]
    sanitized_query = preamble + sanitized_input
    return sanitized_query, identifiers
