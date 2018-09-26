import subprocess

class otp_utils():

    def generatePassword(self, bashCommand):
        subprocess.check_output(['ls', '-l'])
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        return (output, error)
