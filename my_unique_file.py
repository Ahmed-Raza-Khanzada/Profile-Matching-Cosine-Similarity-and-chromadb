import random
import os
import uuid
def make_unique_file():
    my_path = os.listdir("pdfs")
    my_path2 = os.listdir("blur_pdfs2")
    random_name = str(uuid.uuid4())
    while random_name+".pdf" in my_path or random_name+".pdf" in my_path2:
        random_name = str(uuid.uuid4())

    return random_name
