import json
import os
import re
import subprocess as sp
import tomllib

project_info_cache = None
releases_info_cache = None

def get_project_info():
    global project_info_cache
    if project_info_cache is not None:
        return project_info_cache
    with open("pyproject.toml", "rb") as f:
        project_info_cache = tomllib.load(f)["project"]
        return project_info_cache

def get_releases_info():
    global releases_info_cache
    if releases_info_cache is not None:
        return releases_info_cache

    releases_list_json = sp.check_output(["gh", "release", "list", "--json", "tagName"])
    releases_list = json.loads(releases_list_json)

    releases = []

    for release in releases_list:
        if not release["tagName"].startswith("v"):
            continue
        release_data_json = sp.check_output(["gh", "release", "view", release["tagName"], "--json", "name,assets"])
        release_data = json.loads(release_data_json)
        wheels = [asset for asset in release_data["assets"] if "url" in asset and asset["url"].endswith('.whl')]
        releases.append({"tag": release["tagName"], "wheels": wheels})

    releases_info_cache = releases
    return releases_info_cache

lis = "\n".join(
    [f"\t\t<li><a href=\"{r['wheels'][0]['url']}\">{r['wheels'][0]['name']}</a></li>" for r in get_releases_info()]
)
def get_release_ul():
    return f"\t<ul>\n{lis}\t\n\t</ul>"

pinfo = get_project_info()
rinfo = get_releases_info()

package_name_normalized = re.sub(r"[-_.]+", "-", pinfo["name"].lower())

detail = f"""<html lang="en">
<head>
    <title>{pinfo["name"]}</title>
    <style>
        ul {{
            list-style: "\\1F4BC"
        }}
    </style>
</head>
<body>
    <h1>{pinfo["name"]}</h1>
    <p>{pinfo["description"]}</p>
{get_release_ul()}
</body>
</html>"""

index = f"""<html lang="en">
    <head>
        <title>{pinfo["name"]} repository</title>
        <style>
        code.block {{
            display: block;
            border: 1px solid #ccc;
            background-color: #eee;
            padding: 1em;
            margin: 1em;
        }}
        
        ul {{
            list-style: "\\1F4C1";
        }}
        </style>
    </head>
    <body>
        <h1>{pinfo["name"]} repository</h1>
        <p>This URL can be referenced as a <tt>pip</tt> repository to install releases of the {pinfo["name"]} package.</p>
        
        <code class="block">pip install --index-url <span id="this-site"></span> {pinfo["name"]}</code>
    
        <ul>
            <li><a href="{package_name_normalized}/">{pinfo["name"]}</a></li>
        </ul>
        
    </body>
    <script>document.getElementById("this-site").innerText = window.location.href;</script>
</html>"""


os.mkdir("dist_html")
os.mkdir(f"dist_html/{package_name_normalized}")

with open("dist_html/index.html", "w") as f:
    f.write(index)
with open(f"dist_html/{package_name_normalized}/index.html", "w") as f:
    f.write(detail)
