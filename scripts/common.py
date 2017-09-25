import re
from pathlib import Path
import subprocess

def is_font(name):
	name = Path(name).name
	if name.startswith('.'):
		return False

	for ext in ('.ttf', '.otf'):
		if name.endswith(ext):
			return True
	return False

def make_dir(name):
	name = name.replace(' ', '_')
	return ''.join(re.findall(r'([a-zA-Z0-9_\-.]+)', name))

def get_font_info(path):
	info = subprocess.run(['otfinfo', '-i', path], stdout=subprocess.PIPE).stdout.decode('utf8')
	return dict(re.findall('([a-zA-Z0-9 ]+): +(.*)', info))
