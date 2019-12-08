import inspect
import os
import threading
import pytest

from src.main.ClimateApi import ClimateApi
from src.test.TestClimateApi import TestClimateApi
import src.main.mock_recorder as MockRecorder


class TestRecordingClimateApi(TestClimateApi):
    site = "http://localhost:8099"

    MockRecorder.set_real_host('http://climatedataapi.worldbank.org')
    thread1 = threading.Thread(target=MockRecorder.start, daemon=True)
    thread1.start()

    if __name__ == "__main__":
        try:
            pytest.main(["-x", os.getcwd()+"/TestRecordingClimateApi.py"])
        finally:
            os._exit(1)

    @pytest.fixture(autouse=True)
    def startup(self):
        self.climateApi = ClimateApi(self.site)

    def test_averageRainfallForGreatBritainFrom1980to1999Exists(self):
        MockRecorder.RecorderHttpHandler.set_invoking_method(inspect.stack()[0][3])
        assert self.climateApi.getAveAnnualRainfall(1980, 1999, "gbr") == 988.8454972331015

    def test_averageRainfallForFranceFrom1980to1999Exists(self):
        MockRecorder.RecorderHttpHandler.set_invoking_method(inspect.stack()[0][3])
        assert self.climateApi.getAveAnnualRainfall(1980, 1999, "fra") == 913.7986955122727

    def test_averageRainfallForEgyptFrom1980to1999Exists(self):
        MockRecorder.RecorderHttpHandler.set_invoking_method(inspect.stack()[0][3])
        assert self.climateApi.getAveAnnualRainfall(1980, 1999, "egy") == 54.58587712129825

    def test_averageRainfallForGreatBritainFrom1985to1995DoesNotExist(self):
        MockRecorder.RecorderHttpHandler.set_invoking_method(inspect.stack()[0][3])
        with pytest.raises(AttributeError) as execinfo:
            self.climateApi.getAveAnnualRainfall(1985, 1995, "gbr")
        assert "date range 1985-1995 not supported" in execinfo.value.args[0]

    def test_averageRainfallForMiddleEarthFrom1980to1999DoesNotExist(self):
        MockRecorder.RecorderHttpHandler.set_invoking_method(inspect.stack()[0][3])
        with pytest.raises(AttributeError) as excinfo:
            self.climateApi.getAveAnnualRainfall(1980, 1999, "mde")
        assert "not recognized by climateweb" in excinfo.value.args[0]

    def test_averageRainfallForGreatBritainAndFranceFrom1980to1999CanBeCalculatedFromTwoRequests(self):
        MockRecorder.RecorderHttpHandler.set_invoking_method(inspect.stack()[0][3])
        rainfall = self.climateApi.getAveAnnualRainfall(1980, 1999, "gbr", "fra")
        assert rainfall == 951.3220963726872