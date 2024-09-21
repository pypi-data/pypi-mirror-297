#!/usr/bin/env python3
"""A command line tool for extracting text and images from PDF and
output it to plain text, html, xml or tags.
"""

import argparse
import logging
import os
import sys
from typing import Any, Container, Iterable, List, Optional
import pymupdf
import layoutparser as lp
import tempfile
import urllib.request

import pdf2zh.high_level
from pdf2zh.layout import LAParams
from pdf2zh.pdfexceptions import PDFValueError
from pdf2zh.utils import AnyIO

logging.basicConfig()

OUTPUT_TYPES = ((".htm", "html"), (".html", "html"), (".xml", "xml"), (".tag", "tag"))


def float_or_disabled(x: str) -> Optional[float]:
    if x.lower().strip() == "disabled":
        return None
    try:
        return float(x)
    except ValueError:
        raise argparse.ArgumentTypeError(f"invalid float value: {x}")


def extract_text(
    files: Iterable[str] = [],
    outfile: str = "-",
    laparams: Optional[LAParams] = None,
    output_type: str = "text",
    codec: str = "utf-8",
    strip_control: bool = False,
    maxpages: int = 0,
    pages: Optional[Container[int]] = None,
    password: str = "",
    scale: float = 1.0,
    rotation: int = 0,
    layoutmode: str = "normal",
    output_dir: Optional[str] = None,
    debug: bool = False,
    disable_caching: bool = False,
    vfont: str = "",
    vchar: str = "",
    thread: int = 0,
    **kwargs: Any,
) -> AnyIO:
    if not files:
        raise PDFValueError("Must provide files to work upon!")

    if output_type == "text" and outfile != "-":
        for override, alttype in OUTPUT_TYPES:
            if outfile.endswith(override):
                output_type = alttype

    # if outfile == "-":
    #     outfp: AnyIO = sys.stdout
    #     if sys.stdout.encoding is not None:
    #         codec = "utf-8"
    # else:
    #     outfp = open(outfile, "wb")
    outfp: AnyIO = sys.stdout
    pth = os.path.join(tempfile.gettempdir(), 'mfd-tf_efficientdet_d0.pth.tar')
    if not os.path.exists(pth):
        print('Downloading...')
        urllib.request.urlretrieve("https://www.dropbox.com/s/dkr22iux7thlhel/mfd-tf_efficientdet_d0.pth.tar?dl=1",pth)
    model = lp.EfficientDetLayoutModel("lp://efficientdet/MFD/tf_efficientdet_d0",pth)

    for file in files:

        filename = os.path.splitext(os.path.basename(file))[0]

        doc_en = pymupdf.open(file)
        page_count=doc_en.page_count
        for page in doc_en:
            page.insert_font('china-ss')
            page.insert_font('helv')
        doc_en.save('output-en.pdf')
        # doc_en.close()

        # for fname in files:
        with open('output-en.pdf', "rb") as fp:
            pdf2zh.high_level.extract_text_to_fp(fp, **locals())

        doc_en.close()
        doc_zh = pymupdf.open('output-zh.pdf')
        doc_dual = pymupdf.open('output-en.pdf')
        doc_dual.insert_file(doc_zh)
        for id in range(page_count):
            doc_dual.move_page(page_count+id,id*2+1)
        doc_zh.save(f'{filename}-zh.pdf',deflate=1)
        doc_dual.save(f'{filename}-dual.pdf',deflate=1)
        doc_zh.close()
        doc_dual.close()

        os.remove('output-en.pdf')
        os.remove('output-zh.pdf')

    return


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__, add_help=True)
    parser.add_argument(
        "files",
        type=str,
        default=None,
        nargs="+",
        help="One or more paths to PDF files.",
    )

    parser.add_argument(
        "--version",
        "-v",
        action="version",
        version=f"pdf2zh v{pdf2zh.__version__}",
    )
    parser.add_argument(
        "--debug",
        "-d",
        default=False,
        action="store_true",
        help="Use debug logging level.",
    )
    # parser.add_argument(
    #     "--disable-caching",
    #     "-C",
    #     default=False,
    #     action="store_true",
    #     help="If caching or resources, such as fonts, should be disabled.",
    # )

    parse_params = parser.add_argument_group(
        "Parser",
        description="Used during PDF parsing",
    )
    parse_params.add_argument(
        "--pages",
        "-p",
        type=str,
        help="The list of page numbers to parse.",
    )
    # parse_params.add_argument(
    #     "--pagenos",
    #     "-p",
    #     type=str,
    #     help="A comma-separated list of page numbers to parse. "
    #     "Included for legacy applications, use --page-numbers "
    #     "for more idiomatic argument entry.",
    # )
    # parse_params.add_argument(
    #     "--maxpages",
    #     "-m",
    #     type=int,
    #     default=0,
    #     help="The maximum number of pages to parse.",
    # )
    parse_params.add_argument(
        "--password",
        "-P",
        type=str,
        default="",
        help="The password to use for decrypting PDF file.",
    )
    parse_params.add_argument(
        "--vfont",
        "-f",
        type=str,
        default="",
        help="The regex to math font name of formula.",
    )
    parse_params.add_argument(
        "--vchar",
        "-c",
        type=str,
        default="",
        help="The regex to math character of formula.",
    )
    parse_params.add_argument(
        "--thread",
        "-t",
        type=int,
        default=4,
        help="The number of threads to execute translation.",
    )
    # parse_params.add_argument(
    #     "--rotation",
    #     "-R",
    #     default=0,
    #     type=int,
    #     help="The number of degrees to rotate the PDF "
    #     "before other types of processing.",
    # )

    # la_params = LAParams()  # will be used for defaults
    # la_param_group = parser.add_argument_group(
    #     "Layout analysis",
    #     description="Used during layout analysis.",
    # )
    # la_param_group.add_argument(
    #     "--no-laparams",
    #     "-n",
    #     default=False,
    #     action="store_true",
    #     help="If layout analysis parameters should be ignored.",
    # )
    # la_param_group.add_argument(
    #     "--detect-vertical",
    #     "-V",
    #     default=la_params.detect_vertical,
    #     action="store_true",
    #     help="If vertical text should be considered during layout analysis",
    # )
    # la_param_group.add_argument(
    #     "--line-overlap",
    #     type=float,
    #     default=la_params.line_overlap,
    #     help="If two characters have more overlap than this they "
    #     "are considered to be on the same line. The overlap is specified "
    #     "relative to the minimum height of both characters.",
    # )
    # la_param_group.add_argument(
    #     "--char-margin",
    #     "-M",
    #     type=float,
    #     default=la_params.char_margin,
    #     help="If two characters are closer together than this margin they "
    #     "are considered to be part of the same line. The margin is "
    #     "specified relative to the width of the character.",
    # )
    # la_param_group.add_argument(
    #     "--word-margin",
    #     "-W",
    #     type=float,
    #     default=la_params.word_margin,
    #     help="If two characters on the same line are further apart than this "
    #     "margin then they are considered to be two separate words, and "
    #     "an intermediate space will be added for readability. The margin "
    #     "is specified relative to the width of the character.",
    # )
    # la_param_group.add_argument(
    #     "--line-margin",
    #     "-L",
    #     type=float,
    #     default=la_params.line_margin,
    #     help="If two lines are close together they are considered to "
    #     "be part of the same paragraph. The margin is specified "
    #     "relative to the height of a line.",
    # )
    # la_param_group.add_argument(
    #     "--boxes-flow",
    #     "-F",
    #     type=float_or_disabled,
    #     default=la_params.boxes_flow,
    #     help="Specifies how much a horizontal and vertical position of a "
    #     "text matters when determining the order of lines. The value "
    #     "should be within the range of -1.0 (only horizontal position "
    #     "matters) to +1.0 (only vertical position matters). You can also "
    #     "pass `disabled` to disable advanced layout analysis, and "
    #     "instead return text based on the position of the bottom left "
    #     "corner of the text box.",
    # )
    # la_param_group.add_argument(
    #     "--all-texts",
    #     "-A",
    #     default=la_params.all_texts,
    #     action="store_true",
    #     help="If layout analysis should be performed on text in figures.",
    # )

    # output_params = parser.add_argument_group(
    #     "Output",
    #     description="Used during output generation.",
    # )
    # output_params.add_argument(
    #     "--outfile",
    #     "-o",
    #     type=str,
    #     default="-",
    #     help="Path to file where output is written. "
    #     'Or "-" (default) to write to stdout.',
    # )
    # output_params.add_argument(
    #     "--output_type",
    #     "-t",
    #     type=str,
    #     default="text",
    #     help="Type of output to generate {text,html,xml,tag}.",
    # )
    # output_params.add_argument(
    #     "--codec",
    #     "-c",
    #     type=str,
    #     default="utf-8",
    #     help="Text encoding to use in output file.",
    # )
    # output_params.add_argument(
    #     "--output-dir",
    #     "-O",
    #     default=None,
    #     help="The output directory to put extracted images in. If not given, "
    #     "images are not extracted.",
    # )
    # output_params.add_argument(
    #     "--layoutmode",
    #     "-Y",
    #     default="normal",
    #     type=str,
    #     help="Type of layout to use when generating html "
    #     "{normal,exact,loose}. If normal,each line is"
    #     " positioned separately in the html. If exact"
    #     ", each character is positioned separately in"
    #     " the html. If loose, same result as normal "
    #     "but with an additional newline after each "
    #     "text line. Only used when output_type is html.",
    # )
    # output_params.add_argument(
    #     "--scale",
    #     "-s",
    #     type=float,
    #     default=1.0,
    #     help="The amount of zoom to use when generating html file. "
    #     "Only used when output_type is html.",
    # )
    # output_params.add_argument(
    #     "--strip-control",
    #     "-S",
    #     default=False,
    #     action="store_true",
    #     help="Remove control statement from text. "
    #     "Only used when output_type is xml.",
    # )

    return parser


