# ClumsyWrapper
Python Wrapper for the **Clumsy** network tool, which simulates network connectivity in your automation tests and allows you to run real time network stability issues.
Easy to use.

### Why use Clumsy wrapper?
As an automation tester, do you test your product when the network is unstable?  
With this package, you can simulate an unstable network during your test cases.  
Examples of an unstable network:
- 10% loss of packets related to a specific ip or port
- schedule network connectivity failures (e.g. stop the network for 3 seconds every 10 seconds)
- add delay (lag) time to specific packets (with specific ip or port) 

### Step by Step Guide
1. Download clumsy at https://jagt.github.io/clumsy/ 
2. Download the **alpha** package from testpypi:
 
 ```
pip install --extra-index-url https://testpypi.python.org/pypi clumsywrapper
```
3. Import the relevant classes to your test class:

 ```python
from ClumsyWrapper.FilterBuilderHelper import FilterHelper
from ClumsyWrapper.NetworkControllerClumsy import ClumsyConfiguration, ClumsyController
```
4. Under the **setup** function (part of the unitest package or any testing package), do the following:

 a. Create your own filter with the FilterHelper class (or use one of the built-in functions). For example, a filter that blocks 100% traffic on port 8031 (in & out packets):
  
   ```python
 filter_helper = FilterHelper().tcp().dst_port(port_num=8031).or_condition().tcp().src_port(
            port_num=8031).no_more_condition().drop(drop_chance=100).finish_generate_filter()
 ```
 b. Specify the Clumsy installation path in the "ClumsyConfiguration" object:
  
   ```python
 network_configuration = ClumsyConfiguration(clumsy_path="C:\clumsy-0.2-win64")
 ```
 c. Select one of the built-in functions  (like in the above example) or use the custom_config function. Define the 3 parameters:
     - execute_every_seconds - Run clumsy every 'x' seconds. For example, block traffic on port 8031 every **10** seconds.
     - execute_duration - Run clumsy for 'y' seconds. For example, block traffic on port 8031 for **2** seconds.
     - always_on - Or choose this option if you want to always run it.
   
   ```python
  network_configuration.custom_config(custom_filter=filter_helper, execute_every_seconds=10, execute_duration=2,
                                            always_on=False)
 ```
 d. Pass the configuration object to the controller object:
 
   ```python
 self.network_controller = ClumsyController(clumsy_configuration=network_configuration)
 ```
 e. Start Clumsy:
 
  ```python
 self.network_controller.start_async()
 ```
5. Execute your test cases.
6. Under the Teardown function, stop Clumsy:
 
 ```python
self.network_controller.stop()
```

**Note:**
To create your own filter, use the Clumsy help at https://jagt.github.io/clumsy/ 

Full example:
```python
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
