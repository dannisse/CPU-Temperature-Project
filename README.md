# CPU Temperature Project

A software application that utilizes Python to parse through CPU temp data 
to find the piecewise interpolation and global linear least-squares approximation
for each CPU core. 

More Project Information: [SEMESTER PROJECT CS417 - ODU](https://www.cs.odu.edu/~tkennedy/cs417/sum20/Assts/project-cpu-temps/index.html)

## Dependancies
### Hardware
The required hardware needed is any computing device that runs on WindowsOS or macOS
### Software
* Python IDE— such as PyCharm

## Files 
These .txt files are sample CPU temp data taken every 30 seconds from: [.txt CPU data files](https://www.cs.odu.edu/~tkennedy/cs417/sum20/Assts/project-cpu-temps/index.html)

Following test data were used:

* [sensors-2018.12.26.txt](https://www.cs.odu.edu/~tkennedy/cs417/sum20/Assts/project-cpu-temps/Public/sensors-2018.12.26.txt) 
* [sensors-2019.01.26.txt](https://www.cs.odu.edu/~tkennedy/cs417/sum20/Assts/project-cpu-temps/Public/sensors-2019.01.26.txt) 
* [sensors-2019.02.09.txt](https://www.cs.odu.edu/~tkennedy/cs417/sum20/Assts/project-cpu-temps/Public/sensors-2019.02.09.txt)

* [sensors-2018.12.26-no-labels.txt](https://www.cs.odu.edu/~tkennedy/cs417/sum20/Assts/project-cpu-temps/Public/sensors-2018.12.26-no-labels.txt)
* [sensors-2019.01.26-no-labels.txt](https://www.cs.odu.edu/~tkennedy/cs417/sum20/Assts/project-cpu-temps/Public/sensors-2019.01.26-no-labels.txt)
* [sensors-2019.02.09-no-labels.txt](https://www.cs.odu.edu/~tkennedy/cs417/sum20/Assts/project-cpu-temps/Public/sensors-2019.02.09-no-labels.txt)

## Program Arguments & Executions
Program must accept an input filename as the first command line argument and must **NOT** prompt the user for a filename.

All temperature data are whitespaced delimited. An example set of temp data (with labels) are shown below:
```
+61.0°C +63.0°C +50.0°C +58.0°C
+80.0°C +81.0°C +68.0°C +77.0°C
+62.0°C +63.0°C +52.0°C +60.0°C
+83.0°C +82.0°C +70.0°C +79.0°C
+68.0°C +69.0°C +58.0°C +65.0°C 
```

Example set of whitespaced dilimited without labels:
```
61.0 63.0 50.0 58.0
80.0 81.0 68.0 77.0
62.0 63.0 52.0 60.0
83.0 82.0 70.0 79.0
68.0 69.0 58.0 65.0
```

## Output Format
Each line must take the form: 

x<sub>k</sub> <= x < x<sub>k+1</sub>; y<sub>i</sub> = c<sub>0</sub>+c<sub>1</sub>x ; type

Where
* x<sub>k</sub> and x<sub>k+1</sub> are the domain in which y<sub>k</sub> is applicable

* y<sub>k</sub> is the k<sup>th</sup> function

* type is either least-squares or interpolation

After compiling the code, there should be 4 output files generated:

* {basename}-core-0.{txt}
* {basename}-core-1.{txt}
* {basename}-core-2.{txt}
* {basename}-core-3.{txt}

## Documentation
All functions (including parameters and return types) must be documented. PyDoc was utilized for the documentation:
```
def parse_raw_temps(original_temps: TextIO,
                    step_size: int=30, units: bool=True) -> Iterator[Tuple[float, List[float]] ]:
    """
    Take an input file and time-step size and parse all core temps.

    :param original_temps: an input file
    :param step_size:      time-step in seconds
    :param units: True if the input file includes units and False if the file
                  includes only raw readings (no units)

    :yields: A tuple containing the next time step and a List containing _n_
             core temps as floating point values (where _n_ is the number of
             CPU cores)
    """
```
