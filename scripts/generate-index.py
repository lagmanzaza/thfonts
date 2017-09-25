# This is temporary
import os
import json
from pathlib import Path
from jinja2 import Environment

env = Environment(autoescape=True)

TEMPLATE = env.from_string('''<!DOCTYPE html>
<html>
<head>
	<meta charset="UTF-8">
	<title>Thai Web Fonts Collections</title>
	<style>
body{
	margin: 0;
	padding: 0;
}
.collection{
	display: flex;
	flex-wrap: wrap;
}
.font{
	flex: 1;
	max-width: 31%;
	margin: 10px;
	border: #ccc solid 1px;
	padding: 10px;
	border-radius: 2px;
	box-shadow: rgba(50,50,50,.6) 0 2px 5px;
}
.font h1{
	margin: 0;
	font-size: 14pt;
}
.preview{
	font-size: 48pt;
	margin: 10px 0;
}
code{
	word-break: break-word;
	white-space: nowrap;
	overflow: auto;
	display: block;
}
	</style>
</head>
<body>
<div class="collection">
	{% for font in fonts %}
	<div class="font">
		<h1><a href="{{font.homepage}}">{{font.name}}</a></h1>
		{% set url = "fonts/" ~ font.font_dir ~ "/" ~ font.version_dir ~ "/style.css" %}
		<link rel="stylesheet" href="{{url}}">
		<div style="font-family: '{{font.name}}';" class="preview">วิญญูรู้ทฤษฎีน้ำแข็ง</div>
		<p><code>&lt;link rel="stylesheet" href="https://whs.github.io/thfonts/{{url|escape}}"&gt;</code></p>
		<p><small>by <a href="{{font.author.url}}">{{font.author.name}}</a></small></p>
	</div>
	{% endfor %}
</div>

<div class="credit">Collection maintaned by <a href="https://tipme.in.th">TipMe</a></div>
</body>
</html>''')

fonts = []
root = Path(__file__).resolve().parents[1] / 'fonts'
for font_dir in os.scandir(root):
	for version_dir in os.scandir(font_dir.path):
		package = Path(version_dir.path) / 'package.json'
		with package.open() as fp:
			package_data = json.load(fp)

		package_data['font_dir'] = str(font_dir.name)
		package_data['version_dir'] = str(version_dir.name)
		fonts.append(package_data)

print(TEMPLATE.render(fonts=fonts))
