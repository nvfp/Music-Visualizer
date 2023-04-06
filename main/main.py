import os
import subprocess as sp

from main.arg_parser import Args
from main.utils import printer, hex_to_rgb



def render(
    ffmpeg_pth: str,
    music_file_pth: str,
    output_file_pth: str,
    codec,

    r: str,

    title_font,
    title_color,
    pad_color,

    cqt_color_left,
    cqt_color_right,
    cqt_g,
    cqt_bar_t,
    cqt_bar_v,
    cqt_tc,
    cqt_notes_font,

    diff_color_add,
    diff_color_fade,
    diff_rotate,

    spec_color,
    spec_scale,
    spec_saturation,
    spec_win_func,
    spec_drange,

    waves_freqs_color_left,
    waves_freqs_color_right,
    vol_color,
):
    ratios = [str(round(c/255, 2)) for c in hex_to_rgb(cqt_color_left)] + [str(round(c/255, 2)) for c in hex_to_rgb(cqt_color_right)]
    cqt_color = '|'.join(ratios)

    r1, g1, b1 = hex_to_rgb(diff_color_add)
    r2, g2, b2 = hex_to_rgb(diff_color_fade)
    diff_color = f'rc={r1}:gc={g1}:bc={b1}:ac=255: rf={r2}:gf={g2}:bf={b2}:af=5'

    filter_complex = (
        '[0:a]'
            'showcqt='
            's=800x360'
            f': fps={r}'
            f': sono_h=0'
            f': bar_g={cqt_g}'
            f': sono_g={cqt_g}'
            f': bar_t={cqt_bar_t}'
            f': bar_v={cqt_bar_v}'
            f': sono_v=bar_v'
            f': tc={cqt_tc}'
            f': cscheme={cqt_color}'
            f": fontfile='{cqt_notes_font}'"
            f': fontcolor=0xF7EF8A'

            f", drawtext=fontfile='{title_font}':fontcolor={title_color}:x=5:y=5:fontsize=14:text=CQT"
        '[sc]'

        '; [0:a]'
            'avectorscope='
            's=270x360'
            f': r={r}'
            f': draw=line'
            f': scale=cbrt'
            f': mirror=none'
            f': {diff_color}'

            f', pad=454:360:92:0:black'
            
            f", rotate='(PI/180)*{-90 + diff_rotate}'"

            f', pad=456:360:1:0:{pad_color}'

            f", drawtext=fontfile='{title_font}':fontcolor={title_color}:x=5:y=5:fontsize=14:text=Diff"
        '[avs]'

        '; [sc][avs]hstack[up]'

        '; [0:a]'
            'showspectrum='
            's=628x359'
            f': slide=scroll'
            f': color={spec_color}'
            f': scale={spec_scale}'
            f': fscale=log'
            f': saturation={spec_saturation}'
            f': win_func={spec_win_func}'
            f': fps={r}'
            f': drange={spec_drange}'

            f', pad=628:360:0:1:{pad_color}'
            
            f", drawtext=fontfile='{title_font}':fontcolor={title_color}:x=5:y=5:fontsize=14:text=Spectrum"
        '[ss]'

        '; [0:a]'
            'showwaves='
            's=626x179'
            f': mode=p2p'
            f': r={r}'
            f': split_channels=1'
            f': colors={waves_freqs_color_left}|{waves_freqs_color_right}'
            f': draw=full'

            f', pad=628:180:1:1:{pad_color}'
            
            f", drawtext=fontfile='{title_font}':fontcolor={title_color}:x=5:y=5:fontsize=14:text=Waves"
        '[sw]'

        '; [0:a]'
            'showfreqs='
            's=626x179'
            f': rate={r}'  # it looks like some versions of ffmpeg have this bug, comment out this line if your ffmpeg doesn't support this option
            f': mode=line'
            f': cmode=separate'
            f': ascale=cbrt'
            f': fscale=log'
            f': win_func=gauss'
            f': colors={waves_freqs_color_left}|{waves_freqs_color_right}'

            f', pad=628:180:1:1:{pad_color}'
            
            f", drawtext=fontfile='{title_font}':fontcolor={title_color}:x=5:y=5:fontsize=14:text=Power"
        '[sf]'

        '; [sw][sf]vstack[down_right]'
        '; [ss][down_right]hstack[down]'
        '; [up][down]vstack[left]'

        '; [0:a]'
            'showvolume='
            f'r={r}'
            f': b=0'
            f': w=720'
            f': h=12'
            f': f=0'
            f': c={vol_color}'
            f': t=0'
            f': v=0'
            f': o=v'
            f': dm=1'
            f': dmc=0xb7d7f5'

            f", drawtext=fontfile='{title_font}':fontcolor={title_color}:x=2:y=5:fontsize=14:text=Vol"
        '[right]'

        '; [left][right]'
            'hstack'
        '[out_v]'
    )
    code = sp.call([
        ffmpeg_pth,
        '-v', 'error', '-stats',
        '-hwaccel', 'auto',
        '-i', music_file_pth,
        '-filter_complex', filter_complex,
        '-map', '[out_v]',
        '-map', '0:a',
        *codec,
        '-c:a', 'copy',
        '-r', r,
        output_file_pth
    ])
    return code


def main():

    n_rendered = 0

    for idx, input in enumerate(Args.input):
        filename = os.path.basename(input)
        filename_base = os.path.splitext(filename)[0]
        output_file_pth = os.path.join(Args.output, f'{filename_base}.mp4')
        if os.path.exists(output_file_pth):
            printer(f'WARNING: file already exists: {output_file_pth}')
            continue

        printer(f'Rendering [{idx+1}/{len(Args.input)}] "{filename_base}"')
        code = render(
            Args.ffmpeg_pth,

            input,
            output_file_pth,
            Args.codec,

            str(Args.r),

            Args.title_font,
            Args.title_color,
            Args.pad_color,

            Args.cqt_color_left,
            Args.cqt_color_right,
            Args.cqt_gamma,
            Args.cqt_bar_transparency,
            Args.cqt_bar_volume,
            Args.cqt_timeclamp,
            Args.cqt_notes_font,

            Args.diff_color_add,
            Args.diff_color_fade,
            Args.diff_rotate,

            Args.spec_color,
            Args.spec_scale,
            Args.spec_saturation,
            Args.spec_win_func,
            Args.spec_drange,

            Args.waves_color_left,
            Args.waves_color_right,
            Args.vol_color,
        )
        if code != 0:
            printer('WARNING: Oops, something went wrong.')
            continue

        printer(f'Render finished, at {output_file_pth}')
        n_rendered += 1

    printer(f'Done, {n_rendered}/{len(Args.input)} music rendered.')