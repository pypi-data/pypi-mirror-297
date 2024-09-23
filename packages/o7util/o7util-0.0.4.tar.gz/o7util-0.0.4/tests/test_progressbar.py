import unittest
from unittest.mock import patch

import o7util.progressbar

# coverage run -m unittest -v tests.test_progressbar && coverage report && coverage html

class Test_Progressbar(unittest.TestCase):

    @patch('sys.stdout.write')
    @patch('sys.stdout.flush')
    def test_basic(self, *args):
        bar = o7util.progressbar.ProgressBar()
        bar.kick()
        bar.kick(inc=0)

if __name__ == '__main__':
    unittest.main()
