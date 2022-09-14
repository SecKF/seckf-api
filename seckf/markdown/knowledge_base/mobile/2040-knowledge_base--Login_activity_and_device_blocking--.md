## Description:

Login activity and Device blocking

MSTG-AUTH-11: The app informs the user of all sensitive activities with their account. Users are able to view a list of devices, view contextual information (IP address, location, etc.), and to block specific devices.

For applications which require L2 protection, the MASVS states that they should inform the user about all login activities within the app with the possiblity of blocking certain devices. This can be broken down into various scenarios:

	1. The application provides a push notification the moment their account is used on another device to notify the user of different activities. The user can then block this device after opening the app via the push-notification.
	2. The application provides an overview of the last session after login. If the previous session was with a different configuration (e.g. location, device, app-version) compared to the current configuration, then the user should have the option to report suspicious activities and block devices used in the previous session.
	3. The application provides an overview of the last session after login at all times.
	4. The application has a self-service portal in which the user can see an audit-log. This allows the user to manage the different devices that are logged in.
	

## Mitigation:

The developer can make use of specific meta-information and associate it to each different activity or event within the application. This will make it easier for the user to spot suspicious behavior and block the corresponding device. The meta-information may include:

	- Device: The user can clearly identify all devices where the app is being used.
	- Date and Time: The user can clearly see the latest date and time when the app was used.
	- Location: The user can clearly identify the latest locations where the app was used.

The application can provide a list of activities history which will be updated after each sensitive activity within the application. The choice of which activities to audit needs to be done for each application based on the data it handles and the level of security risk the team is willing to have. Below is a list of common sensitive activities that are usually audited:

	- Login attempts
	- Password changes
	- Personal Identifiable Information changes (name, email address, telephone number, etc.)
	- Sensitive activities (purchase, accessing important resources, etc.)
	- Consent to Terms and Conditions clauses

Paid content requires special care, and additional meta-information (e.g., operation cost, credit, etc.) might be used to ensure user's knowledge about the whole operation's parameters.

In addition, non-repudiation mechanisms should be applied to sensitive transactions (e.g. payed content access, given consent to Terms and Conditions clauses, etc.) in order to prove that a specific transaction was in fact performed (integrity) and by whom (authentication).

In all cases, you should verify whether different devices are detected correctly. Therefore, the binding of the application to the actual device should be tested.
