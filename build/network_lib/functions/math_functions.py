import numpy as np

def convert_truths_to_integer(truths_array):
    num_samples = truths_array.shape[0]
    integer_truths = np.zeros(num_samples)
    for i in range(num_samples):
        integer_truths[i] = np.argmax(truths_array[i])
    return integer_truths

#elementwise and
def array_and(array1, array2):
    result = []
    for i in range(len(array1)):
        if array1[i] == array2[i]:
            result.append(1)
        else:
            result.append(0)
    return result

#compares arrays and seperates different states into ints
def array_compare(array1, array2):
    result = []
    for i in range(len(array1)):
        #(was healthy, predicted healthy)
        if array1[i] == 0 and array2[i] == 0:
            result.append(0)
        #(was healthy, predicted unhealthy)
        elif array1[i] == 0 and array2[i] == 1:
            result.append(1) 
        #(was healthy, predicted other)
        elif array1[i] == 0 and array2[i] == 2:
            result.append(2) 
        
        #(was unhealthy, predicted healthy)
        elif array1[i] == 1 and array2[i] == 0:
            result.append(3) 
        #(was unhealthy, predicted unhealthy)
        elif array1[i] == 1 and array2[i] == 1:
            result.append(4) 
        #(was unhealthy, predicted other)
        elif array1[i] == 1 and array2[i] == 2:
            result.append(5) 

        #(was other, predicted healthy)
        elif array1[i] == 2 and array2[i] == 0:
            result.append(6) 
        #(was other, predicted unhealthy)
        elif array1[i] == 2 and array2[i] == 1:
            result.append(7) 
        #(was other, predicted other)
        elif array1[i] == 2 and array2[i] == 2:
            result.append(8) 
        
        else:
            result.append(9)
    return result

def count_occurrences(arr):
    count = np.zeros((3,3))
    for i in range(len(arr)):
        if arr[i] == 0:
            count[0,0] += 1
        elif arr[i] == 1:
            count[0,1] += 1
        elif arr[i] == 2:
            count[0,2] += 1
        elif arr[i] == 3:
            count[1,0] += 1
        elif arr[i] == 4:
            count[1,1] += 1
        elif arr[i] == 5:
            count[1,2] += 1
        elif arr[i] == 6:
            count[2,0] += 1
        elif arr[i] == 7:
            count[2,1] += 1
        elif arr[i] == 8:
            count[2,2] += 1
    return np.transpose(count)

def proc_user_rates(confusion_matrix):
    output = np.zeros((2,3))

    output[0,0] = confusion_matrix[0,0] / (confusion_matrix[0,0] + confusion_matrix[0, 1] + confusion_matrix[0, 2])
    output[0,1] = confusion_matrix[1,1] / (confusion_matrix[1,0] + confusion_matrix[1, 1] + confusion_matrix[1, 2])
    output[0,2] = confusion_matrix[2,2] / (confusion_matrix[2,0] + confusion_matrix[2, 1] + confusion_matrix[2, 2])

    output[1,0] = confusion_matrix[0,0] / (confusion_matrix[0,0] + confusion_matrix[1, 0] + confusion_matrix[2, 0])
    output[1,1] = confusion_matrix[1,1] / (confusion_matrix[0,1] + confusion_matrix[1, 1] + confusion_matrix[2, 1])
    output[1,2] = confusion_matrix[2,2] / (confusion_matrix[0,2] + confusion_matrix[1, 2] + confusion_matrix[2, 2])

    output *= 100
    output = output.astype(int)
    return output