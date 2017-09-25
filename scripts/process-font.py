import os
from pathlib import Path
from collections import defaultdict
from jinja2 import Environment

import fontforge
from common import *

def get_fonts(path):
	out = defaultdict(dict)
	for file in os.listdir(path):
		fullpath = Path(path) / file
		if not is_font(file):
			continue
		
		info = get_font_info(fullpath)
		info['fullpath'] = fullpath
		if info['Subfamily'] in out:
			print('Duplicated subfamily: {} - {}'.format(info['Family'], info['Subfamily']))
			continue
		out[info['Subfamily']] = info
	return dict(out)

def ff_id(font):
	out = font['Family'].replace(' ', '')
	if font['Subfamily'] != 'Regular':
		out += '-' + font['Subfamily'].replace(' ', '')

	return out

jinja_env = Environment()
jinja_env.filters['make_dir'] = make_dir
jinja_env.filters['ff_id'] = ff_id
TEMPLATE = jinja_env.from_string("""
{%- for item in families %}
@font-face {
	font-family: '{{item.Family}}';
	{%- set file_name = item.Subfamily|lower|make_dir %}
	src: url('{{file_name}}.eot?#iefix') format('embedded-opentype'), 
		url('{{file_name}}.woff') format('woff'), 
		url('{{file_name}}.ttf') format('truetype'),
		url('{{file_name}}.svg#{{item|ff_id}}') format('svg');
	{%- if "Bold" in item.Subfamily %}
	font-weight: bold;
	{%- endif %}
	{%- if "Italic" in item.Subfamily %}
	font-style: italic;
	{%- endif %}
	{%- if "Oblique" in item.Subfamily %}
	font-style: oblique;
	{%- endif %}
}
{% endfor %}
""")
def generate_css(families):
	return TEMPLATE.render(families=families).strip()

def convert_fonts(base):
	desired_ext = ('woff', 'svg', 'eot', 'ttf')
	for font in os.listdir(base):
		if not is_font(font):
			continue

		font = base / font
		(name, ext) = font.name.split('.')
		ff = fontforge.open(str(font))
		for convert_to in desired_ext:
			target_name = base / '{}.{}'.format(name, convert_to)
			if target_name.is_file():
				continue
			print('Generating {}'.format(target_name))
			ff.generate(str(target_name))

			if not target_name.is_file():
				print('Tried to generate {} but failed'.format(target_name))
			
			afm = base / '{}.afm'.format(name)
			try:
				afm.unlink()
			except OSError:
				pass

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('dir')

	args = parser.parse_args()

	base = Path(args.dir)
	fonts = get_fonts(base)
	convert_fonts(base)

	with (base / 'style.css').open('w') as fp:
		fp.write(generate_css(fonts.values()))

	for variant in fonts.keys():
		file_name = make_dir(variant.lower())
		with (base / (file_name + '.css')).open('w') as fp:
			fp.write(generate_css([fonts[variant]]))
