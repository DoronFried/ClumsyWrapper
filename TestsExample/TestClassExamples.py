from unittest import TestCase
import time
from NetworkController.NetworkControllerClumsy import ClumsyConfiguration, ClumsyController
from NetworkController.FilterBuilderHelper import FilterHelper
import random


class TestClassExamples(TestCase):

    def setUp(self):
        # using the helper in order to build my own filter
        filter_helper = FilterHelper().tcp().dst_port(port_num=8031).or_condition().tcp().src_port(port_num=8031).no_more_condition().drop(drop_chance=100).finish_generate_filter()
        network_configuration = ClumsyConfiguration(clumsy_path="C:\clumsy-0.2-win64")
        network_configuration.custom_config(custom_filter=filter_helper, execute_every_seconds=10, execute_duration=2, always_on=False)

        self.network_controller = ClumsyController(clumsy_configuration=network_configuration)
        self.network_controller.start_async()

    def tearDown(self):
        self.network_controller.stop()

    def test_something(self):
        for i in range(3):
            print "testing"
            time.sleep(1)
        self.assertEqual(True, True)

