# -*- coding: utf-8 -*-
import copy
from functions import *

#Run this main function and do the interaction in the command line
def main():
    # Each book is a list, book = ['book name, author', '# of copies", "important?"]
    book_inventory = read_books_file()
    #Using the deepcopy make sure that changing the name and properties will not influent the origin one
    original_books = copy.deepcopy(book_inventory)
    #read the library activities
    books_borrowed, added_books, current_day, fee_list, books_out, all_books, book_inventory = read_log_file(book_inventory)
    #do the interract in the command line
    user_interface(current_day, books_borrowed, original_books, added_books, books_out, book_inventory, fee_list)

main()

