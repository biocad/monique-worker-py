import monique_worker_py


def main():
    w = monique_worker_py.Worker(EXAMPLE_A_NAME, example_a_algo)
    w.run()


EXAMPLE_A_NAME = 'exampleA'


def example_a_algo(task_config):
    print(task_config)
    config_a = task_config['configA']
    len_a = len(config_a)
    if len_a < 10:
        raise Exception("Length is too small")
    else:
        return monique_worker_py.WorkerResult({"resultA": len_a}, 1)


if __name__ == "__main__":
    # execute only if run as a script
    main()
