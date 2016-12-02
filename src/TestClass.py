from unittest import TestCase
import time
from NetworkControllerClumsy import ClumsyConfiguration, ClumsyController


class TestClass(TestCase):

    def setUp(self):
        self.network_configuration = ClumsyConfiguration(clumsy_path="C:\Users\Doron-Dell\PycharmProjects\Clumzy Project\clumsy-0.2-win64")
        self.network_configuration.configure_network()

        self.network_controller = ClumsyController(clumsy_configuration=self.network_configuration)
        self.network_controller.start_async()

    def tearDown(self):
        self.network_controller.stop()
        pass

    def test_something(self):
        for i in range(20):
            print "testing"
            time.sleep(1)
        self.assertEqual(True, False)

