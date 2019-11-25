from nltk.data import find
from bllipparser import RerankingParser

def obtain_tags(sentence):
	model_dir = find('models/bllip_wsj_no_aux').path
	parser = RerankingParser.from_unified_model_dir(model_dir)

	best = parser.parse(sentence)
	tree0 = str(best.get_reranker_best())
	tree1 = str(best.get_parser_best())

	open_index = 0
	close_index = -1
	tags0 = []
	for index in range(len(tree0)):
		if tree0[index] == '(':
			open_index = index
		elif tree0[index] == ')':
			if open_index > close_index:
				tags0.append(tuple(reversed(tree0[open_index + 1:index].split())))
			close_index = index

	open_index = 0
	close_index = -1
	tags1 = []
	for index in range(len(tree1)):
		if tree1[index] == '(':
			open_index = index
		elif tree1[index] == ')':
			if open_index > close_index:
				tags1.append(tuple(reversed(tree1[open_index + 1:index].split())))
			close_index = index
	final = []
	for index in range(len(tags0)):
		if tags0[index][1] == 'JJ':
			final.append(tags0[index])
		elif tags1[index][1] == 'JJ':
			final.append(tags1[index])
		else:
			final.append(tags0[index])
	return final

print(obtain_tags('I bought a red very giant ball.'))