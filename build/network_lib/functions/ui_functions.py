import datetime
import matplotlib.pyplot as plt
import numpy as np
import functions.math_functions as lmf
from matplotlib.colors import ListedColormap


## User interaction Functions
def ask_to_save_model(model):
    save = input("Do you want to save the model? [y/n]")
    if save.lower() == 'y':
        date_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        model.save("saved_models//trained_model_" + date_time + ".h5")
        print("Model saved as 'trained_model_" + date_time + ".h5'")
    else:
        print("Model not saved")

def plot_outputs(truths, predictions):
    truths = truths.astype(int)
    predictions = predictions.astype(int)

    truth_grid = np.reshape(truths, (int(np.sqrt(truths.shape[0])), -1))
    prediction_grid = np.reshape(predictions, (int(np.sqrt(predictions.shape[0])), -1))
    cmap = ListedColormap(["lawngreen", "red", "grey"])
    fig, ((ax1, ax2, ax5), (ax3, ax4, ax6)) = plt.subplots(2, 3, figsize=(9,6))
    ax1.imshow(truth_grid, cmap= cmap)
    ax1.set_title('Truth')
    ax1.axis('off')
    ax2.imshow(prediction_grid, cmap= cmap)
    ax2.set_title('Prediction')
    ax2.axis('off')

    cmap = ListedColormap(["red", "lawngreen"])
    right_wrong = lmf.array_and(truths, predictions)
    right_wrong_grid = np.reshape(right_wrong, (int(np.sqrt(truths.shape[0])), -1))
    ax3.imshow(right_wrong_grid, cmap= cmap)
    ax3.set_title('Right Wrong')
    ax3.axis('off')

    cmap = ListedColormap(["lawngreen", "blue", "grey", "red", "lawngreen", "red", "grey", "grey", "lawngreen"])
    confusion = lmf.array_compare(truths, predictions)
    confusion_grid = np.reshape(confusion, (int(np.sqrt(truths.shape[0])), -1))
    ax4.imshow(confusion_grid, cmap= cmap)
    ax4.set_title('Green: correct, B: false pos,\n R: false neg, Grey: Other')
    ax4.axis('off')

    confusion_matrix = lmf.count_occurrences(confusion).astype(int)
    ax5.axis('tight')
    ax5.axis('off')
    ax5.table(cellText=confusion_matrix,
              colLabels=['TrHealthy', 'TrRust', 'TrOther'],
              rowLabels=['PrHealthy', 'PrRust', 'PrOther'],
              cellLoc='center', loc='center')
    
    proc_user = lmf.proc_user_rates(confusion_matrix).astype(int)
    ax6.axis('tight')
    ax6.axis('off')
    ax6.table(cellText=proc_user,
              colLabels=['Healthy', 'Rust', 'Other'],
              rowLabels=['User %', 'Prod %'],
              cellLoc='center', loc='center')

    plt.tight_layout()
    plt.show()