import os
from itertools import batched
import glob
import subprocess
from tempfile import TemporaryDirectory

from PyPDF2 import PdfMerger

from .layout_page import layout_page
from .base_component import Face
from .utils import output_path, inkscape_path


def create_components(component_types: list, name, show_border: bool = False, show_margin: bool = False,
                      keep_as_svg: bool = False, face: str = Face.FRONT, extra_config: dict = None) -> None:
    num_components_on_page = component_types[0].cols * component_types[0].rows

    components = []
    for component_type in component_types:
        components.extend(component_type.create_components(extra_config))

    if face == Face.TEMPLATE:
        components = components[:num_components_on_page]

    with TemporaryDirectory() as folder:
        for i, components_on_page in enumerate(batched(components, num_components_on_page), 1):
            doc = layout_page(components_on_page, show_border=show_border, show_margin=show_margin, face=face)
            if keep_as_svg:
                output_file = output_path(f"{name}.svg")
                doc.save_svg(output_file)
                print(f"Written {len(components)} components to {output_file}")
            else:
                doc.save_svg(os.path.join(folder, f"drawing_{i:03}.svg"))

        if not keep_as_svg:
            subprocess.check_call([
                inkscape_path(),
                f"--export-type=pdf",
                *sorted(glob.glob(os.path.join(folder, "*.svg"))),
            ])

            merge_pdfs(len(components), name, folder)


def merge_pdfs(num_components: int, name, folder: str):
    output_file = output_path(f"{name}.pdf")

    with PdfMerger() as merger:
        for pdf in sorted(glob.glob(os.path.join(folder, "*.pdf"))):
            merger.append(pdf)

        merger.write(output_file)

    print(f"Written {num_components} components to {output_file}")
