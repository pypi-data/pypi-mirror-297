#coding:utf-8

import sys
import os

from . import readseq

try:
	from hellokit import system
except ModuleNotFoundError:
    sys.exit(f'<hellokit> required, try <pip install hellokit>.')


class FQ2FA:
	def __init__(self, fq: str = None):
		"""
		Wrapper transforming fastq to fasta.
		args:
			fq: FILE
				input fastq file (.gz).
		"""

		selt.fq = fq

		system.check_file(self.fq)

	def fq2fa(self):
		handle = system.open_file(self.fq)
		for name, seq, qual in readseq.readseq(handle):
			print(f'>{name}\n{seq}\n')
		handle.close()
