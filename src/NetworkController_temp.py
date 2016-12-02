import os
import random
import subprocess

import time


class NetworkController:

    def __init__(self, clumsy_path):
        self.clumsy_path = clumsy_path
        self.filter_options = {"Ports"}

    def choose_filter(self):
        pass


    def clumsy_network(self, clumsy_path=None):
        """
        Every 30 seconds it dropping the network for 0-7 seconds (random num between 0 -7)
        :param clumsy_path:
        :return:
        """
        if not clumsy_path:
            clumsy_path='C:\Doron\Tasks-Doron\PBI 157390- retry on ES communication errors\Network_control_software\clumsy-0.2-win64'
        os.chdir(clumsy_path)
        self.clumsy_keep_running.value = True
        Start_Clumsy = "clumsy.exe --filter \" tcp.DstPort == 8031 or tcp.SrcPort == 8031 \" --drop on --drop-chance 100"
        Stop_Clumsy = "taskkill /im clumsy.exe /f >nul 2>&1"
        start_time = time.time()
        while self.clumsy_keep_running.value:
            rand_disconnect_time = random.uniform(0, 7)
            print "CLUMSY: stopping network for " + str(rand_disconnect_time) + " seconds. At " + time.strftime("%Y-%m-%d %H:%M:%S")
            subprocess.Popen(Start_Clumsy)
            time.sleep(rand_disconnect_time)
            subprocess.Popen(Stop_Clumsy, shell=True)
            print "CLUMSY: network is back online for " + str(30-rand_disconnect_time) + " seconds. At " + time.strftime("%Y-%m-%d %H:%M:%S")
            time.sleep(20-rand_disconnect_time)


    def clumsy_network_always_on(self, clumsy_path=None):
        """

        :param clumsy_path:
        :return:
        """
        if not clumsy_path:
            clumsy_path='C:\Doron\Tasks-Doron\PBI 157390- retry on ES communication errors\Network_control_software\clumsy-0.2-win64'
        os.chdir(clumsy_path)
        self.clumsy_keep_running.value = True
        Start_Clumsy = "clumsy.exe --filter \" tcp.DstPort == 8031 or tcp.SrcPort == 8031 \" --drop on --drop-chance 30"
        Stop_Clumsy = "taskkill /im clumsy.exe /f >nul 2>&1"
        print "CLUMSY: Starting Clumsy"
        subprocess.Popen(Start_Clumsy)
        while self.clumsy_keep_running.value:
            time.sleep(1)
            pass
        subprocess.Popen(Stop_Clumsy, shell=True)
        print "CLUMSY: Stopping Clumsy"


class Filter:
    def __init__(self, filter_builder_str=None):
        if filter_builder_str is None:
            self.__filter_builder_str = "--filter \""
        else:
            self.__filter_builder_str = filter_builder_str

    def tcp(self):
        return Tcp(self.__filter_builder_str)

    def udp(self):
        return Udp(self.__filter_builder_str)


class Tcp:
    def __init__(self, filter_builder_str):
        self.__filter_builder_str = filter_builder_str + " tcp."

    def dst_port(self, port_num):
        self.__filter_builder_str += "DstPort == {port}".format(port=port_num)
        return AddCondition(self.__filter_builder_str)

    def src_port(self, port_num):
        self.__filter_builder_str += "SrcPort == {port}".format(port=port_num)
        return AddCondition(self.__filter_builder_str)


class Udp:
    def __init__(self, filter_builder_str):
        self.__filter_builder_str = filter_builder_str + " udp."

    def dst_port(self, port_num):
        self.__filter_builder_str += "DstPort == {port}".format(port=port_num)
        return AddCondition(self.__filter_builder_str)

    def src_port(self, port_num):
        self.__filter_builder_str += "SrcPort == {port}".format(port=port_num)
        return AddCondition(self.__filter_builder_str)


class AddCondition:
    def __init__(self, filter_builder_str):
        self.__filter_builder_str = filter_builder_str

    def or_condition(self):
        self.__filter_builder_str += " or"
        return Filter(self.__filter_builder_str)

    def and_condition(self):
        self.__filter_builder_str += " and"
        return Filter(self.__filter_builder_str)

    def no_more_condition(self):
        self.__filter_builder_str += " \""
        return FilterOptions(self.__filter_builder_str)


class FilterOptions:
    def __init__(self, filter_builder_str):
        self.__filter_builder_str = filter_builder_str

    def drop(self, drop_chance):
        self.__filter_builder_str += " --drop on --drop-chance {drop_chance}".format(drop_chance=drop_chance)
        return AddFilterOptions(self.__filter_builder_str)

    def lag(self, lag_time_ms):
        self.__filter_builder_str += " --lag on --lag-time {lag_time}".format(lag_time=lag_time_ms)
        return AddFilterOptions(self.__filter_builder_str)

    def duplicate(self, duplicate_count, duplicate_chance):
        self.__filter_builder_str += " --duplicate on --duplicate-chance {chance} --duplicate-count {count}".format(chance=duplicate_chance, count=duplicate_count)
        return AddFilterOptions(self.__filter_builder_str)


class AddFilterOptions:
    def __init__(self, filter_builder_str):
        self.__filter_builder_str = filter_builder_str

    def add_filter_option(self):
        return FilterOptions(self.__filter_builder_str)

    def finish_generate_filter(self):
        return self.__filter_builder_str

filter1 = Filter()
filter_str = filter1.tcp().dst_port(port_num=8030).or_condition().tcp().src_port(port_num=55).no_more_condition().drop(drop_chance=60).finish_generate_filter()
print filter_str











