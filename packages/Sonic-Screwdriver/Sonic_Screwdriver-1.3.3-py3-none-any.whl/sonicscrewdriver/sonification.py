from strauss.generator import Sampler
from strauss.score import Score
from strauss.sources import Events
from strauss.sonification import Sonification
from pathlib import Path
import copy
import pygame
from threading import Thread
from time import sleep
import urllib.request


def download_sampler(url, save_fn, save_dir):

    save_path = Path(f"{save_dir}",f"{save_fn}")

    with urllib.request.urlopen(url) as response, save_path.open(mode='wb') as out_file:
        print(f"\n Downloading {save_fn}")

        data = response.read() # a `bytes` object
        out_file.write(data)

    return


def load_samplers(config):

    print("\nLoading instrument samples")

    samples = {"flute": {"fn": "flute.sf2",
                         "url": "https://drive.google.com/uc?export=download&id=1DAbIitPRUUGidrhVt4wiwwXrSxOD7RDY", 
                         "preset": None},
               "guitar": {"fn": "guitars.sf2",
                          "url": "https://drive.google.com/uc?export=download&id=18CCYj8AFy7wpDdGg0ADx8GfTTHEFilrs",
                          "preset": 10},
               "piano": {"fn": "piano.sf2",
                         "url": "https://drive.usercontent.google.com/download?id=1p0jY3AgGyD9DJGWC25aEUEaydI_n1-3M&export=download&authuser=0&confirm=t&uuid=a2a840c9-12c4-4ce6-bd29-1b4b5a1dec95&at=AO7h07eGPB-DROS_JntK9vRkyPdv%3A1726224049695",
                         "preset": 1},
               "choir": {"fn": "choir.sf2",
                         "url": " https://drive.usercontent.google.com/download?id=14ZaZagjyWkCztx0WdPhJj6yBjArQtQ3O&export=download&authuser=0",
                         "preset": 1},
               "cello": {"fn": "assortment.sf2",
                         "url": "https://drive.usercontent.google.com/download?id=1VZkoiVOonffpJWxZah-AdQkxaTFIzZ6q&export=download&authuser=0&confirm=t&uuid=20ed40a8-29bc-458b-aede-c4fa0e02a79d&at=AO7h07d-C-xX35_yDTMT54Lm-Qsd%3A1726224260647",
                         "preset": 7},
               "oboe": {"fn": "assortment.sf2",
                        "url": "https://drive.usercontent.google.com/download?id=1VZkoiVOonffpJWxZah-AdQkxaTFIzZ6q&export=download&authuser=0&confirm=t&uuid=20ed40a8-29bc-458b-aede-c4fa0e02a79d&at=AO7h07d-C-xX35_yDTMT54Lm-Qsd%3A1726224260647",
                        "preset": 31}}

    samplers = {}

    for name, info in samples.items():
        try:
            samplers[name] = Sampler(Path(config.instruments_dir, info["fn"]),
                                     sf_preset=info["preset"])
        except FileNotFoundError:
            download_sampler(info["url"], info["fn"], config.instruments_dir)

            samplers[name] = Sampler(Path(config.instruments_dir, info["fn"]),
                                     sf_preset=info["preset"])

    return samplers


def get_sampler(samplers, instrument_val):
    val = instrument_val.get()

    sampler = samplers[val]

    return copy.copy(sampler)


