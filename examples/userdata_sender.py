from monique_worker_py import *
import time


def main():
    # Create component with given name.
    component = Component(SENDER_NAME)
    # Initialize it.
    to_queue, from_queue = component.initialize()
    # Run simple application.
    sender_example(to_queue)


"""This is very important field. Name should be selected once and then fixed."""
SENDER_NAME = 'biocad:production:strelna:line1'


def sender_example(to_queue):
    # Suppose that we have some parameter that will be increase during the time.
    degree = 1
    while True:

        time.sleep(5)

        # this username is just for testing. Use meaningful in real application.
        user = "00000000-0000-0000-0000-000000000000"
        # just for example
        type = SENDER_NAME + ":module1"
        # in our json we'll have only one field with degree
        data = degree

        userdata = create_userdata(user, type, data)
        userdata_message = create_qmessage(userdata)

        print("Sending userdata: {}".format(userdata.to_json()))
        to_queue.send(userdata_message.to_json())

        # boil it up :)
        degree += 1


if __name__ == "__main__":
    # execute only if run as a script
    main()
