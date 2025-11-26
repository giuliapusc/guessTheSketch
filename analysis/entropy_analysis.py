import argparse
from pathlib import Path
import numpy as np
import pandas as pd

from skimage import io
from skimage.measure import shannon_entropy
from skimage.color import rgb2gray
import matplotlib.pyplot as plt


def compute_entropy(img, blocksize=8):
    entropy_img=np.zeros_like(img)

    height, width=img.shape
    for i in range(0, height, blocksize):
        for j in range(0, width,blocksize):
            entropy_img[i:i+blocksize,j:j+blocksize]=shannon_entropy(img[i:i+blocksize,j:j+blocksize])

    nz_entropy=entropy_img[entropy_img!=0]

    return nz_entropy.mean(), nz_entropy.std(), entropy_img


if __name__ == "__main__":
    # parser
    parser = argparse.ArgumentParser(description="Compute Shannon Entropy")

    parser.add_argument(
        "--folder",
        type=str,
        required=True,
        help="Path where to compute the entropy"
    )
    parser.add_argument(
        "--output",
        type=str,
        required=True,
        help="Output file for the analysis"
    )
    parser.add_argument(
        "--filter",
        action="store_true",
        help="Filter buttons in the screenshots (default: False)"
    )

    parser.add_argument(
        "--blocksize",
        type=int,
        nargs='+', 
        default=[32, 64, 128, 256],
        help="Block size as a list of integers (default: [32, 64, 128, 256]). Example: --blocksize 32, 64, 128, 256"
    )

    args = parser.parse_args()

    folder=Path(args.folder)
    blocksize=args.blocksize
    apply_button_filter=args.filter
    output=args.output

    results=[]
    for img_file in folder.glob("*/*.png"):
        subj_id = img_file.parent.name
        file_name= img_file.stem

        image = rgb2gray(io.imread(img_file))
        for b in blocksize:
            m, s, e_img=compute_entropy(image, b)
            results.append((subj_id, file_name, b, m, s))

    pd.DataFrame(results, columns=["subj_id","file_name", "blocksize", "mean_entropy", "std_entropy"]).to_csv(output, index=False)