import os
from .Profile import Profile
import ast
from termcolor import colored
from ..print_output.print_output import printOutput

class Auth(Profile):
    def __init__(self):
        Profile.__init__(self)
        self.register = ""
        self.account = None
        pass

    def PrepRegister(self):
        account = self.web3.eth.account.create()
        printOutput("Your Account is Ready For Registration!!!" +
                      "\n>>> Your Public Address is: " + str(account.address) +
                      "\n>>> Transfer some ether to this and come back for registration!!!" + "\n\n" + str(
            account.address) + "\n\n", "blue")
        return account

    def Register(self, user_name, password):
        web3 = self.getWeb3()
        if not os.path.exists(Profile.getTemporaryDataFileName(self)):
            printOutput("Run Prepearation Register", 'red')
            return
        # if self.callGetUsers(user_name)[0] == user_name:
        #     print(colored(">>> Username exist choose different username", 'red'))
        #     return

        with open(Profile.getTemporaryDataFileName(self), "rb") as binary_file:
            data = binary_file.read()
            ax = (web3.eth.account.privateKeyToAccount(data))
            self.account = ax

        if (self.web3.eth.getBalance(self.account.address)) == 0:
            printOutput("Wallet empty add some ethers and come back"
            +">>> Public Address : " + str(self.account.address), 'red')
            return

        encrypted = self.account.encrypt(password)
        instance = Auth()
        value, account_received = instance.customTransact(
            self.getContractInstance().functions.DeployProfiles(user_name, str(encrypted)))
        self.account = account_received
        if value == True:
            printOutput("Registered successfully..." + "\n>>> Name " + user_name
                          + "\n>>> Public Address: " + str(self.account.address)
                          + "\n>>> Balance : " + str(self.web3.eth.getBalance(self.account.address)), "blue")

    def Login(self, username, password):
        web3 = Profile.getWeb3(self)
        profile_addr = Profile.callGetUsers(self, username)
        if profile_addr=="0x0000000000000000000000000000000000000000":
            printOutput("No user",'red')
            return

        if Profile.callGetUserData(self, name=username, addr=profile_addr)[0] == "NO USER":
            printOutput("User does not exist", 'red')
            return False
        res = ast.literal_eval(Profile.callGetUserData(self, name=username, addr=profile_addr)[1])
        try:
            privatekey_binary = self.web3.eth.account.decrypt(res, password)
            restored = self.web3.eth.account.privateKeyToAccount(privatekey_binary)
            if os.path.exists(Profile.getUserDataFileName(self)):
                os.remove(Profile.getUserDataFileName(self))
            with open(Profile.getUserDataFileName(self), "wb") as binary_file:
                # Write text or bytes to the file
                binary_file.write(privatekey_binary)
            with open(Profile.getUserDataFileName(self), "rb") as binary_file:
                data = binary_file.read()
                ax = (web3.eth.account.privateKeyToAccount(data))
                self.account = ax
            printOutput("Logged in..." + "\n>>> Name " + username
                          + "\n>>> Public Address: " + str(self.account.address)
                          + "\n>>> Balance : " + str(self.web3.eth.getBalance(self.account.address)), "blue")
            return True

        except ValueError:
            printOutput("Wrong Password", 'red')
        return False

    def Clear(self):
        # if os.path.exists(Profile.getTemporaryDataFileName(self)):
        #     os.remove(Profile.getTemporaryDataFileName(self))
        if os.path.exists(Profile.getUserDataFileName(self)):
            os.remove(Profile.getUserDataFileName(self))

    def Logout(self):
        if os.path.exists(Profile.getUserDataFileName(self)):
            os.remove(Profile.getUserDataFileName(self))
        else:
            printOutput("Not Logged in",'red')
            return
        self.account = None
        printOutput("Logged Out!!!", 'blue')
