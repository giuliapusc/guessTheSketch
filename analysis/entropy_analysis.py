import argparse
from pathlib import Path
import numpy as np
import pandas as pd

from skimage import io
from skimage.measure import shannon_entropy
from skimage.color import rgb2gray
from skimage.filters.rank import entropy
from skimage.morphology import footprint_rectangle
from skimage.util import img_as_ubyte

import matplotlib.pyplot as plt

def compute_entropy(image, blocksize=8):
    entropy_full_img = entropy(img_as_ubyte(image), footprint_rectangle((blocksize, blocksize)), shift_x=-blocksize//2, shift_y=-blocksize//2)

    entropy_grid=entropy_full_img[::blocksize, ::blocksize]

    # compute the number of pixels for each block
    height, width=image.shape
    n_pixels=np.full_like(entropy_grid, blocksize**2)

    last_height=height%blocksize if height%blocksize!=0 else blocksize
    last_width=width%blocksize if width%blocksize!=0 else blocksize

    n_pixels[-1,:-1]= last_height*blocksize # last row
    n_pixels[:-1,-1]= last_width*blocksize # last col
    n_pixels[-1,-1]= last_height*last_width # last cell
    #

    nz_entropy_grid=entropy_grid[entropy_grid!=0]
    nz_n_pixels=n_pixels[entropy_grid!=0]

    avg=np.average(nz_entropy_grid, weights=nz_n_pixels)
    std=np.sqrt(np.average((nz_entropy_grid-avg)**2, weights=nz_n_pixels))

    return avg, std, entropy_grid, n_pixels

def compute_entropy_slow(image, blocksize=8):
    entropy_img=np.zeros_like(image)

    height, width=image.shape
    for i in range(0, height, blocksize):
        for j in range(0, width, blocksize):
            entropy_img[i:i+blocksize,j:j+blocksize]=shannon_entropy(image[i:i+blocksize,j:j+blocksize])

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
        default=[2, 4, 8, 16, 32, 64],
        help="Block size as a list of integers (default: [2, 4, 8, 16, 32, 64]). Example: --blocksize 2, 4, 8, 16, 32, 64"
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
            m, s, e_i, n_p=compute_entropy(image, b)

            # testing
            m_slow, s_slow, _=compute_entropy_slow(image, b)
            np.testing.assert_allclose(m, m_slow, err_msg=f"[m] {subj_id}, {file_name}, {b}")
            np.testing.assert_allclose(s, s_slow, err_msg=f"[s] {subj_id}, {file_name}, {b}")
            
            
            results.append((subj_id, file_name, b, m, s))

    pd.DataFrame(results, columns=["subj_id", "file_name", "blocksize", "mean_entropy", "std_entropy"]).to_csv(output, index=False)