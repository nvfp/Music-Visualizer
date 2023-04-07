## Music-Visualizer
Visualizing various aspects of music: CQT, channel differences, spectrums, waves, power, and volumes.

[![An example of the visualization](/img.jpg)](https://www.youtube.com/watch?v=OXY-12lkqgE)

### [Demo video](https://www.youtube.com/watch?v=OXY-12lkqgE).

## How to install
1. Download this repository and save it to your machine (e.g. ~/code/Music-Visualizer)
2. Install [FFmpeg](https://ffmpeg.org/download.html) on your machine, if it is not already installed.

## Introductory usage
- Take a look at all the available options
    ```sh
    python Music-Visualizer -h
    ```
- Single file
    ```sh
    python Music-Visualizer -i music.mp3
    ```
    ```sh
    python Music-Visualizer -i full/path/to/the/music.m4a
    ```
    With custom output dir:
    ```sh
    python Music-Visualizer -i music.wav -o abs/path/to/the/folder
    ```
    With custom ffmpeg:
    ```sh
    python Music-Visualizer -i music.wav -ff ~/ffmpeg/bin/ffmpeg.exe
    ```
- Multiple files
    ```sh
    python Music-Visualizer -i folder/of/music
    ```
- Using GPU
    - AMD:
        ```sh
        python Music-Visualizer -i folder/of/music -g a
        ```
    - NVIDIA:
        ```sh
        python Music-Visualizer -i folder/of/music -g n
        ```
    Lossless render (full quality):
    ```sh
    python Music-Visualizer -i folder/of/music -g n -q 0
    ```
- 60 frames per second
    ```sh
    python Music-Visualizer -i music.m4a -r 60
    ```

## Customized style
- custom title font:
    - Linux:
        ```sh
        python Music-Visualizer -i music.m4a -tf ~/.fonts/Arial.ttf
        ```
    - Windows:
        ```sh
        python Music-Visualizer -i music.m4a -tf C\:/Windows/Fonts/Arial.ttf
        ```
    - MacOS:
        ```sh
        python Music-Visualizer -i music.m4a -tf /Library/Fonts/Arial.ttf
        ```
- color scheme:
    ```sh
    python Music-Visualizer -i music.m4a -pc #fafbfa -wcl #3280c9 -wcr #32c958 -vc #ee2020
    ```

## Limitations
- The only resolution option available is HD (1280x720)

## Troubleshooting
- if you encounter this error message `Option 'rate' not found`, search for "#BUG" in `main/main.py` and follow the written instructions
- if `--vol_color` showing wrong color, check the comments near the end of the file `main/arg_parser.py`

## License
This project is licensed under the MIT license.
