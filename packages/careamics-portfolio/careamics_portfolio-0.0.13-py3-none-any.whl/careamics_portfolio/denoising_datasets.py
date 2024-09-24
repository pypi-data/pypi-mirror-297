from .portfolio_entry import PortfolioEntry

DENOISING = "denoising"


class CARE_U2OS(PortfolioEntry):
    """U2OS cells with artificial noise dataset.

    Attributes
    ----------
        portfolio (str): Name of the portfolio to which the dataset belong.
        name (str): Name of the dataset.
        url (str): URL of the dataset.
        description (str): Description of the dataset.
        license (str): License of the dataset.
        citation (str): Citation to use when referring to the dataset.
        file_name (str): Name of the downloaded file.
        hash (str): SHA256 hash of the downloaded file.
        size (int): Size of the dataset in MB.
        tags (list[str]): List of tags associated to the dataset.
        is_zip (bool): Whether the dataset is a zip file.
    """

    def __init__(self) -> None:
        super().__init__(
            portfolio=DENOISING,
            name="CARE_U2OS",
            url="https://dl-at-mbl-2023-data.s3.us-east-2.amazonaws.com/"
            "image_restoration_data.zip",
            file_name="image_restoration_data.zip",
            sha256="4112d3666a4f419bbd51ab0b7853c12e16c904f89481cbe7f1a90e48f3241f72",
            description="CARE dataset used during the MBL course. Original data from"
            "the image set BBBC006v1 of the Broad Bioimage Benchmark Collection "
            "(Ljosa et al., Nature Methods, 2012). The iamges were corrupted with "
            "artificial noise.",
            license="CC0-1.0",
            citation="We used the image set BBBC006v1 from the Broad Bioimage "
            "Benchmark Collection [Ljosa et al., Nature Methods, 2012].",
            size=760.5,
            tags=["denoising", "nuclei", "fluorescence"],
        )


class N2N_SEM(PortfolioEntry):
    """SEM dataset.

    Attributes
    ----------
        portfolio (str): Name of the portfolio to which the dataset belong.
        name (str): Name of the dataset.
        url (str): URL of the dataset.
        description (str): Description of the dataset.
        license (str): License of the dataset.
        citation (str): Citation to use when referring to the dataset.
        file_name (str): Name of the downloaded file.
        hash (str): SHA256 hash of the downloaded file.
        size (int): Size of the dataset in MB.
        tags (list[str]): List of tags associated to the dataset.
        is_zip (bool): Whether the dataset is a zip file.
    """

    def __init__(self) -> None:
        super().__init__(
            portfolio=DENOISING,
            name="N2N_SEM",
            url="https://download.fht.org/jug/n2n/SEM.zip",
            file_name="SEM.zip",
            sha256="03aca31eac4d00a8381577579de2d48b98c77bab91e2f8f925999ec3252d0dac",
            description="SEM dataset from T.-O. Buchholz et al "
            "(Methods Cell Biol, 2020).",
            license="CC-BY-4.0",
            citation="T.-O. Buchholz, A. Krull, R. Shahidi, G. Pigino, G. Jékely, "
            'F. Jug, "Content-aware image restoration for electron '
            'microscopy", Methods Cell Biol 152, 277-289',
            size=172.7,
            tags=["denoising", "electron microscopy"],
        )


class N2V_BSD68(PortfolioEntry):
    """BSD68 dataset.

    Attributes
    ----------
        portfolio (str): Name of the portfolio to which the dataset belong.
        name (str): Name of the dataset.
        url (str): URL of the dataset.
        description (str): Description of the dataset.
        license (str): License of the dataset.
        citation (str): Citation to use when referring to the dataset.
        file_name (str): Name of the downloaded file.
        hash (str): SHA256 hash of the downloaded file.
        size (int): Size of the dataset in MB.
        tags (list[str]): List of tags associated to the dataset.
        is_zip (bool): Whether the dataset is a zip file.
    """

    def __init__(self) -> None:
        super().__init__(
            portfolio=DENOISING,
            name="N2V_BSD68",
            url="https://download.fht.org/jug/n2v/BSD68_reproducibility_data.zip",
            file_name="BSD68_reproducibility_data.zip",
            sha256="32c66d41196c9cafff465f3c7c42730f851c24766f70383672e18b8832ea8e55",
            description="This dataset is taken from K. Zhang et al (TIP, 2017). \n"
            "It consists of 400 gray-scale 180x180 images (cropped from the "
            "BSD dataset) and splitted between training and validation, and "
            "68 gray-scale test images (BSD68).\n"
            "All images were corrupted with Gaussian noise with standard "
            "deviation of 25 pixels. The test dataset contains the uncorrupted "
            "images as well.\n"
            "Original dataset: "
            "https://www2.eecs.berkeley.edu/Research/Projects/CS/vision/bsds/",
            license="Unknown",
            citation='D. Martin, C. Fowlkes, D. Tal and J. Malik, "A database of '
            "human segmented natural images and its application to "
            "evaluating segmentation algorithms and measuring ecological "
            'statistics," Proceedings Eighth IEEE International '
            "Conference on Computer Vision. ICCV 2001, Vancouver, BC, "
            "Canada, 2001, pp. 416-423 vol.2, doi: "
            "10.1109/ICCV.2001.937655.",
            size=395.0,
            tags=["denoising", "natural images"],
        )


