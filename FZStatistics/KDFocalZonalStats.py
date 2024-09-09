# coding=utf-8
import os, sys
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from osgeo import gdal, gdal_array, gdalconst
import numpy as np
import itertools
from functools import partial
import multiprocessing as mp
import configparser

gl_nodata = -9999.0
import math

def divide(shape, div_columns, div_rows, wnd_size):
    blocks = []

    div_xsize = int(np.ceil(shape[0] / div_columns))
    div_ysize = int(np.ceil(shape[1] / div_rows))

    fringe_x = wnd_size[1] // 2
    fringe_y = wnd_size[0] // 2

    for y in range(0, shape[1], div_ysize):
        if y + div_ysize < shape[1]:
            rows = div_ysize
        else:
            rows = shape[1] - y

        for x in range(0, shape[0], div_xsize):

            if x + div_xsize < shape[0]:
                cols = div_xsize
            else:
                cols = shape[0] - x

            right = x + cols - 1
            down = y + rows - 1

            div_pos = np.array([x, right, y, down,
                                max(0, x - fringe_x),
                                min(shape[0] - 1, right + fringe_x),
                                max(0, y - fringe_y),
                                min(shape[1] - 1, down + fringe_y)]).astype(np.int32)
            blocks.append(div_pos)

    return blocks


def arr_stats_ign_nodata(arr, stats_type, percentile):
    rst = gl_nodata

    if stats_type == "MEAN":
        rst = np.nanmean(arr)
    elif stats_type == "PERCENTILE":
        rst = np.nanpercentile(arr, percentile)
    elif stats_type == "STD":
        rst = np.nanstd(arr)
    elif stats_type == "MAXIMUM":
        rst = np.nanmax(arr)
    elif stats_type == "MINIMUM":
        rst = np.nanmin(arr)
    elif stats_type == "SUM":
        rst = np.nansum(arr)
    elif stats_type == "MEDIAN":
        rst = np.nanmedian(arr)
    elif stats_type == "VARIETY":
        rst = np.nanvar(arr)
    elif stats_type == "RANGE":
        rst = np.nanmax(arr) - np.nanmin(arr)
    elif stats_type == "MAJORITY":
        flat_arr = np.ravel(arr)
        valid_vals = flat_arr[~np.isnan(flat_arr)]
        uniq_elems, counts = np.unique(valid_vals, return_counts=True)
        rst = uniq_elems[np.argmax(counts)]
    elif stats_type == "MINORITY":
        flat_arr = np.ravel(arr)
        valid_vals = flat_arr[~np.isnan(flat_arr)]
        uniq_elems, counts = np.unique(valid_vals, return_counts=True)
        rst = uniq_elems[np.argmin(counts)]
    elif stats_type == "CELLS COUNT":
        flat_arr = np.ravel(arr)
        valid_vals = flat_arr[~np.isnan(flat_arr)]
        rst = len(valid_vals)
    elif stats_type == "COEFFICIENT OF VARIATION":
        std = np.nanstd(arr)
        mean = np.nanmean(arr)
        rst = std / mean

    return rst


def arr_stats(arr, stats_type, percentile):
    rst = gl_nodata
    if stats_type == "MEAN":
        rst = np.mean(arr)
    elif stats_type == "PERCENTILE":
        rst = np.percentile(arr, percentile)
    elif stats_type == "STD":
        rst = np.std(arr)
    elif stats_type == "MAXIMUM":
        rst = np.max(arr)
    elif stats_type == "MINIMUM":
        rst = np.min(arr)
    elif stats_type == "SUM":
        rst = np.sum(arr)
    elif stats_type == "MEDIAN":
        rst = np.median(arr)
    elif stats_type == "VARIETY":
        rst = np.var(arr)
    elif stats_type == "RANGE":
        rst = np.max(arr) - np.min(arr)
    elif stats_type == "MAJORITY":
        flat_arr = np.ravel(arr)
        uniq_elems, counts = np.unique(flat_arr, return_counts=True)
        rst = uniq_elems[np.argmax(counts)]
    elif stats_type == "MINORITY":
        flat_arr = np.ravel(arr)
        uniq_elems, counts = np.unique(flat_arr, return_counts=True)
        rst = uniq_elems[np.argmin(counts)]
    elif stats_type == "CELLS COUNT":
        flat_arr = np.ravel(arr)
        rst = len(flat_arr)
    elif stats_type == "COEFFICIENT OF VARIATION":
        std = np.nanstd(arr)
        mean = np.nanmean(arr)
        rst = std / mean
    return rst


