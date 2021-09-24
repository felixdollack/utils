import argparse
import fitz
import os


def extract_1st_page(infile, should_rescale):
    # open document and load 1st page
    doc = fitz.open(infile)
    page = doc.loadPage(0)

    # if scaling is desired scale to a4
    if should_rescale:
        tmp = fitz.open()
        if page.rect.width > page.rect.height:
            fmt = fitz.PaperRect("a4-l")  # landscape if input suggests
        else:
            fmt = fitz.PaperRect("a4")
        rescaled = tmp.newPage(width = fmt.width, height = fmt.height)
        rescaled.showPDFpage(rescaled.rect, doc, page.number)
        page = rescaled

    # get page as pixels to return and close document
    pix = page.getPixmap()
    doc.close()
    return pix


def main(args):
    # extract input arguments
    path = args.inpath
    outpath = args.outpath
    extension = args.ext.lower()
    rescale = args.scale

    # list files in input folder
    files = [os.path.join(path, x) for x in os.listdir(path) if x.endswith('.pdf')]

    for file in files:
        coverpage = extract_1st_page(file, rescale)

        # create output filename
        filename = os.path.basename(file)
        outfile = os.path.join(outpath, filename[:-3] + extension)

        # save cover page
        coverpage.writePNG(outfile)


if __name__ == '__main__':
    """
Usage:

# minimal (default output folder is coverpages and extension is png)
python extractPaperCover.py folder

# using a different output folder
python extractPaperCover.py folder -o outputFolder

# using a different file extension
python extractPaperCover.py folder -e jpeg"""

    parser = argparse.ArgumentParser(description="""Load a pdf, extract the 1st page and save it with extension (default=png) to output path (default=coverpages)""")
    parser.add_argument('inpath', help='Path to folder with all papers')
    parser.add_argument('-o', '--outpath', default="coverpages", help='Output path of paper cover pages')
    parser.add_argument('-e', '--ext', default='png', help='Output file extension')
    parser.add_argument('-s', '--scale', default=True, action='store_true', help='Flag to rescale pages to A4 (default=True)')
    args = parser.parse_args()

    if not os.path.exists(args.outpath):
        os.mkdir(args.outpath)

    main(args)
