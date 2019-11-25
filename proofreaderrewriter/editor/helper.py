from nltk.tokenize import word_tokenize
from nltk import pos_tag

def space_needed(token):
	if token[1] == '.' or token[1] == ',' or token[0] == "n't":
		return ''
	return ' '

def word(token):
	if token[0] == '``':
		return '"'
	else:
		return token[0]

def convert(tokens_list, corrupted_indices):
	'''
	tokens_list -> Simply the nltk.pos_tag(word_tokenize())
	corrupted_indices -> List of tuples, each tuple has index w.r.t token_list and list of suggestions.
	'''
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
		string += word(tokens_list[0])
	for index in range(1, len(tokens_list)):
		if index in ind:
			ans.append((string + space_needed(tokens_list[index]), []))
			ans.append((word(tokens_list[index]), corrupted_indices[current_index][1]))
			current_index += 1
			string = ''
		else:
			string += space_needed(tokens_list[index]) + word(tokens_list[index])
	if string != '':
		ans.append((string + space_needed(tokens_list[index]), []))
	final = []
	for pair in ans:
		mod = pair[0][0]
		for i in range(1, len(pair[0])):
			if pair[0][i-1] == '"' and pair[0][i] == ' ':
				pass
			else:
				mod += pair[0][i]
		final.append((mod, pair[1]))
	return final

def adj_convert(tokens_list, corrupted_indices):
	'''
	tokens_list -> Simply the nltk.pos_tag(word_tokenize())
	corrupted_indices -> List of tuples, each tuple has index w.r.t token_list and list of suggestions.
	'''
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
	cur = 0
	if current_index == 0:
		string += word(tokens_list[0])
	index = 1
	while index < len(tokens_list):
		# print(index, ans)
		try:
			if index in ind[cur]:
				ans.append((string + space_needed(tokens_list[index]), []))
				temp = word(tokens_list[index])
				for temp_index in range(1, len(ind[cur])):
					index += 1
					temp += ' ' + word(tokens_list[ind[cur][temp_index]])
				ans.append((temp, corrupted_indices[current_index][1]))
				current_index += 1
				string = ''
				cur += 1
			else:
				string += space_needed(tokens_list[index]) + word(tokens_list[index])
		except:
			string += space_needed(tokens_list[index]) + word(tokens_list[index])
		index += 1
	if string != '':
		ans.append((string, []))
	final = []
	for pair in ans:
		mod = pair[0][0]
		for i in range(1, len(pair[0])):
			if pair[0][i-1] == '"' and pair[0][i] == ' ':
				pass
			else:
				mod += pair[0][i]
		final.append((mod, pair[1]))
	return final