import sys, os, shutil
from .unitypredictcli import UnityPredictCli
from .unitypredictUtils import ReturnValues as Ret
import argparse

def main():
    cliExec = "UnityPredict SDK"
    parser = argparse.ArgumentParser(
            description="Welcome to {}".format(cliExec)
    )
   
    parser.add_argument("--configure", action="store_true", help=f"configure the credentials of {cliExec}")
    parser.add_argument("--list_profiles", action="store_true", help=f"show credentials configured for {cliExec}")
    parser.add_argument("-e", "--engine", action="store_true", help=f"Access the engine specific operations in {cliExec}")
    parser.add_argument("-c", "--create", default=None, help="""create the AppEngine with a name. 
                                                                            Used after the [-e][--engine]""")
    parser.add_argument("-r", "--remove", default=None, help="""remove the AppEngine. 
                                                                            Used after the [-e][--engine]""")
    parser.add_argument("-d", "--deploy", default=None, help="""deploy the AppEngine to UnityPredict. 
                                                                            Used after the [-e][--engine]""")

    args = parser.parse_args()

    num_args = len(sys.argv) - 1
    
    if (num_args == 0):
        parser.print_help()
        sys.exit(0)

    cliDriver = UnityPredictCli()

    if args.configure:
        inputApiKey = input("Enter your UnityPredict account API Key: ")
        inputApiKey = inputApiKey.strip()
        ret = cliDriver.configureCredentials(uptApiKey=inputApiKey)
        sys.exit(0)

    if args.list_profiles:
        cliDriver.showProfiles()
        sys.exit(0)

    if args.engine:
        currPath = os.getcwd()
        if args.create != None:
            enginePath = os.path.join(currPath, args.create)
            if os.path.exists(enginePath):
                print ("""The engine already exists on the current directory. You can:
                    - Change the directory
                    - Use [-c][--create] flag to change the name of the engine
                    """)
                sys.exit(0)
            os.mkdir(enginePath)
            os.chdir(enginePath)
            ret = cliDriver.createEngine()
            os.chdir(currPath)
            if ret == Ret.ENGINE_CREATE_ERROR:
                if os.path.exists(enginePath):
                    print (f"Removing Engine {args.create} due to Engine Creation errors!")
                    shutil.rmtree(enginePath)
            sys.exit(0)
        if args.remove != None:
            enginePath = os.path.join(currPath, args.remove)
            if os.path.exists(enginePath):
                shutil.rmtree(enginePath)
                print(f"Removed the engine {args.remove} Successfully!!")
            else:
                print(f"Engine {args.remove} not detected!!")
            sys.exit(0)
        if args.deploy != None:
            print (f"Deploy {args.deploy}")
            sys.exit(0)
        else:
            print ("Incomplete arguements present. Please check the help section for the usage")
            parser.print_help()
        sys.exit(0)
    


