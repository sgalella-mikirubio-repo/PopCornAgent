import speech_recognition as sr


# Create a recognizer instance
def speech_recognizer():
    """Transform audio from speaker to sentence.
    Returns:
        audio_detected: String containing the detected audio
    """
    r = sr.Recognizer()
    mic = sr.Microphone()
    # r.Microphone.list_microphone_names()
    with mic as source:
        audio = r.listen(source)
    audio_detected = r.recognize_google(audio)
    return audio_detected
