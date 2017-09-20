
import numpy as np
import string
from optimizers import GeneticOptimizer
from optimizers import get_individual_score

from sklearn.model_selection import train_test_split
from sklearn.ensemble import BaggingClassifier
from sklearn.tree import DecisionTreeClassifier


if __name__ == "__main__":

    print("\n================================================================================")

    datasetFolderName = 'UCI_Datasets/'
    datasetFileName = 'letter-recognition.data'

    letter_mapping = list(string.ascii_uppercase)
    letter_dataset = np.loadtxt(datasetFolderName + datasetFileName, delimiter=",")
    letter_data = letter_dataset[:, 1:17]
    letter_target = letter_dataset[:, 0]
    X_train, X_test, y_train, y_test = train_test_split(letter_data, letter_target, test_size=0.4)
    X_test, X_val, y_test, y_val = train_test_split(X_test, y_test, test_size=0.5)


    n_estimators = 100
    pop_size = n_estimators // 2
    iterations = 5000   
    mutation_rate = 0.2
    crossover_rate = 0.9
    n_jobs = 4
    elitism = False
    n_point_crossover = True

    print("\nGenerating estimators from Bagging method...")
    max_samples_ratio = 0.5
    bagging = BaggingClassifier(base_estimator=DecisionTreeClassifier(), n_estimators=n_estimators, max_samples=max_samples_ratio)
    bagging.fit(X_train, y_train)


    gen_opt = GeneticOptimizer(estimators=bagging.estimators_, 
                               classes=bagging.classes_, 
                               data=X_test, 
                               target=y_test, 
                               pop_size=pop_size, 
                               mutation_rate=mutation_rate,
                               crossover_rate=crossover_rate,
                               iterations=iterations,
                               elitism=elitism,
                               n_point_crossover=n_point_crossover,
                               n_jobs=n_jobs)

    best_found, initial_score = gen_opt.run_genetic_evolution()

    print()
    print("Best individual score found: %f%% (+%f%%)" % (best_found[0] * 100, (best_found[0] - initial_score) * 100))
    print("Estimators combination for the best score:")
    print(best_found[1])

    print("\nTesting best combination on validation set...")
    final_score = get_individual_score(best_found[1], bagging.estimators_, X_val, y_val, bagging.classes_)
    print("Final score: %f%% (+%f%%)" % (final_score * 100, (final_score - initial_score) * 100))

    print("\n================================================================================")
