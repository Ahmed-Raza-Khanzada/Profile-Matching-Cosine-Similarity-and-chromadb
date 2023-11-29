import math
import string
import sys
import re

def Correct_format_individual(value):
  if value=="" or value == None or value == "None" :
    return "None"
  if ((type(value)==str and len(value)>0)) or (type(value)==int):
    if type(value)==int:
      return str(value)
    return value
  my_text = ""
  if type(value) ==list and len(value)>0:
    for j in value:
      if  j!=None or j!="None" or j!="":
        my_text += j
    return my_text
  else:
    if type(value)==list:
      return "None"
    else:
      return value
    

            


def Correct_format(array1):
  my_array = []
  for i in array1:
    if  i==None or i=="None" or i =="":
      my_array.append("")
      continue
    my_array.append(Correct_format_individual(i))
  return my_array
def get_profile_Data4Semantic(data,selected_keys = [],not_keys_vals = ["Painter based in the city of Leiden\nAll paintings are for sale\nContact: guido.marsman@gmail.com"]):
  def check_dict_values(prof,keys):
    for key in keys:
        if key in selected_keys:
          if prof[key]!=None:
              return True
    return False
  if data!=None and len(data)>0:
    keys = [i  for i in data[0].keys()]
  else:
    return
  if len(selected_keys)<1:
    selected_keys = keys

  prof_data = []
  for prof in data:
    prof_info = ""
    check=check_dict_values(prof,keys)
    if check:
      for key in keys:
        if key in selected_keys:
          # if key=="biography":
          #     if prof[key] in not_keys_vals:
          #         print("&&&&&&&&&&&&&&&&&&&&&&&&&","biography",prof[key],"*********************************************")
          #         continue

          prof_info =prof_info+f" {key}: " + Correct_format_individual(prof[key])
    else:
       
        prof_info = "None"
    prof_data.append(prof_info)
  return prof_data




# Function to deduplicate values in a tuple
def deduplicate_tuple(tuple_value):
    # Convert tuple to list
    list_value = list(tuple_value)
    # Remove duplicate values in list
    list_value = list(dict.fromkeys(list_value))
    # Convert list back to tuple
    tuple_value = tuple(list_value)
    return tuple_value

def clean_text(text):
    # Use regular expression to remove non-alphanumeric characters and whitespace
    if text==None:
        return None
    elif text=="" or text == " ":
      return None
    
    elif type(text)==list:
      text = " ".join(text)
    cleaned_text = text
    return cleaned_text

def read_file(filename):
	
	try:
		with open(filename, 'r') as f:
			data = f.read()
		return data
	
	except IOError:
		print("Error opening or reading input file: ", filename)
		sys.exit()


translation_table = str.maketrans(string.punctuation+string.ascii_uppercase,
									" "*len(string.punctuation)+string.ascii_lowercase)
	

def get_words_from_line_list(text):
  if text!=None:
    text = text.translate(translation_table)
    word_list = text.split()
    return word_list
  return [" "]
 

# counts frequency of each word
# returns a dictionary which maps
# the words to their frequency.
def count_frequency(word_list):
	
	D = {}
	
	for new_word in word_list:
		
		if new_word in D:
			D[new_word] = D[new_word] + 1
			
		else:
			D[new_word] = 1
			
	return D

def word_frequencies_for_file(document):
	
  # line_list = read_file(filename)
  word_list = get_words_from_line_list(document)

  freq_mapping = count_frequency(word_list)
  # print("File", filename, ":", )

  # print(len(line_list), "lines, ", )

  # print(len(word_list), "words, ", )
  # print(len(freq_mapping), "distinct words")
  # print("*"*20)

  return freq_mapping


# returns the dot product of two documents
def dotProduct(D1, D2):
	Sum = 0.0
	
	for key in D1:
		
		if key in D2:
			Sum += (D1[key] * D2[key])
			
	return Sum

# returns the angle in radians
# between document vectors
def vector_angle(D1, D2):
	numerator = dotProduct(D1, D2)
	denominator = math.sqrt(dotProduct(D1, D1)*dotProduct(D2, D2))
	
	return math.acos(numerator / denominator)


def documentSimilarity(filename_1, filename_2):
  
          
  # filename_1 = sys.argv[1]
  # filename_2 = sys.argv[2]
  sorted_word_list_1 = word_frequencies_for_file(filename_1)
  sorted_word_list_2 = word_frequencies_for_file(filename_2)
  distance = vector_angle(sorted_word_list_1, sorted_word_list_2)

  # print("The distance between the documents is: % 0.6f (radians)"% distance)

  return distance




def identify_documents(d1):
  try:
    if d1[0][0]["about"] :
      return "Linkedin"
  except:
      try:
        if d1[0]["discription"]:
            return "insta"
      except:
         try:
          if d1[0]["details"]:
              return "facebook"
         except:
          return "Incorrect format"