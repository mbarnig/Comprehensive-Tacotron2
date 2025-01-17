""" from https://github.com/keithito/tacotron """
# modified by Marco Barnig on 14.8.2021
import re
from text import cleaners
from text.cleaners import phone2ids_cleaners
from text.symbols import symbols, bos, eos


# Mappings from symbol to numeric ID and vice versa:
_symbol_to_id = {s: i for i, s in enumerate(symbols)}
_id_to_symbol = {i: s for i, s in enumerate(symbols)}

# Regular expression matching text enclosed in curly braces:
_curly_re = re.compile(r"(.*?)\{(.+?)\}(.*)")


def text_to_sequence(text, cleaner_names):
    """Converts a string of text to a sequence of IDs corresponding to the symbols in the text.

    The text can optionally have ARPAbet sequences enclosed in curly braces embedded
    in it. For example, "Turn left on {HH AW1 S S T AH0 N} Street."

    Args:
      text: string to convert to a sequence
      cleaner_names: names of the cleaner functions to run the text through

    Returns:
      List of integers corresponding to the symbols in the text
    """
    # check if text-cleaner == phonemizer
    text_cleaner = "none"

    if text_cleaner == "phonemizer" :
        sequence = phone2ids_cleaners(text, symbols)
        # Append eos at the end of the sequence
        sequence = sequence + [_symbol_to_id[eos]]
        return sequence
    else :
        sequence = []

        # Check for curly braces and treat their contents as ARPAbet:
        while len(text):
            m = _curly_re.match(text)

            if not m:
                print("*** text/__init__.py : clean text ***")
                print(_clean_text(text, cleaner_names))
                sequence += _symbols_to_sequence(_clean_text(text, cleaner_names))
                break
            sequence += _symbols_to_sequence(_clean_text(m.group(1), cleaner_names))
            sequence += _arpabet_to_sequence(m.group(2))
            text = m.group(3)

        # Append eos at the end of the sequence
        sequence = sequence + [_symbol_to_id[eos]]
        return sequence


def sequence_to_text(sequence):
    '''Converts a sequence of IDs back to a string'''
    result = ''
    for symbol_id in sequence:
        if symbol_id in _id_to_symbol:
            s = _id_to_symbol[symbol_id]
            # Enclose ARPAbet back in curly braces:
            if len(s) > 1 and s[0] == '@':
                s = '{%s}' % s[1:]
                result += s
    return result.replace('}{', ' ')


def _clean_text(text, cleaner_names):
    for name in cleaner_names:
        cleaner = getattr(cleaners, name)
        if not cleaner:
            raise Exception('Unknown cleaner: %s' % name)
        text = cleaner(text)
    return text


def _symbols_to_sequence(symbols):
    mysymbols2ids = [_symbol_to_id[s] for s in symbols if _should_keep_symbol(s)]
    print("*** text/__init__.py : mysymbol2ids ***")
    print(mysymbols2ids)
    return mysymbols2ids 


def _arpabet_to_sequence(text):
    return _symbols_to_sequence(['@' + s for s in text.split()])


def _should_keep_symbol(s):
    return s in _symbol_to_id and s != '_' and s != '~'
