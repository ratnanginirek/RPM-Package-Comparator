# RPM-Package-Comparator
A utility for comparing installed RPM Packages across two Linux nodes. 

* Compares the package version between the two nodes by extracting the packages using the following command:
  ```bash
  sudo rpm -qa --last
  ```
> [!NOTE]
> Save the list of the packages for uploading it to the python script:
> ```bash
> sudo rpm -qa --last > installed_packages.txt
> ```

* Run the package using following command:
  ```bash
  sudo python3 rpmpackagecomparison.py
  ```
* The script will save the output in HTML format with the file name **package_comparison_report.html**