def f_stats_yx(value_arr, cond_arr,
               is_ign_nodata, threshold, stats_type, percentile,
               yx_pos):
    (y, x) = yx_pos

    y_size, x_size = value_arr.shape

    fringe_y = cond_arr.shape[0] // 2
    fringe_x = cond_arr.shape[1] // 2

    lc_x_l = max(0, x - fringe_x)
    lc_x_r = min(x_size - 1, x + fringe_x)
    lc_y_u = max(0, y - fringe_y)
    lc_y_d = min(y_size - 1, y + fringe_y)

    lc_cond_x_l = lc_x_l - (x - fringe_x)
    lc_cond_x_r = lc_x_r - (x - fringe_x)
    lc_cond_y_u = lc_y_u - (y - fringe_y)
    lc_cond_y_d = lc_y_d - (y - fringe_y)

    lc_value_arr = value_arr[lc_y_u:(lc_y_d + 1), lc_x_l:(lc_x_r + 1)]
    lc_cond_arr = cond_arr[lc_cond_y_u:(lc_cond_y_d + 1), lc_cond_x_l:(lc_cond_x_r + 1)]

    rst_arr = np.where(lc_cond_arr == True, lc_value_arr, np.NaN)

    rst = gl_nodata
    if is_ign_nodata == True:
        non_nan_count = np.count_nonzero(~np.isnan(rst_arr))
        if non_nan_count >= threshold:
            rst = arr_stats_ign_nodata(rst_arr, stats_type, percentile)
    else:
        rst = arr_stats(rst_arr, stats_type, percentile)

    return rst


def fz_stats_yx(value_arr, zone_arr, cond_arr,
                is_ign_nodata, threshold, stats_type, percentile,
                yx_pos):
    (y, x) = yx_pos

    y_size, x_size = value_arr.shape

    fringe_y = cond_arr.shape[0] // 2
    fringe_x = cond_arr.shape[1] // 2

    lc_x_l = max(0, x - fringe_x)
    lc_x_r = min(x_size - 1, x + fringe_x)
    lc_y_u = max(0, y - fringe_y)
    lc_y_d = min(y_size - 1, y + fringe_y)

    lc_cond_x_l = lc_x_l - (x - fringe_x)
    lc_cond_x_r = lc_x_r - (x - fringe_x)
    lc_cond_y_u = lc_y_u - (y - fringe_y)
    lc_cond_y_d = lc_y_d - (y - fringe_y)

    lc_value_arr = value_arr[lc_y_u:(lc_y_d + 1), lc_x_l:(lc_x_r + 1)]
    lc_zone_arr = zone_arr[lc_y_u:(lc_y_d + 1), lc_x_l:(lc_x_r + 1)]
    lc_cond_arr = cond_arr[lc_cond_y_u:(lc_cond_y_d + 1), lc_cond_x_l:(lc_cond_x_r + 1)]

    rst = gl_nodata

    cur_zone = zone_arr[y][x]
    if ~np.isnan(cur_zone):
        lc_zone_bool_arr = (lc_zone_arr == cur_zone).astype(bool)
        lc_new_cond_arr = np.logical_and(lc_zone_bool_arr, lc_cond_arr)
        rst_arr = lc_value_arr[lc_new_cond_arr]
        if is_ign_nodata == True:
            non_nan_count = np.count_nonzero(~np.isnan(rst_arr))
            if non_nan_count >= threshold:
                rst = arr_stats_ign_nodata(rst_arr, stats_type, percentile)
        else:
            rst = arr_stats(rst_arr, stats_type, percentile)
    return rst


def z_stats(value_arr, is_ign_nodata, threshold, stats_type, percentile):
    if is_ign_nodata == True:
        non_nan_count = np.count_nonzero(~np.isnan(value_arr))
        if non_nan_count >= threshold:
            rst = arr_stats_ign_nodata(value_arr, stats_type, percentile)
    else:
        rst = arr_stats(value_arr, stats_type, percentile)
    return rst


