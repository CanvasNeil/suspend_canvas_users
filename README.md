# Suspend Canvas User Accounts

⛔ Script to suspend Canvas user accounts using a CSV input file with user ids.

## Dependencies
* [Canvas API Token](https://community.canvaslms.com/t5/Admin-Guide/How-do-I-manage-API-access-tokens-as-an-admin/ta-p/89)
* Required external Python libraries: 
    * requests
    
## Executing Program
* Update your __*Canvas API Token*__ and __*Canvas Portal's Base URL*__ in the `config.py` file.
* Add Canvas user ids to suspend in the `input_user_id.csv` file. User IDs can be retrieved from the [user provisioning report](https://community.canvaslms.com/t5/Admin-Guide/How-do-I-view-reports-for-an-account/ta-p/109).
* Execute `suspend_users.py`.
* Upon successful execution, a CSV output file listing suspension status will be created in the current working directory. Open the file to verify all the users are successfully suspended.
* A more comprehensive log file will be created in the `log` directory within the current working directory.
<p align="left"><kbd><img src="https://user-images.githubusercontent.com/102522513/180081617-d563c0f2-e826-4166-89ab-f209c76a3fce.png"></kbd></p>
