import prepare
import client

def main():
    prepare.prepare()

    client.run()

def callback(son):
    print(son)

def stopper():
        prepare.unpare()

if __name__ == '__main__':
    try:
        # Stuff we want to do (in this case, just call our main function)
        main()
    except KeyboardInterrupt:
        # What to do if there's a keyboard interrupt (ctrl+c) exception
        # In this case, we're just going to print a message
        print('\nProgram terminated with keyboard interrupt.')
    finally:
        # What to do before we exit the block
        stopper()