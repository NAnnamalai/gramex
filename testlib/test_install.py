import io
import os
import re
import shutil
import unittest
from orderedattrdict import AttrDict
from nose.tools import ok_
from . import folder
from gramex import variables
from gramex.install import init, _ensure_remove
from shutilwhich import which


class TestInit(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.appname = 'test-gramex-init'
        cls.app_dir = os.path.join(folder, cls.appname)
        cls.cwd = os.getcwd()

    def test_init(self):
        if os.path.exists(self.app_dir):
            shutil.rmtree(self.app_dir, onerror=_ensure_remove)
        os.makedirs(self.app_dir)
        os.chdir(self.app_dir)
        init([], AttrDict())

        # Ensure files are present
        source = os.path.join(variables['GRAMEXPATH'], 'apps', 'init')
        for path in os.listdir(source):
            path = path.replace('appname', self.appname.replace('-', '_'))
            ok_(os.path.exists(os.path.join(self.app_dir, path)), path + ' in init')

        # Ensure templates work
        with io.open(os.path.join(self.app_dir, 'gramex.yaml'), encoding='utf-8') as handle:
            line = handle.readline().strip()
            ok_('don\'t delete this line' in line)
            ok_(re.match(r'# Generated by gramex init 1\.\d+', line))

        # If Git LFS is present, ensure that it's set up to track assets/**
        if which('git-lfs'):
            path = os.path.join(self.app_dir, '.gitattributes')
            ok_(os.path.exists(path), 'Git LFS worked')
            with open(path, encoding='utf-8') as handle:
                ok_('assets/**' in handle.read(), 'Git LFS tracks assets/**')
            path = os.path.join(self.app_dir, '.gitignore')
            with open(path, encoding='utf-8') as handle:
                ok_('assets/**' not in handle.read(), '.gitignore allows assets/**')
        # Else, check that .gitignore does not commit assets/**
        else:
            path = os.path.join(self.app_dir, '.gitignore')
            with open(path, encoding='utf-8') as handle:
                ok_('assets/**' in handle.read(), '.gitignore allows assets/**')

    @classmethod
    def tearDown(cls):
        os.chdir(cls.cwd)
        try:
            shutil.rmtree(cls.app_dir, onerror=_ensure_remove)
        except OSError:
            # Ideally, we should clean up the app_dir
            # But on Windows, npm / git may prevent this for some time. Ignore this
            pass
