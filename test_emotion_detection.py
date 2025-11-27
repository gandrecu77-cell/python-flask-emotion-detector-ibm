from EmotionDetection import emotion_detector
import unittest
import json

class TestEmotionDetector(unittest.TestCase):
    def test_emotion_detector(self):
        # Test case for positive sentiment
        result_11 = emotion_detector('I am glad this happened')
        result_1 = json.loads(result_11)
        print("ssss->" + str(result_1['joy']))
        self.assertGreater(result_1['joy'],0, 'SENT_OK')
        # Test case for negative sentiment
        result_22 = emotion_detector('I am really mad about this')
        result_2 = json.loads(result_22)
        self.assertGreater(result_2['anger'],0, 'SENT_NEGATIVE')
        # Test case for neutral sentiment
        result_33 = emotion_detector('I feel disgusted just hearing about this')
        result_3 = json.loads(result_33)
        self.assertGreater(result_3['disgust'],0, 'SENT_BORING')
        result_44 = emotion_detector('I am so sad about this')
        result_4 = json.loads(result_44)
        self.assertGreater(result_4['sadness'],0, 'SENT_LOW')
        result_55 = emotion_detector('I am really afraid that this will happen')
        result_5 = json.loads(result_55)
        self.assertGreater(result_5['fear'],0, 'SENT_FEAR')

unittest.main()