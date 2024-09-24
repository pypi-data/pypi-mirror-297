import unittest, os, sys
sys.path.append(os.path.normpath(os.path.join(os.path.abspath(sys.path[0]), '../src')))
from cylon import get_remote_folders


class GeneralTests(unittest.TestCase):

    def setUp(self) -> None:
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    def test_get_remote_folders_list(self):
        self.assertIsNone(get_remote_folders("", ""), "get_remote_folders('','') should be None")

        lst = get_remote_folders("cbravo@kind.cl", "~/git/data")
        for tmp in lst:
            self.assertTrue(tmp.endswith(".git"))

    def test_get_remote_folders_dict(self):
        lst = get_remote_folders("cbravo@kind.cl", "~/git/data", get_description=True)
        for tmp in lst:
            self.assertTrue(tmp.endswith(".git"), "A folder in the index does not end in .git")
            self.assertTrue(isinstance(lst[tmp], str), "A description is not a string")

if __name__ == '__main__':
    unittest.main(verbosity=2)
