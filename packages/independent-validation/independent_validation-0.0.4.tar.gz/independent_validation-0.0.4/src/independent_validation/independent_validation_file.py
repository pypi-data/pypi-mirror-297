import numpy as np
import time

def independent_validation(classifier, X, y, batch_size=1, start_trainset_size=10, scaler=None, talk=False):
    # verdoppeln der batch_size halbiert die nötige Zeit circa.
    start_trainset_size = max(batch_size, start_trainset_size)

    shuffled_indices = np.random.permutation(len(X))
    X = np.array(X)[shuffled_indices]
    y = np.array(y)[shuffled_indices]

    classes = np.unique(y)

    X_train = X[:start_trainset_size]
    y_train = y[:start_trainset_size]
    X = X[start_trainset_size:]
    y = y[start_trainset_size:]
    classifier.fit(X_train, y_train)  # do I need to use partial_fit here for those that can use that?
    true_values = y.tolist()
    predictions = []  # this seems to be faster than using an array.
    t = time.time()
    if scaler is not None:
        scaler.fit(X_train)
    while True:
        if batch_size < len(X):
            X_batch = X[:batch_size]
            y_batch = y[:batch_size]
            X = X[batch_size:]
            y = y[batch_size:]
        else:
            X_batch = X
            y_batch = y

        if scaler is not None:
            preds = classifier.predict(scaler.transform(X_batch))
        else:
            preds = classifier.predict(X_batch)
        predictions.extend(preds.tolist())  #

        X_train = np.vstack([X_train, X_batch])  # wie schnell ist das?
        # Alternative: Einen Datensatz nehmen und jedesmal neu indexieren.
        y_train = np.concatenate([y_train, y_batch])

        if hasattr(classifier, 'partial_fit') and scaler is None:
            classifier.partial_fit(X_batch, y_batch, classes=classes)
        else:
            if scaler is not None:
                scaler.fit(X_train)
                classifier.fit(scaler.transform(X_train), y_train)
            else:
                classifier.fit(X_train, y_train)

        if np.array_equal(X_batch, X):
            return predictions, true_values
        else:
            if talk:
                print(f'Data samples:\t\t{len(predictions)} / {len(true_values)}')
                print(f'estimated time:\t\t {round((time.time() - t))} / {round((time.time() - t) / ((len(predictions) / len(true_values))**2))}')