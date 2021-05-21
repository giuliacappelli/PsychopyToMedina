import argparse
from collections import Counter
import pandas as pd
import numpy as np
# import warnings
# warnings.filterwarnings("ignore")

"""
Reshapes the dataframe to use as input in my Medina-like model scripts
"""

my_parser = argparse.ArgumentParser()

my_parser.add_argument('--language',
					   '-l',
					   action='store',
					   default='eng',
					   help='target language of Likert experiment')

args = my_parser.parse_args()

infoVerbs = "info_verbs_"+args.language+".csv"
nameOfFile = "original_"+args.language+".csv"
medinaFile = "medina_likert_"+args.language+".csv"

taggedFile = "___tagged_likert_"+args.language+".csv"
reducedFile = "___reduced_likert_"+args.language+".csv"
tempFile = "___temp_likert_"+args.language+".csv"
dumpFile = "___dump_"+args.language+".csv"

csv1 = pd.read_csv(nameOfFile)

# rename participants with completion timestamps to avoid unnecessarily renaming duplicate names
csv1 = csv1.rename({'participant': 'partname', 'date': 'participant'}, axis=1)

participantInfo = csv1.loc[csv1.kind == 'EXP'].groupby(['participant'], as_index=False)['slider.response'].nunique()
participantInfo = participantInfo.rename({'slider.response': 'sliderresponse'}, axis=1) # .loc requires no dots in col name
badOnes = participantInfo.loc[participantInfo.sliderresponse < 3]['participant'].tolist()
participantInfo = participantInfo.rename({'sliderresponse': 'slider.response'}, axis=1) # restore original col name
print(len(badOnes), "bad participants \r\n", badOnes)

if badOnes:
	csv1 = csv1[~csv1['participant'].str.contains('|'.join(badOnes))] # removes bad participants from (copy of) original dataframe
else:
	csv1 = csv1

csv2 = pd.read_csv(infoVerbs)
csv_out = csv1.merge(csv2, how="outer", on=['verb']) # "outer merge" keeps unmatched rows (merge defaults to inner merge)
csv_out.sort_values(by=['participant'], ascending=[True]).to_csv(taggedFile, index=False)

taggedFile2 = pd.read_csv(taggedFile)

subsetFile = taggedFile2[['dObj', 'verb', 'participant', 'kind', 'telicity', 'perf', 'iter', 'mannspec', 'slider.response']]

subsetFile.to_csv(reducedFile, index=False)
reducedFile = pd.read_csv(reducedFile)

reducedFile['slider.response'] = pd.to_numeric(reducedFile['slider.response'])
medinaTable = pd.pivot_table(reducedFile, values="slider.response", index=['dObj', 'verb', 'kind', 'telicity', 'perf', 'iter', 'mannspec'], columns=['participant'])
medinaTable.to_csv(tempFile)

tempFile2 = pd.read_csv(tempFile)
tempFile2 = tempFile2.rename(columns={'perf': 'perfectivity', 'iter': 'iterativity'})
tempFile2['telicity'] = tempFile2['telicity'].replace(['yes','no'],['telic','atelic'])
tempFile2['perfectivity'] = tempFile2['perfectivity'].replace(['yes','no'],['perf','imperf'])
tempFile2['mannspec'] = tempFile2['mannspec'].replace(['yes','no'],['spec','nospec'])
tempFile2['iterativity'] = tempFile2['iterativity'].replace(['yes','no'],['iter','noiter'])

conditions = [
	((tempFile2['kind'] != "EXP") & (tempFile2['dObj'] == "yes")),
	((tempFile2['kind'] == "EXP") & (tempFile2['dObj'] == "no"))
	]
values = ['control', 'target']
tempFile2['sentence'] = np.select(conditions, values)

	# participants with original names!
# tempFile2.drop(['dObj', 'kind'], axis = 1).to_csv(medinaFile, index=False, sep = '\t', float_format='%.f')

new_participants = []
for num in range(len(tempFile2.select_dtypes('float64').columns)):
	new_participants.append("part"+str(num+1))
part_dict1 = {tempFile2.select_dtypes('float64').columns[i]: new_participants[i] for i in range(len(tempFile2.select_dtypes('float64').columns))}
list_oldnames = ['dObj', 'verb', 'kind', 'telicity', 'perfectivity', 'iterativity', 'mannspec', 'sentence']
part_dict2 = {list_oldnames[k]: list_oldnames[k] for k in range(len(list_oldnames))}
part_dict = {**part_dict1, **part_dict2}
tempFile2.columns = tempFile2.columns.to_series().map(part_dict)
	# participants anonymized! (renamed to part1, part2...)
tempFile2.drop(['dObj', 'kind'], axis = 1).to_csv(medinaFile, index=False, sep = '\t', float_format='%.f')
