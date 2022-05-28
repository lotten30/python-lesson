import numpy as np
import pandas as pd
from glob import glob
import nibabel as nib
import matplotlib.pyplot as plt


def _get_df(base_path='public-covid-data', folder='rp_im'):
    data_dict = pd.DataFrame({'FilePath': glob('{}/{}/*'.format(base_path, folder)),
                              'FileName': [p.split('/')[-1] for p in glob('{}/{}/*'.format(base_path, folder))]})
    
    return data_dict


def get_df_all(base_path='public-covid-data'):
    """
    base_path以下のフォルダのパスをデータフレームで返す

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

    Returns
    ----------
        Numpy Array (shape=(height, width, z))
    """
    nifti = nib.load(path)
    data = nifti.get_fdata()

    return np.rollaxis(data, 1, 0)


def label_color(mask_volume,
                ggo_color=[255, 0, 0],
                consolidation_color=[0, 255, 0],
                effusion_color=[0, 0, 255]):
    """
    Maskデータ(h, w, z)をRGBカラー画像データ(h, w, z, 3)に変換する

    Parameters
    ----------
        mask_volume(ndarray): (h, w, z)が0~3までのNumpy Array
        ggo_color(list): GGOラベル(ラベル=1)のRGB値
        consolidation_color(list): Consolidationラベル(ラベル=2)のRGB値
        effusion_color(list): Effusionラベル(ラベル=3)のRGB値

    Returns
    ----------
        mask_color(ndarray): MaskデータのRGB変換後データ(h, w, z, 3)
    """

    shp = mask_volume.shape
    # 箱作成
    mask_color = np.zeros((shp[0], shp[1], shp[2], 3), dtype=np.float32)
    # 色付け
    mask_color[np.equal(mask_volume, 1)] = ggo_color
    mask_color[np.equal(mask_volume, 2)] = consolidation_color
    mask_color[np.equal(mask_volume, 3)] = effusion_color

    return mask_color


def hu_to_gray(volume):
    """
    CTデータをHUからグレースケール(0~255)に変換する

    Returns
    ----------
        volume_rerange(ndarray): 0~255のグレースケール
    """

    maxhu = np.max(volume)
    minhu = np.min(volume)
    volume_rerange = (volume - minhu)/max((maxhu - minhu), 1e-3)
    volume_rerange = volume_rerange * 255
    volume_rerange = np.stack(
        [volume_rerange, volume_rerange, volume_rerange], axis=-1)

    return volume_rerange.astype(np.uint8)


def overlay(gray_volume, mask_volume, mask_color, alpha=0.3):
    """
    グレースケールのCTとマスクデータを重ね合わせる(overlay)

    Parameters
    ----------
        gray_volume(ndarray): CTデータのグレースケールデータ(shape=(h, w, z, 3))
        mask_volume(ndarray): Maskデータ(shape=(h, w, z))
        mask_color(ndarray): MaskデータのRGBデータ(shape=(h, w, z, 3))
        alpha(float): 0.0-1.0でマスクの透明度 0に近いほど透明

    Returns
    ----------
        overlayed(ndarray): CTとマスクのoverlayされたNumPy Array (shape=(h, w, z, 3))
    """

    mask_filter = np.greater(mask_volume, 0)
    mask_filter = np.stack([mask_filter, mask_filter, mask_filter], axis=-1)
    overlayed = np.where(mask_filter, ((1-alpha)*gray_volume +
                         alpha*mask_color).astype(np.uint8), gray_volume)

    return overlayed


def vis_overlay(overlayed,
                original_volume,
                mask_volume,
                cols=5,
                display_num=50,
                figsize=(15, 15)):
    """


    Parameters
    ----------
        overlayed(ndarray): CTとマスクのoverlayされたNumPy Array (shape=(h, w, z, 3))
        cols(int): 列数
        display_num(int): グラフ化する枚数
        figsize(tuple): 表示する画像のサイズ

    Returns
    ----------

    """

    rows = (display_num-1) // cols + 1
    total_num = overlayed.shape[-2]
    interval = total_num / display_num
    if interval < 1:
        interval = 1
    fig, ax = plt.subplots(rows, cols, figsize=figsize)
    for i in range(display_num):
        row_i = i//cols
        col_i = i % cols
        idx = int((i*interval))
        if idx >= total_num:
            break
        stats = get_hu_stats(original_volume[:, :, idx], mask_volume[:, :, idx])
        title = 'slice #: {}'.format(idx)
        title += '\nggo_mean: {:.0f}±{:.0f}'.format(stats['ggo_mean'], stats['ggo_std'])
        title += '\nconsolidation_mean: {:.0f}±{:.0f}'.format(stats['consolidation_mean'], stats['consolidation_std'])
        title += '\neffusion_mean: {:.0f}±{:.0f}'.format(stats['effusion_mean'], stats['effusion_std'])
        ax[row_i, col_i].imshow(overlayed[:, :, idx])
        ax[row_i, col_i].set_title(title)
        ax[row_i, col_i].axis('off')
    fig.tight_layout()


def get_hu_stats(volume,
                 mask_volume,
                 label_dict={1: 'ggo', 2: 'consolidation', 3: 'effusion'}):
    """


    Parameters
    ----------
        volume(ndarray): 
        mask_volume(ndarray): 
        label_dict(dict): 

    Returns
    ----------

    """

    result = {}
    for label in label_dict.keys():
        prefix = label_dict[label]
        roi_hu = volume[np.equal(mask_volume, label)]
        result[prefix + '_mean'] = np.mean(roi_hu)
        result[prefix + '_std'] = np.std(roi_hu)

    return result
