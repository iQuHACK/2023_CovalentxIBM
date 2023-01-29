from process_input import read_input
import pickle as pk


def predict(feature, qflag=True):
    '''
    input:
            feature (nd.array): feature
    return :
            p (int): prediction result, 1 for spam 0 for no
    '''
    if qflag:
        filename = "models/qsvc.pkl"
    else:
        filename = "models/svc.pkl"
    with open(filename, "rb") as fd:
        model = pk.load(fd)
    return model.predict(feature)


def transform(text):
    '''
    input:
            text (str): email body text
    return:
            output (nd.array): feature
    '''
    return read_input(text)


if __name__ == '__main__':
    pass
