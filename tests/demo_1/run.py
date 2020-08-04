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
			msg = ""
			for line in f:
				if len(msg) > 0:
					if("ERROR" not in line):
						msg += line
						
				if("ERROR" in line):
					if len(msg) > 0:
						
						try:
							self.assertThat("False", assertMessage=msg.split("actual: ")[0])
							actual = msg.split("actual: ")[1].split("\n")[0]
							expected = msg.split("expected: ")[1].split("\n")[0]
							diff_index = next((i for i in range(min(len(actual), len(expected))) if actual[i]!=expected[i]), len(actual)-1)

							actual_highlighted = f"{actual[:diff_index]}\033[91m{actual[diff_index:]}\033[0m"
							expected_highlighted = f"{actual[:diff_index]}\033[91m{expected[diff_index:]}\033[0m"

							print(f"\t\texpected: {expected_highlighted}")
							print(f"\t\tactual: {actual_highlighted}")
							print("\t\t" + " "*(8+diff_index) + "^")
						except:
							pass
						msg = ""
					msg = line.split("-")[3:]
					msg = "-".join(msg)
		
		
