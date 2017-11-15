import pandas as pd 

file_name = 'dataset/review.json'
review_data = pd.read_json(file_name,lines=True)

def extract_reviews_for_rest(business_list):
	for i in range(len(review_data)):
		if(review_data['business_id'][i] in business_list):
			print review_data['business_id'][i], review_data['text'][i]


business_list =[u'VsewHMsfj1Mgsl2i_hio7w', u'X94hpx48QK-v8MmV0YLK7A', u'4GIqWxEvczRvgDuZ404dWw', u'IqUKgj5hd3iUdQX80kw47g', u'ODZLMTbjCnpDNkW1JbMjlQ']
extract_reviews_for_rest(business_list)