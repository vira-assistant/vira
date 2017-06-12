# -*- coding: utf-8 -*-
"""Demo

A demo of VIRA.

Authored by Ikechi Akujobi, Matthew Chen, Chris Salguero.
Cstring_294W, Spring 2016-2017.
© Stanford University.
"""

import pyaudio
import wave
import osax
import sys
import time

import vira


def speak_and_print(voice_util, phrase):
    if voice_util:
        voice_util.utter_phrase(phrase)
    print phrase

def play_alert():
    chunk = 1024
    wf = wave.open('vira/voice_files/alert.wav')
    p = pyaudio.PyAudio()

    stream = p.open(
        format = p.get_format_from_width(wf.getsampwidth()),
        channels = wf.getnchannels(),
        rate = wf.getframerate(),
        output = True)
    data = wf.readframes(chunk)

    while data != '':
        stream.write(data)
        data = wf.readframes(chunk)

    stream.close()
    p.terminate()
    return


def main():
    print "VIRA is loading...", '\r',
    sys.stdout.flush()
    config = vira.config.get_config()
    apps_dir_path = config.APP_DATA_DIR
    steam_util = vira.steam_util.SteamUtility(apps_dir_path)
    apps = steam_util.get_all_apps()
    spell_util = vira.spell_util.SpellUtility(apps)
    voice_util = vira.voice_util.VoiceUtility('vira/voice_files/output.mp3')
    weather_util = vira.weather_util.WeatherUtility()
    
    # pyglet.app.run()
    sys.stdout.write("\033[K")  # clear "loading..." line
    sys.stdout.flush()

    # alert = pyglet.media.load('')
    # alert.play()

    names = ["Vira", "Ikechi", "Matt", "Chris", "Giovanni", "Monica", "Violet"]
    speech_util = vira.speech_util.SpeechUtility(voice_util, apps + names)
    speech_util.get_name()
    speech_util.print_hello()

    phrase = "{}, the following games are available:".format(speech_util.first_name)
    speak_and_print(voice_util, phrase)
    while True:
        for app in apps:
            voice_util.utter_phrase(app)
            print "    - {}".format(app)
        print

        app = speech_util.get_app(spell_util)
        if app in apps:
            phrase = "Sounds good, {}. Opening {}...".format(speech_util.first_name, app)
            speak_and_print(voice_util, phrase)
            steam_util.spawn_app(app, config.APP_EXTENSION)
            break
        else:
            speak_and_print(voice_util, "Unfortunately, I don't think we have that app.")
            speak_and_print(voice_util, "Sorry, {}!".format(speech_util.first_name))
            phrase = "As a reminder, {}, the following games are available:".format(speech_util.first_name)
            speak_and_print(voice_util, phrase)

    sa = osax.OSAX()
    vol_settings = []
    curr_volume = None
    for k, v in sa.get_volume_settings().iteritems():
        vol_settings.append(k)
    while True:
        prompt = speech_util.listen_for_command().lower()
        if "vira" in prompt:
            curr_volume = abs(sa.get_volume_settings()[vol_settings[2]] - 1.0)
            play_alert()
            sa.set_volume(0)
            command = speech_util.listen_for_command().lower()
            sa.set_volume(curr_volume / 14.0)
            if "weather" in command:
                speak_and_print(voice_util, "{}, ".format(speech_util.first_name) + weather_util.get_weather())
        else:
            print "Garbage: {}".format(prompt)




if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
