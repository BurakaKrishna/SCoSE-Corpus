# SCoSE-Corpus
Utilities for processing the [Saarbrücken Corpus of Spoken English (SCoSE)](https://ca.talkbank.org/access/SCoSE.html) 
available from [TalkBank](https://talkbank.org/). 
The corpus consists of 14 transcribed dialogues of general talk on a range of topics between two or more participants.
The utilities process the original transcripts into plain text or json formats and remove disfluency and other 
annotation characters. The intent is to create a more machine-readable format for NLP and computational modelling tasks.

## Scripts
scose_to_json.py script processes the 14 dialogues from the original .cha format into .json files using the format
outlined below.
This format is intended to facilitate annotation of the dialogue using the 
[Conversation Analysis Modelling Schema](https://nathanduran.github.io/Conversation-Analysis-Modelling-Schema/).

scose_to_text.py processes the 14 dialogues from the original .cha format into plain text files,
with one line per-utterance, using the format outlined below.
Setting the *utterance_only* flag to true will remove the speaker label from the output text files.

scose_utilities.py script contains various helper functions for loading/saving and processing the data.

## Data Format
The original transcripts have had all disfluency and annotation characters removed. For example '|', '◉', '=', '@'.
The metadata headers and utterance timestamps (marked with '&#9633;') have also been removed.

Any sentences that are continued on another line by the same speaker (marked with '+') have been
concatenated to form complete uninterrupted sentences.

Certain words, such as swear words or names, were redacted in the original transcripts and replaced with *'xxx'*.
These have been raplaced with an *\<unk\>* token.

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
## Licensing and Attribution
The code within this repository is distributed under the [GNU General Public License](https://www.gnu.org/licenses/gpl-3.0.en.html).

The corpora available from [TalkBank](https://talkbank.org/), and the adapted format within this repository,
is licensed under a [Creative Commons Attribution 3.0 Unported License](http://creativecommons.org/licenses/by/3.0/).

<a rel="license" href="http://creativecommons.org/licenses/by/3.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/3.0/88x31.png" /></a>