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

def label_color(mask_volume,
                ggo_color = [255, 0, 0],
                consolidation_color = [0, 255, 0],
                effusion_color = [0, 0, 255]):

    shp = mask_volume.shape
    # 箱作成
    mask_color = np.zeros((shp[0], shp[1], shp[2], 3), dtype=np.float32)
    # 色付け
    mask_color[np.equal(mask_volume, 1)] = ggo_color
    mask_color[np.equal(mask_volume, 2)] = consolidation_color
    mask_color[np.equal(mask_volume, 3)] = effusion_color

    return mask_color

def hu_to_gray(volume):
    maxhu = np.max(volume)
    minhu = np.min(volume)
    volume_rerange = (volume - minhu)/max((maxhu - minhu), 1e-3)
    volume_rerange = volume_rerange * 255
    volume_rerange = np.stack([volume_rerange, volume_rerange, volume_rerange], axis=-1)

    return volume_rerange.astype(np.uint8)