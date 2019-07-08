import os
import re

from scose_utilities import *
import spacy
from spacy.tokenizer import Tokenizer
nlp = spacy.load('en')
tokenizer = Tokenizer(nlp.vocab)

# Data source and output paths
archive_dir = "scose_archive/"
data_dir = "scose_data/text/"

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
            if all(char not in excluded_chars for char in word) and not any(char.isdigit() for char in word):

                # Strip any characters in the list
                if any(char in strip_chars for char in word):
                    word = re.sub('[:⌊⌋⌈⌉“”"◉()]', '', word)

                # If it is a redacted word i.e. 'xxx', replace with <unk>
                if 'xxx' in word:
                    word = word.replace('xxx', '<unk>')

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

    # Concatenate multi-line-utterance's with '+'
    prev_utt_index = len(tmp_utterances) - 1
    for utt in reversed(tmp_utterances):

        prev_utt_index -= 1
        next_utt = None

        # If we find an utterance that may be concatenated (i.e. has a '+')
        if len(utt['text']) > 0:
            for word in utt['text']:
                if any(char in ['+'] for char in word):

                    # Get the next (i.e. previous) utterance
                    if prev_utt_index >= 0:
                        next_utt = tmp_utterances[prev_utt_index]

                    # If the previous speaker was the same person, concatenate them
                    if next_utt is not None and utt['speaker'] == next_utt['speaker']:

                        # First check if there is punctuation at the end of the utterance being concatenated to
                        if any(char in ['.', '!', '?'] for char in next_utt['text'][-1]):
                            # If so replace with comma
                            next_utt['text'][-1] = re.sub('[.!?]', ',', next_utt['text'][-1])

                        # Remove the '+' from the current utterance
                        for plus_word in reversed(utt['text']):
                            if any(char in ['+'] for char in plus_word):
                                utt['text'].remove(plus_word)

                        # Concatenate them
                        # print("Concatenating '", next_utt['text'], "' + '", utt['text'], "'")
                        next_utt['text'] = next_utt['text'] + utt['text']
                        # And remove the current from the list
                        tmp_utterances.remove(utt)

    # Now remove any +'s and erroneous punctuation from the tokens and join into sentence
    for utt in tmp_utterances:

        for word in reversed(utt['text']):
            if any(char in ['+'] for char in word):
                utt['text'].remove(word)

        # Check utterance is not only punctuation (because the rest was invalid/removed)
        if len(utt['text']) == 1 and all(char in ['.', '?', '!', ' '] for char in utt['text'][0]):
            # If so, remove
            utt['text'].remove(utt['text'][0])

        # Check for 'floating' punctuation (because other chars/words were removed)
        if len(utt['text']) >= 2 and all(char in ['.', '?', '!', ' '] for char in utt['text'][-1]):
            # If so remove it from the end and add to the next word
            char =utt['text'].pop()
            utt['text'][-1] += char

        # Join words for complete sentence
        utt['text'] = " ".join(utt['text'])
        # Strip leading and trailing whitespace
        utt['text'].strip()
        # Strip duplicate whitespace
        utt['text'] = re.sub(' +', ' ', utt['text'])

    utterances = []

    # Remove empty utterances
    for utt in tmp_utterances:
        if len(utt['text']) > 0 and not all(char in ['.', '?', '!', ' '] for char in utt['text']):
            utterances.append(utt)

    # Write dialogue to text file
    with open(data_dir + file_name + '.txt', 'w+', encoding="utf8") as file:
        for utt in utterances:
            file.write(utt['speaker'] + "|" + utt['text'] + "\n")
