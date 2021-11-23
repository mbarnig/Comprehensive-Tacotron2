import gruut

def text2phone(text):
    phonemizer_args = {
        "remove_stress": True,
        "ipa_minor_breaks": True,
        "ipa_major_breaks": True
    }
    
    ph_list = gruut.text_to_phonemes(
        text,
        lang="nl",
        return_format="word_phonemes",
        phonemizer_args=phonemizer_args,
    )
    
    # Join and re-split to break apart diphtongs, suprasegmentals, etc.
    ph_words = ["|".join(word_phonemes) for word_phonemes in ph_list]
    ph = "| ".join(ph_words)
    
    return ph
    
lb_text = "Ech sin en décke Bëlles, an ech sin midd !"    
myphonemes = text2phone(lb_text)
print(myphonemes)
