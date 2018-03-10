from monique_worker_py import *


def main():
    # Create component with given name.
    component = Component(RECEIVER_NAME)
    # Initialize it.
    to_queue, from_queue = component.initialize()
    # Run simple application.
    receiver_example(from_queue)


"""This is very important field. Name should be selected once and then fixed."""
RECEIVER_NAME = 'biocad:it:monitoring'


def receiver_example(from_queue):

    while True:
        # receive every 'userdata' message from queue
        [_, in_message] = from_queue.recv_multipart()

        # parsing message to QMessage
        qmessage = qmessage_from_json(in_message)

        # get userdata from qmessage
        userdata = qmessage.cnt.contents

        # here we simulate filtering userdata that we recieve.
        # We do some meaningful work if only type that we get is the same as we expected.
        # Your can realize any logic with filtering what you want.
        if userdata.get_type() == 'biocad:production:strelna:line1:module1':
            print("Got useful userdata: {}".format(userdata.to_json().decode('utf8')))
            print("Do some work here...")
        else:
            print('This userdata is not interesting, skip it...')


if __name__ == "__main__":
    # execute only if run as a script
    main()
