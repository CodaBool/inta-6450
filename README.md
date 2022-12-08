# Running Locally
1. Add json files to data folder
2. Create a python Virtual Environment
  ### Unix
  1. `python3 -m venv venv`
  2. `source venv/bin/activate`
  ### Windows
  1. `python -m venv venv`
  2. `source venv/Scripts/activate`

3. Install requirements `pip install -r requirements.txt`

#### you can deactivate the environment at any time with the `deactivate` command

# Targets
- Broken SSL/TLS or Incorrect SSL/TLS
	- zip_file_in_transit_check_broken_ssl
	- broken_ssl
	- sensitive_data_cert_validation
- Bluetooth file transmissions
	- leaked_logcat_data_bluetooth_mac (duplicate)
	- sensitive_data_http_bluetooth_mac
	- leaked_data_in_files_bluetooth_mac
- Data stored in log files
	- leaked_logcat_data_build_fingerprint
	- leaked_logcat_data_android_id
	- leaked_logcat_data_bluetooth_mac (duplicate)
	- leaked_logcat_data_dns1
	- 30+ under "leaked_logcat_data_"
- Decryption of keychain
	- sensitive_data_http_custom (?)
- API excessive data exposure
	- api_excessive_data_exposure
- Vulnerability to SQL injection or Heartbleed
	- sqlcipher_key_leakage_check (?)
	- potential_sqlcipher_key_leakage_check
- Foreign Cloud Storage
	- api_resource_misconfiguration
- Word writable files, and executables
	- writable_executable_files_private_check
	- writable_executable_files_check
- Poor handshake or HTTP transfer of data in cleartext
- HTML data storage, data sent to third parties
- Lack of input validation checks
- Insecure 3 rd party libraries
- File system access for web views

### Possible stories
- if it requests URL for Facebook is it less secure?
- if it requrests to more URLs is it less secure?


file_name
urls
permissions amount
vulnerabilities
game bool (improve this)
score
obj['title']
obj['publisher']