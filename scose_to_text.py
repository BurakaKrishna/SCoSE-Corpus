from scose_utilities import *

# Data source and output paths
archive_dir = "scose_archive/"
data_dir = "scose_data/text"

# If flag is set will only write utterances and not speaker
utterance_only_flag = False

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

    # Write to text file
    dialogue_to_text_file(data_dir, dialogue['dialogue_id'], dialogue, utterance_only_flag)

