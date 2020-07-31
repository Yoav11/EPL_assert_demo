from pysys.constants import *
from pysys.basetest import BaseTest
from apama.correlator import CorrelatorHelper
import os

class PySysTest(BaseTest):
	def execute(self):
		corr = CorrelatorHelper(self, name='correlator')
		corr.start(logfile='correlator.log')
		corr.injectEPL('../../../Asserts.mon')
		tests = os.listdir(self.input)
		tests.sort()
		for test in tests:
			if test.endswith('.mon'):
				corr.injectEPL(test)
				corr.flush()
		corr.shutdown()

	def validate(self):
		with open(os.path.join(self.output, "correlator.log")) as f:
			for line in f:
				if("ERROR" in line):
					msg = line.split("-")[3:]
					msg = "-".join(msg)
					self.assertThat("False", assertMessage=msg)	
		
		