class N2V_SEM(PortfolioEntry):
    """SEM dataset.

    Attributes
    ----------
        portfolio (str): Name of the portfolio to which the dataset belong.
        name (str): Name of the dataset.
        url (str): URL of the dataset.
        description (str): Description of the dataset.
        license (str): License of the dataset.
        citation (str): Citation to use when referring to the dataset.
        file_name (str): Name of the downloaded file.
        hash (str): SHA256 hash of the downloaded file.
        size (int): Size of the dataset in MB.
        tags (list[str]): List of tags associated to the dataset.
        is_zip (bool): Whether the dataset is a zip file.
    """

    def __init__(self) -> None:
        super().__init__(
            portfolio=DENOISING,
            name="N2V_SEM",
            url="https://download.fht.org/jug/n2v/SEM.zip",
            file_name="SEM.zip",
            sha256="e1999b5d10abb1714b7663463f83d0bfb73990f5e0705b6cd212c4d3e824b96c",
            description="Cropped images from a SEM dataset from T.-O. Buchholz et al "
            "(Methods Cell Biol, 2020).",
            license="CC-BY-4.0",
            citation="T.-O. Buchholz, A. Krull, R. Shahidi, G. Pigino, G. Jékely, "
            'F. Jug, "Content-aware image restoration for electron '
            'microscopy", Methods Cell Biol 152, 277-289',
            size=13.0,
            tags=["denoising", "electron microscopy"],
        )


class N2V_RGB(PortfolioEntry):
    """RGB dataset.

    Attributes
    ----------
        portfolio (str): Name of the portfolio to which the dataset belong.
        name (str): Name of the dataset.
        url (str): URL of the dataset.
        description (str): Description of the dataset.
        license (str): License of the dataset.
        citation (str): Citation to use when referring to the dataset.
        file_name (str): Name of the downloaded file.
        hash (str): SHA256 hash of the downloaded file.
        size (int): Size of the dataset in MB.
        tags (list[str]): List of tags associated to the dataset.
        is_zip (bool): Whether the dataset is a zip file.
    """

    def __init__(self) -> None:
        super().__init__(
            portfolio=DENOISING,
            name="N2V_RGB",
            url="https://download.fht.org/jug/n2v/RGB.zip",
            file_name="RGB.zip",
            sha256="4c2010c6b5c253d3a580afe744cbff969d387617c9dde29fea4463636d285657",
            description="Banner of the CVPR 2019 conference with extra noise.",
            license="CC-BY-4.0",
            citation='A. Krull, T.-O. Buchholz and F. Jug, "Noise2Void - Learning '
            'Denoising From Single Noisy Images," 2019 IEEE/CVF '
            "Conference on Computer Vision and Pattern Recognition (CVPR),"
            " 2019, pp. 2124-2132",
            size=10.4,
            tags=["denoising", "natural images", "RGB"],
        )


class Flywing(PortfolioEntry):
    """Flywing dataset.

    Attributes
    ----------
        portfolio (str): Name of the portfolio to which the dataset belong.
        name (str): Name of the dataset.
        url (str): URL of the dataset.
        description (str): Description of the dataset.
        license (str): License of the dataset.
        citation (str): Citation to use when referring to the dataset.
        file_name (str): Name of the downloaded file.
        hash (str): SHA256 hash of the downloaded file.
        size (int): Size of the dataset in MB.
        tags (list[str]): List of tags associated to the dataset.
        is_zip (bool): Whether the dataset is a zip file.
    """

    def __init__(self) -> None:
        super().__init__(
            portfolio=DENOISING,
            name="Flywing",
            url="https://download.fht.org/jug/n2v/flywing-data.zip",
            file_name="flywing-data.zip",
            sha256="01106b6dc096c423babfca47ef27059a01c2ca053769da06e8649381089a559f",
            description="Image of a membrane-labeled fly wing (35x692x520 pixels).",
            license="CC-BY-4.0",
            citation="Buchholz, T.O., Prakash, M., Schmidt, D., Krull, A., Jug, "
            "F.: Denoiseg: joint denoising and segmentation. In: European "
            "Conference on Computer Vision (ECCV). pp. 324-337. Springer (2020) 8, 9",
            size=10.2,
            tags=["denoising", "membrane", "fluorescence"],
        )


class Convallaria(PortfolioEntry):
    """Convallaria dataset.

    Attributes
    ----------
        portfolio (str): Name of the portfolio to which the dataset belong.
        name (str): Name of the dataset.
        url (str): URL of the dataset.
        description (str): Description of the dataset.
        license (str): License of the dataset.
        citation (str): Citation to use when referring to the dataset.
        file_name (str): Name of the downloaded file.
        hash (str): SHA256 hash of the downloaded file.
        size (int): Size of the dataset in MB.
        tags (list[str]): List of tags associated to the dataset.
        is_zip (bool): Whether the dataset is a zip file.
    """

    def __init__(self) -> None:
        super().__init__(
            portfolio=DENOISING,
            name="Convallaria",
            url="https://cloud.mpi-cbg.de/index.php/s/BE8raMtHQlgLDF3/download",
            file_name="Convallaria_diaphragm.zip",
            sha256="8a2ac3e2792334c833ee8a3ca449fc14eada18145f9d56fa2cb40f462c2e8909",
            description="Image of a convallaria flower (35x692x520 pixels).\n"
            "The image also comes with a defocused image in order to allow \n"
            "estimating the noise distribution.",
            license="CC-BY-4.0",
            citation="Krull, A., Vičar, T., Prakash, M., Lalit, M., & Jug, F. (2020). "
            "Probabilistic noise2void: Unsupervised content-aware denoising. Frontiers"
            " in Computer Science, 2, 5.",
            size=344.0,
            tags=["denoising", "membrane", "fluorescence"],
        )
