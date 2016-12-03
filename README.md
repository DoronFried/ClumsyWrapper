# ClumsyWrapper
Python Wrapper for clumsy network tool.
For simulating network issues in your automation tests.
Examine your product with unstable network.
Easy to use.

### Why using Clumsy wrapper?
As automation tester, do you test your product when the network is unstable?  
With this package you can simulate unstable network during your test cases.  
Examples of unstable network:
- loss 10% of packets that comes from specific ip or port
- stop the network for x seconds every y seconds
- add delay (lag) time to specific packets (with specific ip or port) 
- and etc.

> Step by Step Guide
- First Download clumsy https://jagt.github.io/clumsy/ 
- Then Download the alpha package from testpypi:
```
pip install --extra-index-url https://testpypi.python.org/pypi clumsywrapper
```
- Import the relevant classes to your test class:
```
from ClumsyWrapper.FilterBuilderHelper import FilterHelper
from ClumsyWrapper.NetworkControllerClumsy import ClumsyConfiguration, ClumsyController
```
- Under the setup method (part of the unitest package or any testing package):
 - create your own filter with the filter_helper class (or use one of the built-in functions). In this example you can see a filter that will 100% block port 8031 (in & out packets):
 ```
 filter_helper = FilterHelper().tcp().dst_port(port_num=8031).or_condition().tcp().src_port(
            port_num=8031).no_more_condition().drop(drop_chance=100).finish_generate_filter()
 ```
 - Insert Clumsy installation path to the "ClumsyConfiguration" object:
 ```
 network_configuration = ClumsyConfiguration(clumsy_path="C:\clumsy-0.2-win64")
 ```
 - Choose one of the builtin functions or (like in this example) choose the custom_config function. Define the 3 parameters:
    - execute_every_seconds - run clumsy every 'x' seconds. In this example we will block the network for port 8031 every **10** seconds.
    - execute_duration - run clumsy for duration of 'x' seconds. In this example we will block the network for port 8031 for duration of **2** seconds.
     - always_on - Or choose this option if you want to always run it
 ```
  network_configuration.custom_config(custom_filter=filter_helper, execute_every_seconds=10, execute_duration=2,
                                            always_on=False)
 ```
 - Then pass the configuration object to the controller object:
 ```
 self.network_controller = ClumsyController(clumsy_configuration=network_configuration)
 ```
  - Start clumsy:
 ```
 self.network_controller.start_async()
 ```
- Execute your test cases.
- Under the teardown function stop clumsy:
```
self.network_controller.stop()
```

**note:**
for creating your own filter use clumsy manual guide in https://jagt.github.io/clumsy/ 

Full example:
```
import unittest

from ClumsyWrapper.FilterBuilderHelper import FilterHelper
from ClumsyWrapper.NetworkControllerClumsy import ClumsyConfiguration, ClumsyController


class MyTestCase(unittest.TestCase):
    def setUp(self):
        # using the helper in order to build my own filter
        filter_helper = FilterHelper().tcp().dst_port(port_num=8031).or_condition().tcp().src_port(
            port_num=8031).no_more_condition().drop(drop_chance=100).finish_generate_filter()
        # install clumsy and insert the installation path:
        network_configuration = ClumsyConfiguration(clumsy_path="C:\clumsy-0.2-win64")
        network_configuration.custom_config(custom_filter=filter_helper, execute_every_seconds=10, execute_duration=2,
                                            always_on=False)

        self.network_controller = ClumsyController(clumsy_configuration=network_configuration)
        self.network_controller.start_async()

    def tearDown(self):
        self.network_controller.stop()

    def test_something(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
```