class KDFocalZonalStats:
    def __init__(self, config):
        self.config = config

    def build_tmpl(self, cell_size):
        mask = None
        if self.config.wnd_type == "RECTANGLE":
            hl = self.config.half_length
            hw = self.config.half_width
            if self.config.unit == "Map":
                hl = int(math.ceil(hl / cell_size))
                hw = int(math.ceil(hw / cell_size))
            mask = np.full((2 * hw + 1, 2 * hl + 1), True)
        elif self.config.wnd_type == "CIRCLE":
            rad = self.config.radius
            if self.config.unit == "Map":
                rad = int(math.ceil(rad / cell_size))
            n = 2 * rad + 1
            a, b = (rad, rad)
            y, x = np.ogrid[-a:n - a, -b:n - b]
            mask = x ** 2 + y ** 2 <= rad ** 2
        elif self.config.wnd_type == "ELLIPSE":
            sml = self.config.semi_majr_length
            rat = self.config.ratio
            ang = self.config.angle
            if self.config.unit == "Map":
                sml = int(math.ceil(sml / cell_size))

            a2 = sml ** 2
            b2 = (math.ceil(sml * rat)) ** 2
            ag = ang * math.pi / 180
            c2 = np.cos(ag) ** 2
            s2 = np.sin(ag) ** 2

            B = 2 * (a2 - b2) * np.sin(ag) * np.cos(ag)
            bcas = b2 * c2 + a2 * s2
            bsac = b2 * s2 + a2 * c2
            ab4 = -4 * a2 * b2
            bac = B ** 2 - 4 * bsac * bcas

            y2 = math.ceil(np.abs(np.sqrt(ab4 * bsac / bac)))
            x2 = math.ceil(np.abs(np.sqrt(ab4 * bcas / bac)))

            xp = int(x2)
            yp = int(y2)

            xx = xp * 2 + 1
            yy = yp * 2 + 1

            mask = np.full((yy, xx), False)
            for y in range(int(yy)):
                for x in range(int(xx)):
                    xt = ((np.cos(ag) * (x - xp) + np.sin(ag) * (y - yp)) ** 2) / b2
                    yt = ((np.sin(ag) * (x - xp) - np.cos(ag) * (y - yp)) ** 2) / a2
                    mask[y][x] = ((xt + yt) <= 1)
        return mask

    def process(self):
        value_ds = gdal.Open(self.config.value_file_name, gdalconst.GA_ReadOnly)
        value_band1 = value_ds.GetRasterBand(1)
        value_nodata = value_band1.GetNoDataValue()

        geotf = value_ds.GetGeoTransform()
        value_cell_size = geotf[1]

        value_shape = np.array([value_band1.XSize, value_band1.YSize])

        out_ds = value_ds.GetDriver().Create(
            self.config.result_file_name, int(value_shape[0]), int(value_shape[1]), 1,
            value_ds.GetRasterBand(1).DataType)
        out_ds.SetProjection(value_ds.GetProjection())
        out_ds.SetGeoTransform(value_ds.GetGeoTransform())

        if self.config.stats_method == "Focal Stats":
            cond_arr = self.build_tmpl(value_cell_size)
            win_size = np.array(cond_arr.shape)
            div_pos_list = divide(value_shape, self.config.div_columns, self.config.div_rows, win_size)
            print("The raster was divide into %d Areas." % len(div_pos_list))
            s = time.time()
            for i in range(len(div_pos_list)):
                start_time = time.time()
                div_pos = div_pos_list[i]
                value_arr = value_band1.ReadAsArray(int(div_pos[4]), int(div_pos[6]),
                                                    int(div_pos[5] - div_pos[4] + 1),
                                                    int(div_pos[7] - div_pos[6] + 1))

                value_arr[value_arr == value_nodata] = np.nan

                block = np.array([div_pos[0] - div_pos[4], div_pos[1] - div_pos[4],
                                  div_pos[2] - div_pos[6], div_pos[3] - div_pos[6]])

                rows = block[3] - block[2] + 1
                cols = block[1] - block[0] + 1
                yx_pos_lst = list(itertools.product(range(block[2], block[3] + 1),
                                                    range(block[0], block[1] + 1)))

                func = partial(f_stats_yx, value_arr, cond_arr,
                               self.config.is_ign_nodata, self.config.threshold,
                               self.config.stats_type, self.config.percentile)
                pool = mp.Pool(processes=self.config.proc_nums)
                rst_list = pool.map(func, yx_pos_lst)
                pool.close()
                pool.join()

                rst_arr = np.array(rst_list)
                rst_arr = rst_arr.reshape(rows, cols)

                out_ds.GetRasterBand(1).WriteArray(rst_arr, int(div_pos[0]), int(div_pos[2]))
                out_ds.GetRasterBand(1).SetNoDataValue(gl_nodata)

                estart_time = time.time()
                print(estart_time - start_time)

            e = time.time()
            print(e - s)
            print("end")
        elif self.config.stats_method == "Zonal Stats":
            value_arr = value_band1.ReadAsArray()

            zone_ds = gdal.Open(self.config.zone_file_name, gdalconst.GA_ReadOnly)
            zone_band1 = zone_ds.GetRasterBand(1)
            zone_nodata = zone_band1.GetNoDataValue()
            zone_arr = zone_band1.ReadAsArray()

            rst_arr = np.full_like(value_arr, value_nodata)

            unique_value_arr = np.unique(zone_arr[~np.isnan(zone_arr)])

            start_time = time.time()
            for value in unique_value_arr:
                if value != zone_nodata:
                    mask = (zone_arr == value)
                    v_a = value_arr[mask]
                    rst_arr[mask] = z_stats(v_a, self.config.is_ign_nodata, self.config.threshold,
                                            self.config.stats_type, self.config.percentile)
            out_ds.GetRasterBand(1).WriteArray(rst_arr)
            out_ds.GetRasterBand(1).SetNoDataValue(value_nodata)
            end_time = time.time()
            print(end_time - start_time)
            print("end")
        elif self.config.stats_method == "FZ Mixed Stats":
            zone_ds = gdal.Open(self.config.zone_file_name, gdalconst.GA_ReadOnly)
            zone_band1 = zone_ds.GetRasterBand(1)
            zone_nodata = zone_band1.GetNoDataValue()

            mask_mat = self.build_tmpl(value_cell_size)
            win_size = np.array(mask_mat.shape)
            div_pos_list = divide(value_shape, self.config.div_columns, self.config.div_rows, win_size)

            print("The raster was divide into %d Areas." % len(div_pos_list))
            s = time.time()
            for i in range(len(div_pos_list)):
                start_time = time.time()
                div_pos = div_pos_list[i]

                value_arr = value_band1.ReadAsArray(int(div_pos[4]), int(div_pos[6]),
                                                    int(div_pos[5] - div_pos[4] + 1),
                                                    int(div_pos[7] - div_pos[6] + 1))

                value_arr = value_arr.astype(np.float64)
                value_arr[value_arr == value_nodata] = np.nan

                zone_arr = zone_band1.ReadAsArray(int(div_pos[4]), int(div_pos[6]),
                                                   int(div_pos[5] - div_pos[4] + 1),
                                                   int(div_pos[7] - div_pos[6] + 1))

                zone_arr = zone_arr.astype(np.float64)
                zone_arr[zone_arr == zone_nodata] = np.nan

                block = np.array([div_pos[0] - div_pos[4], div_pos[1] - div_pos[4],
                                  div_pos[2] - div_pos[6], div_pos[3] - div_pos[6]])

                #rst_arr = self.fz_stats_mp(value_arr, zone_arr, mask_mat, block)

                rows = block[3] - block[2] + 1
                cols = block[1] - block[0] + 1

                yx_pos_lst = list(itertools.product(range(block[2], block[3] + 1),
                                                    range(block[0], block[1] + 1)))

                func = partial(fz_stats_yx, value_arr, zone_arr, mask_mat,
                               self.config.is_ign_nodata, self.config.threshold,
                               self.config.stats_type, self.config.percentile)

                pool = mp.Pool(processes=self.config.proc_nums)
                rst_list = pool.map(func, yx_pos_lst)
                pool.close()
                pool.join()

                rst_arr = np.array(rst_list)
                rst_arr = rst_arr.reshape(rows, cols)

                out_ds.GetRasterBand(1).WriteArray(rst_arr, int(div_pos[0]), int(div_pos[2]))
                out_ds.GetRasterBand(1).SetNoDataValue(gl_nodata)

                estart_time = time.time()
                print(estart_time - start_time)

            e = time.time()
            print(e - s)
            print("end")

