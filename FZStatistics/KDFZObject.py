# coding=utf-8

class KDFZObject:
    def __init__(self, value_file_name, zone_file_name, result_file_name,
                 unit,
                 wnd_type,
                 half_length, half_width,
                 radius,
                 semi_majr_length, ratio, angle,
                 stats_type, percentile,
                 div_columns, div_rows, proc_nums, threshold,
                 is_ign_nodata,
                 stats_method):

        self.value_file_name = value_file_name
        self.zone_file_name = zone_file_name
        self.result_file_name = result_file_name

        self.unit = unit

        self.wnd_type = wnd_type

        self.half_length = half_length
        self.half_width = half_width

        self.radius = radius

        self.semi_majr_length = semi_majr_length
        self.ratio = ratio
        self.angle = angle

        self.stats_type = stats_type
        self.percentile = percentile

        self.div_columns = div_columns
        self.div_rows = div_rows
        self.proc_nums = proc_nums
        self.threshold = threshold

        self.is_ign_nodata = is_ign_nodata

        self.stats_method = stats_method

