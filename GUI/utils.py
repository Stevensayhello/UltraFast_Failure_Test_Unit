# This file contain all the utils functions need for post data analysis.
import re


def lsb_to_volt(input_lsb):
    output_v = input_lsb * 2.5 / 2 ** 16
    return output_v


def attenuation(in_volt, freq):
    freq_att = 0.8799 - (3.7625 * 10 ** -10) * freq  # deal with changed due to freq
    out_volt = in_volt * 1.25 / freq_att

    return out_volt


def ready_time(in_time):
    # p = 10**-12.
    # n = 10**-9.
    time = in_time
    result = re.split(r"n|p|u", time, maxsplit=3)
    time_num = float(result[0])

    if 'p' in time:
        return time_num * 10 ** -12
    elif 'n' in time:
        return time_num * 10**-9
    else:
        return time_num * 10**-6
