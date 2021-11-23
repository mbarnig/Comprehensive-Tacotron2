from text.symbols import get_phonemes
from text.cleaners import text2phone, phone2ids
from utils.tools import get_configs_of

def main():
    preprocess_config = get_configs_of("Marylux")
    print(preprocess_config)
    print(preprocess_config["preprocessing"]["text"]["text_cleaners"])
    #if preprocess_config["preprocessing"]["text"]["text_cleaners"] == "phonemizer": 
    #    print("This is the phonemizer")
        
    my_set = get_phonemes()
    # print(my_set)
    text = "Hello Biischt, am Raum."
    my_ph = text2phone(text)
    print("*** my output ***")
    print(my_ph)
    my_ids = phone2ids(text, my_set)
    print("*** my ids ***")
    print(my_ids)

if __name__ == "__main__":
    main()