def parse_args(args: Optional[List[str]]) -> argparse.Namespace:
    parsed_args = create_parser().parse_args(args=args)

    # Propagate parsed layout parameters to LAParams object
    # if parsed_args.no_laparams:
    #     parsed_args.laparams = None
    # else:
    #     parsed_args.laparams = LAParams(
    #         line_overlap=parsed_args.line_overlap,
    #         char_margin=parsed_args.char_margin,
    #         line_margin=parsed_args.line_margin,
    #         word_margin=parsed_args.word_margin,
    #         boxes_flow=parsed_args.boxes_flow,
    #         detect_vertical=parsed_args.detect_vertical,
    #         all_texts=parsed_args.all_texts,
    #     )

    if parsed_args.pages:
        pages = []
        for p in parsed_args.pages.split(","):
            if "-" in p:
                start, end = p.split("-")
                pages.extend(range(int(start) - 1, int(end)))
            else:
                pages.append(int(p) - 1)
        parsed_args.pages = pages

    # if parsed_args.pagenos:
    #     parsed_args.page_numbers = {int(x) - 1 for x in parsed_args.pagenos.split(",")}

    # if parsed_args.output_type == "text" and parsed_args.outfile != "-":
    #     for override, alttype in OUTPUT_TYPES:
    #         if parsed_args.outfile.endswith(override):
    #             parsed_args.output_type = alttype

    return parsed_args


def main(args: Optional[List[str]] = None) -> int:
    parsed_args = parse_args(args)
    extract_text(**vars(parsed_args))
    return 0


if __name__ == "__main__":
    sys.exit(main())
