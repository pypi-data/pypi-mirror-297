README: 
Python's math, and scipy implementations compared to the C-wrapped implementation of the LM technique for estimating the loglikelihood function.

Prerequisites:
This code requires a Linux environment and specific Python packages:
	- Python 3: Ensure you have Python 3.11 or higher installed on your system. You can check by running python3 --version in your terminal.
	- Packages: The script relies on the following Python libraries:
		1. mpmath
		2. scipy
		3. numpy

Description:
	- This code compares 3 techniques in terms of the time and number of iterations of estimating the loglikelihood function in the context of executing Minka's fixed-point iteration in order to fit categorical count data using the Dirichlet multinomial distribution.
	- These techniques are Python's math implementation, Python's scipy implementation, and a C-wrapped implementation of the LM technique. 

Notes:
	- The package alm2 contains multiple Python scripts that load a count dataset, randomly sample from it, and apply the LM technique to compute the loglikelihood function to model the data using Dirichlet multinomial distribution.
	- The package comprises a set of C and associated header files that provide the C implementation of LM technique. The compiled version (the .so file) is Linux compatible, and is utilized within the LM technique implementation.
	- The code is configured to execute under a Linux distribution and assumes all necessary code and data files are in the same directory.
	- It is assumed that Python 3.11 or higher is installed, the code requires the packages numpy, scipy, and mpmath are installed apriori.
	- executor.py is the entry script, it loads the dataset, calls scrambler.py to randomly sample a subset of the dataset, and calls LogL-global-v5.py to fit the subset using the Dirichlet multinomial distribution while utilizing the LM technique to compute the loglikelihood function required by the Minka procedure to do the data fitting.
	- The code will execute and produce the time, number of iterations and psi using Python's math library implementation of the loglikelihood function, then using Python's scipy implementation of the loglikelihood function, then using the LM C-wrapped implementation of the loglikelihood function.
	- For the LM technique, the results of the distance functions and goodness-of-fit tests are provided.
Running the code:
	- The package alm2 is publicly available at PYPI (refer to the package link in the paper or search for alm2 on PYPI)
	- There are two ways to install alm2 and run its code:
		I) using pip (as illustrated on alm2 webpage on PYPI), and after the successful installation of alm2:
			1. Execute the command pip show alm2 to get the path to the package code, denoted by PATH
			2. Enter the command import alm2.executor in a Python IDE, or using Python's command line 
			3. Choose the way you installed alm2 by entering p 
			4. Enter PATH
			5. Enter the name of a dataset file from the list displayed
			6. Enter one of the ratios displayed (i.e. the ratio of the dataset to be used in building the Dirichlet model)
			7. Enter the mpmath and LM precision values, to reproduce the results in the accompanying paper choose 6 for both
			8. The code should execute and produce the designated results.
		
		II) using download file option from alm2 webpage on PYPI, after downloading the package and uncompressing its file, open a terminal and:
			1. Navigate to the alm2 directory that contains the executor.py script, and let the absolute path to this file be denoted by PATH
			2. Run the executor using the command python3 executor.py 
			3. Choose the way you installed alm2 by entering  d
			4. Enter PATH
			5. Then, follow the steps 5-8 from option (I) above.
Exceptions:
		- The LM technique verifies that the loglikelihood is computable using the provided value of precision before the actual computation, if that accuracy cannot be achieved the script aborts with an informative error message of the form:
		*********** ERROR (check_with_asym1): LogL too large to ensure the desired precision in double; switch to multiprecision
		*********** ABORTING
		*********** ERROR FROM MINKA by LM PROCEDURE: LogL too large to ensure the desired precision in double; switch to multiprecision
		- The theoretical explanation for this is outlined in the accompanying paper, see the discussion about the asymptotic state of the system.
		- This exception was not reported with any the datasets in this directory using the precision value of 6, however, it was reported with other datasets with various levels of precision. Should the user test the code with higher values of precision, they may or may not experience this exception.

Disclaimer:
	- This script is provided for educational and research purposes only. The authors are not responsible for any misuse or unintended consequences of using this script. Any commercial use of this software is prohibited without the explicit consensus of the authors.

License:	
	- This software is licensed under the GNU General Public License version 3 (GPL-3), as published by the Free Software Foundation. You can find a copy of the license at https://www.gnu.org/licenses/gpl-3.0.en.html
	

Authors:
	- Sherenaz Al-Haj Baddar (s.baddar@ju.edu.jo)
	- Alessandro Languasco (alessandro.languasco@unipd.it)
	- Mauro Migliardi (mauro.migliardi@unipd.it)
	
	
	