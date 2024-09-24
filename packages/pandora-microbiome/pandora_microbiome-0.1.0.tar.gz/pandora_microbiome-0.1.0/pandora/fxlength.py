#coding:utf-8


import sys

from . import readseq

try:
	from hellokit import system
except ModuleNotFoundError:
    sys.exit(f'<hellokit> required, try <pip install hellokit>.')


class fxLength:
	def __init__(self, seq: str = None, plot: bool = Flase, avg_only: bool=False):
		"""
		Calculationg length of each sequence and print them,
		plot a histgram if plot was set, average length adds on figure.

		args:
			seq: FILE
				input sequence file, fastq or fasta.
			plot: BOOL
				set to plot histgram of sequences' length.
			avg_only: BOOL
				set to print average length only.
		"""

		self.seq = seq
		self.plot = plot
		self.avg_only = avg_only

		system.check_file(self.seq)

	def fxlength(self):
		length = {}
		length['length'] = {}
		if not self.avg_only: print(f'seqid\tlength\n')
		handle = system.open_file(self.seq)
		for name, seq, qual in readseq.readseq(handle):
			if not self.avg_only: print(f'{name}\t{len(seq)}\n')
			length['length'][name] = len(seq)

		if self.avg_only or self.plot:
			try:
				import pandas as pd
			except ModuleNotFoundError:
				sys.exit(f'<pandas> required, try <pip install pandas>.')

			# dict to DataFrame
			length = pd.DataFrame.from_dict(length)

		if self.avg_only: print(mean(length.length))

		if self.plot:

			try:
				import matplotlib
			except ModuleNotFoundError:
				sys.exit(f'<matplotlib> required, try <pip install matplotlib>.')

			matplotlib.use('Agg')
			import matplotlib.pyplot as plt

			ax = plt.subplot()
			xticks = [i for i in range(0, length.max()[0], 20)]
			s = 6 if len(xticks) <20 else 1
			ax.set_xticks(xticks)
			ax.set_xticklabels(xticks, fontdict={'fontsize':s})
			ax.text(0.95, 0.01, mean(length.length),
        			verticalalignment='bottom',
					horizontalalignment='right')
			# print(xticks)
			length.hist(column='length', grid=False, bins=10000, ax=ax)
			plt.savefig(self.seq + '.len.pdf', dpi=600)
