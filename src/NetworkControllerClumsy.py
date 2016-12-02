import multiprocessing
import os
import random
import subprocess
from time import strftime
import time


class ClumsyConfiguration:

    def __init__(self, clumsy_path):
        """
        :param str clumsy_path : clumsy installation path
        """
        self.clumsy_path = clumsy_path
        self.Start_Clumsy = ""
        self.Stop_Clumsy = ""
        pass

    def configure_network(self, port=None, tcp=None, udp=None, always_on=None, stop_every=None, stop_duration=None, drop_chance=None):
        self.Start_Clumsy = "clumsy.exe --filter \"tcp.DstPort == 8031 or tcp.SrcPort == 8031\" --drop on --drop-chance 100"
        self.Stop_Clumsy = "taskkill /im clumsy.exe /f >nul 2>&1"
        pass


class ClumsyController:
    def __init__(self, clumsy_configuration):
        """
        :param ClumsyConfiguration clumsy_configuration:
        """
        self.__clumsy_keep_running = multiprocessing.Value('b', True)
        self.clumsy_configuration = clumsy_configuration
        os.chdir(self.clumsy_configuration.clumsy_path)

    def start_async(self):
        self.__threads = []
        p = multiprocessing.Process(target=self._start_clumsy)
        self.__threads.append(p)
        p.start()

    def _start_clumsy(self):
        self.__clumsy_keep_running.value = True
        while self.__clumsy_keep_running.value:
            rand_disconnect_time = random.uniform(0, 7)
            print "CLUMSY: stopping network for " + str(rand_disconnect_time) + " seconds. At " + strftime("%Y-%m-%d %H:%M:%S")
            subprocess.Popen(self.clumsy_configuration.Start_Clumsy)
            time.sleep(rand_disconnect_time)
            subprocess.Popen(self.clumsy_configuration.Stop_Clumsy, shell=True)
            print "CLUMSY: network is back online for " + str(30-rand_disconnect_time) + " seconds. At " + strftime("%Y-%m-%d %H:%M:%S")
            time.sleep(30-rand_disconnect_time)
        print "stopping clumsy"

    def stop(self):
        self.__clumsy_keep_running.value = False
        for thread in self.__threads:
            thread.join()
        print "stopping network tool"


def main():
    pass
    # bla = NetworkController(clumsy_path="C:\Users\Doron-Dell\PycharmProjects\Clumzy Project\clumsy-0.2-win64")
    # bla.configure_network()
    # bla.start_async()
    # time.sleep(10)
    # bla.stop()

if __name__ == '__main__':
    main()