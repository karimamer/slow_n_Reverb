import click
from pedalboard import Pedalboard, Chorus, Reverb, Delay, Resample
from pedalboard.io import AudioFile


@click.command()
@click.option('--input_file', type=click.Path())
@click.option('--output_file', type=click.Path())
@click.option('--samplerate',  default=44100, type=int)
@click.option('--slow_factor', default=0.5, type=float)
@click.option('--room_size', default=0.75, type=float)
@click.option('--delay_seconds', default=0.5, type=float)
def main(input_file: str, output_file: str, samplerate: int, slow_factor: float, room_size: float, delay_seconds: float):
    if slow_factor < 0.1:
        raise ValueError("Slow factor must be greater than 1")

    with AudioFile(input_file, 'r') as f:
        audio = f.read(f.frames)
        samplerate = f.samplerate * slow_factor
    
    # Make a Pedalboard object, containing multiple plugins:
    board = Pedalboard(
        [Chorus(), 
        Reverb(room_size=room_size),
        Delay(delay_seconds=delay_seconds, mix=1.0),
        Resample(samplerate)])

    effected = board(audio, samplerate)

    # Write the audio back as a wav file:
    with AudioFile(output_file, 'w', samplerate, effected.shape[0]) as f:
        f.write(effected)
    
if __name__ == '__main__':
    main()
        



