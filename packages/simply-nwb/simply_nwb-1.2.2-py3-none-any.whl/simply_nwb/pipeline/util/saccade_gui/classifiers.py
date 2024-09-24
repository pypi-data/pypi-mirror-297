import numpy as np


class DirectionalClassifier(object):
    def is_too_noisy(self, waveform):
        std = np.std(waveform)
        mean = np.mean(np.mean(waveform, axis=0))
        ratio = np.abs(std/mean)  # Want ratio to be < .1

        if ratio > .15:
            return True
        return False

    def predict(self, data):
        # data is (saccadenum, t)
        predicts = []
        for idx in range(data.shape[0]):
            sacc = data[idx, :]
            if self.is_too_noisy(sacc[:25]) or self.is_too_noisy(sacc[-25:]):
                predicts.append(0)
                continue

            start_mean = np.mean(sacc[:30])
            end_mean = np.mean(sacc[-30:])
            # pos is temporal=-1 (end - start), neg is nasal=1, other is noise
            diff = end_mean - start_mean
            if diff >= 0:
                predicts.append(-1)
            else:
                predicts.append(1)

        return np.array(predicts)[:, None]
