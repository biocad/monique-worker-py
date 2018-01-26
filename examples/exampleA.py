import monique_worker_py


def main():
    # Create worker with given name and algorithm.
    w = monique_worker_py.Worker(EXAMPLE_A_NAME, example_a_algo)
    # And then just run it.
    w.run()


"""This is very important field. Name should be selected once and then fixed."""
EXAMPLE_A_NAME = 'exampleA'

"""This field will refactored later. But now it is necessary for the WorkerResult."""
EXAMPLE_A_VERSION = 1


def example_a_algo(task_config):
    print(task_config)
    config_a = task_config['configA']

    # This is dummy example. Just count length of the string.
    len_a = len(config_a)
    if len_a < 10:
        # This is how you can make task failed.
        raise Exception("Length is too small")
    else:
        # And this is format for the result. Just construct object that can be converted to the JSON format.
        # The config and result should be described and fix in API documentation.
        result = {"resultA": len_a}
        return monique_worker_py.WorkerResult(result, EXAMPLE_A_VERSION)


if __name__ == "__main__":
    # execute only if run as a script
    main()
