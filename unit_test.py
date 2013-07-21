#!/usr/bin/env python
# File: unit_test_template.py

import unittest
import sys
import os
import subprocess

sys.path.append(os.path.dirname(os.getcwd()))

from find_repos import find_repos_in, relative_to

class TestFindRepos(unittest.TestCase):
    _repo_root_path = '/tmp/test_find_repos/root'
    _repo_empty_path = '/tmp/test_find_repos/none'
    _repo_list = ['aaa', 'bbb', 'ccc', 'ddd', 'eee/one', 'eee/two']

    @classmethod
    def setUpClass(cls):
        # create a collestion of repositories 
        if not os.path.exists(cls._repo_empty_path):
            os.makedirs(cls._repo_empty_path)
        for repo in cls._repo_list:
            repo_path = os.path.join(cls._repo_root_path, repo)
            if not os.path.exists(repo_path):
                os.makedirs(repo_path)
            if not os.path.exists(os.path.join(repo_path, '.hg')):
                if subprocess.call(['hg', 'init', repo_path]) != 0:
                    unittest.TestCase.fail()

    @classmethod
    def tearDownClass(cls):
        # don't bother removing the repositories for now
        pass

    def test_option_empty(self):
        result = []
        find_repos_in(TestFindRepos._repo_empty_path, result)
        self.assertEqual(len(result), 0)

    def test_option_root(self):
        result = []
        find_repos_in(TestFindRepos._repo_root_path, result)
        self.assertEqual(len(result), len(TestFindRepos._repo_list))


    def test_relative_root(self):
        result = []
        find_repos_in(TestFindRepos._repo_root_path, result)
        relative = [relative_to(TestFindRepos._repo_root_path, repo) for repo in result]
        self.assertEqual(len(relative), len(TestFindRepos._repo_list))
        self.assertEqual(sorted(relative), sorted(TestFindRepos._repo_list))


if __name__ == '__main__':
    unittest.main()

