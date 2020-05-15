"""
An app that plays and records a sound on an Android system.
Much of the code is based off https://hub.packtpub.com/sound-recorder-android/

Features to implement
1. Implement playback in a separate button.
2. Simultaneous playback and recording!


TODO: 
> Check for unprocessed audio handling because apparently most 
audio input sources already process the data!! 
> Use AudioRecord (https://developer.android.com/reference/kotlin/android/media/AudioRecord) 
instead of MediaRecorder. MediaRecorder only allows lossy recording of 
audio because it uses codecs!
> Change the way the recording is triggered. Right now it's triggered
by a 'on_press' action. It needs to be changed into a 'on_press_down' action. 

"""
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.logger import Logger
from jnius import autoclass
from time import sleep, time
import os 

app_name = "playrec"

# get the needed Java classes
MediaRecorder = autoclass('android.media.MediaRecorder')
AudioSource = autoclass('android.media.MediaRecorder$AudioSource')
OutputFormat = autoclass('android.media.MediaRecorder$OutputFormat')
AudioEncoder = autoclass('android.media.MediaRecorder$AudioEncoder')
Environment = autoclass('android.os.Environment')

path = Environment.getExternalStorageDirectory().getAbsolutePath()

app_folder = os.path.join(path, app_name)

Logger.info('App: storage path == "%s"' % path)

Logger.info('Made it till preparing the mrecorder!')

mRecorder = MediaRecorder()

class Miaow(BoxLayout):
    
    def __init__(self, **kwargs):
        super(Miaow, self).__init__(**kwargs)
        self.cols = 1
        self.rec_button = Button(text='5 seconds rec',
                                 on_press=self.begin_rec,
                                 background_color=(1, 1, 1, .85))
        self.add_widget(self.rec_button)
        
    def clearitup(self, instance):
        self.draw_region.canvas.clear()


    def init_recording(self):
        # create out recorder
        self.rec_button.background_color = (1, .3, .4, .85)
        self.rec_button.text = 'Recording....'
        sleep(0.5)
        mRecorder.setAudioSource(AudioSource.DEFAULT)
        mRecorder.setOutputFormat(OutputFormat.THREE_GPP)
        # the timestamp:
        timestamp = str(int(time()))
        file_w_timestamp = '/'+timestamp+'_time' +'.3gp'
        
        if os.path.isdir(app_folder):
            pass
        else:
            os.mkdir(app_folder)
        
        storage_path = (app_folder + file_w_timestamp)
        Logger.info(f'The target file is {file_w_timestamp}')
        mRecorder.setOutputFile(storage_path)
        mRecorder.setAudioEncoder(AudioEncoder.AAC)
        mRecorder.setAudioSamplingRate(16000)
        mRecorder.prepare()

    def begin_rec(self, instance):
        Logger.info('Initialising MediaRecorder...')
        self.init_recording()
        # record 5 seconds
        Logger.info('In the begin_rec')
        
        mRecorder.start()
        
        sleep(5)
        mRecorder.stop()
        
        Logger.info('recording stopped..')
        mRecorder.reset()
        Logger.info('recording released')
        self.rec_button.text = '5 seconds rec over'
        self.rec_button.background_color = (1, 1, 1, .85)



class RecorderApp(App):
    def build(self):
        return Miaow()
    


if __name__ == '__main__':
    RecorderApp().run()