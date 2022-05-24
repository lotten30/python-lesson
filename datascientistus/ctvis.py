import numpy as np
import pandas as pd
from glob import glob
import nibabel as nib


def _get_df(base_path='public-covid-data', folder='rp_im'):
    data_dict = pd.DataFrame({'FilePath': glob('{}/{}/*'.format(base_path, folder)),
                               'FileName': [p.split('/')[-1] for p in glob('{}/{}/*'.format(base_path, folder))]})
    return data_dict 


def get_df_all(base_path='public-covid-data'):
    """
    base_path以下のフォルダのパスをデータフレームで返す
    
    Parameters
    ---------------
        base_path(str): データを保存しているフォルダのパス
        (default = 'public-covid-data)
    
    Returns
    ---------------
        DataFrame:
            FilePathImage: イメージファイルのパス
            FileName: ファイル名
            FilePathMask: マスクファイルのパス
    """
    
    rp_im_df = _get_df(base_path, 'rp_im')
    rp_msk_df = _get_df(base_path, 'rp_msk')
    return rp_im_df.merge(rp_msk_df, on='FileName', suffixes=('Image', 'Mask'))


def load_nifti(path):
    """
    NIfTIファイルをNumpy Arrayとして読み込む

    Parameters
    ----------
        path(str): NIfTIファイルのパス

    Returns
    ----------
        Numpy Array (shape=(height, width, z))
    """
    nifti = nib.load(path)
    data = nifti.get_fdata()
    return np.rollaxis(data, 1, 0)