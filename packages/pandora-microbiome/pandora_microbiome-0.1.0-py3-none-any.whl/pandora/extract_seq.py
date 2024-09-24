#coding:utf-8

import sys

from . import readseq

try:
	import pandas as pd
except ModuleNotFoundError:
    sys.exit(f'<pandas> required, try <pip install pandas>.')

try:
	from hellokit import system
except ModuleNotFoundError:
    sys.exit(f'<hellokit> required, try <pip install hellokit>.')


class Extract_Seq:
	def __init__(self, seqid: str = None, idlist: str = None, seqin: str = None,
				fastq: bool = False):
		"""
		Extract sequences from fasta or fastq file.

		args:
			seqid: STR
				sequence id to extract.
			idlist: FILE
				sequence id list to extract.
			seqin: FILE
				input fasta or fastq sequence file.
			fasta: BOOL
				True means input is fasta, otherwise fastq.
		"""

		self.seqid = seqid
		self.idlist = idlist
		self.seqin = seqin
		self.fastq = fastq

		system.check_file(self.seqin)
		if self.idlist: system.check_file(self.idlist)

	def extract_seq(self):
		handle = system.open_file(self.seqin)
		allid = [self.seqid] if self.seqid else pd.read_csv(self.idlist, squeeze=False, header=None, index_col=0, sep='\t').index
		if not self.fastq:
			for name, seq, qual in readseq.readseq(handle):
				if name in allid:
					print(f'>{name}\n{seq}\n')
		else:
			for name, seq, qual in readseq.readseq(handle):
				if name in allid:
					print(f'@{name}\n{seq}\n+\n{qual}\n')
