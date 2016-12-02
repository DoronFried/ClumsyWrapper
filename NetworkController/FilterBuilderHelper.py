

class FilterHelper:
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
        return FilterHelper(self.__filter_builder_str)

    def and_condition(self):
        self.__filter_builder_str += " and"
        return FilterHelper(self.__filter_builder_str)

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