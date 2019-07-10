from scose_utilities import *

# Data source and output paths
archive_dir = "scose_archive/"
data_dir = "scose_data/json"

# Excluded characters for ignoring i.e. '=='
excluded_chars = {'<', '>', '-', '#', '&', '|', '=', '@', '', '[', ']'}
strip_chars = [':', '⌊', '⌋', '⌈', '⌉', '“', '”', '"', '(', ')', '◉']

# Get a list of all the dialogues
dialogue_list = os.listdir(archive_dir)

dialogue_data = dict()
dialogues = []
num_dialogues = 0

for file_name in dialogue_list:

    # Load the file data
    file_data = load_text_data(archive_dir + file_name)

    # Process each dialogue
    dialogue = process_dialogue(file_data, file_name, excluded_chars, strip_chars)

    # Append to set
    num_dialogues += 1
    dialogues.append(dialogue)

# Add dataset metadata
dialogue_data['dataset'] = "scose"
dialogue_data['num_dialogues'] = num_dialogues
dialogue_data['dialogues'] = dialogues

# Save to JSON file
save_json_data(data_dir, dialogue_data['dataset'], dialogue_data)