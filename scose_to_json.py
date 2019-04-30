import os
import re
from scose_utilities import *
import spacy
from spacy.tokenizer import Tokenizer
nlp = spacy.load('en')
tokenizer = Tokenizer(nlp.vocab)

# Data source and output paths
archive_dir = "scose_archive/"
data_dir = "scose_data/"

# Excluded characters for ignoring i.e. '=='
excluded_chars = {'<', '>', '-', '#', '|', '=', '@', '', '[', ']'}
strip_chars = [':', '⌊', '⌋', '⌈', '⌉', '“', '”', '"', '(', ')', '◉']

# Get a list of all the tasks
dialogue_list = os.listdir(archive_dir)

dialogue_data = dict()
dialogues = []
num_dialogues = 0

for file_name in dialogue_list:

    # Load the file data
    file_data = load_data(archive_dir + file_name)

    # Get the file name
    file_name = file_name.split('.')[0]

    tmp_utterances = []
    for line in file_data:

        # Ignore non-dialogue lines that start with @ or %
        if line[0] is '@' or line[0] is '%':
            continue

        # Split on tab to get the speaker and text
        line = line.split('\t')
        speaker = re.sub('[*:]', '', line[0])
        text = line[1].strip()

        # Tokenise text
        utterance_tokens = tokenizer(text)

        # Remove the word annotations and filter disfluency
        utterance_text = []
        for word in utterance_tokens:
            word = word.text

            # If no excluded characters are present just add it
            if all(char not in excluded_chars for char in word) and not  any(char.isdigit() for char in word):

                if any(char in strip_chars for char in word):
                    word = re.sub('[:⌊⌋⌈⌉“”"◉()]', '', word)

                utterance_text.append(word)

        # Create utterances
        utterance = dict()
        # Set speaker
        utterance['speaker'] = speaker
        # Set the utterance text
        utterance['text'] = utterance_text
        # Set labels to empty
        utterance['ap_label'] = ""
        utterance['da_label'] = ""
        # Add empty slots data
        utterance['slots'] = dict()

        # Add to utterances
        tmp_utterances.append(utterance)

    # Concatenate multi-utterance's with '+'
    tmp_utt = None
    for utt in reversed(tmp_utterances):

        # If we find an utterance that must be concatenated
        if len(utt['text']) > 0 and any(char in ['+'] for char in utt['text'][0]):
            # Save to temp and delete from list
            tmp_utt = utt
            tmp_utterances.remove(utt)

        # Else if we have one then concatenate
        elif tmp_utt and tmp_utt['speaker'] == utt['speaker']:
            # print("Concatenating '", utt['text'], "' + '", tmp_utt['text'], "'")
            utt['text'] = utt['text'] + tmp_utt['text']
            tmp_utt = None

    # Now remove the +'s from the tokens and join into sentence
    for utt in tmp_utterances:

        for word in reversed(utt['text']):
            if any(char in ['+'] for char in word):
                utt['text'].remove(word)

        # Check utterance is not only punctuation (because the rest was invalid/removed)
        if len(utt['text']) == 1 and all(char in ['.', '?', '!', ' '] for char in utt['text'][0]):
            # If so, remove
            utt['text'].remove(utt['text'][0])

        # Join words for complete sentence
        utt['text'] = " ".join(utt['text'])
        # Strip leading and trailing whitespace
        utt['text'].strip()
        # Strip duplicate whitespace
        utt['text'] = re.sub(' +', ' ', utt['text'])

    dialogue = dict()
    utterances = []
    num_utterances = 0

    # Remove empty utterances
    for utt in tmp_utterances:
        if len(utt['text']) > 0:
            utterances.append(utt)

    # Create dialogue
    dialogue['dialogue_id'] = file_name
    dialogue['num_utterances'] = len(utterances)
    dialogue['utterances'] = utterances

    # Add to dialogues
    num_dialogues += 1
    dialogues.append(dialogue)

# Add dataset metadata
dialogue_data['dataset'] = "scose"
dialogue_data['num_dialogues'] = num_dialogues
dialogue_data['dialogues'] = dialogues

# Save to JSON file
save_json_data(data_dir, dialogue_data['dataset'], dialogue_data)