from kivy.app import App


class NTApp(App):

    def build(self):
        return SM


if __name__ == "__main__":
    from screenmanager import SM
    # for i in range(100):
    #     DATABASE.add_note(Note(text="This is note number {}".format(i+1)))
    ThisApp = NTApp()
    ThisApp.run()
