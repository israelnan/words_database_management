#################################################################
# FILE : wordsearch.py
# WRITER : israel_nankencki , israelnan , 305702334
# EXERCISE : intro2cs2 ex5 2021
# DESCRIPTION: A program for reading matrix and words list files, searching the words in the matrix in given directions
# , and writing an output file with all the search results.
# STUDENTS I DISCUSSED THE EXERCISE WITH: none.
# WEB PAGES I USED: none
# NOTES:
#################################################################

##############################################################################
#                                   Imports                                  #
##############################################################################
import os
import sys


def read_wordlist(filename):
    """
    this function creates a list of words to search from a given text file.
    :param filename: string represent the root directory for the text file, or its name if it's in the same directory.
    :return: a list with all words in the text file.
    """
    with open(filename, 'r') as f:
        data = f.read()
        words = data.splitlines()
    f.close()
    return words


def read_matrix(filename):
    """
    this function creates a 2D list represent the matrix to search the words in from a text file.
    :param filename: string represent the root directory for the text file, or its name if it's in the same directory.
    :return: a 2D list represent the matrix to search in.
    """
    matrix = []
    with open(filename, 'r') as f:
        data = f.read()
        lines = data.splitlines()
        for line in lines:
            mat_row = []
            for letter in line:
                if letter.isalpha():
                    mat_row.append(letter)
            matrix.append(mat_row)
    f.close()
    return matrix


def find_words(word_list, matrix, directions):
    """
    this function managing the words search from a given list in the given matrix in the directions specified.
    :param word_list: a list of words to search in the matrix.
    :param matrix: a 2D list represent the matrix to search the words in.
    :param directions: the given directions for searching the words in the matrix.
    :return: a list with tuples of founded words and their appearances number.
    """
    return words_paths_dicts_creator(word_list, matrix, directions)


def is_the_whole_word_in_matrix(word, mat_dict):
    """
    this function helps 'words_path_dict_creator' to determine whether all the letters of a given word are in the
    matrix, and it needs to be search.
    :param word: the given words from the words list.
    :param mat_dict: a dict with all different letters in the matrix, with lists of its appearances coordinates as its
    values.
    :return: True if all the letters in the word in the matrix, False otherwise.
    """
    for letter in word:
        if letter not in mat_dict:
            return False
    return True


def matrix_to_dict(matrix):
    """
    this function creates a dict with all different letters in the matrix and lists of its appearances coordinates as
    values. used to increase the search efficiency.
    :param matrix: a 2D list represent the matrix to search the words in.
    :return: a dict with all different letters in the matrix and lists of its appearances coordinates as values.
    """
    mat_dict = {}
    for row in range(len(matrix)):
        for col in range(len(matrix[0])):
            if matrix[row][col] not in mat_dict:
                mat_dict[matrix[row][col]] = [(row, col)]
            else:
                mat_dict[matrix[row][col]].append((row, col))
    return mat_dict


def direction_finder(coor_1, coor_2):
    """
    this function helps to determine the direction of given step in path search for word appearance in the matrix.
    :param coor_1: tuple with coordinates of starting point in the given step.
    :param coor_2: tuple with coordinates of ending point in the given step.
    :return: the direction of the step if it's a legal step, 'nop' otherwise.
    """
    if coor_1[1] == coor_2[1] and coor_2[0] - coor_1[0] == -1:
        return 'u'
    if coor_1[1] == coor_2[1] and coor_2[0] - coor_1[0] == 1:
        return 'd'
    if coor_1[0] == coor_2[0] and coor_2[1] - coor_1[1] == -1:
        return 'l'
    if coor_2[0] == coor_1[0] and coor_2[1] - coor_1[1] == 1:
        return 'r'
    if coor_2[1] - coor_1[1] == 1 and coor_2[0] - coor_1[0] == -1:
        return 'w'
    if coor_2[1] - coor_1[1] == -1 and coor_2[0] - coor_1[0] == -1:
        return 'x'
    if coor_2[1] - coor_1[1] == 1 and coor_2[0] - coor_1[0] == 1:
        return 'y'
    if coor_2[1] - coor_1[1] == -1 and coor_2[0] - coor_1[0] == 1:
        return 'z'
    return 'nop'


def words_paths_dicts_creator(words_list, matrix, directions):
    """
    this function creates a dict with all words founded in the matrix, and lists with all paths to it as values.
    :param words_list: the list of words to be found in the matrix.
    :param matrix: a 2D list represent the matrix to search the words in.
    :param directions: a string represent the directions to search the words.
    :return: a list with tuples of words founded and their number of appearances in the matrix.
    """
    words_paths_list = []
    mat_dict = matrix_to_dict(matrix)
    for word in words_list:
        if is_the_whole_word_in_matrix(word, mat_dict):
            words_paths_list.append({word: whole_word_finder(word[1::], mat_dict, directions,
                                                             first_letter_lister(word, mat_dict))})
    words_paths_list = direction_filter(words_paths_list, directions)
    return words_appearance_counter(words_paths_list)


