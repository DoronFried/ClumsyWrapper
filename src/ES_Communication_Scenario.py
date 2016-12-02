import multiprocessing
import os
import random
import subprocess
from cloudshell.api.cloudshell_api import CloudShellAPISession, InputNameValue
from time import strftime
import time



class ESCommunicationScenario:
    def __init__(self, host, username, password, domain):

        self.host = host

        self.username = username
        self.password = password
        self.domain = domain
        # create api session:
        self.api_session = self._get_api_session()
        # var clumsy_keep_running is a shared variable between the Sub-Thread and the Main-Thread
        self.clumsy_keep_running = multiprocessing.Value('b', True)

    def _set_api_session(self):
        self.api_session = self._get_api_session()

    def _get_api_session(self):
        return CloudShellAPISession(host=self.host,
                                    username=self.username,
                                    password=self.password,
                                    domain=self.domain)

    def test_es_communication(self, duration_in_minutes):
        print "SCENARIO: Starting scenario for " + str(duration_in_minutes) + " minutes. At " + strftime("%Y-%m-%d %H:%M:%S")
        long_text_to_send = "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
        reservation_id = "f9f83292-452a-4aaa-88bf-facd56017e43"
        success_count = 0
        failed_count = 0
        errors = []
        time_flag = True
        i = 0
        start_time = time.time()
        start_time_date = strftime("%Y-%m-%d_%H:%M:%S")
        while time_flag:
            try:
                print "SCENARIO: Creating new resource"
                temp_resource = self.api_session.CreateResource(resourceFamily="Bridge",
                                                                resourceModel="Bridge Generic Model",
                                                                resourceName="Bridge_ES_communication" + str(i),
                                                                resourceAddress='1')
                print "SCENARIO: Adding driver to the resource"
                self.api_session.UpdateResourceDriver(resourceFullPath=temp_resource.Name,
                                                      driverName="ES_Communication_testing_driver")
                print "SCENARIO: Add resource to reservation"
                self.api_session.AddResourcesToReservation(reservationId=reservation_id,
                                                           resourcesFullPath=[temp_resource.Name])
                print "SCENARIO: start to run 100 commands"
                for number_executions in range(100):
                    try:
                        execute_resource_command = self.api_session.ExecuteCommand(reservationId=reservation_id,
                                                                               targetType="Resource",
                                                                               targetName=temp_resource.Name,
                                                                               commandName="communication_test",
                                                                               commandInputs=[InputNameValue("long_string",
                                                                                                               long_text_to_send)])

                        if execute_resource_command.Output == "Communication ok":
                            success_count += 1
                            print "SCENARIO: Command successfully ended. At " + strftime("%Y-%m-%d %H:%M:%S")
                        else:
                            failed_count += 1
                            errors.append(strftime("%Y-%m-%d %H:%M:%S") + " (command output is not success):\n" +execute_resource_command.Output)
                            print "SCENARIO: Error occurred, command output: " + execute_resource_command.Output +\
                                                                                ". At " + strftime("%Y-%m-%d %H:%M:%S")
                    except Exception as e:
                        failed_count += 1
                        errors.append(strftime("%Y-%m-%d %H:%M:%S") + " (Execute command failed):\n" + e.message)
                        print "SCENARIO: This is the Error msg:" + strftime("%Y-%m-%d %H:%M:%S") + ":\n" + e.message + "\n"
                print "SCENARIO: finished to run 100 commands, delete resource. At " + strftime("%Y-%m-%d %H:%M:%S")
                self.api_session.DeleteResource(resourceFullPath=temp_resource.Name)
            except Exception as er:
                errors.append(strftime("%Y-%m-%d %H:%M:%S") + ":\n" + er.message)
            i += 1
            time_flag = (time.time()-start_time) < (duration_in_minutes*60)
            self.clumsy_keep_running.value = time_flag
        end_time = time.time()
        all_executed_commands = failed_count + success_count
        print "SCENARIO: The Scenario is about to end, Starting to Save the results in a file. at " + strftime("%Y-%m-%d %H:%M:%S")
        actual_duration_in_minutes = (end_time-start_time)/60
        file_name = 'ES Communication' + start_time_date.replace(":", "-") + ".txt"
        file = open("C:\\Doron\\Tasks-Doron\\PBI 157390- retry on ES communication errors\\results\\" + file_name, "w")
        print "SCENARIO: Result text file has been created at " + strftime("%Y-%m-%d %H:%M:%S")
        file.write("ES Communication Testing" + "\n")
        file.write("User defined the test to run for " + str(duration_in_minutes) + " minutes" + "\n")
        file.write("Actual duration " + str(actual_duration_in_minutes) + " minutes" + "\n")
        file.write("The test started at: " + start_time_date + "\n")
        file.write("The test ended at: " + strftime("%Y-%m-%d %H:%M:%S") + "\n")
        print "SCENARIO: Enqueue " + str(all_executed_commands) + " commands at " + strftime("%Y-%m-%d %H:%M:%S")
        file.write("Enqueue " + str(all_executed_commands) + " commands\n")
        print "SCENARIO: Succeed executions " + str(success_count) + ". at " + strftime("%Y-%m-%d %H:%M:%S")
        file.write("Succeed executions " + str(success_count) + "\n")
        print "SCENARIO: Failed executions " + str(failed_count) + ". at " + strftime("%Y-%m-%d %H:%M:%S")
        file.write("Failed executions " + str(failed_count) + "\n")
        file.write("Success results (%) " + str((success_count/float(all_executed_commands))*100) + "\n")
        file.write("Errors messages:" + "\n")
        for error_msg in errors:
            file.write(error_msg + "\n")
        file.close()
        print "SCENARIO: Done writing the results to a file at " + strftime("%Y-%m-%d %H:%M:%S") + ". "

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

    def multi_process(self, duration_in_minutes, clumsy_always_on=False):
        if clumsy_always_on:
            func_to_call = [self.clumsy_network_always_on, self.test_es_communication]
            args_to_func = [None, duration_in_minutes]
            jobs = []
            for i in range(2):
                p = multiprocessing.Process(target=func_to_call[i], args=(args_to_func[i],))
                jobs.append(p)
                p.start()
            for i in range(2):
                jobs[i].join()
        else:
            func_to_call = [self.clumsy_network, self.test_es_communication]
            args_to_func = [None, duration_in_minutes]
            jobs = []
            for i in range(2):
                p = multiprocessing.Process(target=func_to_call[i], args=(args_to_func[i],))
                jobs.append(p)
                p.start()
            for i in range(2):
                jobs[i].join()


def main():
    for i in range(3):
        print "Main method: starting Scenario " + str(i) + " at " + strftime("%Y-%m-%d %H:%M:%S") + "-------------------------------------------------------------------"
        es_communication = ESCommunicationScenario(host='localhost', username='admin', password='admin', domain='Global')
        es_communication.multi_process(duration_in_minutes=60)
        print "Main method: finished Scenario " + str(i) + " at " + strftime("%Y-%m-%d %H:%M:%S") + "-------------------------------------------------------------------"
    for i in range(3):
        print "Main method: starting Scenario " + str(i) + " at " + strftime("%Y-%m-%d %H:%M:%S") + "-------------------------------------------------------------------"
        es_communication = ESCommunicationScenario(host='localhost', username='admin', password='admin', domain='Global')
        es_communication.multi_process(duration_in_minutes=60, clumsy_always_on=True)
        print "Main method: finished Scenario " + str(i) + " at " + strftime("%Y-%m-%d %H:%M:%S") + "-------------------------------------------------------------------"


if __name__ == "__main__":
    main()
