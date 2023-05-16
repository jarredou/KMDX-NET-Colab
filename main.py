## DO NOT CHANGE THIS FILE

import os
import numpy as np
import soundfile
import time
import argparse
import os

import pathlib

from my_submission.music_separation_model import MusicSeparationModel

MySeparationModel = MusicSeparationModel

class Separator:
    """
        Entrypoint for the evaluator to connect to the user's agent
        Abstracts some operations that are done on client side
            - Reading sound files from shared disk
            - Checking predictions for basic issues
            - Writing predictions to shared disk
    """
    def __init__(self):
                 
        self.model = MySeparationModel()
        self.instruments = ['bass', 'drums', 'other', 'vocals']

    def raise_aicrowd_error(self, msg):
        """ Will be used by the evaluator to provide logs """
        raise NameError(msg)

    def check_output(self, separated_music_arrays, output_sample_rates):
        assert set(self.instruments) == set(separated_music_arrays.keys()), "All instrument not present"
    
    def save_prediction(self, prediction_path, separated_music_arrays, output_sample_rates):
        if not os.path.exists(prediction_path):
            os.mkdir(prediction_path)
        
        for instrument in self.instruments:

            filename = pathlib.Path(args.input).stem
            folder_path = os.path.join(prediction_path, filename)
            full_path = os.path.join(prediction_path, filename, f'{filename}_{instrument}.wav')
            pathlib.Path(folder_path).mkdir(parents=True, exist_ok=True)

            soundfile.write(full_path, 
                            data=separated_music_arrays[instrument],
                            samplerate=output_sample_rates[instrument])        

    def separate_music_file(self, song_path):
        
        music_array, samplerate = soundfile.read(song_path)
        
        separated_music_arrays, output_sample_rates = self.model.separate_music_file(music_array, samplerate)

        self.check_output(separated_music_arrays, output_sample_rates)
        
        prediction_path = os.path.join(args.output)
        self.save_prediction(prediction_path, separated_music_arrays, output_sample_rates)

        return True



def main():
  global args
  p = argparse.ArgumentParser()
  p.add_argument('--input', '-i', type=str, required=True)
  p.add_argument('--output','-o', default='separated/',
                              help='Output path')
  p.add_argument('--shifts','-S', default=0, type=int,
                              help='Predict with randomised equivariant stabilisation')
  args = p.parse_args()
  
  S = Separator()
  S.separate_music_file(song_path=args.input)

if __name__ == '__main__':
    start_time = time.perf_counter()
    main()
    
    print("Successfully completed music demixing.")
    print(f"Files saved in {args.output}{pathlib.Path(args.input).stem}/...")
    print('Total time: {0:.{1}f}s'.format(time.perf_counter() - start_time, 1))
