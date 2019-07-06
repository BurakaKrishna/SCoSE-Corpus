# SCoSE-Copus
Utilities for Processing the [Saarbrücken Corpus of Spoken English (SCoSE)](https://ca.talkbank.org/access/SCoSE.html) 
available from [TalkBank](https://talkbank.org/). 
The corpus consists of 14 transcribed dialogues of general talk on a range of topics between two or more participants.
The utilities process the original transcripts into plain text or json formats and remove disfluency and other 
annotation characters. The intent is to create a more machine-readable format for NLP and computational modelling tasks.

## Scripts
scose_to_json.py script processes the 14 dialogues from the original .cha format into .json files using the format
outlined below.
This format is intended to facilitate annotation of the dialogue using the 
[Conversation Analysis Schema](https://nathanduran.github.io/CA-Schema/)
and [Dialogue tagger](https://github.com/NathanDuran/CA-Dialogue-Tagger).

scose_to_text.py processes the 14 dialogues from the original .cha format into plain text files using the format
outlined below.

scose_utilities.py script contains various helper functions for loading/saving and processing the data.

## Data Format
The original transcripts have had all disfluency and annotation characters removed. For example '|', '◉', '=', '@'.
The metadata 'headers' have also been removed.

Any sentences that are continued on another line by the same speaker (marked with '+') have been
concatenated to form complete uninterrupted sentences.

Certain words, such as swear words or names, were redacted in the original transcripts and replaced with 'xxx'.

### Example Text Format
ERI|didn't they, didn't you ever hear that they, they found an entire woolly mammoth, frozen.

JAC|yeah, and they ate it.

ERI|an entire one though.

JAC|yeah.

### Example JSON Format
The following is an example of the JSON format for the SCoSE corpus.

```json
    {
        "dataset": "dataset_name",
        "num_dialogues": 1,
        "dialogues": [
            {
                "dialogue_id": "dataset_name_1",
                "num_utterances": 2,
                "utterances": [
                    {
                        "speaker": "A",
                        "text": "Utterance 1 text.",
                        "ap_label": "AP-Label",
                        "da_label": "DA-Label"
                    },
                    {
                        "speaker": "B",
                        "text": "Utterance 2 text.",
                        "ap_label": "AP-Label",
                        "da_label": "DA-Label",
                        "slots": { //Optional
                            "slot_name": "slot_value"
                        }
                    }
                ],
                "scenario": { //Optional
                    "db_id": "1",
                    "db_type": "i.e booking",
                    "task": "i.e book",
                    "items": []
                }
            }
        ]
    }
```
