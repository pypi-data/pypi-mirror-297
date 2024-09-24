#coding:utf-8

import sys

from . import readseq

try:
	import numpy as np
except ModuleNotFoundError:
    logger.error(f'<numpy> required, try <pip install numpy>.')
	sys.exit()
try:
	from hellokit import system
except ModuleNotFoundError:
    logger.error(f'<hellokit> required, try <pip install hellokit>.')
	sys.exit()

class Phred:
	def __init__(self, fq: str = None, num: int =  1000):

		"""
		Check phred value of input fastq.
		args:
			fq: FILE
				input fastq file.
			num : INT
				number of sequence for phred check.
		"""

		self.fq = fq
		self.num = num

		system.check_file(self.fq)

	def check_phred(self):
		universal_quals, universal_mins, c = [], [], 0
		handle = system.open(self.fq)
		for name, seq, qual in readseq.readseq(handle):
			if c < num:
				qual = [ord(i) for i in qual]
				universal_quals.extend(qual)
				universal_mins.append(min(qual))
				c += 1
			else:
				break
		print(f'Mean of all input ASCII: {np.mean(universal_quals)}\n')
		print(f'Mean of all minimum ASCII: {np.mean(universal_mins)}\n')
		print(f'SD of all minimum ASCII: {np.std(universal_mins)}\n')
