def space_needed(token):
	if token[1] == '.' or token[0] == "n't":
		return ''
	return ' '

def convert(tokens_list, corrupted_indices):
	"""
	tokens_list -> Simply the nltk.pos_tag(word_tokenize())
	corrupted_indices -> List of tuples, each tuple has index w.r.t token_list and list of suggestions.
	"""
	if len(tokens_list) == 0:
		return []
	ans = []
	ind = [pair[0] for pair in corrupted_indices]
	current_index = 0
	try:
		if corrupted_indices[0][0] == 0:
			ans.append((tokens_list[0][0], corrupted_indices[0][1]))
			current_index = 1
	except:
		pass
	tokens_mod = []
	string = ''
	if current_index == 0:
		string += tokens_list[0][0]
	for index in range(1, len(tokens_list)):
		if index in ind:
			ans.append((string + space_needed(tokens_list[index]), []))
			ans.append((tokens_list[index][0], corrupted_indices[current_index][1]))
			current_index += 1
			string = ''
		else:
			string += space_needed(tokens_list[index]) + tokens_list[index][0]
	if string != '':
		ans.append((string + space_needed(tokens_list[index]), []))
	return ans
