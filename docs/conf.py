# Configuration file for the Sphinx documentation builder.

import os
import sys
from sphinx_needs import __version__
print ('sphinx-needs version: ' + str(__version__))
from sphinx_needs.api import add_dynamic_function

sys.path.append(os.path.abspath('.'))
import metamodel

sys.path.append(os.path.abspath('scripts'))

from gitlink import get_edit_url_from_folder, extent_url_with_file, get_githoster_edit_url_for_need


# -- Project information

import datetime

currentDateTime = datetime.datetime.now()
date = currentDateTime.date()

project = 'HowTo-Sphinx'
copyright = f'2024 - {date.year}, PhilipPartsch'
author = 'PhilipPartsch'

release = '0.1'
version = '0.0.1'

# -- General configuration
on_rtd = os.environ.get("READTHEDOCS") == "True"

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
    'sphinx.ext.doctest',
    'sphinx_needs',
    'sphinxcontrib.plantuml',
    'sphinxcontrib.test_reports',
    'sphinxcontrib.collections',
    'sphinxcontrib.jquery', # https://github.com/sphinx-contrib/jquery
    'sphinx_preview',
]

templates_path = ['_templates']

exclude_patterns = ['_tools/*',]

# to use numref see https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-numfig
# numfig = True

# -- intersphinx

#intersphinx_mapping = {
#    'python': ('https://docs.python.org/3/', None),
#    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
#}
#intersphinx_disabled_domains = ['std']


# -- Sphinx-Preview

# The config for the preview features, which allows to "sneak" into a link.
# Docs: https://sphinx-preview.readthedocs.io/en/latest/#configuration
preview_config = {
    # Add a preview icon only for this type of links
    # This is very theme and HTML specific. In this case "div-mo-content" is the content area
    # and we handle all links there.
    #"selector": "div.md-content a",
    "selector": "div.main a",
    # A list of selectors, where no preview icon shall be added, because it makes often no sense.
    # For instance the own ID of a need object, or the link on an image to open the image.
    "not_selector": "div.needs_head a, h1 a, h2 a, a.headerlink, a.md-content__button, a.image-reference, em.sig-param a, a.paginate_button",
    #"not_selector": "div.needs_head a, h1 a, h2 a",
    "set_icon": True,
    "icon_only": True,
    "icon_click": True,
    "icon": "🔎",
    #"icon": "icon:search",
    "width": 600,
    "height": 400,
    "offset": {
        "left": 0,
        "top": 0
    },
    "timeout": 0,
}

# -- Options for HTML output

html_theme = 'sphinx_rtd_theme'
#html_theme = 'alabaster'
#html_theme = 'sphinx_immaterial'

html_css_files = ['custom.css']

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# -- Options for EPUB output
epub_show_urls = 'footnote'

# -- get edit url for git hoster
print('edit url to git hoster:')
import pathlib
current_folder = pathlib.Path().resolve()
git_hoster_edit_url = get_edit_url_from_folder(current_folder, with_docu_part = True, docu_part_default = 'docs')
print('git hoster edit url: ' + git_hoster_edit_url)

# sphinxcontrib.plantuml configuration
local_plantuml_path = os.path.join(os.path.dirname(__file__), "_tools", "plantuml.jar")

if on_rtd:
    plantuml = f"java -Djava.awt.headless=true -jar {local_plantuml_path}"
else:
    plantuml = f"java -jar {local_plantuml_path}"

print('plantuml path: ' + str(plantuml))

plantuml_output_format = 'svg'

# sphinx_needs configuration

needs_role_need_max_title_length = -1

needs_build_json = True

needs_id_regex = metamodel.needs_id_regex

needs_types = metamodel.needs_types

needs_extra_options = metamodel.needs_extra_options

needs_extra_links = metamodel.needs_extra_links

needs_services = metamodel.needs_services

needs_layouts = metamodel.needs_layouts

needs_global_options = metamodel.needs_global_options

needs_render_context = metamodel.needs_render_context

needs_warnings = metamodel.needs_warnings

needs_string_links = metamodel.needs_string_links

needs_external_needs = metamodel.needs_external_needs

needs_default_layout = 'clean_with_edit_link'

# -- custom extensions ---------------------------------------

from docutils import nodes  # noqa: E402
from sphinx.application import Sphinx  # noqa: E402
from sphinx.directives import SphinxDirective  # noqa: E402


class NeedExampleDirective(SphinxDirective):
    """Directive to add example content to the documentation.

    It adds a container with a title, a code block, and a parsed content block.
    """

    optional_arguments = 1
    final_argument_whitespace = True
    has_content = True

    def run(self):
        count = self.env.temp_data.setdefault("needs-example-count", 0)
        count += 1
        self.env.temp_data["needs-example-count"] = count
        root = nodes.container(classes=["needs-example"])
        self.set_source_info(root)
        title = f"Example {count}"
        title_nodes, _ = (
            self.state.inline_text(f"{title}: {self.arguments[0]}", self.lineno)
            if self.arguments
            else ([nodes.Text(title)], [])
        )
        root += nodes.rubric("", "", *title_nodes)
        code = nodes.literal_block(
            "", "\n".join(self.content), language="rst", classes=["needs-example-raw"]
        )
        root += code
        parsed = nodes.container(classes=["needs-example-raw"])
        root += parsed
        self.state.nested_parse(self.content, self.content_offset, parsed)
        return [root]


def setup(app):
    app.add_config_value(name = 'gitlink_edit_url_to_git_hoster', default = git_hoster_edit_url, rebuild = '', types = [str])

    app.add_directive("example", NeedExampleDirective)

    add_dynamic_function(app, get_githoster_edit_url_for_need)

    for func in metamodel.needs_functions:
        add_dynamic_function(app, func)