def direction_filter(words_paths_list, directions):
    """
    this function filters the paths founded to be only those in a single direction that's in the given directions.
    :param words_paths_list: A list with dicts for all words and all of its founded paths.
    :param directions: the given directions for this search.
    :return: A list with dicts for all words and all of its founded paths, only those which stands with the
     requirements.
    """
    filtered_word_dicts_list = []
    for word_dict in words_paths_list:
        filtered_all_path_list = []
        for word in word_dict:
            if len(word_dict[word]) > 0:
                for path in word_dict[word]:
                    direction_str = direction_finder(path[0], path[1])
                    if direction_str in directions:
                        for step in range(1, len(path)):
                            step_str = direction_finder(path[step - 1], path[step])
                            if step_str != direction_str:
                                direction_str = ''
                                break
                            else:
                                continue
                    if direction_str != '':
                        filtered_all_path_list.append(path)
            if len(filtered_all_path_list) > 0:
                filtered_word_dicts_list.append({word: filtered_all_path_list})
    return filtered_word_dicts_list


def words_appearance_counter(words_paths_dicts_list):
    """
    this function helps the function above to create a list of tuples with the words founded and its appearances number.
    :param words_paths_dicts_list: a dict with all words founded in the matrix, and a list of paths to it.
    :return: a list of tuples with the words founded and its appearances number.
    """
    words_counter_list = []
    for word_dict in words_paths_dicts_list:
        for word in word_dict:
            if len(word_dict[word]) > 0:
                words_counter_list.append((word, len(word_dict[word])))
    return words_counter_list


def first_letter_lister(word, mat_dict):
    """
    this function creates a list with all lists of coordinates for first letter in a given word.
    :param word: the given word to be found.
    :param mat_dict: a dict with all different letters in the matrix and lists of its appearances coordinates as values.
    :return: a list with all lists of coordinates for first letter in the word.
    """
    all_primer_paths = []
    for coor in mat_dict[word[0]]:
        all_primer_paths.append([coor])
    return all_primer_paths


def whole_word_finder(word, mat_dict, directions, all_path_list):
    """
    this is a recursive function that finds the whole path to a given word in the matrix.
    :param word: a given word to be found in the matrix.
    :param mat_dict: a list with all lists of coordinates for first letter in the word.
    :param directions: the directions allowed for this search.
    :param all_path_list: the different paths to the word in the matrix.
    :return: a list with all different paths to the word in the matrix.
    """
    if word == '':
        return all_path_list
    new_all_path_list = []
    for path_list in all_path_list:
        for next_coor in mat_dict[word[0]]:
            if direction_finder(path_list[-1], next_coor) in directions:
                new_all_path_list.append(path_list + [next_coor])
    return whole_word_finder(word[1::], mat_dict, directions, new_all_path_list)


def write_output(results, filename):
    """
    this function writes (or overwrites) the output text file with the words founded in the matrix and its appearances
     number.
    :param results: a list with tuples of the words founded in the matrix and its appearances number.
    :param filename: the name of the file for the function to write (or overwrite).
    :return: None.
    """
    with open(filename, 'w') as f:
        for result in results:
            f.write(result[0] + ',' + str(result[1]))
            f.write('\n')
    f.close()
    return


def is_it_valid_input(argv_list):
    """
    this function helps the command line to determine whether the number of arguments is exactly 4 as required or not.
    :param argv_list: a list with all arguments inserted in command line.
    :return: True if the number of arguments is 4, False otherwise.
    """
    if len(argv_list) == 5:
        return True
    print("this isn't the number or arguments we've expected")
    return False


def is_words_file_exists(words_filename):
    """
    this function helps the command line to determine whether the words list textfile is existed or not.
    :param words_filename: a string with the required filename inserted to command line.
    :return: True if the file exist in directory, False otherwise.
    """
    if os.path.exists(words_filename):
        return True
    print("word file doesn't exists")
    return False


def is_matrix_file_exists(mat_filename):
    """
    this function helps the command line to determine whether the matrix textfile is existed or not.
    :param mat_filename: a string with the required filename inserted to command line.
    :return: True if the file exist in directory, False otherwise.
    """
    if os.path.exists(mat_filename):
        return True
    print("matrix file doesn't exists")
    return False


def is_directions_are_legal(directions):
    """
    this function helps the command line to determine the given directions are validity.
    :param directions: a string with required direction for this search inserted to command line.
    :return: True if all directions are valid, False otherwise.
    """
    for direction in directions:
        if direction not in "udrlwxyz":
            print("at least one of the directions isn't legal")
            return False
    return True


if __name__ == '__main__':
    if not is_it_valid_input(sys.argv):
        sys.exit()
    elif not is_words_file_exists(sys.argv[1]):
        sys.exit()
    elif not is_matrix_file_exists(sys.argv[2]):
        sys.exit()
    elif not is_directions_are_legal(sys.argv[4]):
        sys.exit()
    else:
        funded_words = find_words(read_wordlist(sys.argv[1]), read_matrix(sys.argv[2]), sys.argv[4])
        write_output(funded_words, sys.argv[3])
