import multiprocessing
import os
import subprocess
from time import strftime
import time


class ClumsyConfiguration:

    def __init__(self, clumsy_path):
        """
        :param str clumsy_path : clumsy installation path. e.g. 'C:\clumsy-0.2-win64'
        """
        self.clumsy_path = clumsy_path
        self.Start_Clumsy_Filter_Command = ""
        self.Stop_Clumsy_Command = "taskkill /im clumsy.exe /f >nul 2>&1"
        self.always_on = False
        self.execute_every_seconds = 0
        self.execute_duration = 0

    def stopping_network_ip_in_and_out_every_x_sec_for_y_sec_duration(self, execute_every_seconds, execute_duration_seconds, ip, drop_chance=100):
        """
        Built-in function.
        This function is simulating unstable network, when it falls down for 'x' seconds duration every 'y' seconds
        :param int execute_every_seconds: run clumsy every 'x' seconds. e.g. drop the network every 30 seconds.
        :param int execute_duration_seconds: run clumsy for duration of 'y' seconds. e.g. drop the network for a 5 seconds.
        :param str ip: insert the ip you want to block
        :param int drop_chance: how many packets you want to loss (in percent)
        :return:
        """
        self.execute_every_seconds = execute_every_seconds
        self.execute_duration = execute_duration_seconds
        self.Start_Clumsy_Filter_Command = "clumsy.exe --filter \" ip.DstAddr == {ip} or ip.SrcAddr == {ip} \" --drop on --drop-chance {drop_chance}".format(ip=ip, drop_chance=drop_chance)

    def stopping_network_port_in_and_out_every_x_sec_for_y_sec_duration(self, execute_every_seconds, execute_duration, port, tcp=True, drop_chance=100):
        """

        :param int execute_every_seconds: run clumsy every 'x' seconds. e.g. drop the network every 30 seconds.
        :param int execute_duration: run clumsy for duration of 'y' seconds. e.g. drop the network for a 5 seconds.
        :param port: insert the port you want to block
        :param tcp: for tcp protocol insert True, for udp protocol insert False
        :param drop_chance: how many packets you want to loss (in percent)
        :return:
        """
        self.execute_every_seconds = execute_every_seconds
        self.execute_duration = execute_duration
        if tcp:
            self.Start_Clumsy_Filter_Command = "clumsy.exe --filter \" tcp.DstPort == {port} or tcp.SrcPort == {port} \" --drop on --drop-chance {drop_chance}".format(port=port, drop_chance=drop_chance)
        else:
            self.Start_Clumsy_Filter_Command = "clumsy.exe --filter \" udp.DstPort == {port} or udp.SrcPort == {port} \" --drop on --drop-chance {drop_chance}".format(port=port, drop_chance=drop_chance)

    def packets_drop_for_specific_port_always_on(self, port, tcp=True, drop_chance=10):
        """

        :param port: insert the port you want to block
        :param tcp: for tcp protocol insert True, for udp protocol insert False
        :param drop_chance: how many packets you want to loss (in percent)
        :return:
        """
        self.always_on = True
        if tcp:
            self.Start_Clumsy_Filter_Command = "clumsy.exe --filter \" tcp.DstPort == {port} or tcp.SrcPort == {port} \" --drop on --drop-chance {drop_chance}".format(port=port, drop_chance=drop_chance)
        else:
            self.Start_Clumsy_Filter_Command = "clumsy.exe --filter \" udp.DstPort == {port} or udp.SrcPort == {port} \" --drop on --drop-chance {drop_chance}".format(port=port, drop_chance=drop_chance)

    def packets_drop_for_specific_ip_always_on(self, ip, drop_chance=10):
        """

        :param ip: insert the ip you want to block
        :param drop_chance: how many packets you want to loss (in percent)
        :return:
        """
        self.always_on = True
        self.Start_Clumsy_Filter_Command = "clumsy.exe --filter \" ip.DstAddr == {ip} or ip.SrcAddr == {ip} \" --drop on --drop-chance {drop_chance}".format(ip=ip, drop_chance=drop_chance)

    def custom_config(self, custom_filter, execute_every_seconds, execute_duration, always_on=False):
        """
        User can insert his own custom filter.
        Example of a user that want to stop the network for port 8031 every 30 seconds for a duration of 0-7 seconds
        (random number between 0-7):
             custom_filter = --filter \"tcp.DstPort == 8031 or tcp.SrcPort == 8031\" --drop on --drop-chance 100
             execute_every_seconds = 30
             execute_duration =  random.uniform(0, 7)
             always_on = False
        In order to get more examples of different filters enter to the follow link https://jagt.github.io/clumsy/
        :param str custom_filter: Enter your own filter. e.g. --filter \"tcp.DstPort == 8031 or tcp.SrcPort == 8031\" --drop on --drop-chance 100.
        :param bool always_on: run clumsy all the time. e.g. drop 30% packets during my automation test.
        :param int execute_every_seconds: run clumsy every 'x' seconds. e.g. drop the network every 30 seconds.
        :param int execute_duration: run clumsy for duration of 'y' seconds. e.g. drop the network for a 5 seconds.
        :return:
        """
        self.Start_Clumsy_Filter_Command = "clumsy.exe {custom_filter}".format(custom_filter=custom_filter)
        self.always_on = always_on
        self.execute_every_seconds = execute_every_seconds
        self.execute_duration = execute_duration


class ClumsyController:
    def __init__(self, clumsy_configuration):
        """
        :param ClumsyConfiguration clumsy_configuration: insert the object that represent the chosen filter
        """
        self.__clumsy_keep_running = multiprocessing.Value('b', True)
        self.__clumsy_configuration = clumsy_configuration
        self.__threads = []
        os.chdir(self.__clumsy_configuration.clumsy_path)

    def start_async(self):
        p = multiprocessing.Process(target=self._start_clumsy)
        self.__threads.append(p)
        p.start()

    def _start_clumsy(self):
        if self.__clumsy_configuration.always_on:
            print "CLUMSY: Starting Clumsy (Disrupts the network)"
            subprocess.Popen(self.__clumsy_configuration.Start_Clumsy_Filter_Command)
            while self.__clumsy_keep_running.value:
                time.sleep(1)
            subprocess.Popen(self.__clumsy_configuration.Stop_Clumsy_Command, shell=True)
            print "CLUMSY: Stopping Clumsy (Network is back to be stable)"
        else:
            self.__clumsy_keep_running.value = True
            while self.__clumsy_keep_running.value:
                print "CLUMSY: clumsy up for (Disrupts the network) " + str(self.__clumsy_configuration.execute_duration) + " seconds. At " + strftime("%Y-%m-%d %H:%M:%S")
                subprocess.Popen(self.__clumsy_configuration.Start_Clumsy_Filter_Command)
                time.sleep(self.__clumsy_configuration.execute_duration)
                subprocess.Popen(self.__clumsy_configuration.Stop_Clumsy_Command, shell=True)
                print "CLUMSY: clumsy down for (Network is back to be stable) for " + str(self.__clumsy_configuration.execute_every_seconds - self.__clumsy_configuration.execute_duration) + " seconds. At " + strftime("%Y-%m-%d %H:%M:%S")
                time.sleep(self.__clumsy_configuration.execute_every_seconds - self.__clumsy_configuration.execute_duration)
            print "CLUMSY: Ending Clumsy"

    def stop(self):
        self.__clumsy_keep_running.value = False
        for thread in self.__threads:
            thread.join()
        print "Stopping network tool"


def main():
    pass

if __name__ == '__main__':
    main()