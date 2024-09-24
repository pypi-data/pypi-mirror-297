# conf.py adjustments

import sys
from MPSPlots.styles import use_mpsplots_style
import TradeTide

from TradeTide.directories import project_path, doc_css_path

sys.path.insert(0, project_path)
sys.path.insert(0, project_path.joinpath('TradeTide'))


def setup(app):
    app.add_css_file(str(doc_css_path))


autodoc_mock_imports = [
    'numpy',
    'matplotlib',
    'numpydoc',
    'MPSPlots',
]

project = 'TradeTide'
copyright = '2024, Martin Poinsinet de Sivry-Houle'
author = 'Martin Poinsinet de Sivry-Houle'

version = TradeTide.__version__

extensions = [
    'sphinx.ext.mathjax',
    'numpydoc',
    'sphinx_gallery.gen_gallery',
]

def reset_mpl(gallery_conf, fname):
    use_mpsplots_style()

sphinx_gallery_conf = {
    'examples_dirs': '../examples',
    'gallery_dirs': 'gallery',
    'image_scrapers': ('matplotlib'),
    'ignore_pattern': '/__',
    'plot_gallery': True,
    'thumbnail_size': [600, 600],
    'download_all_examples': False,
    'reset_modules': reset_mpl,
    'line_numbers': False,
    'remove_config_comments': True,
    'capture_repr': ('_repr_html_', '__repr__'),
    'nested_sections': True,
}

autodoc_default_options = {
    'members': False,
    'members-order': 'bysource',
    'undoc-members': False,
    'show-inheritance': True,
}

numpydoc_show_class_members = False

source_suffix = '.rst'
master_doc = 'index'
language = 'en'
highlight_language = 'python3'

html_theme = "pydata_sphinx_theme"

exclude_trees = []
default_role = "autolink"
pygments_style = "sphinx"

# Sphinx-gallery configuration
binder_branch = "main"
major, minor = version[:2]
binder_branch = f"v{major}.{minor}.x"

html_theme_options = {
    "logo": {
        "alt_text": "TradeTide's logo",
        "text": "TradeTide",
        "link": "https://your-github-username.github.io/TradeTide/",  # Update this for GitHub Pages
    },
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/MartinPdeS/TradeTide",
            "icon": "fa-brands fa-github",
        },
        {
            "name": "PyPI",
            "url": "https://pypi.org/project/tradetide/",
            "icon": "fa-solid fa-box",
        },
    ],
    "navbar_align": "left",
    "navbar_end": ["version-switcher", "navbar-icon-links"],
    "show_prev_next": False,
    "show_version_warning_banner": True,
    "footer_start": ["copyright"],
    "footer_end": ["sphinx-version", "theme-version"],
    "pygment_light_style": "default",
    "pygment_dark_style": "github-dark",
}

htmlhelp_basename = 'TradeTidedoc'
latex_elements = {}
latex_documents = [
    (master_doc, 'TradeTide.tex', 'TradeTide Documentation',
     'Martin Poinsinet de Sivry-Houle', 'manual'),
]
man_pages = [
    (master_doc, 'tradetide', 'TradeTide Documentation',
     [author], 1)
]
texinfo_documents = [
    (master_doc, 'TradeTide', 'TradeTide Documentation',
     author, 'TradeTide', 'One line description of project.',
     'Miscellaneous'),
]

epub_title = project
html_static_path = ['_static']
templates_path = ['_templates']
html_css_files = ['default.css']
epub_exclude_files = ['search.html']
