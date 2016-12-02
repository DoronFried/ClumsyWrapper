

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
        Start_Clumsy = "clumsy.exe --filter \"tcp.DstPort == 8031 or tcp.SrcPort == 8031\" --drop on --drop-chance 100"
        Stop_Clumsy = "taskkill /im clumsy.exe /f >nul 2>&1"
        start_time = time.time()
        while self.clumsy_keep_running.value:
            rand_disconnect_time = random.uniform(0, 7)
            print "CLUMSY: stopping network for " + str(rand_disconnect_time) + " seconds. At " + strftime("%Y-%m-%d %H:%M:%S")
            subprocess.Popen(Start_Clumsy)
            time.sleep(rand_disconnect_time)
            subprocess.Popen(Stop_Clumsy, shell=True)
            print "CLUMSY: network is back online for " + str(30-rand_disconnect_time) + " seconds. At " + strftime("%Y-%m-%d %H:%M:%S")
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
        Start_Clumsy = "clumsy.exe --filter \"tcp.DstPort == 8031 or tcp.SrcPort == 8031\" --drop on --drop-chance 30"
        Stop_Clumsy = "taskkill /im clumsy.exe /f >nul 2>&1"
        print "CLUMSY: Starting Clumsy"
        subprocess.Popen(Start_Clumsy)
        while self.clumsy_keep_running.value:
            time.sleep(1)
            pass
        subprocess.Popen(Stop_Clumsy, shell=True)
        print "CLUMSY: Stopping Clumsy"


class FilterBuilder:
    def __init__(self):
        self.final_filter = ""
        pass

    def generate_filter(self):
        pass


class Filter:
    def __init__(self, drop=None):
        self.drop = drop
        """:type str: insert drop chance in % between 0-100. if not specified it will not drop any packet"""
        self.__dst = False
        self.__src = False

    def dst(self):
        self.__dst = True
        return Dst()

    def src(self):
        self.__src = True
        return Src()


class Dst:
    def __init__(self):
        self.m_tcp = False
        self.m_udp = False
        pass

    def tcp_protocol(self):
        self.m_tcp = True
        return Tcp()

    def udp_protocol(self):
        self.m_udp = True
        return Udp()


class Src:
    def __init__(self):
        self.m_tcp = False
        self.m_udp = False
        pass

    def tcp_protocol(self):
        self.m_tcp = True
        return Tcp()

    def udp_protocol(self):
        self.m_udp = True
        return Udp()


class Tcp:
    def __init__(self):
        self.m_port = False

    def port(self):
        self.m_port = True
        return Port()


class Udp:
    def __init__(self):
        self.m_port = False

    def port(self):
        self.m_port = True
        return Port()


class Port:
    def __init__(self):
        self.m_port = 0

    def port_number(self, port):
        self.m_port = port
        return AddCondition()


class AddCondition:
    def __init__(self):
        self.__or = False
        self.__and = False
        pass

    def or_condition(self):
        self.__or = True
        return Filter()

    def and_condition(self):
        self.__and = True
        return Filter()


class AddNumber:
    def __init__(self):
        self.__number = 0
        pass

    def add_one(self):
        self.__number += 1
        return self

    def add_two(self):
        self.__number += 2
        return self



AddNumber.add_one().add_two()

filter1 = Filter()
filter1.dst().tcp_protocol()

filter1.dst().tcp_protocol().port().port_number(8031).or_condition().src().tcp_protocol().port().port_number(8055)
--filter \"tcp.DstPort == 8031 or tcp.SrcPort == 8031\"


filter.dst.tcp.port(8031).src.tcp.port(8031).drop(30)














