"""
An app that plays and records a sound on an Android system.
Much of the code is based off https://hub.packtpub.com/sound-recorder-android/

TODO: 
> Check for unprocessed audio handling because apparently most 
audio input sources already process the data!!

"""
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.logger import Logger
from jnius import autoclass
from time import sleep

# get the needed Java classes
MediaRecorder = autoclass('android.media.MediaRecorder')
AudioSource = autoclass('android.media.MediaRecorder$AudioSource')
OutputFormat = autoclass('android.media.MediaRecorder$OutputFormat')
AudioEncoder = autoclass('android.media.MediaRecorder$AudioEncoder')
Environment = autoclass('android.os.Environment')


storage_path = (Environment.getExternalStorageDirectory()
                .getAbsolutePath() + '/kivy_recording.3gp')


path = Environment.getExternalStorageDirectory().getAbsolutePath()
Logger.info('App: storage path == "%s"' % path)

Logger.info('Made it till preparing the mrecorder!')

mRecorder = MediaRecorder()

class Miaow(BoxLayout):
    
    def __init__(self, **kwargs):
        super(Miaow, self).__init__(**kwargs)
        self.cols = 2
        self.clear_button = Button(text='Clear', on_press=self.clearitup)
        self.rec_button = Button(text='5 seconds rec',
                                 on_press=self.begin_rec)
        self.add_widget(self.clear_button)
        self.add_widget(self.rec_button)
        
    def clearitup(self, instance):
        self.draw_region.canvas.clear()


    def init_recording(self):
        
        # create out recorder
        
        mRecorder.setAudioSource(AudioSource.DEFAULT)
        mRecorder.setOutputFormat(OutputFormat.THREE_GPP)
        
        mRecorder.setOutputFile(storage_path)
        mRecorder.setAudioEncoder(AudioEncoder.AMR_NB)
        mRecorder.prepare()

    def begin_rec(self, instance):
        Logger.info('Initialising MediaRecorder...')
        self.init_recording()
        # record 5 seconds
        Logger.info('In the begin_rec')
        
        mRecorder.start()
        self.rec_button.text = 'Recording....'
        sleep(5)
        mRecorder.stop()
        Logger.info('recording stopped..')
        mRecorder.reset()
        Logger.info('recording released')
        self.rec_button.text = 'Rec stopped....'



class RecorderApp(App):
    def build(self):
        return Miaow()
    


if __name__ == '__main__':
    RecorderApp().run()