def get_scale(scale_val):
    val = scale_val.get()

    # Major
    if val == "major":
        scale = [["C3","D3","E3","F3","G3","A3","B3",
                  "C4","D4","E4","F4","G4","A4","B4",
                  "C5","D5","E5","F5","G5","A5","B5"]]

    # Minor
    if val == "minor":
        scale = [["C3","D3","D#3","F3","G3","G#3","A#3",
                  "C4","D4","D#4","F4","G4","G#4","A#4",
                  "C5","D5","D#5","F5","G5","G#5","A#5"]]

    # Pentatonic
    if val == "pentatonic":
        scale = [["C3","D#3","F3","G3","A#3",
                  "C4","D#4","F4","G4","A#4",
                  "C5","D#5","F5","G5","A#5"]]

    #BLUES
    if val == "blues":
        scale = [["C3","D#3","F3","F#3","G3","A#3",
                  "C4","D#4","F4","F#4","G4","A#4",
                  "C5","D#5","F5","F#5","G5","A#5"]]

    # Chromatic
    if val == "chromatic":
        scale = [["C3","C#3","D3","D#3","E3","F3","F#3","G3","G#3","A3","A#3","B3",
                  "C4","C#4","D4","D#4","E4","F4","F#4","G4","G#4","A4","A#4","B4",
                  "C5","C#5","D5","D#5","E5","F5","F#5","G5","G#5","A5","A#5","B5"]]

    return scale


def sonification(samplers, instrument_val, scale_val, spec, wave, settings, config):

    # Get the instrument sampler
    sampler = get_sampler(samplers, instrument_val)

    # Setup the range of notes
    scale = get_scale(scale_val)

    score = Score(scale, len(scale[0]))

    # Convert the spectrum data to a pitch and time dictionary.
    maps = {'pitch':spec,
            'time': wave}

    # Sound setup
    system = "mono"

    # manually set note properties to get a suitable sound
    sampler.modify_preset({'note_length':settings["soni_params"]["note_length"], # hold each note for x seconds
                           'volume_envelope': {'use':'on',
                                                # A,D,R values in seconds, S sustain fraction from 0-1 that note
                                                # will 'decay' to (after time A+D)
                                                'A': 0.01,    # ✏️ Time to fade in note to maximum volume, using 10 ms
                                                'D': 0,    # ✏️ Time to fall from maximum volume to sustained level (s), irrelevant while S is 1 
                                                'S': 0.5, # ✏️ fraction of maximum volume to sustain note at while held, 1 implies 100% 
                                                'R': settings["soni_params"]["R"]}}) # ✏️ Time to fade out once note is released

    # alternatively can avoid setting manually above anf just load the 'staccato' preset
    # generator.load_preset('staccato')

    # set 0 to 100 percentile limits so the full pitch range is used...
    # setting 0 to 101 for pitch means the sonification is 1% longer than
    # the time needed to trigger each note - by making this more than 100%
    # we give all the notes time to ring out (setting this at 100% means
    # the final note is triggered at the momement the sonification ends)
    lims = {'time': ('0','110'),
            'pitch': ('0','100')}

    # set up source
    sources = Events(maps.keys())
    sources.fromdict(maps)
    sources.apply_mapping_functions(map_lims=lims)

    soni = Sonification(score, sources, sampler, system)
    soni.render()
    soni.save(f"{config.output_dir}/spectrum.wav")

    return


def play_audio_clicked(audio_progress, config):
    Thread(target=play_audio,
           kwargs={"audio_progress":audio_progress, "config":config}).start()
    return


def play_audio(audio_progress, config):

    # Stop any audio already playing and reset the progress bar
    stop_audio(audio_progress)

    # Load in the audio file
    pygame.mixer.music.load(f"{config.output_dir}/spectrum.wav")

    # Get the audio file time length and calculate how quick the
    # progress bar should move. (in seconds)
    audio_length = float(pygame.mixer.Sound(f"{config.output_dir}"
                                            "/spectrum.wav").get_length())

    # Get the audio length at the point of the last note playing
    # (i.e exclude the sustain time of the last note)
    audio_length /= 1.1

    # Play the audio and start progress bar
    pygame.mixer.music.play(loops=0)
    audio_progress.start(int(audio_length*10))

    time_passed = 0
    while pygame.mixer.music.get_busy() == True:
        sleep(0.1)
        time_passed += 0.1
        if time_passed > audio_length:
            audio_progress.stop()
        else:
            continue

    # Stop progress bar after the length of the audio file.
    stop_audio(audio_progress)

    return


def stop_audio(audio_progress):

    pygame.mixer.music.stop()
    audio_progress.stop()
    # audio_progress.set(0)

    return
